from PyQt5.QtWidgets import QApplication
from GUI.mainWindow import MainWindow
import sys


def main(genreList=[]):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(genreList)
    app.exec_()
    output = mainWindow.grabUserInfo()
    return(output)

