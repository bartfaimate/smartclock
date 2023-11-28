from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QStackedWidget,
    QStackedLayout,
    QSwipeGesture,
    QGestureRecognizer,
)
from PySide2.QtCore import QEvent, Qt, QPoint
from PySide2.QtGui import QMouseEvent

from clock2py.calendar_widget import Calendar2Widget
from clock2py.clock_widget import ClockWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        self.resize(840, 480)
        # self.windowType()
        layout = QHBoxLayout(self)
        calendar = Calendar2Widget()
        clock = ClockWidget(parent=self)

        self.stacked_widget = QStackedLayout(self)
        self.stacked_widget.addWidget(clock)
        self.stacked_widget.addWidget(calendar)
        self.index = self.stacked_widget.currentIndex()
        layout.addLayout(self.stacked_widget)
        self.setLayout(layout)

        self.swipe = 0, 0

    # def event(self, event: QEvent) -> bool:
    #     print(event.type())
    #     return super().event(event)

    # def event(self, event: QEvent):
    #     if event.type() == QEvent.Gesture:
    #         print("gesture")
    #     if event.type() == QEvent.MouseButtonPress:
    #         print("press")
    #         return self.handleswipe(event)
    #     if event.type() == QEvent.DragMove:
    #         print("drag")

    #     return True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print("press")
        self.startPos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        print("release")
        self.endPos = event.pos()
        self.mov = self.endPos - self.startPos
        self.handleswipe(self.mov)
        return super().mouseReleaseEvent(event)

    def handleswipe(self, movement: QPoint):
        if movement.y() > 100:
            return
        if abs(movement.x()) < abs(3 * movement.y()):
            return
        if movement.x() > 0:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - 1)
