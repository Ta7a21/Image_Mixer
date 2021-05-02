from PyQt5 import QtWidgets, uic
import functions as tools
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('app.ui', self)

        components = [self.comp_1, self.comp_2]
        images = [self.image_1, self.image_2]
        openImages = [self.actionImage_1, self.actionImage_2]
        sliders = [self.slider_1, self.slider_2]
        sliderLabels = [self.sliderValue_1, self.sliderValue_2]
        self.actionExit.triggered.connect(self.close)
        for i in range(2):
            tools.openConnect(self, images[i], components[i], openImages[i])
            tools.sliderConnect(self, sliders[i], sliderLabels[i])
        self.mixerComp_1.activated[str].connect(lambda: tools.comboboxChange(
            self, self.mixerComp_2, self.mixerComp_1.currentText()))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
