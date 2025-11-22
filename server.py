import http.server
import socketserver
import json
import os

PORT = 8000
DATA_FILE = "data.json"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                # Return empty object or null, frontend handles default
                self.wfile.write(b"null")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/data":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open(DATA_FILE, "wb") as f:
                f.write(post_data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_error(404)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
