"""Tests for the health-check HTTP server (app.app)."""

import json
import threading
import unittest
from http.client import HTTPConnection

# Allow the import to work when running from the project root:
#   python -m unittest discover -s tests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.app import create_server  # noqa: E402


class TestHealthEndpoint(unittest.TestCase):
    """Start a real server on an ephemeral port and make HTTP requests."""

    @classmethod
    def setUpClass(cls) -> None:
        # Port 0 lets the OS pick a free port – avoids collisions.
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()  # stops serve_forever()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    # -- helper ----------------------------------------------------------- #

    def _get(self, path: str) -> tuple:
        """Make a GET request and return (status_code, parsed_json_body)."""
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            body = json.loads(resp.read().decode("utf-8"))
            return resp.status, body
        finally:
            conn.close()

    # -- tests ------------------------------------------------------------ #

    def test_health_returns_200(self) -> None:
        status, body = self._get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})

    def test_health_content_type(self) -> None:
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request("GET", "/health")
            resp = conn.getresponse()
            resp.read()  # consume body
            self.assertEqual(resp.getheader("Content-Type"), "application/json")
        finally:
            conn.close()

    def test_unknown_path_returns_404(self) -> None:
        status, body = self._get("/nonexistent")
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    def test_root_returns_404(self) -> None:
        status, body = self._get("/")
        self.assertEqual(status, 404)
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
