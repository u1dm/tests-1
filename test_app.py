import json
import threading
import unittest
import urllib.error
import urllib.request

from app import create_server


class AppServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get(self, path):
        with urllib.request.urlopen(f"{self.base_url}{path}", timeout=2) as response:
            return response.status, response.headers.get_content_type(), response.read().decode("utf-8")

    def test_health_returns_ok(self):
        status, content_type, body = self.get("/health")

        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(json.loads(body), {"status": "ok"})

    def test_version_returns_app_metadata(self):
        status, content_type, body = self.get("/version")

        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(json.loads(body)["version"], "0.1.0")

    def test_metrics_is_prometheus_compatible(self):
        status, content_type, body = self.get("/metrics")

        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/plain")
        self.assertIn("app_uptime_seconds", body)
        self.assertIn('app_info{name="devops-demo-app",version="0.1.0"} 1', body)

    def test_unknown_route_returns_404(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(f"{self.base_url}/missing", timeout=2)

        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
