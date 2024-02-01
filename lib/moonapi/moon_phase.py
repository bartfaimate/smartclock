import base64
import requests
import datetime as dt

from typing import Literal, Union
from moonapi.exceptions import MoonPhaseApiError

from enum import Enum

DateLike = Union[str, dt.datetime, dt.date]


class DSO(Enum):
    G = "Galaxy"
    DU = "Duplicate"
    A = "Asterism"
    STR = "Star"
    PNE = "Planetary Nebula"
    NF = "Not Found"
    OC = "Open Cluster"
    GC = "Globular Cluster"
    PG = "Part of Galaxy"
    SNR = "Super Nova Remnat"
    SC = "Star Cloud"



class MoonPhaseApi:

    def __init__(self, app_id: str, app_secret: str) -> None:
        userpass = f"{app_id}:{app_secret}"
        self.app_id = app_id
        self.app_secret = app_secret
        self.auth_string = base64.b64encode(userpass.encode()).decode()
        self.host = "https://api.astronomyapi.com/"

    def body_positions(
        self,
        lat: float,
        long: float,
        elevation: int,
        from_date: DateLike,
        to_date: DateLike,
        time: str,
    ):
        
        from_date = from_date if isinstance(from_date, str) else from_date.strftime("%Y-%m-%d")
        to_date = to_date if isinstance(to_date, str) else to_date.strftime("%Y-%m-%d")


        url = f"{self.host}api/v2/bodies/positions?latitude={lat}&longitude={long}&elevation={elevation}&from_date={from_date}&to_date={to_date}&time={time}"

        resp = requests.get(url, auth=(self.app_id, self.app_secret))
        if not resp.ok:
            raise MoonPhaseApiError(resp.status_code)
        return resp.json()

    def moon_phase(
        self,
        lat: float,
        long: float,
        date: Union[str, dt.datetime, dt.date],
        format: Literal["png", "svg"] = "png",
        moon_style: Literal["default", "shaded", "sketch"] = "default",
        background_style: Literal["stars", "solid"] = "stars",
        heading_color: Literal["white"] = "white",
        type: Literal["landscape-simple", "portrait-simple"] = "landscape-simple",
        orientation: Literal["south-up", "north-up"] = "north-up"
    ):

        date = date if isinstance(date, str) else date.strftime("%Y-%m-%d")
        url = f"{self.host}api/v2/studio/moon-phase"

        body = {
            "format": format,
            "style": {
                "moonStyle": moon_style,
                "backgroundStyle": background_style,
                "backgroundColor": heading_color,
                "headingColor": heading_color,
                "textColor": heading_color,
            },
            "observer": {"latitude": lat, "longitude": long, "date": date},
            "view": {"type": type, "orientation": orientation},
        }

        resp = requests.post(url, json=body, auth=(self.app_id, self.app_secret))
        if not resp.ok:
            raise MoonPhaseApiError(resp.status_code)
        return resp.json()
    

    # def star_chart(
    #     self,
    #     lat: float,
    #     long: float,
    #     date: Union[str, dt.datetime, dt.date],
        
    #     format: Literal["png", "svg"] = "png",
    #     moon_style: Literal["default", "inverted", "navy", "red"] = "default",
    # ):

    #     date = date if isinstance(date, str) else date.strftime("%Y-%m-%d")
    #     url = f"{self.host}api/v2/studio/moon-phase"

    #     body = {
    #         "format": format,
    #         "style": {
    #             "moonStyle": moon_style,
    #             "backgroundStyle": background_style,
    #             "backgroundColor": "red",
    #             "headingColor": heading_color,
    #             "textColor": "red",
    #         },
    #         "observer": {"latitude": lat, "longitude": long, "date": date},
    #         "view": {"type": "area", "orientation": "south-up"},
    #     }

    #     resp = requests.post(url, json=body, auth=(self.app_id, self.app_secret))
    #     if not resp.ok:
    #         raise MoonPhaseApiError(resp.status_code)
    #     return resp.json()
