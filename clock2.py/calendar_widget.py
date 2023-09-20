from PySide2.QtWidgets import QWidget, QApplication, QCalendarWidget, QHBoxLayout
from PySide2.QtCore import  QLocale, Qt, QDate, QRect, QPoint
from  PySide2.QtGui import QColor, QBrush, QPainter

from google_calendar import authenticate, get_events
import PySide2

import sys

COLORS = {
    "EVENT": {
        "BG": QColor(10, 64, 155, 50),
        "FONT": QColor(10,10,10),
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
        self.events_dates = {QDate(date) for date in self.events}

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
            marker_coords_x = rect.x() + rect.width()//2
            marker_coords_y = rect.y() + rect.height()//4
            painter.setBrush(COLORS["EVENT"]["BG"])
            painter.drawEllipse(QPoint(marker_coords_x, marker_coords_y), 5,5)
            # painter.drawRect(rect)
            # painter.fillRect(rect, COLORS["EVENT"]["BG"])
            # painter.drawRect(rect)

    
    def get_events_for_month(self, date:  QDate):
        
        raise NotImplementedError
    
    def get_events_for_day(self, date:  QDate):
        
        raise NotImplementedError