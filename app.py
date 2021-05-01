from PyQt5 import QtWidgets, uic
import functions as tools
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('app.ui', self)

        images = [self.actionImage_1, self.actionImage_2]
        sliders = [self.slider_1, self.slider_2]
        sliderLabels = [self.sliderValue_1, self.sliderValue_2]
        self.actionExit.triggered.connect(self.close)
        for i in range(2):
            images[i].triggered.connect(lambda: tools.browsefiles(self))
            tools.sliderConnect(self, sliders[i], sliderLabels[i])
        self.mixerComp_1.activated[str].connect(lambda: tools.comboboxChange(
            self, self.mixerComp_2, self.mixerComp_1.currentText()))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
