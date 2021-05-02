from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np


def applyFourier(self, image, compWidget):
    arr=np.asarray(image)
    print(arr)
    arr2 = np.array(image.getdata())
    print(arr2)
    fft = np.fft.fft2(image)
    magnitude = np.abs(fft)
    phase = np.angle(fft)
    real = np.real(fft)
    imaginary = np.imag(fft)
   # magnitude1 = np.fft.ifft2(magnitude)
    #print(magnitude1)
    
    magnitude = np.interp(magnitude, (magnitude.min(),magnitude.max()),(0,255))
    magnitude1 = Image.fromarray(magnitude)
    
    
    # if magnitude1.mode != 'RGB':
    #     magnitude1 = magnitude1.convert('RGB')
        
    
    # phase1 = Image.fromarray(np.angle(fft))
    # real1 = Image.fromarray(np.real(fft))
    # imaginary1 = Image.fromarray(np.imag(fft))
    qim = ImageQt(magnitude1)
    pix = QPixmap.fromImage(qim)
    pix = pix.scaled(230, 230, QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.FastTransformation)
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(self)
    scene.addItem(item)
    compWidget.setScene(scene)
    print(compWidget)
    print(len(fft))
    print(type(magnitude1))
    print(type(image))


def read_image(self, filename, imageWidget, compWidget):
    img = Image.open(filename)
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
        self, "Open file", "../", " *.png;;" "*.jpeg;;"
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
