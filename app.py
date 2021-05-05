from PyQt5 import QtWidgets, uic
import functions as tools
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("app.ui", self)

        components = [self.comp_1, self.comp_2]
        combo = [self.singleComp_1, self.singleComp_2]
        images = [self.image_1, self.image_2]
        openImages = [self.actionImage_1, self.actionImage_2]
        sliders = [self.slider_1, self.slider_2]
        sliderLabels = [self.sliderValue_1, self.sliderValue_2]
        imageComp = [self.mixerImage_1, self.mixerImage_2]
        mixers = [self.mixerComp_1, self.mixerComp_2]
        self.outputs = {"Output 1": self.output_1, "Output 2": self.output_2}
        for i in range(2):
            tools.openConnect(self, images[i], openImages[i], i)
            tools.fftCompConnect(self, combo[i], components[i], i)
            tools.sliderConnect(self, sliders[i], sliderLabels[i])
            tools.outComboConnect(self, mixers[i])
            tools.mixerImagesConnect(self, imageComp[i])
        self.setOutput.activated[str].connect(lambda: tools.output(self))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
