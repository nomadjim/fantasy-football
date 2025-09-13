import os
import ssl
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
REDIRECT = os.getenv("YAHOO_REDIRECT_URI", "https://localhost:8080/")

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
            self.wfile.write(b"Yahoo auth complete. You can close this window.")
            print(f"\nCODE captured: {CODE}")

def main():
    global CODE
    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
        # Wrap socket with SSL
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

        auth_url = (
            f"https://api.login.yahoo.com/oauth2/request_auth"
            f"?client_id={CLIENT_ID}"
            f"&redirect_uri={REDIRECT}"
            f"&response_type=code"
            f"&scope=fspt-w"
        )

        print("Go to this URL to log in with Yahoo:\n")
        print(auth_url + "\n")
        webbrowser.open(auth_url)

        print(f"Listening on {REDIRECT} ... waiting for Yahoo redirect.")
        httpd.handle_request()

        if CODE:
            print(f"\n✅ Authorization code captured: {CODE}")
        else:
            print("\n❌ No code captured. Try again.")

if __name__ == "__main__":
    main()