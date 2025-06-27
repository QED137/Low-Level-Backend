# http_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer  # Built-in HTTP server classes

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 🧠 HTTP parsing is already done when this method is called.
        # `self.path` gives the requested URL path like '/ask'
        if self.path == "/ask":
            self.send_response(200)  # Send HTTP status 200 OK
            self.send_header("Content-Type", "text/plain")  # Set content type header
            self.end_headers()  # End of headers
            self.wfile.write(b"Hello from http.server!")  # Write body of response
        else:
            self.send_error(404, "Not Found")  # Built-in method to return 404 error

print("Starting server at http://localhost:8000")
HTTPServer(("", 8000), MyHandler).serve_forever()  # Start HTTP server loop
