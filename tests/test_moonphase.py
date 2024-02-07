import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import datetime as dt

import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from moonapi.moon_phase import MoonPhaseApi

load_dotenv()
loc = Nominatim(user_agent="Geopy Library")

# entering the location name
getLoc = loc.geocode("Vienna")


APP_ID = os.getenv("APPLICATION_ID")
APP_SECRET = os.getenv("APPLICATION_SECRET")


class TestMoonPhaseApi(unittest.TestCase):

    def test_moonphase(self):
        api = MoonPhaseApi(app_id=APP_ID, app_secret=APP_SECRET)
        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        result = api.moon_phase(lat=lat, long=long, date="2024-01-31")

        self.assertTrue(isinstance(result, dict))
        self.assertTrue("imageUrl" in result.get("data", {}))

        ## with datetime
        api = MoonPhaseApi(app_id=APP_ID, app_secret=APP_SECRET)
        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        result = api.moon_phase(lat=lat, long=long, date=dt.datetime(2024, 1, 31), format="svg", orientation="north-up")

        self.assertTrue(isinstance(result, dict))
        self.assertTrue("imageUrl" in result.get("data", {}))

        ## with date
        api = MoonPhaseApi(app_id=APP_ID, app_secret=APP_SECRET)
        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        result = api.moon_phase(lat=lat, long=long, date=dt.date(2024, 1, 31))

        self.assertTrue(isinstance(result, dict))
        self.assertTrue("imageUrl" in result.get("data", {}))

    def test_download(self):
        api = MoonPhaseApi(app_id=APP_ID, app_secret=APP_SECRET)
        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        result = api.moon_phase(lat=lat, long=long, date="2024-01-31")

        self.assertTrue(isinstance(result, dict))
        self.assertTrue("imageUrl" in result.get("data", {}))
        url = result.get("data", {}).get("imageUrl")

        image_path = api.download_image(url)
        self.assertTrue(image_path.exists())
        self.assertTrue(image_path.suffix.endswith("png"))
        with open(image_path, "rb") as f:
            data = f.read()
            self.assertTrue(len(data) > 0)

        ## svg
        result = api.moon_phase(lat=lat, long=long, date="2024-01-31", format="svg")

        self.assertTrue(isinstance(result, dict))
        self.assertTrue("imageUrl" in result.get("data", {}))
        url = result.get("data", {}).get("imageUrl")

        image_path = api.download_image(url)
        self.assertTrue(image_path.exists())
        self.assertTrue(image_path.suffix.endswith("svg"))
        with open(image_path, "rb") as f:
            data = f.read()
            self.assertTrue(len(data) > 0)

    def test_body_positions(self):
        api = MoonPhaseApi(app_id=APP_ID, app_secret=APP_SECRET)
        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        result = api.body_positions(lat=lat, long=long, elevation=100, time="19:30:00", from_date="2024-01-31", to_date="2024-01-31")

        self.assertTrue(isinstance(result, dict))



if __name__ == "__main__":
    unittest.main(verbosity=2)
