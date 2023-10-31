from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QStackedWidget,
    QStackedLayout,
    QSwipeGesture,
    QGestureRecognizer
)
from PySide2.QtCore import QEvent
from PySide2.QtGui import QMouseEvent

from clock2py.calendar_widget import Calendar2Widget
from clock2py.clock_widget import ClockWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(840, 480)
        # self.windowType()
        layout = QHBoxLayout(self)
        calendar = Calendar2Widget()
        clock = ClockWidget(parent=self)

        stacked_widget = QStackedLayout(self)
        stacked_widget.addWidget(clock)
        stacked_widget.addWidget(calendar)

        layout.addLayout(stacked_widget)
        self.setLayout(layout)

    def event(self, event: QEvent):
        if event.type() == QEvent.Gesture:
            print("gesture")
        if event.type() == QEvent.MouseButtonPress:
            print("press")
            return self.handleswipe(event)
        if event.type() == QEvent.DragMove:
            print("drag")

        return True
    
    def handleswipe(self, event: QMouseEvent):
        print(event.pos())

