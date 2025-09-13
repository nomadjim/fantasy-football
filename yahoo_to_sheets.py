import os
import json
import requests
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("YAHOO_REDIRECT_URI", "http://localhost:8080/")
SCOPE = os.getenv("YAHOO_SCOPE", "fspt-w")

AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
TOKEN_FILE = "token.json"


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def get_yahoo_session():
    # Try to load token from file
    token = load_token()
    extra = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}

    if token:
        # Refresh automatically if needed
        return OAuth2Session(
            CLIENT_ID,
            token=token,
            auto_refresh_url=TOKEN_URL,
            auto_refresh_kwargs=extra,
            token_updater=save_token,
        )

    # No saved token — start fresh login
    yahoo = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=[SCOPE])
    authorization_url, state = yahoo.authorization_url(AUTH_URL)

    print("Go to this URL and authorize:")
    print(authorization_url)

    redirect_response = input("Paste the full redirect URL here: ").strip()

    token = yahoo.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=redirect_response,
    )

    save_token(token)
    return yahoo


def main():
    yahoo = get_yahoo_session()

    # Example call: Get logged-in user’s games
    url = "https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games"
    response = yahoo.get(url, headers={"Accept": "application/json"})

    if response.status_code == 200:
        print("Yahoo API call success!")
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()