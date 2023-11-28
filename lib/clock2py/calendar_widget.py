import datetime
import sys

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
from PySide2.QtGui import QColor, QPainter, QMouseEvent, QPen, QFont, QPaintEvent
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
        self.day_widget = QListWidget()
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
        self.day_widget.clear()

        events = self.calendar.get_events_for_day(date)

        for timestamp, summary in events.items():
            timestamp: datetime.datetime
            item = f"{timestamp.time()} {summary}"
            self.day_widget.addItem(str(item))


class DayWidget(QWidget):

    def __init__(self, parent) -> None:
        self.parent = parent
        super(DayWidget, self).__init__(parent)
        self.setGeometry(parent.geometry())

    def paintEvent(self, event: QPaintEvent) -> None:
       self.paintDay()

    def paintDay(self):
        self.fontsize = 20
        painter = QPainter(self)

        pen = QPen()
        pen.setColor(Qt.green)
        painter.setPen(Qt.black)
        # painter.setFont(QFont("Arial", min(self.height(), self.width()) - 60))
        font = QFont("Helvetica")
        font.setPixelSize(self.fontsize)
        painter.setFont(font)

        for i in range(24):
            y1, y2 = i * 40,   i * 40
            line = QLine(0, y1, self.width(), y2)
            painter.drawText(0, y1, f"{i}")
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
        calendar = DayWidget(parent=self)
        scrollarea.setWidget(calendar)

        layout.addWidget(scrollarea)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
