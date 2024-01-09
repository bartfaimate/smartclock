import datetime
import sys

import PySide2
from PySide2.QtCore import (
    QLocale,
    Qt,
    QDate,
    QRect,
    QPoint,
    Slot,
    QTimer,
    QLine,
    QEvent,
)
from PySide2.QtGui import QColor, QPainter, QMouseEvent, QPen, QFont, QPaintEvent, QPainterPath
from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QCalendarWidget,
    QHBoxLayout,
    QSplitter,
    QListWidget,
    QScrollArea,
    QGraphicsWidget,
)

from clock2py.google_calendar import GoogleCalendar
from clock2py.day_widget import DayWidget
from clock2py.calendar_widget import CalendarWidget
from clock2py.google_event import GoogleEvent

COLORS = {
    "EVENT": {
        "BG": QColor(10, 64, 155, 50),
        "FONT": QColor(10, 10, 10),
    },
}


class CalendarWithDayWidget(QSplitter):
    def __init__(self, parent=None):
        super(CalendarWithDayWidget, self).__init__()
        self.parent = parent
        self.calendar = CalendarWidget(parent=self)
        # self.day_widget = QListWidget()
        if self.parent:
            self.setGeometry(parent.geometry())

        today = datetime.datetime.today()
        self.scrollarea = QScrollArea()
        self.day_widget = DayWidget(parent=self.scrollarea, date=QDate(today))

        self.scrollarea.setWidget(self.day_widget)
        self.addWidget(self.calendar)
        # self.addWidget(self.scrollarea)
        self.calendar.clicked.connect(self.handleClicked)

    @Slot(QDate)
    def handleClicked(self, date: QCalendarWidget):
        self.addWidget(self.scrollarea)

        self.day_widget.setDate(date)
        # self.day_widget.clear()
        #
        # events = self.calendar.get_events_for_day(date)
        #
        # for timestamp, google_event in events.items():
        #     timestamp: datetime.datetime
        #     item = f"{timestamp.time()} {google_event[0].summary}"
        #     self.day_widget.addItem(str(item))


class Window(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        # self.setGeometry(100, 100, 1920, 1080)
        self.setGeometry(100, 100, 840, 480)

        layout = QHBoxLayout()
        scrollarea = QScrollArea()
        calendar = CalendarWithDayWidget()
        scrollarea.setWidget(scrollarea)

        layout.addWidget(calendar)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
