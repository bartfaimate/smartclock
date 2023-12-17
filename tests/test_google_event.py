import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import datetime as dt
import pytz

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.google_event import GoogleEvent


class TestGoogleEvent(unittest.TestCase):

    def test_constructor(self):
        event = GoogleEvent(start="2023-12-12", end="2023-12-13", summary="Test")
        self.assertEqual(event.duration, dt.timedelta(1))

        event = GoogleEvent(start="2023-12-12T12:00", end="2023-12-13T9:00", summary="Test")
        expected = 21*3600
        self.assertEqual(event.duration, dt.timedelta(seconds=expected))

        event = GoogleEvent(start="2023-12-12T12:00", end="2023-12-19T9:00", summary="Test")
        expected = 21*3600
        self.assertEqual(event.duration, dt.timedelta(days=6, seconds=expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
