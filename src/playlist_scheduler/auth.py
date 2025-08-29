from pathlib import Path
from platformdirs import user_cache_dir, user_data_dir
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

APP_NAME = "PlaylistScheduler"
APP_AUTHOR = "euclio"

SCOPES = [
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def fetch_google_credentials():
    creds = None

    creds_file = Path(user_cache_dir(APP_NAME, APP_AUTHOR)) / "token.json"
    secrets_file = Path(user_data_dir(APP_NAME, APP_AUTHOR)) / "credentials.json"

    if creds_file.exists():
        creds = Credentials.from_authorized_user_file(creds_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)

        creds_file.parent.mkdir(parents=True, exist_ok=True)

        with creds_file.open("w") as token:
            token.write(creds.to_json())

    return creds
