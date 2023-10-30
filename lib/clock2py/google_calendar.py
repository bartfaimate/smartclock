import datetime
import sys
from pathlib import Path
from typing import Union
from collections import defaultdict
from functools import lru_cache
from cachetools import cached, TTLCache

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file credentials.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

import datetime as dt

import logging


log = logging.getLogger("google-calendar")
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stdout)


class GoogleCalendar:

    timeout = 900

    def __init__(self) -> None:
        self.token_file = Path(__file__).parent.joinpath("token.json").resolve()
        self.credentials_file = Path(__file__).parent.joinpath("credentials.json").resolve()
        try:
            self.creds = self.authenticate()
        except RuntimeError as e:
            if self.token_file.exists():
                self.token_file.unlink()
                self.authenticate()
        self.timeout = 1800

    def authenticate(self):
        creds = None
        # The file credentials.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        
        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(self.token_file.as_posix(), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    log.error(f"Authentication failed {e}")
                    raise RuntimeError("Authentication failed")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file.as_posix(), SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with self.token_file.open("w") as token:
                token.write(creds.to_json())
        return creds

    # @lru_cache(maxsize=128)
    @cached(TTLCache(128, ttl=timeout))
    def get_events_for_month(self, year: int, month: int):
        begin = datetime.datetime(year=year, month=month, day=1) - datetime.timedelta(
            days=5
        )
        end = begin + datetime.timedelta(days=40)

        return self.get_events(max_results=500, begin=begin, end=end)

    def get_events_this_month(self):
        begin = datetime.datetime.now() - dt.timedelta(days=30)
        end = datetime.datetime.now() + dt.timedelta(days=30)

        return self.get_events(max_results=500, begin=begin, end=end)

    # @lru_cache(maxsize=128)
    @cached(TTLCache(128, ttl=timeout))
    def get_event_for_day(self, date: Union[str, datetime.datetime]):
        begin = parse_time(date)
        end = begin + dt.timedelta(days=1)
        return self.get_events(max_results=50, begin=begin, end=end)

    # @lru_cache(maxsize=128)
    @cached(TTLCache(128, ttl=timeout))
    def get_events(self, max_results: int = 100, begin=None, end=None):
        if not begin or not end:
            now = datetime.datetime.now()
            begin = begin or now
            end = end or (dt.timedelta(days=30) + begin)
        begin = parse_time(begin)
        end = parse_time(end)
        begin = begin.isoformat() + "Z"
        end = end.isoformat() + "Z"

        try:
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API
            log.info(f"Getting the upcoming events between {begin} and {end}")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=begin,
                    timeMax=end,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                log.warning("No upcoming events found.")
                return {}

            # Prints the start and name of the next 10 events
            result = {}
            result = defaultdict(list)
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                start = parse_time(start)
                end = event["end"].get("dateTime", event["end"].get("date"))
                end = parse_time(end)
                for date_ in subset(start_date=start, end_date=end):
                    log.info(f"{date_}: {event['summary']}")
                    result[date_].append(event["summary"])
            return result

        except HttpError as error:
            log.error(f"An error occurred: {error}")


def subset(start_date, end_date):
    start_date = parse_time(start_date)
    end_date = parse_time(end_date)
    duration = max(1, (end_date - start_date).days)
    for i in range(duration):
        yield start_date + datetime.timedelta(days=i)


def parse_time(time_expr: str) -> datetime.datetime:
    if not time_expr:
        raise RuntimeError("Tiem exrpession should be provided")
    if isinstance(time_expr, datetime.datetime):
        return time_expr
    if isinstance(time_expr, datetime.date):
        return datetime.datetime(
            time_expr.year, time_expr.month, time_expr.day, 0, 0, 0
        )
    if not isinstance(time_expr, str):
        return time_expr
    try:
        dt_part, tz_info = time_expr.split("+")
        tz_info = tz_info.replace(":", "")
        time_expr = f"{dt_part}+{tz_info}"
        time_expr = dt.datetime.strptime(time_expr, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        time_expr = dt.datetime.strptime(time_expr, "%Y-%m-%d")
    return time_expr


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    calendar = GoogleCalendar()
    # calendar.get_events()
    # calendar.get_events_this_month()
    # calendar.get_event_for_day("2023-10-13")
    calendar.get_events_for_month(2023, 12)


if __name__ == "__main__":
    main()
