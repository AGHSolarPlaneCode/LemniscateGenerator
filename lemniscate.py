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
    def __init__(self, configData = (0, 2*np.pi, 1), movePos = (0.0, 0.0), parent=None):
        super(LemnisticateWidget,self).__init__(parent=parent)

        # get data (default or from user)
        self.lemData = configData
        self.movingPos = movePos

        # Sliders with labels

        self.sliders = [(QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel()),
                        (QSlider(Qt.Horizontal), QLabel())]
        # QLabels

        self.titleLabels = [QLabel("T1"), QLabel("T2"), QLabel("ALPHA")]

        # QCharts & QChartView

        self.lemChart = QChart()
        self.chartView = QChartView(self.lemChart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        # Layouts MAIN -> VERICAL |-| SUBMAIN -> HORIZONTAL

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.chartView)

        self.slidersLayouts = (QHBoxLayout(), QHBoxLayout(), QHBoxLayout())

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

        self.setLayout(self.mainLayout)

    def updateSliders(self):
        if self.sliders[0][0].value() > self.sliders[1][0].value():   # t1 > t2 -> t2 = t1 + 2
            self.sliders[1][0].setSliderPosition(self.sliders[1][0].value() + 2)

        self.sliders[0][1].setText(self.sliders[0][0].value().__str__())
        self.sliders[1][1].setText(self.sliders[1][0].value().__str__())
        self.sliders[2][1].setText(self.sliders[2][0].value().__str__())


    def labelUpdate(self):
        self.t1SliderLbl.setText(self.t1ParamSlider.value().__str__())
        self.t2SliderLbl.setText(self.t2ParamSlider.value().__str__())
        self.alphaSliderLbl.setText(self.alphaParamSlider.value().__str__())

    def updateLemData(self, data):
        print("Update data")


    def generateLemnisticate(self):
        # generation pattern
        print("Generate")



    def saveToWaypoints(self, path):
        print("Save to .waypoints")


