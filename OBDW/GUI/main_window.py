from PyQt5.QtWidgets import QMainWindow, QShortcut, QColorDialog
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush, QIcon
from PyQt5.QtCore import Qt, QThread
from GUI.mainWidget import MainWidget
from GUI.scrollBar import ScrollBar
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Boring GUI")
        # Palet stuff
        self.palette = QPalette()
        # no opaque paint
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        self.mainWidget = MainWidget()
        # Set to pinik gradient
        self.changeBackground("#C970A4")
        # self.mainWidget.combobox.currentTextChanged.connect(
        #    self.changeBackground)
        self.mainWidget.colorButton.clicked.connect(self.handelButtonColor)

        # Make shortcut so you dont have to hit x button
        QShortcut("Ctrl+q", self, activated=self.close)
        self.setCentralWidget(self.mainWidget)

        #self.thread = QThread()
        # self.thread.started.connect()
        # self.thread.start()

    def handelButtonColor(self):
        colorDialog = QColorDialog.getColor()
        if colorDialog.isValid():
            self.changeBackground(colorDialog.name())

    def changeBackground(self, colorName):
        # old way with combobox
        '''colorSelection = {"Pink": QColor(201, 112, 164), "Blue": QColor(81, 116, 161), "Green": QColor(
            111, 128, 81), "Gray": QColor(102, 109, 117), "Purple": QColor(132, 95, 150), "Red": QColor(163, 69, 69)} 
        selectColor = colorSelection[colorName]'''

        self.mainWidget.scrollArea.setHorizontalScrollBar(
            ScrollBar(colorName))
        self.mainWidget.scrollArea.setVerticalScrollBar(
            ScrollBar(colorName))
        gradient = QLinearGradient(0, 0, 0, 350)
        gradient.setColorAt(0.0, QColor(240, 240, 240))
        gradient.setColorAt(1.0, QColor(colorName))
        self.palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(self.palette)
