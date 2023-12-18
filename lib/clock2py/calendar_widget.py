import datetime
import sys
from enum import  Enum
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
from clock2py.google_event import GoogleEvent

COLORS = {
    "EVENT": {
        "BG": QColor(10, 64, 155, 50),
        "FONT": QColor(10, 10, 10),
    },
}


class Calendar2Widget(QSplitter):
    def __init__(self):
        super(Calendar2Widget, self).__init__()

        self.calendar = CalendarWidget()
        # self.day_widget = QListWidget()
        today = datetime.datetime.today()
        self.day_widget = DayWidget(parent=self, date=QDate(today))
        self.addWidget(self.calendar)
        self.addWidget(self.day_widget)
        self.calendar.clicked.connect(self.handleClicked)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print("cal press")
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        print("cal release")
        return super().mouseReleaseEvent(event)

    @Slot(QDate)
    def handleClicked(self, date: QCalendarWidget):
        self.day_widget.setDate(date)
        # self.day_widget.clear()
        #
        # events = self.calendar.get_events_for_day(date)
        #
        # for timestamp, google_event in events.items():
        #     timestamp: datetime.datetime
        #     item = f"{timestamp.time()} {google_event[0].summary}"
        #     self.day_widget.addItem(str(item))


class HourFormat(Enum):
    FORMAT_AM_PM = 1
    FORMAT_24H = 2


class DayWidget(QWidget):

    FORMAT_MAP = {i : f"am {str(i % 12 ).zfill(2)}" if i < 12 else f"pm {str(i % 12 ).zfill(2)}" for i in range(0, 24)}
    FORMAT_MAP.update({
        0: "am 12",
        12: "pm 12"
    })

    def __init__(self, parent, date: QDate, hour_format:HourFormat = HourFormat.FORMAT_24H) -> None:
        self.parent = parent
        self.date = date
        super(DayWidget, self).__init__(parent)
        self.setGeometry(parent.geometry())
        self.blockheight = 40
        self.hour_format = HourFormat.FORMAT_AM_PM

        self.google_calendar = GoogleCalendar()
        self.google_events = self.getGoogleEventsForDate()

    def setDate(self, date: QDate):
        self.date = date
        self.google_events = self.getGoogleEventsForDate()
        self.update()

    def hourPos(self, hour: int):
        return self.blockheight * hour

    def setHourFormat(self, hour_format: HourFormat):
        self.hour_format = hour_format

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paintDay()
        self.paintGoogleEvents()
        # self.drawRect(0, 24)

    def calculateBlockHeight(self):
        self.blockheight = 40 if self.parent.height() < 24 * 40 else self.parent.height() / 24

    def getGoogleEventsForDate(self):
        date = self.date.toPython()
        self.google_events = self.google_calendar.get_event_for_day(date)
        return self.google_events

    # def addGoogleEvent(self, google_event: GoogleEvent):
    #     raise NotImplementedError

    def paintGoogleEvents(self):
        for event in self.google_events:
            event: GoogleEvent
            end = event.end.hour if event.start.date() == event.end.date() else 24

            self.drawRect(event.start.hour, end, event.summary)

    def drawRect(self, start, end, summary = "", color=Qt.blue):
        self.calculateBlockHeight()

        painter = QPainter(self)

        pen = QPen()
        pen.setColor(color)
        painter.setPen(color)
        height = (end-start) * self.blockheight
        rect = QRect(100, self.hourPos(start), self.width()-200, height)
        rect_center = QPoint(100 + rect.width()/2, self.hourPos(start) + height/2)
        # painter.drawRect(rect)
        path = QPainterPath()
        path.addRoundRect(rect, 10)
        painter.fillPath(path, color)

        pen.setColor(Qt.black)
        painter.setPen(Qt.black)
        painter.drawText(rect_center, summary)

    def paintDay(self):
        self.calculateBlockHeight()
        self.fontsize = 20
        painter = QPainter(self)

        pen = QPen()
        pen.setColor(Qt.green)
        painter.setPen(Qt.black)
        # painter.setFont(QFont("Arial", min(self.height(), self.width()) - 60))
        font = QFont("Helvetica")
        font.setPixelSize(self.fontsize)
        painter.setFont(font)

        self.setFixedHeight(24 * self.blockheight)

        for i in range(1, 25):
            hour = i - 1
            y1, y2 = i * self.blockheight,   i * self.blockheight
            line = QLine(0, y1, self.width(), y2)
            formatted_time = f"{str(hour).zfill(2)}:00" if self.hour_format == HourFormat.FORMAT_24H else f"{self.FORMAT_MAP[hour]}:00"

            painter.drawText(0, y1-self.blockheight+self.fontsize, formatted_time)

            painter.drawLine(line)


class CalendarWidget(QCalendarWidget):
    def __init__(self):
        super(CalendarWidget, self).__init__()
        self.setNavigationBarVisible(True)
        self.setLocale(QLocale.English)
        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.google_calendar = self.init_calendar()
        super(CalendarWidget, self).clicked.connect(self.handleClicked)
        super(CalendarWidget, self).currentPageChanged.connect(
            self.handleCurrentPageChanged
        )
        fetch_period = 5 * 60 * 1000  # 5 min
        # fetch_period = 10 * 1000  # 5 min
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start(fetch_period)

    def init_calendar(self):
        today = QDate().currentDate()
        self.year = today.year()
        self.month = today.month()

        google_calendar = GoogleCalendar()
        self.events = google_calendar.get_events_this_month()
        self.events_dates = {QDate(date) for date in self.events}
        return google_calendar

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print("cal press")
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        print("cal release")
        return super().mouseReleaseEvent(event)
    
    def paintCell(self, painter: QPainter, rect: QRect, date: QDate) -> None:
        super(CalendarWidget, self).paintCell(painter, rect, date)
        today = QDate().currentDate()
        painter.save()
        if date == today:
            # painter.drawRect(rect)
            painter.fillRect(rect, COLORS["EVENT"]["BG"])
            # painter.drawRect(rect)
        painter.restore()

        if date in self.events_dates:
            # painter.setPen(original_color)
            # painter.drawText(rect, flags, str(date.day()))

            # painter.setPen(COLORS["EVENT"]["BG"])
            marker_coords_x = rect.x() + rect.width() // 2
            marker_coords_y = rect.y() + rect.height() // 4
            painter.setBrush(COLORS["EVENT"]["BG"])
            painter.drawEllipse(QPoint(marker_coords_x, marker_coords_y), 5, 5)
            # painter.drawRect(rect)
            # painter.fillRect(rect, COLORS["EVENT"]["BG"])
            # painter.drawRect(rect)

    def get_events_for_month(self, year: int, month: int):
        events = self.google_calendar.get_events_for_month(year, month)
        self.events_dates = {QDate(date) for date in events}

    def get_events_for_day(self, date: QDate):
        date = date.toPython()
        return self.google_calendar.get_event_for_day(date)

    @Slot(int, int)
    def handleCurrentPageChanged(self, year: int, month: int):
        self.year = year
        self.month = month
        self.get_events_for_month(year, month)

    @Slot(QDate)
    def handleClicked(self, date: QCalendarWidget):
        self.get_events_for_day(date)

    @Slot()
    def handleTimeout(self):
        self.fetch()

    def fetch(self):
        # TODO: make cache timed cache
        self.get_events_for_month(self.year, self.month)
        self.update()

    def event(self, event: QEvent) -> bool:
        # print(event.type())
        return super().event(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print("cal press")
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        print("cal release")
        return super().mouseReleaseEvent(event)


class Window(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        # self.setGeometry(100, 100, 1920, 1080)
        self.setGeometry(100, 100, 840, 480)

        layout = QHBoxLayout()
        scrollarea = QScrollArea()
        calendar = DayWidget(parent=self, date=QDate(2023,12,29))
        scrollarea.setWidget(calendar)

        layout.addWidget(scrollarea)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
