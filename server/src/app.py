import socketserver
import http.server


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # self.path = f"/client/index.html"
            pass
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

PORT = 8000
handleRequest = MyHTTPRequestHandler
server = socketserver.TCPServer(("", PORT), handleRequest)

if __name__ == "__main__":
    print("[server] Runnig on port:", PORT )
    print(f"[server] http://localhost:{PORT}", )
    server.serve_forever()