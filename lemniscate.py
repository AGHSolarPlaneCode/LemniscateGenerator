# Lemnisate class
# Generating lemniscate (according to sliders)
# (QtChart, SaveToFile, Update (new Slider data))
# Default lemniscate

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QLineEdit
from PyQt5.QtChart import QChart, QScatterSeries, QChartView, QValueAxis
from PyQt5.QtGui import  QPainter

import numpy as np


# lemniscate params:  t1, t2, alpha, startPos[x,y]

class LemnisticateWidget(QWidget):
    def __init__(self, t = (0, 2*np.pi,60), movePos = (0.0, 0.0), alpha=1, parent=None):
        super(LemnisticateWidget,self).__init__(parent=parent)

        # get data (default or from user)

        self.tRange = t
        self.mPosition = movePos
        self.alpha = alpha

        # Sliders with labels

        self.sliders = [(QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel())]
        # QLineEdit

        self.pointLEdit = (QLineEdit(), QLineEdit())

        self.pointLEdit[0].setPlaceholderText('50.0619474')
        self.pointLEdit[0].setMaxLength(10)
        self.pointLEdit[1].setPlaceholderText('19.9368564')
        self.pointLEdit[1].setMaxLength(10)

        # QLabels

        self.titleLabels = [QLabel("T1"), QLabel("T2"), QLabel("ALPHA")]
        self.posLabels = (QLabel('xPos'), QLabel('yPos'))

        # QCharts & QChartView

        self.lemChart = QChart()
        self.chartView = QChartView(self.lemChart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        # Layouts MAIN -> VERICAL |-| SUBMAIN -> HORIZONTAL

        self.mainLayout = QVBoxLayout()
        self.slidersLayouts = (QHBoxLayout(), QHBoxLayout(), QHBoxLayout())
        self.sPointLayout = QHBoxLayout()

        # Layout & Sliders config

        self.sPointLayout.addWidget(self.posLabels[0])
        self.sPointLayout.addWidget(self.pointLEdit[0])
        self.sPointLayout.addWidget(self.posLabels[1])
        self.sPointLayout.addWidget(self.pointLEdit[1])

        self.mainLayout.addWidget(self.chartView)

        self.sliders[0][0].valueChanged.connect(self.updateSliders)
        self.sliders[1][0].valueChanged.connect(self.updateSliders)
        self.sliders[2][0].valueChanged.connect(self.updateSliders)

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

        self.setLayout(self.mainLayout)

        self.generateLemnisticate(self.tRange, self.mPosition,self.alpha)

    def updateSliders(self):
        if self.sliders[0][0].value() > self.sliders[1][0].value():   # t1 > t2 -> t2 = t1 + 2
            self.sliders[1][0].setSliderPosition(self.sliders[1][0].value() + 2)

        self.sliders[0][1].setText(self.sliders[0][0].value().__str__())
        self.sliders[1][1].setText(self.sliders[1][0].value().__str__())
        self.sliders[2][1].setText(self.sliders[2][0].value().__str__())

        # self.generateLemnisticate(<...sliders_data...>)


    def generateLemnisticate(self,t = (0, 2*np.pi,100), movePos = (0.0, 0.0), alpha=1):
        t = np.linspace(t[0], t[1], num=t[2])

        self.plotData = QScatterSeries()

        x = []
        y = []

        for i in t:
            self.plotData.append(movePos[0] + (movePos[0] - alpha * np.sqrt(2) * np.cos(i) / (np.sin(i) ** 2 + 1))
            ,movePos[1] + (movePos[1] - alpha * np.sqrt(2) * np.cos(i) * np.sin(i) / (np.sin(i) ** 2 + 1)))


        # print(self.plotData.pointsVector())
        self.lemChart.addSeries(self.plotData)


    def saveToWaypoints(self, path):
        print("Save to .waypoints")


