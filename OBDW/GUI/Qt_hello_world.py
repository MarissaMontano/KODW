#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    width = mainWindow.width()
    height = mainWindow.height()
    mainWindow.resize(width/.7, height/.5)
    mainWindow.show()
    app.exec_()

