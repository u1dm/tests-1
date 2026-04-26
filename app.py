import json
import os
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


APP_NAME = os.getenv("APP_NAME", "devops-demo-app")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
STARTED_AT = time.time()


class AppHandler(BaseHTTPRequestHandler):
    server_version = "DevOpsDemoHTTP/0.1"

    def do_GET(self):
        routes = {
            "/": self.index,
            "/health": self.health,
            "/version": self.version,
            "/metrics": self.metrics,
        }
        handler = routes.get(self.path)

        if handler is None:
            self.respond_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return

        handler()

    def index(self):
        self.respond_json(
            {
                "name": APP_NAME,
                "version": APP_VERSION,
                "endpoints": ["/health", "/version", "/metrics"],
            }
        )

    def health(self):
        self.respond_json({"status": "ok"})

    def version(self):
        self.respond_json({"name": APP_NAME, "version": APP_VERSION})

    def metrics(self):
        uptime_seconds = max(0, int(time.time() - STARTED_AT))
        body = (
            "# HELP app_uptime_seconds Application uptime in seconds\n"
            "# TYPE app_uptime_seconds counter\n"
            f"app_uptime_seconds {uptime_seconds}\n"
            "# HELP app_info Application build information\n"
            "# TYPE app_info gauge\n"
            f'app_info{{name="{APP_NAME}",version="{APP_VERSION}"}} 1\n'
        )
        self.respond(body, "text/plain; version=0.0.4; charset=utf-8")

    def respond_json(self, payload, status=HTTPStatus.OK):
        self.respond(json.dumps(payload, sort_keys=True) + "\n", "application/json", status)

    def respond(self, body, content_type, status=HTTPStatus.OK):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        return


def create_server(host="0.0.0.0", port=None):
    resolved_port = int(port or os.getenv("PORT", "8000"))
    return ThreadingHTTPServer((host, resolved_port), AppHandler)


def main():
    host = os.getenv("HOST", "0.0.0.0")
    server = create_server(host=host)
    address, port = server.server_address
    print(f"{APP_NAME} {APP_VERSION} listening on {address}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
