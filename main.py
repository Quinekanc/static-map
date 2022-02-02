import requests
from PyQt5.QtGui import QMouseEvent, QPainter, QBrush, QColor, QPaintEvent, QPen, QKeyEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
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
        self.setWindowTitle("\"Клиент\" Тындекс Карт")

        self.scale = 0.01
        self.mapLongtitude = 37.620070
        self.mapLattitude = 55.753630
        self.mapType = 'map'

        self.mapLabel = QLabel(self)
        self.mapLabel.move(10, 10)

        self.mapToggle = QPushButton(self)
        self.mapToggle.move(680, 10)
        self.mapToggle.setText('Схема')
        self.mapToggle.setChecked(True)

        self.satToggle = QPushButton(self)
        self.satToggle.move(680, 40)
        self.satToggle.setText('Спутник')

        self.gibToggle = QPushButton(self)
        self.gibToggle.move(680, 70)
        self.gibToggle.setText('Гибрид')

        self.mapToggle.clicked.connect(self.changeMapToMap)
        self.satToggle.clicked.connect(self.changeMapToSat)
        self.gibToggle.clicked.connect(self.changeMapToGib)

        self.updateMap()

    def changeMapToGib(self):
        self.mapType = 'sat,skl'
        self.updateMap()

    def changeMapToSat(self):
        self.mapType = 'sat'
        self.updateMap()

    def changeMapToMap(self):
        self.mapType = 'map'
        self.updateMap()

    def updateMap(self):
        mapImg = QPixmap()
        mapImg.loadFromData(getMapByCoords(self.mapLongtitude,
                                           self.mapLattitude, 650, 450, self.mapType, self.scale))
        self.mapLabel.setPixmap(mapImg)
        self.mapLabel.resize(mapImg.width(), mapImg.height())

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_PageUp:
            if self.scale > 0.01:
                self.scale -= 0.01
                self.updateMap()

        if a0.key() == Qt.Key_PageDown:
            if self.scale < 10:
                self.scale += 0.01
                self.updateMap()

        if a0.key() == Qt.Key_Up:
            self.mapLattitude += 0.001
            self.updateMap()

        if a0.key() == Qt.Key_Down:
            self.mapLattitude -= 0.001
            self.updateMap()

        if a0.key() == Qt.Key_Left:
            self.mapLongtitude -= 0.001
            self.updateMap()

        if a0.key() == Qt.Key_Right:
            self.mapLongtitude += 0.001
            self.updateMap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
