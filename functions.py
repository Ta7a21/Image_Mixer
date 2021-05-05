from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt
import numpy as np
import matplotlib.pyplot as plt
import logging

# log = logging.getLogger("__name__")

images = [0, 0]
grayImages = [0, 0]


class image:
    def __init__(self, magnitude, phase, real, imaginary, imgSize, pixelSize):
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
        self.compnts = {
            "Magnitude": self.magnitude,
            "Phase": self.phase,
            "Real": self.real,
            "Imaginary": self.imaginary,
            "Uniform Magnitude": self.uniMagnitude,
            "Uniform Phase": self.uniPhase,
        }
        self.imgSize = imgSize
        self.pixelSize = pixelSize

    def fftComponent(self, combo, compWidget, index):
        resetCombo(combo)
        txt = combo.currentText()
        comp = grayImages[index].compnts[txt]
        if txt == 'Imaginary':
            comp = abs(comp)
        plt.imsave("ay 7aga.jpg", comp*10, cmap='gray')
        fftcomp = Image.fromarray((comp*10).astype(np.uint8))
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

    def mixer(self, ratio, compnts, index, widget):
        final_compnts = [0, 0]
        phaseInd = 0
        magInd = 1
        if compnts[0] == "Real" or compnts[0] == "Imaginary":
            for i in range(2):
                final_compnts[i] = images[index[i]].compnts[compnts[i]] * (ratio[i]) + images[
                    1 - index[i]
                ].compnts[compnts[i]] * (1 - (ratio[i]))
            ifft = np.fft.ifft2(final_compnts[0] + final_compnts[1])

        else:
            if compnts[0] == "Magnitude" or compnts[0] == "Uniform Magnitude":
                phaseInd = 1
                magInd = 0

            final_compnts[phaseInd] = 1j * (
                images[index[phaseInd]].compnts[compnts[phaseInd]] *
                (ratio[phaseInd])
                + images[1 - index[phaseInd]].compnts[compnts[phaseInd]]
                * (1 - ratio[phaseInd])
            )
            final_compnts[phaseInd] = np.exp(final_compnts[phaseInd])

            final_compnts[magInd] = images[index[magInd]].compnts[compnts[magInd]] * (
                ratio[magInd]
            ) + images[1 - index[magInd]].compnts[compnts[magInd]] * (1 - ratio[magInd])

            ifft = np.fft.ifft2(final_compnts[0] * final_compnts[1])

        ifft = np.real_if_close(ifft)
        img = Image.fromarray((ifft).astype(np.uint8))
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        self.setImage(pix, widget)


def read_image(self, filename, imageWidget, index):
    img = Image.open(filename)
    grayImg = ImageOps.grayscale(img)

    imgSize = img.size[1] * img.size[0]
    pixelSize = len(img.getdata()[0])

    for i in range(2):
        if index == i and type(images[1 - i]) != int:
            if imgSize != images[1 - i].imgSize or pixelSize != images[1 - i].pixelSize:
                QMessageBox.critical(
                    self, "Error", "Select two images with the same size")
                return

    fft = np.fft.fft2(img)
    images[index] = image(
        np.abs(fft), np.angle(fft), np.real(
            fft), np.imag(fft), imgSize, pixelSize
    )

    fftGray = np.fft.fftshift(np.fft.fft2(grayImg))
    fftGrayLog = np.log(1 + fftGray)
    grayImages[index] = image(
        np.abs(fftGrayLog), np.angle(fftGray), np.real(
            fftGrayLog), np.imag(fftGray), imgSize, 0
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


def mixerImagesConnect(self, imageComp):
    imageComp.activated[str].connect(lambda: output(self))


def fftCompConnect(self, combo, compWidget, index):
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

    final_img = image(0, 0, 0, 0, 0, 0)

    mixerImage = [
        int(self.mixerImage_1.currentText()[-1]) - 1,
        int(self.mixerImage_2.currentText()[-1]) - 1,
    ]
    mixerComp = [self.mixerComp_1.currentText(
    ), self.mixerComp_2.currentText()]
    sliders = [self.slider_1.value() / 100.0, self.slider_2.value() / 100.0]
    if 0 in images:
        QMessageBox.critical(
            self, "Error", "Select two images to mix between them")
        return
    resetCombo(self.setOutput)
    for i in range(2):
        img = images[mixerImage[i]].compnts[mixerComp[i]]
        final_img.compnts[mixerComp[i]] = img
    final_img.mixer(sliders, mixerComp, mixerImage, outputWidget)
