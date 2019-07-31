from PyQt5.QtWidgets import QMainWindow, QShortcut, QColorDialog, QAction, QMenu
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush, QIcon
from PyQt5.QtCore import Qt, QThread
from GUI.mainWidget import MainWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("OBDW")
        self.setStyleSheet('background-color: rgb(27, 27, 27);')
        self.mainWidget = MainWidget()
        #set cancel/ok button functionality 
        self.mainWidget.cancelButton.clicked.connect(self.close)
        self.userClassifier = ''
        self.userGenres = []
        self.mainWidget.okButton.clicked.connect(self.handleOK)

        # TODO: mess with palette stuff
        # text white, background dark gray
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor(27, 27, 27))
        self.palette.setColor(QPalette.Button, QColor(27, 27, 27))  
        self.setPalette(self.palette)

        # menue bar
        classifierMenu = QMenu("&Classifiers", self)
        gradBoost = QAction("&Gradient Boosting", self)
        gradBoost.triggered.connect(self.gradientBoost)
        knear = QAction("&K-Nearest Neighbors", self)
        knear.triggered.connect(self.kNearest)
        rbfsvm = QAction("&RBF SVM", self)
        rbfsvm.triggered.connect(self.rbfSvm)
        classifierMenu.addAction(knear)
        classifierMenu.addAction(rbfsvm)
        classifierMenu.addAction(gradBoost)
        classifierMenu.setStyleSheet("QMenu::item {background-color: rgb(33, 33, 33);}")
        
        closeAction = QAction("&Close", self)
        closeAction.setStatusTip('Close the Appliction')
        closeAction.triggered.connect(self.close)

        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addMenu(classifierMenu)
        helpMenu.addAction(closeAction)
        
        mainMenu.setStyleSheet("""
        QMenu::item {background-color: rgb(33, 33, 33);}
        QMenuBar{background-color: rgb(33, 33, 33);}""")
        self.setCentralWidget(self.mainWidget)

    #talk about them here
    def kNearest(self):
        print('near')

    def rbfSvm(self):
        print('rbf')

    def gradientBoost(self):
        print('boost')
    
    def handleOK(self):
        # update genere and classifier
        items = self.mainWidget.genreTable.selectedItems()
        for item in items:
            self.userGenres.append(item.text())
        self.userClassifier = self.mainWidget.classifierCombo.currentText()
        self.close()

    def grabUserInfo(self):
        return([self.userGenres, self.userClassifier])
