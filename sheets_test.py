from __future__ import print_function
import os.path
from dotenv import load_dotenv
load_dotenv()
import os
CLIENT_ID = os.getenv("dj0yJmk9TFVCWVV2N1RYUWQwJmQ9WVdrOU9XTjJaV015VDBjbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWNk")
CLIENT_SECRET = os.getenv("59fc330f20faa328c7c4713789bff184caada70a")
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: read-only access
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Your Google Sheet ID
SPREADSHEET_ID = "14TtTE7q8Bmqpd0gRizh5Lh9kg-hS8vcvXNYMAbytk8E"

# Match these with your actual tab names in the sheet
RANGES = {
    "Roster": "Roster!A1:Z50",
    "FreeAgents": "FreeAgents!A1:Z50",
    "Matchups": "Matchups!A1:Z50"
}

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    for name, rng in RANGES.items():
        print(f"\n=== {name} Data ===")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=rng
        ).execute()
        values = result.get('values', [])

        if not values:
            print("No data found.")
        else:
            for row in values:
                print(row)

if __name__ == '__main__':
    main()