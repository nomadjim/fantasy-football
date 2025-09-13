import os
import json
import requests
from flask import Flask, request, redirect
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("YAHOO_REDIRECT_URI")

TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"

app = Flask(__name__)

@app.route("/")
def home():
    # Step 1: Redirect user to Yahoo login
    auth_url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=fspt-w"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Step 2: Yahoo sends code to /callback
    code = request.args.get("code")
    if not code:
        return "❌ No code received from Yahoo."

    # Step 3: Exchange code for tokens
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    auth = (CLIENT_ID, CLIENT_SECRET)

    response = requests.post(TOKEN_URL, data=data, auth=auth)
    if response.status_code != 200:
        return f"❌ Token request failed: {response.text}"

    tokens = response.json()
    with open("yahoo_token.json", "w") as f:
        json.dump(tokens, f, indent=2)

    return "✅ Yahoo OAuth complete. Tokens saved to yahoo_token.json."

if __name__ == "__main__":
    app.run(port=8080)