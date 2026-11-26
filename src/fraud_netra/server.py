import json
import socket
import warnings
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from secrets import token_hex
from time import monotonic

from PIL import Image, UnidentifiedImageError

MAX_REQUEST_BYTES = 1_048_576
MAX_PIXELS = 4_000_000
SOCKET_TIMEOUT_SECONDS = 2


class RequestError(Exception):
    def __init__(self, status, code, message):
        self.status = status
        self.code = code
        self.message = message


def parse_multipart(content_type, body):
    message = BytesParser(policy=policy.default).parsebytes(
        f"MIME-Version: 1.0\r\nContent-Type: {content_type}\r\n\r\n".encode() + body
    )
    if not message.is_multipart():
        raise RequestError(400, "INVALID_MULTIPART", "Expected multipart form data.")
    fields = {}
    for part in message.iter_parts():
        if part.is_multipart():
            raise RequestError(400, "INVALID_MULTIPART", "Nested multipart is unsupported.")
        name = part.get_param("name", header="content-disposition")
        if name not in {"file", "document_type"} or name in fields:
            raise RequestError(400, "INVALID_MULTIPART", "Expected one file and document_type field.")
        payload = part.get_payload(decode=True)
        fields[name] = (payload or b"") if name == "file" else part.get_content()
    if set(fields) != {"file", "document_type"}:
        raise RequestError(400, "INVALID_MULTIPART", "Expected one file and document_type field.")
    if not isinstance(fields["document_type"], str) or not fields["document_type"].strip():
        raise RequestError(400, "INVALID_DOCUMENT_TYPE", "document_type must not be empty.")
    if len(fields["document_type"]) > 64:
        raise RequestError(400, "INVALID_DOCUMENT_TYPE", "document_type is too long.")
    return fields["file"], fields["document_type"].strip()


def validate_png(data):
    image_stream = BytesIO(data)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(image_stream) as image:
                if image.format != "PNG":
                    raise RequestError(415, "UNSUPPORTED_FORMAT", "Only PNG fixtures are supported.")
                if image.n_frames != 1:
                    raise RequestError(400, "INVALID_DOCUMENT", "Only one-frame PNGs are supported.")
                if image.width * image.height > MAX_PIXELS:
                    raise RequestError(413, "PIXEL_LIMIT_EXCEEDED", "PNG exceeds the pixel limit.")
                image.verify()
            image_stream.seek(0)
            with Image.open(image_stream) as image:
                image.load()
    except RequestError:
        raise
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        raise RequestError(400, "INVALID_DOCUMENT", "The PNG fixture is invalid or unreadable.") from None


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(SOCKET_TIMEOUT_SECONDS)

    def log_message(self, format, *args):
        return

    def send_json(self, status, value):
        encoded = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/healthz":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": {"code": "NOT_FOUND", "message": "Route not found."}})

    def do_POST(self):
        if self.path != "/v1/documents/analyze":
            self.send_json(404, {"error": {"code": "NOT_FOUND", "message": "Route not found."}})
            return
        started = monotonic()
        try:
            if self.headers.get("Transfer-Encoding"):
                raise RequestError(400, "INVALID_REQUEST", "Transfer-Encoding is unsupported.")
            try:
                length = int(self.headers.get("Content-Length", ""))
            except ValueError:
                raise RequestError(400, "INVALID_REQUEST", "A valid Content-Length is required.") from None
            if length < 0:
                raise RequestError(400, "INVALID_REQUEST", "A valid Content-Length is required.")
            if length > MAX_REQUEST_BYTES:
                raise RequestError(413, "REQUEST_TOO_LARGE", "Request exceeds the 1 MiB limit.")
            content_type = self.headers.get("Content-Type", "")
            if not content_type.lower().startswith("multipart/form-data;"):
                raise RequestError(415, "UNSUPPORTED_MEDIA_TYPE", "Expected multipart/form-data.")
            body = self.rfile.read(length)
            if len(body) != length:
                raise RequestError(400, "INVALID_REQUEST", "Request body ended unexpectedly.")
            image_bytes, _document_type = parse_multipart(content_type, body)
            validate_png(image_bytes)
        except RequestError as error:
            self.send_json(error.status, {"error": {"code": error.code, "message": error.message}})
            return
        except (socket.timeout, TimeoutError):
            self.send_json(408, {"error": {"code": "REQUEST_TIMEOUT", "message": "Request timed out."}})
            return
        self.send_json(
            200,
            {
                "document_id": f"doc_{token_hex(6)}",
                "sha256": sha256(image_bytes).hexdigest(),
                "authenticity_score": None,
                "verdict": "INCONCLUSIVE",
                "processing_time_ms": int((monotonic() - started) * 1000),
                "verdict_reason": "No validated screening profile is configured.",
                "risk_breakdown": {
                    "synthetic_ai_likelihood": None,
                    "metadata_tampering": None,
                    "font_anomaly_score": None,
                    "math_inconsistency": None,
                },
                "detected_anomalies": [],
                "heatmap_overlay_url": None,
            },
        )


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
