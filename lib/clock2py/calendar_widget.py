from PySide2.QtWidgets import QWidget, QApplication, QCalendarWidget, QHBoxLayout
from PySide2.QtCore import QLocale, Qt, QDate, QRect, QPoint, Slot
from PySide2.QtGui import QColor, QBrush, QPainter

from .google_calendar import GoogleCalendar
import PySide2

import datetime
import sys

COLORS = {
    "EVENT": {
        "BG": QColor(10, 64, 155, 50),
        "FONT": QColor(10, 10, 10),
    },
}


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

    def init_calendar(self):
        google_calendar = GoogleCalendar()
        self.events = google_calendar.get_events_this_month()
        self.events_dates = {QDate(date) for date in self.events}
        return google_calendar

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
        self.google_calendar.get_event_for_day(date)

    @Slot(int, int)
    def handleCurrentPageChanged(self, year: int, month: int):
        self.get_events_for_month(year, month)

    @Slot(QDate)
    def handleClicked(self, date: QCalendarWidget):
        self.get_events_for_day(date)
