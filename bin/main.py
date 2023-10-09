from PySide2.QtWidgets import QWidget, QApplication, QHBoxLayout, QStackedWidget
from pathlib import Path

import sys
sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.calendar_widget import CalendarWidget
from clock2py.clock_widget import ClockWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(840, 480)
        layout = QHBoxLayout(self)
        calendar = CalendarWidget()
        clock = ClockWidget()

        stacked_widget = QStackedWidget(self)
        stacked_widget.addWidget(clock)
        stacked_widget.addWidget(calendar)

        layout.addWidget(stacked_widget)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
