import requests
from PyQt5.QtGui import QMouseEvent, QPainter, QBrush, QColor, QPaintEvent, QPen, QKeyEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QPoint
import sys
from finder import findObject, getMapByCoords


mapCoordX = 1
mapCoordY = 1
zoom = 1


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 150, 1280, 720)
        self.setWindowTitle("Супрематизм")

        mapImg = QPixmap()
        mapImg.loadFromData(getMapByCoords(37.620070, 55.753630))

        self.mapLabel = QLabel(self)
        self.mapLabel.setPixmap(mapImg)
        self.mapLabel.move(10, 10)
        self.mapLabel.resize(mapImg.width(), mapImg.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
