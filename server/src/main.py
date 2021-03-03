from http.server import HTTPServer
from controllers.UserController import MyHTTPRequestHandler

print("[server] Iniciando...")
PORT = 3000
handleRequest = MyHTTPRequestHandler
serverAdress = ('', PORT)
server = HTTPServer(serverAdress, handleRequest)

print("[server] Runnig on port:", PORT )
print(f"[server] http://localhost:{PORT}", )

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
server.shutdown()
print("[server] Shutdown...")