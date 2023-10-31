from PySide2.QtWidgets import (
    QApplication,
)
from pathlib import Path

import sys

sys.path.append(Path(__file__).parents[1].joinpath("lib").as_posix())

from clock2py.window import Window


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
