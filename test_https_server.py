import http.server, ssl

server_address = ('localhost', 8080)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile="certs/key.pem",
    certfile="certs/cert.pem",
    server_side=True
)
print("Serving on https://localhost:8080/")
httpd.serve_forever()