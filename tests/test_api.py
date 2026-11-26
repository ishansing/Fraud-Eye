import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from io import BytesIO

from PIL import Image

from fraud_netra.server import Handler


def png_bytes(size=(8, 8), color="white"):
    image = Image.new("RGB", size, color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def multipart(file_bytes, *, document_type="bank_statement"):
    boundary = "fixture-boundary"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="document_type"\r\n\r\n'
        f"{document_type}\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="synthetic.png"\r\n'
        "Content-Type: image/png\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()
    return boundary, body


def request(server, body, boundary):
    request = urllib.request.Request(
        f"http://127.0.0.1:{server.server_port}/v1/documents/analyze",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        return urllib.request.urlopen(request, timeout=3)
    except urllib.error.HTTPError as error:
        return error


def test_health_endpoint_responds_over_loopback():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/healthz") as response:
            assert response.status == 200
            assert json.load(response) == {"status": "ok"}
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def with_server(test):
    def run():
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            test(server)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    return run


@with_server
def test_synthetic_png_returns_inconclusive_with_original_digest(server):
    from hashlib import sha256

    boundary, body = multipart(png_bytes())
    response = request(server, body, boundary)
    result = json.load(response)

    assert response.status == 200
    assert result["verdict"] == "INCONCLUSIVE"
    assert result["sha256"] == sha256(png_bytes()).hexdigest()
    assert result["document_id"].startswith("doc_")
    assert result["authenticity_score"] is None
    assert result["detected_anomalies"] == []
    assert result["heatmap_overlay_url"] is None


@with_server
def test_invalid_png_returns_structured_error(server):
    boundary, body = multipart(b"not a PNG")
    response = request(server, body, boundary)
    result = json.load(response)

    assert response.status == 400
    assert result["error"]["code"] == "INVALID_DOCUMENT"


@with_server
def test_image_over_pixel_limit_is_rejected(server):
    boundary, body = multipart(png_bytes((2001, 2000)))
    response = request(server, body, boundary)
    result = json.load(response)

    assert response.status == 413
    assert result["error"]["code"] == "PIXEL_LIMIT_EXCEEDED"


@with_server
def test_request_over_byte_limit_is_rejected_before_reading_body(server):
    boundary = "fixture-boundary"
    too_large = urllib.request.Request(
        f"http://127.0.0.1:{server.server_port}/v1/documents/analyze",
        data=b"",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": "1048577",
        },
        method="POST",
    )
    try:
        response = urllib.request.urlopen(too_large)
    except urllib.error.HTTPError as error:
        response = error
    result = json.load(response)

    assert result["error"]["code"] == "REQUEST_TOO_LARGE"
