from PySide2.QtWidgets import QWidget, QApplication, QCalendarWidget, QHBoxLayout
from PySide2.QtCore import  QLocale, Qt, QDate
from  PySide2.QtGui import QColor, QBrush


import PySide2

import sys

from calendar_widget import CalendarWidget


class ClockWidget(QWidget):

    def __init__(self):
        super(self).__init__()




class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(840, 480)
        layout = QHBoxLayout(self)
        calendar = CalendarWidget()
        layout.addWidget( calendar)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
