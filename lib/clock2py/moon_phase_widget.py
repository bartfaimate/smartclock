from cachetools import cached, LRUCache
import datetime as dt
import sys
import typing
import os
from pathlib import Path

from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from PySide2.QtCore import Qt, QTimer, QTime, QRect, Slot, QEvent
from PySide2.QtGui import QFont, QPainter, QPalette, QColor, QPen, QPaintEvent 
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PySide2.QtSvg import QSvgWidget


sys.path.append(Path(__file__).parents[2].joinpath("lib").as_posix())

from moonapi.moon_phase import MoonPhaseApi
from moonapi.exceptions import MoonPhaseApiError

class MoonPhaseWidget(QSvgWidget):

    def __init__(self, parent=None, posx=0, posy=0):
        super(MoonPhaseWidget, self).__init__(parent)


        self.parent = parent
        self.position = (posx, posy)
        
        self.timer = QTimer()
        # self.timer.timeout.connect(self.handleTimeout)
        self.timer.start(1000 * 60)  # update every minute

        self.moon_api = self._init_moon_api()
        lat, long = MoonPhaseWidget.get_lat_long("Vienna")
        result = self.moon_api.moon_phase(lat=lat, long=long, date=dt.datetime.today(), format="svg")
        destination = self.moon_api.download_image(result["data"]["imageUrl"])
        self.load(destination.as_posix())


    @staticmethod
    @cached(LRUCache(maxsize=128))
    def get_lat_long(city: str):
        loc = Nominatim(user_agent="Geopy Library")
        getLoc = loc.geocode(city)

        lat, long = (
            getLoc.latitude,
            getLoc.longitude,
        )
        return lat, long

    def _init_moon_api(self):
        APP_ID = os.getenv("APPLICATION_ID")
        APP_SECRET = os.getenv("APPLICATION_SECRET")
        return MoonPhaseApi(APP_ID, APP_SECRET)
    
    # @Slot()
    # def handleTimeout(self):
    #     # self.paint()
    #     self.update()


class Window(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        # self.setGeometry(100, 100, 1920, 1080)
        self.setGeometry(100, 100, 840, 480)

        layout = QHBoxLayout()

        digit = MoonPhaseWidget(parent=self, posx=20, posy=20)

        layout.addWidget(digit)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
