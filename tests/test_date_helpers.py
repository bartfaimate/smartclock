import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import datetime as dt
import pytz

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.helpers.date_helper import parse_time, get_tz_offset, do_ranges_overlap


class TestDateHelpers(unittest.TestCase):

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

    def test_do_ranges_overlap(self):
        start1 = dt.datetime(2023, 12, 1, 12, 0, 0)
        end1 = dt.datetime(2023, 12, 1, 12, 30, 0)

        start2 = dt.datetime(2023, 12, 1, 12, 15, 0)
        end2 = dt.datetime(2023, 12, 1, 12, 30, 0)

        self.assertTrue(do_ranges_overlap(start1, end1, start2, end2))

        start1 = dt.datetime(2023, 12, 1, 12, 0, 0)
        end1 = dt.datetime(2023, 12, 1, 12, 30, 0)

        start2 = dt.datetime(2023, 12, 1, 12, 30, 0)
        end2 = dt.datetime(2023, 12, 1, 12, 40, 0)

        self.assertFalse(do_ranges_overlap(start1, end1, start2, end2))


        start1 = dt.datetime(2023, 12, 1, 12, 0, 0)
        end1 = dt.datetime(2023, 12, 1, 12, 30, 0)

        start2 = dt.datetime(2023, 12, 1, 13, 30, 0)
        end2 = dt.datetime(2023, 12, 1, 13, 40, 0)

        self.assertFalse(do_ranges_overlap(start1, end1, start2, end2))

        start1 = dt.datetime(2023, 12, 1, 12, 0, 0)
        end1 = dt.datetime(2023, 12, 1, 12, 30, 0)

        start2 = dt.datetime(2023, 12, 1, 11, 30, 0)
        end2 = dt.datetime(2023, 12, 1, 13, 40, 0)

        self.assertTrue(do_ranges_overlap(start1, end1, start2, end2))



if __name__ == "__main__":
    unittest.main(verbosity=2)
