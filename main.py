import requests
from PyQt5.QtGui import QMouseEvent, QPainter, QBrush, QColor, QPaintEvent, QPen, QKeyEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QPoint
import sys
from helper import getMapByCoords, find_obj


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
        self.point = [self.mapLongtitude, self.mapLattitude]

        self.searchObj = QLineEdit(self)
        self.searchObj.resize(150, 25)
        self.searchObj.move(680, 10)

        self.searchObjEnter = QPushButton(self)
        self.searchObjEnter.move(835, 10)
        self.searchObjEnter.resize(25, 25)
        self.searchObjEnter.setText('->')

        self.mapLabel = QLabel(self)
        self.mapLabel.move(10, 10)

        self.mapToggle = QPushButton(self)
        self.mapToggle.move(680, 50)
        self.mapToggle.setText('Схема')
        self.mapToggle.setChecked(True)

        self.satToggle = QPushButton(self)
        self.satToggle.move(680, 80)
        self.satToggle.setText('Спутник')

        self.gibToggle = QPushButton(self)
        self.gibToggle.move(680, 110)
        self.gibToggle.setText('Гибрид')

        self.mapToggle.clicked.connect(self.changeMapToMap)
        self.satToggle.clicked.connect(self.changeMapToSat)
        self.gibToggle.clicked.connect(self.changeMapToGib)
        self.searchObjEnter.clicked.connect(self.searchingObj)

        self.updateMap()

    def searchingObj(self):
        try:
            search = self.searchObj.text()
            response = find_obj(search)

            json_response = response.json()
            toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            toponym_cords = toponym['Point']['pos'].split()

            self.mapLongtitude, self.mapLattitude = toponym_cords
            self.point = toponym_cords
            self.updateMap()

        except Exception:
            pass

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
        mapImg.loadFromData(getMapByCoords(self.mapLongtitude, self.mapLattitude, 650, 450, self.point, self.mapType,
                                           self.scale))
        self.mapLabel.setPixmap(mapImg)
        self.mapLabel.resize(mapImg.width(), mapImg.height())

    def keyPressEvent(self, a0: QKeyEvent):
        try:
            if a0.key() == Qt.Key_PageUp:
                if self.scale > 0.01:
                    self.scale -= 0.01
                    self.updateMap()

            if a0.key() == Qt.Key_PageDown:
                if self.scale < 10:
                    self.scale += 0.01
                    self.updateMap()

            if a0.key() == Qt.Key_Up:
                if -180 <= self.mapLattitude <= 180:
                    self.mapLattitude += 0.001
                    self.updateMap()

            if a0.key() == Qt.Key_Down:
                if -180 <= self.mapLattitude <= 180:
                    self.mapLattitude -= 0.001
                    self.updateMap()

            if a0.key() == Qt.Key_Left:
                if -180 <= self.mapLongtitude <= 180:
                    self.mapLongtitude -= 0.001
                    self.updateMap()

            if a0.key() == Qt.Key_Right:
                if -180 <= self.mapLongtitude <= 180:
                    self.mapLongtitude += 0.001
                    self.updateMap()

        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
