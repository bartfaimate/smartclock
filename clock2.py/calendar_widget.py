from PySide2.QtWidgets import QWidget, QApplication, QCalendarWidget, QHBoxLayout
from PySide2.QtCore import  QLocale, Qt, QDate
from  PySide2.QtGui import QColor, QBrush

from google_calendar import authenticate, get_events
import PySide2

import sys

COLORS = {
    "EVENT": {
        "BG": QColor(10, 64, 155),
        "FONT": QColor(10,10,155),
    },
}

class CalendarWidget(QCalendarWidget):

    def __init__(self):
        super(CalendarWidget, self).__init__()
        self.setNavigationBarVisible(True)
        self.setLocale(QLocale.English)
        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.init_calendar()

    def init_calendar(self):
        creds = authenticate()
        self.events = get_events(creds)

    def paintCell(self, painter: PySide2.QtGui.QPainter, rect: PySide2.QtCore.QRect, date: PySide2.QtCore.QDate) -> None:
        for event_date, summary in self.events.items():

            if date == QDate(event_date):
                painter.save()
                painter.setPen(COLORS["EVENT"]["FONT"])
                flags = Qt.TextSingleLine | Qt.AlignCenter
                painter.drawText(rect, flags, str(date.day()))

                # painter.setPen(COLORS["EVENT"]["BG"])
                # painter.drawRect(rect)
                # painter.fillRect(rect, COLORS["EVENT"]["BG"])
                # painter.drawRect(rect)
            else:
                super(CalendarWidget, self).paintCell(painter, rect, date)
