import http.server
import socketserver

PORT = 8000


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        length = int(self.headers["Content-Length"])
        path = self.path[1:]
        with open(path, "wb") as f:
            f.write(self.rfile.read(length))
        self.send_response(200)
        self.end_headers()


Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
