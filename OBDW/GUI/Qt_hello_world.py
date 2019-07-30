from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    width = mainWindow.width()
    height = mainWindow.height()
    mainWindow.resize(width/.6, height/.7)
    mainWindow.show()
    app.exec_()
    output = mainWindow.grabUserInfo()
    return(output)

