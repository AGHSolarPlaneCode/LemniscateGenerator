# Main appliction window (Sliders)
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
import lemniscate as lem

class LemniscatePlotterApp(QMainWindow):
    def __init__(self, lemWidget, parent=None):
        super(LemniscatePlotterApp, self).__init__(parent=parent)
        self.setFixedSize(1200, 700)
        self.setWindowTitle('Lemnisticate Generator')
        self.setCentralWidget(lemWidget)


if __name__ == '__main__':
    print("LemniscatePLotterAapp")

    qApp = QApplication(sys.argv)

    widget = lem.LemnisticateWidget()

    lemApp = LemniscatePlotterApp(lemWidget=widget)

    lemApp.show()

    sys.exit(qApp.exec_())