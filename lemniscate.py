# Lemnisate class
# Generating lemniscate (according to sliders)
# (QtChart, SaveToFile, Update (new Slider data))
# Default lemniscate

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QShortcut, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSpacerItem, \
    QSlider, QLineEdit
from PyQt5.QtChart import QChart, QScatterSeries, QChartView, QValueAxis
from PyQt5.QtGui import  QPainter, QDoubleValidator

import numpy as np

# TODO: 1. Set axis 2. Save to .waypoint  3. Connect with sliders 4. Add 'num' slider and button to save data
# TODO: 1. MainWindow Menu/Actions

# lemniscate params:  t1, t2, alpha, startPos[x,y]

class LemnisticateWidget(QWidget):
    def __init__(self, t = (0, 2*np.pi,50), movePos = (0.0, 0.0), alpha=1, parent=None):
        super(LemnisticateWidget,self).__init__(parent=parent)

        # get data (default or from user)

        self.tRange = t
        self.mPosition = movePos
        self.alpha = alpha

        # Sliders with labels

        self.sliders = [(QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel())]

        # QValidator

        self.doubleValid = QDoubleValidator()

        # QLineEdit

        self.pointLEdit = (QLineEdit(), QLineEdit())

        self.pointLEdit[0].setValidator(self.doubleValid)
        self.pointLEdit[0].setPlaceholderText('50.0619474')
        self.pointLEdit[0].setMaxLength(10)
        self.pointLEdit[1].setValidator(self.doubleValid)
        self.pointLEdit[1].setPlaceholderText('19.9368564')
        self.pointLEdit[1].setMaxLength(10)

        # QPushButton

        self.waypointsSubButton = QPushButton('Save to .waypoints')
        self.movePatternButton = QPushButton('Move pattern')
        self.movePatternButton.setFixedSize(200, 40)
        self.waypointsSubButton.setFixedSize(200,40)
        self.movePatternButton.clicked.connect(self.updateData)

        # QLabels

        self.titleLabels = [QLabel("T1"), QLabel("T2"), QLabel("POINTS NUMBER")]
        self.posLabels = (QLabel('xPos'), QLabel('yPos'))

        # QSpacer

        self.spacer = QSpacerItem(20,20)

        # QCharts & QChartView & QAxisValue

        self.lemChart = QChart()

        self.chartView = QChartView(self.lemChart)
        #self.chartView.setFixedSize()
        self.chartView.setRubberBand(QChartView.RectangleRubberBand)

        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.plotData = QScatterSeries()

        self.x_series = QValueAxis()

        self.x_series.setRange(-10, 10)
        self.x_series.setTickCount(35)
        self.x_series.setLabelFormat("%.2f")
        self.x_series.setTitleText("X")
        self.lemChart.setAxisX(self.x_series)

        self.y_series = QValueAxis()

        self.y_series.setRange(-10, 10)
        self.y_series.setTickCount(15)
        self.y_series.setLabelFormat("%.2f")
        self.y_series.setTitleText("Y")
        self.lemChart.setAxisY(self.y_series)

        # QShortcut

        self.zoomReset = QShortcut(Qt.Key_R, self)
        self.zoomReset.activated.connect(self.lemChart.zoomReset)

        # Layouts MAIN -> VERICAL |-| SUBMAIN -> HORIZONTAL

        self.mainLayout = QVBoxLayout()
        self.slidersLayouts = (QHBoxLayout(), QHBoxLayout(), QHBoxLayout())
        self.sPointLayout = QHBoxLayout()
        self.waypointsButtonLayout = QHBoxLayout()

        # Layout & Sliders config

        self.sPointLayout.addWidget(self.posLabels[0])
        self.sPointLayout.addWidget(self.pointLEdit[0])
        self.sPointLayout.addWidget(self.posLabels[1])
        self.sPointLayout.addWidget(self.pointLEdit[1])

        self.waypointsButtonLayout.addWidget(self.movePatternButton, Qt.AlignCenter)
        self.waypointsButtonLayout.addWidget(self.waypointsSubButton, Qt.AlignCenter)

        self.mainLayout.addWidget(self.chartView)

        self.sliders[0][0].valueChanged.connect(self.updateData)
        self.sliders[1][0].valueChanged.connect(self.updateData)
        self.sliders[2][0].valueChanged.connect(self.updateData)

        for idx, val in enumerate(self.sliders):
            val[0].setMinimum(0)
            val[0].setMaximum(100)
            val[1].setText(val[0].value().__str__())
            self.slidersLayouts[idx].addWidget(val[1])
            self.slidersLayouts[idx].addWidget(val[0])

        self.mainLayout.addWidget(self.titleLabels[0])
        self.mainLayout.addLayout(self.slidersLayouts[0])
        self.mainLayout.addWidget(self.titleLabels[1])
        self.mainLayout.addLayout(self.slidersLayouts[1])
        self.mainLayout.addWidget(self.titleLabels[2])
        self.mainLayout.addLayout(self.slidersLayouts[2])
        self.mainLayout.addLayout(self.sPointLayout)
        self.mainLayout.addItem(self.spacer)
        self.mainLayout.addLayout(self.waypointsButtonLayout)


        self.setLayout(self.mainLayout)

        self.generateLemnisticate(self.tRange, self.mPosition,self.alpha)

    def updateData(self):
        if self.sliders[0][0].value() > self.sliders[1][0].value():   # t1 > t2 -> t2 = t1 + 2
            self.sliders[1][0].setSliderPosition(self.sliders[1][0].value() + 2)

        # range -> t1 < t2

        t1 = np.round((self.sliders[0][0].value() * np.pi), 2)
        t2 = np.round((self.sliders[1][0].value() * np.pi), 2)

        self.sliders[0][1].setText(t1.__str__())     # T1
        self.sliders[1][1].setText(t2.__str__())     # T2

        self.sliders[2][1].setText(self.sliders[2][0].value().__str__())      # Points number

        self.generateLemnisticate(t=(t1, t2, self.sliders[2][0].value())
                                  ,movePos=(0, 0))


    def generateLemnisticate(self,t = (0, 2*np.pi,100), movePos = (0.0, 0.0), alpha=1):

        self.plotData.clear()

        t = np.linspace(t[0], t[1], num=t[2])

        for i in t:
            tx = alpha * np.sqrt(2) * np.cos(i) / (np.sin(i) ** 2 + 1)
            ty = alpha * np.sqrt(2) * np.cos(i) * np.sin(i) / (np.sin(i) ** 2 + 1)

            self.plotData.append(tx, ty)


        data = self.plotData.pointsVector()

        print("POINTS AMOUNT: ",len(data))

        minx = 0; miny = 0
        maxx = 0; maxy = 0

        print(data)
        for j in data:
            if j.x() < minx:
                minx = j.x()
            if j.y() < miny:
                miny = j.y()

            if j.x() > maxx:
                maxx = j.x()
            if j.y() > maxy:
                maxy = j.y()

        print(minx, maxx)
        print(miny, maxy)


        self.x_series.setRange(minx-2, maxx+2)
        self.y_series.setRange(miny-2, maxy+2)

        self.lemChart.addSeries(self.plotData)


    def saveToWaypoints(self, path):
        print("Save to .waypoints")


