import sys
import typing
from PySide2.QtCore import Qt, QTimer, QTime, QRect, Slot
from PySide2.QtGui import QFont, QPainter, QPalette, QColor, QPen, QPaintEvent
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout


class FlipDigit(QWidget):
    def __init__(self, parent=None, posx=0, posy=0):
        super(FlipDigit, self).__init__(parent)
        self.digit = 0
        self.position = (posx, posy)
        self.hours = 0
        self.minutes = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start(1000)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paint()

    def setTime(self):
        time = QTime()

    def drawColons(self, painter):
        painter.drawText(340, self.height() - 60, ":")

    def drawHours(self, painter: QPainter, hours: int):
        digit1 = hours % 10
        digit2 = hours // 10
        painter.drawText(0, self.height() - 60, str(digit2))
        painter.drawText(180, self.height() - 60, str(digit1))

    def drawMinutes(self, painter: QPainter, minutes: int):
        digit1 = minutes % 10
        digit2 = minutes // 10
        painter.drawText(430, self.height() - 60, str(digit2))
        painter.drawText(610, self.height() - 60, str(digit1))

    def paint(self):
        pen = QPen()
        pen.setColor(Qt.green)
        painter = QPainter(self)

        painter.setPen(Qt.black)
        # painter.setFont(QFont("Arial", min(self.height(), self.width()) - 60))
        font = QFont("Helvetica")
        font.setPixelSize(350)
        painter.setFont(font)

        font = QFont()
        self.drawHours(painter, self.hours)
        self.drawColons(painter)
        self.drawMinutes(painter, self.minutes)

    @Slot()
    def handleTimeout(self):
        now = QTime.currentTime()
        self.hours = now.hour()
        self.minutes = now.minute()
        self.paint()
        self.update()


class Window(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Smartclock")
        self.setGeometry(100, 100, 840, 480)
        layout = QHBoxLayout()

        digit = FlipDigit(parent=self, posx=20, posy=20)

        layout.addWidget(digit)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # clock = FlipClock()
    window = Window()

    sys.exit(app.exec_())
