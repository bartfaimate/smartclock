import logging
import sys

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

from clock2py.calendar_with_day_widget import CalendarWithDayWidget
from clock2py.clock_widget import ClockWidget
from clock2py.moon_phase_widget import MoonPhaseWidget


log = logging.getLogger("window")
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stdout)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowFlags(
            Qt.Window
            # | Qt.FramelessWindowHint
            # | Qt.WindowSystemMenuHint
            # | Qt.WindowMinimizeButtonHint
            # | Qt.WindowMaximizeButtonHint
            # | Qt.WindowCloseButtonHint
        )
        self.resize(840, 480)
        # self.windowType()
        layout = QHBoxLayout(self)
        
        self.stacked_widget = QStackedLayout(self)
        widgets = self.init_widgets()
        if not widgets:
            raise RuntimeError("No widgets could be initialised... Shutting down")
        for widget in widgets:
            self.stacked_widget.addWidget(widget)
      

        self.index = self.stacked_widget.currentIndex()
        layout.addLayout(self.stacked_widget)
        self.setLayout(layout)

        self.swipe = 0, 0

    def init_widgets(self):
        widgetst_to_init = {
            "clock": ClockWidget,
            "calendar": CalendarWithDayWidget,
            "moon_widget": MoonPhaseWidget,

        }
        widgets = []
        for name, widget_class in widgetst_to_init.items():
            try:
                log.info(f"Initialise {name}...")
                widget = widget_class(parent=self)
            except:
                log.warning(f"Could not initialise {name} widget")
            else:
                widgets.append(widget)
        
        return widgets

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # print("press")
        self.startPos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # print("release")
        self.endPos = event.pos()
        self.mov = self.endPos - self.startPos
        self.handleswipe(self.mov)
        return super().mouseReleaseEvent(event)

    def handleswipe(self, movement: QPoint):
        if movement.y() > 100:
            return
        if abs(movement.x()) < 50:
            return
        if abs(movement.x()) < abs(3 * movement.y()):
            return
        if movement.x() > 0:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - 1)
