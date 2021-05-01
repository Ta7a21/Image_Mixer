from PyQt5.QtWidgets import QFileDialog


def read_png(filename):
    print("alo")


def read_jpeg(filename):
    print("alo2")


def browsefiles(self):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", " *.png;;" "*.jpeg;;"
    )
    file_path = fname[0]
    if file_path.endswith(".png"):
        read_png(file_path)
    elif file_path.endswith(".jpeg"):
        read_jpeg(file_path)


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
