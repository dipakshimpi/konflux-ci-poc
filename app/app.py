"""Minimal health-check HTTP server.

Run directly:
    python app/app.py

The server listens on 127.0.0.1:8000 by default.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "0.0.0.0"
PORT = 8000


class HealthHandler(BaseHTTPRequestHandler):
    """Handle incoming HTTP requests."""

    def _send_json(self, status_code: int, body: dict) -> None:
        """Serialise *body* as JSON and send it with the given status code."""
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    # --- route handlers -------------------------------------------------- #

    def do_GET(self) -> None:  # noqa: N802 – required method name
        """Route GET requests."""
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "not found"})

    # Silence per-request log lines (keeps test output clean).
    def log_message(self, format, *args) -> None:  # noqa: A002
        pass


def create_server(host: str = HOST, port: int = PORT) -> HTTPServer:
    """Create and return an HTTPServer instance (but do not start it).

    Exposed as a function so tests can import and start the server on an
    ephemeral port without running ``main()``.
    """
    return HTTPServer((host, port), HealthHandler)


def main() -> None:
    """Start the server and serve requests until interrupted."""
    server = create_server()
    print(f"Serving on http://{HOST}:{PORT}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
