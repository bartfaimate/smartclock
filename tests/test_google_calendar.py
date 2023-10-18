import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.google_calendar import GoogleCalendar


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



if __name__ == "__main__":
    unittest.main(verbosity=2)
