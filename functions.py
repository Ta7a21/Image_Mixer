from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import matplotlib.pyplot as plt
import cv2


def applyFourier(self, image, compWidget):
    # arr = np.asarray(image)
    fft = np.fft.fft2(image)
    print(fft)
    fftshift = np.fft.fftshift(fft)
    print(fftshift)
    magnitude = np.abs(fftshift)
    phase = np.angle(fft)
    real = np.real(fft)
    imaginary = np.imag(fft)
    magnitude1 = Image.fromarray((phase).astype(np.uint8))

    if magnitude1.mode != 'RGB':
        magnitude1 = magnitude1.convert('RGB')
    # arr = np.array(magnitude1.getdata())
    # print(arr)
    # phase1 = Image.fromarray(np.angle(fft))
    # real1 = Image.fromarray(np.real(fft))
    # imaginary1 = Image.fromarray(np.imag(fft))
    plt.imshow(phase)
    plt.show()
    qim = ImageQt(magnitude1)
    pix = QPixmap.fromImage(qim)
    pix = pix.scaled(230, 230, QtCore.Qt.IgnoreAspectRatio,
                     QtCore.Qt.FastTransformation)
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(self)
    scene.addItem(item)
    compWidget.setScene(scene)
    # print(compWidget)
    # print(len(fft))
    # print(type(magnitude1))
    # print(type(image))


def read_image(self, filename, imageWidget, compWidget):
    img = cv2.imread(filename)
    pix = QPixmap(filename)
    pix = pix.scaled(230, 230, QtCore.Qt.KeepAspectRatio,
                     QtCore.Qt.FastTransformation)
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(self)
    scene.addItem(item)
    imageWidget.setScene(scene)
    applyFourier(self, img, compWidget)
# def read_jpeg(filename):
#     print("alo2")


def openConnect(self, imageWidget, compWidget, openImage):
    openImage.triggered.connect(
        lambda: browsefiles(self, imageWidget, compWidget))


def browsefiles(self, imageWidget, compWidget):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", " *.png;;" "*.jpg;;"
    )
    file_path = fname[0]

    read_image(self, file_path, imageWidget, compWidget)


def sliderConnect(self, slider, label):
    slider.valueChanged.connect(
        lambda: sliderChange(self, slider, label))


def sliderChange(self, slider, label):
    label.setText(str(slider.value())+" %")


def comboboxChange(self, combobox, txt):
    items = {'Magnitude': ['Phase', 'Uniform Phase'], 'Phase': [
        'Magnitude', 'Uniform Magnitude'], 'Real': ['Imaginary'], 'Imaginary': ['Real'], 'Uniform Magnitude': ['Phase', 'Uniform Phase'], 'Uniform Phase': [
        'Magnitude', 'Uniform Magnitude']}
    combobox.clear()
    combobox.addItems(items[txt])
