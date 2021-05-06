from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image as ImagePil, ImageOps
from PIL.ImageQt import ImageQt
import numpy as np
import matplotlib.pyplot as plt
import logging
import logging.config
import json
from getSystemInfo import getSystemInfo

logging.basicConfig(
    filename="log.txt",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=20,
)
logging.info(f"System info: {json.loads(getSystemInfo())}")


class Image:
    def __init__(self, magnitude, phase, real, imaginary, imgSize, pixelSize):
        self.magnitude = magnitude
        self.phase = phase
        self.real = real
        self.imaginary = imaginary * 1j
        self.compnts = {}
        self.uniMagnitude = np.array((magnitude * 0) + 1) if type(real) != int else 0
        self.uniPhase = np.array(phase * 0) if type(real) != int else 0
        self.imgSize = imgSize
        self.pixelSize = pixelSize

    def dictInit(self):
        self.compnts = {
            "Magnitude": self.magnitude,
            "Phase": self.phase,
            "Real": self.real,
            "Imaginary": self.imaginary,
            "Uniform Magnitude": self.uniMagnitude,
            "Uniform Phase": self.uniPhase,
        }

    def fftComponent(self, window, comboBox, compntWidget, index):
        logging.info(f"The size of image{index+1} is {images[index].imgSize}.")
        if images[index].imgSize == 0:
            comboBox.setCurrentIndex(-1)
            errorMssg(window, "Select an image to view its component.")
            logging.warning("No image selected.")
            return

        txt = comboBox.currentText()
        compnt = grayImages[index].compnts[txt]
        if txt == "Imaginary":
            compnt = abs(compnt)
        # plt.imsave("ay 7aga.jpg", compnt * 10, cmap="gray")
        fftcompnt = ImagePil.fromarray((compnt).astype(np.uint8))
        # fftcompnt.save(txt + ".jpg")
        qtImage = ImageQt(fftcompnt)
        pixelMap = QPixmap.fromImage(qtImage)
        self.setImage(pixelMap, compntWidget)

    def mixer(self, ratio, compnts, index, widget):
        final_compnts = [0, 0]
        phaseInd = 0
        magInd = 1

        if compnts[0] == "Real" or compnts[0] == "Imaginary":
            for i in range(2):
                final_compnts[i] = images[index[i]].compnts[compnts[i]] * (
                    ratio[i]
                ) + images[1 - index[i]].compnts[compnts[i]] * (1 - (ratio[i]))

            ifft = np.fft.ifft2(final_compnts[0] + final_compnts[1])

        else:
            if compnts[0] == "Magnitude" or compnts[0] == "Uniform Magnitude":
                phaseInd = 1
                magInd = 0

            final_compnts[phaseInd] = 1j * (
                images[index[phaseInd]].compnts[compnts[phaseInd]] * (ratio[phaseInd])
                + images[1 - index[phaseInd]].compnts[compnts[phaseInd]]
                * (1 - ratio[phaseInd])
            )
            final_compnts[phaseInd] = np.exp(final_compnts[phaseInd])
            final_compnts[magInd] = images[index[magInd]].compnts[compnts[magInd]] * (
                ratio[magInd]
            ) + images[1 - index[magInd]].compnts[compnts[magInd]] * (1 - ratio[magInd])

            ifft = np.fft.ifft2(final_compnts[0] * final_compnts[1])

        ifft = np.real_if_close(ifft)

        img = ImagePil.fromarray((ifft).astype(np.uint8))
        qtImage = ImageQt(img)
        pixelMap = QPixmap.fromImage(qtImage)
        self.setImage(pixelMap, widget)

    def setImage(self, pixelMap, widget):
        pixelMap = pixelMap.scaled(
            230, 230, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation
        )
        item = QtWidgets.QGraphicsPixmapItem(pixelMap)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        widget.setScene(scene)


images = []
grayImages = []
for i in range(2):
    images.append(Image(0, 0, 0, 0, 0, 0))
    grayImages.append(0)


def read_image(self, filename, imageWidget, index):
    img = ImagePil.open(filename)
    logging.info(f"User choose image{index+1} from {filename}.")
    grayImg = ImageOps.grayscale(img)

    imgSize = img.size[1] * img.size[0]
    pixelSize = len(img.getdata()[0])
    logging.info(f"image{[index+1]} is of size ({img.size[0]},{img.size[1]}) and an alpha of length {pixelSize}.")
    for i in range(2):
        if (
            index == i
            and images[1 - i].imgSize
            and (
                imgSize != images[1 - i].imgSize or pixelSize != images[1 - i].pixelSize
            )
        ):
            errorMssg(self, "Select two images with the same size.")
            logging.critical("User selected images with different sizes or alpha values.")
            return

    fft = np.fft.fft2(img)
    images[index] = Image(
        np.abs(fft), np.angle(fft), np.real(fft), np.imag(fft), imgSize, pixelSize
    )
    images[index].dictInit()
    fftGray = np.fft.fftshift(np.fft.fft2(grayImg))
    fftGrayLog = 20*(np.log(fftGray))
    grayImages[index] = Image(
        np.abs(fftGrayLog),
        np.angle(fftGray),
        np.real(fftGrayLog),
        np.imag(fftGray),
        imgSize,
        0,
    )
    grayImages[index].dictInit()
    pixelMap = QPixmap(filename)
    images[index].setImage(pixelMap, imageWidget)


def browsefiles(self, imageWidget, index):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", "*.jpg;;" " *.png;;" "*.jpeg;;"
    )
    file_path = fname[0]
    extensionsToCheck = (".jpg", ".png", ".jpeg")
    if fname[0].endswith(extensionsToCheck):
        read_image(self, file_path, imageWidget, index)
    elif fname[0] != "":
        errorMssg(self, "Invalid format.")
        logging.warning(f"The user did not select a valid file format. {fname[0]}")
        return
    else:
        return


def openConnect(self, imageWidget, openImage, index):
    openImage.clicked.connect(lambda: browsefiles(self, imageWidget, index))


def mixerImagesConnect(self, imageCompnt):
    imageCompnt.activated[str].connect(lambda: output(self))


def fftCompConnect(self, comboBox, compntWidget, index):
    comboBox.activated[str].connect(
        lambda: images[index].fftComponent(self, comboBox, compntWidget, index)
    )


def outComboConnect(self, comboBox):
    comboBox.activated[str].connect(lambda: comboBoxChange(self, comboBox))


def sliderConnect(self, slider, label):
    slider.valueChanged.connect(lambda: sliderChange(self, slider, label))


def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")
    output(self)


def comboBoxChange(self, comboBox):
    if comboBox == self.mixerComp_1:
        txt = comboBox.currentText()
        comboBox2 = self.mixerComp_2
        items = {
            "Magnitude": ["Phase", "Uniform Phase"],
            "Phase": ["Magnitude", "Uniform Magnitude"],
            "Real": ["Imaginary"],
            "Imaginary": ["Real"],
            "Uniform Magnitude": ["Phase", "Uniform Phase"],
            "Uniform Phase": ["Magnitude", "Uniform Magnitude"],
        }
        comboBox2.clear()
        comboBox2.addItems(items[txt])

    output(self)


def output(self):
    outputTxt = self.setOutput.currentText()
    if outputTxt == "":
        errorMssg(self, "Select an output slot.")
        logging.critical("No output slot selected")
        return
    outputWidget = self.outputs[outputTxt]

    final_img = Image(0, 0, 0, 0, 0, 0)

    mixerImages = [
        int(self.mixerImage_1.currentText()[-1]) - 1,
        int(self.mixerImage_2.currentText()[-1]) - 1,
    ]
    mixerCompnts = [self.mixerComp_1.currentText(), self.mixerComp_2.currentText()]
    sliders = [self.slider_1.value() / 100.0, self.slider_2.value() / 100.0]
    for img in images:
        if not img.imgSize:
            self.setOutput.setCurrentIndex(-1)
            errorMssg(self, "Select two images to mix between them.")
            logging.error("The user tried to mix only one image")
            return
    for i in range(2):
        img = images[mixerImages[i]].compnts[mixerCompnts[i]]
        final_img.compnts[mixerCompnts[i]] = img
    final_img.mixer(sliders, mixerCompnts, mixerImages, outputWidget)


def reset(self, imgs, compnts, comboBoxes, outputs):
    objects = [imgs, compnts]
    for i in range(2):
        images[i].imgSize = 0
        for j in range(2):
            if type(objects[j][i].scene()) == QtWidgets.QGraphicsScene:
                for item in objects[j][i].scene().items():
                    objects[j][i].scene().removeItem(item)
        if type(outputs["Output " + str(i + 1)].scene()) == QtWidgets.QGraphicsScene:
            for item in outputs["Output " + str(i + 1)].scene().items():
                outputs["Output " + str(i + 1)].scene().removeItem(item)
        comboBoxes[i].setCurrentIndex(-1)
    self.setOutput.setCurrentIndex(-1)


def errorMssg(self, txt):
    QMessageBox.critical(self, "Error", txt)
