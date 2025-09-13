import os
import ssl
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
REDIRECT = os.getenv("YAHOO_REDIRECT_URI")

PORT = 8080
CODE = None

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global CODE
        query = urlparse(self.path).query
        params = parse_qs(query)
        if "code" in params:
            CODE = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Yahoo auth complete. You can close this window.".encode("utf-8"))

httpd = socketserver.TCPServer(("localhost", PORT), OAuthHandler)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print("Go to this URL and log in:")
print(f"https://api.login.yahoo.com/oauth2/request_auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT}&response_type=code&scope=fspt-w")

webbrowser.open(f"https://api.login.yahoo.com/oauth2/request_auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT}&response_type=code&scope=fspt-w")

httpd.handle_request()

print(f"CODE captured: {CODE}")