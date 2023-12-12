import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import datetime as dt
import pytz

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.google_calendar import GoogleCalendar, parse_time, get_tz_offset


class TestGoogleCalendar(unittest.TestCase):
    
    def test_get_events(self):
        with patch.object(GoogleCalendar, 'authenticate', return_value=None) as mock_authenticate:
            calendar = GoogleCalendar()
            self.assertIsNone(calendar.creds)
            begin = "2023-12-01"
            end = "2024-01-01"
            self.assertTrue(mock_authenticate.called)
            with patch("clock2py.google_calendar.build") as mock_build:
                mock_events = {}
                result = calendar.get_events(begin=begin, end=end)
                self.assertTrue(isinstance(result, dict))
                self.assertEqual(result, 5)

    def test_parse_time(self):
        self.assertEqual(parse_time("2023-12-01"), dt.datetime(2023, 12, 1))
        self.assertEqual(parse_time("2023-12-01T12:30"), dt.datetime(2023, 12, 1, 12, 30))
        self.assertEqual(parse_time("2023-12-01T12:30:12"), dt.datetime(2023, 12, 1, 12, 30, 12))
        self.assertEqual(parse_time("2023-12-01T12:30:00"), dt.datetime(2023, 12, 1, 12, 30, 0))
        with self.assertRaises(ValueError):
            self.assertEqual(parse_time("2023-12-01T12:60:00"), dt.datetime(2023, 12, 1, 12, 30, 0))

        self.assertEqual(parse_time("2023-12-01T12:10:00+02:00"), dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=dt.timezone(dt.timedelta(seconds=7200))))

    def test_timezone(self):
        dtime = dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=dt.timezone(dt.timedelta(seconds=7200)))
        self.assertEqual(get_tz_offset(dtime), "+02:00")

        dtime = dt.datetime(2023, 12, 1, 12, 10, 0)
        self.assertEqual(get_tz_offset(dtime), "+01:00")

        tz = pytz.timezone("UTC")
        dtime = dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=tz)
        self.assertEqual(get_tz_offset(dtime), "+00:00")

        tz = pytz.timezone("CET")
        dtime = dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=tz)
        self.assertEqual(get_tz_offset(dtime), "+01:00")

        tz = pytz.timezone("EST")
        dtime = dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=tz)
        self.assertEqual(get_tz_offset(dtime), "-05:00")

        dtime = dt.datetime(2023, 12, 1, 12, 10, 0, tzinfo=dt.timezone(dt.timedelta(seconds=-7200)))
        self.assertEqual(get_tz_offset(dtime), "-02:00")



if __name__ == "__main__":
    unittest.main(verbosity=2)
