import datetime as dt
from typing import  Union
from dataclasses import dataclass
import  logging
import sys

from clock2py.helpers.date_helper import parse_time

log = logging.getLogger("google-event")
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stdout)


@dataclass
class GoogleEvent:

    created: dt.datetime
    updated: dt.datetime
    start: dt.datetime
    end: dt.datetime
    duration: dt.timedelta
    summary: str
    description: str

    def __init__(self,
                 start: Union[str, dt.datetime],
                 end: Union[str, dt.datetime],
                 summary: str,
                 created: Union[str, dt.datetime] = None,
                 updated: Union[str, dt.datetime] = None,
                 description:str = None):
        self.start = parse_time(start)
        self.end = parse_time(end)
        self.summary = summary
        self.created = parse_time(created) if created else dt.datetime.now()
        self.updated = parse_time(updated) if updated else dt.datetime.now()
        self.description = description or ""

        self.duration = self.end - self.start


