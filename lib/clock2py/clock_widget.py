import sys
import typing
from PySide2.QtCore import Qt, QTimer, QTime, QRect, Slot
from PySide2.QtGui import QFont, QPainter, QPalette, QColor, QPen, QPaintEvent
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout


class ClockWidget(QWidget):
    def __init__(self, parent=None, posx=0, posy=0):
        super(ClockWidget, self).__init__(parent)
        self.parent = parent
        self.digit = 0
        self.position = (posx, posy)
        self.hours = 0
        self.minutes = 0
        self.setCurrentTime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start(1000)
        self.fontsize = self.parent.width() * 10 // 25

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paint()

    def drawColons(self, painter):
        pos = 340
        pos = self.parent.width() * 10 // 25
        painter.drawText(pos, self.height() - 60, ":")
        # 840 - 340 = 500
        # 840 - 22 = 818 - 340 = 478 

    def drawHours(self, painter: QPainter, hours: int):
        digit1 = hours % 10
        digit2 = hours // 10
        second = self.width() // 2 + 50
        # painter.drawText(0, self.height() - 60, str(digit2))
        # painter.drawText(second, self.height() - 60, str(digit1))
        hours = f"0{hours}" if hours < 10 else f"{hours}"
        painter.drawText(0, self.height() - 60, hours)


    def drawMinutes(self, painter: QPainter, minutes: int):
        digit1 = minutes % 10
        digit2 = minutes // 10
        first = 430
        first = 430

        first = self.fontsize // 2

        second = self.width() // 2 + 10
        # painter.drawText(first, self.height() - 60, str(digit2))
        # painter.drawText(first + second, self.height() - 60, str(digit1))
        minutes = f"0{minutes}" if minutes < 10 else f"{minutes}"
        painter.drawText(second, self.height() - 60, minutes)


    def paint(self):
        pen = QPen()
        pen.setColor(Qt.green)
        painter = QPainter(self)

        painter.setPen(Qt.black)
        # painter.setFont(QFont("Arial", min(self.height(), self.width()) - 60))
        font = QFont("Helvetica")
        font.setPixelSize(self.fontsize)
        painter.setFont(font)

        font = QFont()
        self.drawHours(painter, self.hours)
        self.drawColons(painter)
        self.drawMinutes(painter, self.minutes)

    def setCurrentTime(self):
        now = QTime.currentTime()
        self.hours = now.hour()
        self.minutes = now.minute()

    @Slot()
    def handleTimeout(self):
        self.setCurrentTime()
        self.paint()
        self.update()


class Window(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        # self.setGeometry(100, 100, 1920, 1080)
        self.setGeometry(100, 100, 840, 480)

        layout = QHBoxLayout()

        digit = ClockWidget(parent=self, posx=20, posy=20)

        layout.addWidget(digit)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
