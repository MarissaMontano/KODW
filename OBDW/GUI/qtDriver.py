from PyQt5.QtWidgets import QApplication
from GUI.mainWindow import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exec_()
    output = mainWindow.grabUserInfo()
    return(output)

