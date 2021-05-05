from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt
import numpy as np
import matplotlib.pyplot as plt
import logging

# log = logging.getLogger("__name__")

class image:
    def __init__(self, magnitude, phase, real, imaginary, imgSize):
        self.magnitude = magnitude
        self.phase = phase
        self.real = real
        self.imaginary = imaginary * 1j

        if type(real) != int:
            self.uniMagnitude = np.array((magnitude * 0) + 1)
            self.uniPhase = np.array(phase * 0)
        else:
            self.uniMagnitude = 0
            self.uniPhase = 0
        self.comp = {
            "Magnitude": self.magnitude,
            "Phase": self.phase,
            "Real": self.real,
            "Imaginary": self.imaginary,
            "Uniform Magnitude": self.uniMagnitude,
            "Uniform Phase": self.uniPhase,
        }
        self.imgSize = imgSize
        # self.pixelSize = pixelSize

    def fftComponent(self, combo, compWidget, index):
        resetCombo(combo)
        txt = combo.currentText()
        comp = images[index].comp[txt]
        fftcomp = Image.fromarray(np.abs(np.fft.ifft2(comp)).astype(np.uint8))
        fftcomp.save(txt + ".jpg")
        qim = ImageQt(fftcomp)
        pix = QPixmap.fromImage(qim)
        self.setImage(pix, compWidget)

    def setImage(self, pix, Widget):
        pix = pix.scaled(
            230, 230, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation
        )
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        Widget.setScene(scene)

    def mixer(self, ratio, comp, index, widget):
        final_comp = [0, 0]
        phaseInd = 0
        magInd = 1
        if comp[0] == "Real" or comp[0] == "Imaginary":
            for i in range(2):
                final_comp[i] = images[index[i]].comp[comp[i]] * (ratio[i]) + images[
                    1 - index[i]
                ].comp[comp[i]] * (1 - (ratio[i]))
            ifft = np.fft.ifft2(final_comp[0] + final_comp[1])

        else:
            if comp[0] == "Magnitude" or comp[0] == "Uniform Magnitude":
                phaseInd = 1
                magInd = 0

            final_comp[phaseInd] = 1j * (
                images[index[phaseInd]].comp[comp[phaseInd]] * (ratio[phaseInd])
                + images[1 - index[phaseInd]].comp[comp[phaseInd]]
                * (1 - ratio[phaseInd])
            )
            final_comp[phaseInd] = np.exp(final_comp[phaseInd])

            final_comp[magInd] = images[index[magInd]].comp[comp[magInd]] * (
                ratio[magInd]
            ) + images[1 - index[magInd]].comp[comp[magInd]] * (1 - ratio[magInd])

            ifft = np.fft.ifft2(final_comp[0] * final_comp[1])

        ifft = np.real_if_close(ifft)
        img = Image.fromarray((ifft).astype(np.uint8))
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        self.setImage(pix, widget)


images = [0, 0]


# def showDialog():
#     msgBox = QMessageBox()
#     msgBox.setIcon(QMessageBox.Critical)
#     msgBox.setText("Select two images with the same size")
#     msgBox.setWindowTitle("Error")
#     msgBox.setStandardButtons(QMessageBox.Ok)
#     return msgBox


#    msgBox.exec()
# #    if returnValue == QMessageBox.Ok:
# #       print('OK clicked')


def read_image(self, filename, imageWidget, index):
    img = Image.open(filename).convert('LA')
    grayImg = ImageOps.grayscale(img)

    imgSize = grayImg.size[1] * grayImg.size[0]
    # pixelSize = len(grayImg.getdata()[0])

    if index == 0 and type(images[1]) != int:
        if imgSize != images[1].imgSize :
            # showDialog()
            QMessageBox.critical(self, "Error", "Select two images with the same size")
            return
    elif index == 1 and type(images[0]) != int:
        if imgSize != images[0].imgSize :
            # showDialog()
            QMessageBox.critical(self, "Error", "Select two images with the same size")
            return

    fft = np.fft.fft2(grayImg)
    fft = 
    images[index] = image(
        np.abs(fft), np.angle(fft), np.real(fft), np.imag(fft), imgSize
    )

    pix = QPixmap(filename)
    images[index].setImage(pix, imageWidget)


def browsefiles(self, imageWidget, index):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", "*.jpg;;" " *.png;;" "*.jpeg;;"
    )
    file_path = fname[0]
    read_image(self, file_path, imageWidget, index)


def openConnect(self, imageWidget, openImage, index):
    openImage.clicked.connect(lambda: browsefiles(self, imageWidget, index))


def imageCompConnect(self, imageComp):
    imageComp.activated[str].connect(lambda: output(self))


def comboConnect(self, combo, compWidget, index):
    combo.activated[str].connect(
        lambda: images[index].fftComponent(combo, compWidget, index)
    )


def outComboConnect(self, combo):
    combo.activated[str].connect(lambda: comboboxChange(self, combo))


def sliderConnect(self, slider, label):
    slider.valueChanged.connect(lambda: sliderChange(self, slider, label))


def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")
    output(self)


def comboboxChange(self, combobox):
    if combobox == self.mixerComp_1:
        txt = combobox.currentText()
        combobox2 = self.mixerComp_2
        items = {
            "Magnitude": ["Phase", "Uniform Phase"],
            "Phase": ["Magnitude", "Uniform Magnitude"],
            "Real": ["Imaginary"],
            "Imaginary": ["Real"],
            "Uniform Magnitude": ["Phase", "Uniform Phase"],
            "Uniform Phase": ["Magnitude", "Uniform Magnitude"],
        }
        combobox2.clear()
        combobox2.addItems(items[txt])

    output(self)


def resetCombo(combobox):
    index = combobox.findText("Choose Component")
    combobox.removeItem(index)
    index = combobox.findText("Choose Output")
    combobox.removeItem(index)

def output(self):
    outputTxt = self.setOutput.currentText()
    outputWidget = self.outputs[outputTxt]

    final_img = image(0, 0, 0, 0, 0)

    mixerImage = [
        int(self.mixerImage_1.currentText()[-1]) - 1,
        int(self.mixerImage_2.currentText()[-1]) - 1,
    ]
    mixerComp = [self.mixerComp_1.currentText(), self.mixerComp_2.currentText()]
    sliders = [self.slider_1.value() / 100.0, self.slider_2.value() / 100.0]
    if 0 in images:
        QMessageBox.critical(self, "Error", "Select two images to mix between them")
        return
    resetCombo(self.setOutput)
    for i in range(2):
        img = images[mixerImage[i]].comp[mixerComp[i]]
        final_img.comp[mixerComp[i]] = img
    final_img.mixer(sliders, mixerComp, mixerImage, outputWidget)
