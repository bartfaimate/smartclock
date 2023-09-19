import datetime
import os.path

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

import datetime as dt


def authenticate():
    creds = None
    # The file credentials.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = Path(__file__).parent.joinpath('token.json').resolve()
    credentials_file = Path(__file__).parent.joinpath('credentials.json').resolve()

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(token_file.as_posix(), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file.as_posix(), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with token_file.open("w") as token:
            token.write(creds.to_json())
    return creds


def get_events(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return {}

        # Prints the start and name of the next 10 events
        result = {}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = parse_time(start)

            print(start, event['summary'])
            result.update({start: event['summary']})
        return result

    except HttpError as error:
        print('An error occurred: %s' % error)


def parse_time(time_string: str):
    try:
        dt_part, tz_info = time_string.split("+")
        tz_info = tz_info.replace(":", "")
        time_string = f"{dt_part}+{tz_info}"
        time_string = dt.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        time_string = dt.datetime.strptime(time_string, "%Y-%m-%d")
    return time_string

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = authenticate()
    get_events(creds)


if __name__ == '__main__':
    main()
