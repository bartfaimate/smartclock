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


class HourFormat(Enum):
    FORMAT_AM_PM = 1
    FORMAT_24H = 2


class DayWidget_bkp(QWidget):

    FORMAT_MAP = {i : f"am {str(i % 12 ).zfill(2)}" if i < 12 else f"pm {str(i % 12 ).zfill(2)}" for i in range(0, 24)}
    FORMAT_MAP.update({
        0: "am 12",
        12: "pm 12"
    })

    def __init__(self, parent, date: QDate, hour_format:HourFormat = HourFormat.FORMAT_24H) -> None:
        self.parent = parent
        self.date = date
        super(DayWidget_bkp, self).__init__(parent)
        # self.setGeometry(parent.geometry())
        self.blockheight = 20
        self.hour_format = hour_format

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
        # self.setGeometry(parent.geometry())
        self.blockheight = 20
        self.hour_format = hour_format

        self.google_calendar = GoogleCalendar()
        self.google_events = self.getGoogleEventsForDate()

    def setDate(self, date: QDate):
        self.date = date
        self.google_events = self.getGoogleEventsForDate()
        self.update()


    def setHourFormat(self, hour_format: HourFormat):
        self.hour_format = hour_format

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paintDay()
        self.paintGoogleEvents()
        # self.drawRect(0, 24)

    def calculateBlockHeight(self):
        self.blockheight = 40 if self.parent.height() < 24 * 40 else self.parent.height() / 10

    def getGoogleEventsForDate(self):
        date = self.date.toPython()
        self.google_events = self.google_calendar.get_event_for_day(date)
        return self.google_events

    def paintGoogleEvents(self):
        for index, event in enumerate(self.google_events):
            event: GoogleEvent

            self.drawEvent(event, index)

    def drawEvent(self, event: GoogleEvent, index: int):
        color = Qt.white
        self.calculateBlockHeight()
        painter = QPainter(self)

        pen = QPen()
        pen.setColor(color)
        painter.setPen(color)

        height = self.blockheight
        rect = QRect(1, index*height+10, self.width()-200, height)
        time_pos = QPoint(1, index * height+20)
        summary_pos = QPoint(1, index * height + height//2)
        # painter.drawRect(rect)
        path = QPainterPath()
        path.addRoundRect(rect, 10)
        painter.fillPath(path, color)

        pen.setColor(Qt.black)
        painter.setPen(Qt.black)
        painter.drawRoundRect(rect, 10)
        painter.drawText(time_pos, str(event.start))
        painter.drawText(summary_pos, event.summary)


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




class Window(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        # self.setGeometry(100, 100, 1920, 1080)
        self.setGeometry(100, 100, 840, 480)

        layout = QHBoxLayout()
        scrollarea = QScrollArea()
        day_widget = DayWidget(parent=self, date=QDate(2023,12,31))
        scrollarea.setWidget(day_widget)

        layout.addWidget(day_widget)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
