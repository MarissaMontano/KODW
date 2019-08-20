from PyQt5.QtWidgets import QMainWindow, QShortcut, QColorDialog, QAction, QMenu, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush, QIcon
from PyQt5.QtCore import Qt, QThread
from GUI.mainWidget import MainWidget
from GUI.basicWidget import BasicWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self, genreList = [], *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Palette stuff - text white, background dark gray
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor(27, 27, 27))
        self.palette.setColor(QPalette.Button, QColor(27, 27, 27))  
        self.setPalette(self.palette)

        # Menue Bar
        # Menu for classifier info 
        classifierMenu = QMenu("&Classifiers", self)
        gradBoost = QAction("&Gradient Boosting", self)
        gradBoost.triggered.connect(self.startGradientBoost)
        knear = QAction("&K-Nearest Neighbors", self)
        knear.triggered.connect(self.startKNearest)
        rbfsvm = QAction("&RBF SVM", self)
        rbfsvm.triggered.connect(self.startRbfSvm)
        classifierMenu.addAction(knear)
        classifierMenu.addAction(rbfsvm)
        classifierMenu.addAction(gradBoost)
        classifierMenu.setStyleSheet("""
            QMenu::item {background-color: rgb(33, 33, 33); color: rgb(126, 126, 126); }
            QMenu::item:pressed {color: rgb(255,255,255);}
            QMenu::item:selected {color: rgb(255,255,255);}""")
        # Action to close gui
        closeAction = QAction("&Close", self)
        closeAction.setStatusTip('Close the Appliction')
        closeAction.triggered.connect(self.close)
        # main menue that adds all other menues and actions
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addMenu(classifierMenu)
        helpMenu.addAction(closeAction)
        helpMenu.setStyleSheet("""
            QMenu::item {background-color: rgb(33, 33, 33); color: rgb(126, 126, 126); }
            QMenu::item:pressed {color: rgb(255,255,255);}
            QMenu::item:selected {color: rgb(255,255,255);}""")
        mainMenu.setStyleSheet("""
            QMenuBar{background-color: rgb(33, 33, 33);color: rgb(126, 126, 126); }
            QMenuBar::item:pressed {color: rgb(255,255,255);}
            QMenuBar::item:selected {color: rgb(255,255,255);}""")

        # Set width/height of main window
        width = self.width()
        height = self.height()
        self.resize(width/.6, height/.6)

        # Default to showing the main widget first
        self.startMainWidget(genreList)


    def startKNearest(self):
        ''' Method to show info about the k-nearest neighbor classifier from the basic widget templet

                Input:  None
                Output: None
        '''
        self.basicWidget = BasicWidget()
        self.setWindowTitle("K-Nearest Neighbors Info")
        self.basicWidget.classLable.setText("What is a K-Nearest Neighbors classifier?\n")
        self.basicWidget.classInfo.setText("The K-nearest neighbor classifier is basically a voting system based off of close by neighbors, k of them to be specific. The idea around k-nearest neighbors is it groups itself based on its k-nearest neighbors. For example, if its k-nearest neighbors are a majority of songs the user likes, its going to get grouped in with a list of good songs.")
        self.basicWidget.backtoMain.clicked.connect(self.startMainWidget)
        self.setCentralWidget(self.basicWidget)
        self.show()

    def startRbfSvm(self):
        ''' Method to show info about the RBF SVM classifier from the basic widget templet

                Input:  None
                Output: None
        '''
        self.basicWidget = BasicWidget()
        self.setWindowTitle("RBF SVM Info")
        self.basicWidget.classLable.setText("What is a RBF SVM classifier?\n")
        self.basicWidget.classInfo.setText("First of all an RBF SVM is a type of Support Vector Machine, a Linear non-separable SVM to be specific. SVM are used to maximize the decision boundary between two categories. Because the data were using can be non-separable (no clear line can be drawn) we have to use the kernel trick with RBF. This creates new features based on the distance between a center and other points (higher the gamma closer the reach, so we have a non-linear line used as the decision boundary). ")
        self.basicWidget.backtoMain.clicked.connect(self.startMainWidget)
        self.setCentralWidget(self.basicWidget)
        self.show()

    def startGradientBoost(self):
        ''' Method to show info about the gradient boosting classifier from the basic widget templet

                Input:  None
                Output: None
        '''
        self.basicWidget = BasicWidget()
        self.setWindowTitle("Gradient Boosting Info")
        self.basicWidget.classLable.setText("What is a Gradient Boosting classifier?\n")
        self.basicWidget.classInfo.setText("The Gradient Boosting classifier is a method to minimize loss by converting weak learners to strong learners. Like (Simple Linear Regression) SLR we want to fit a model to the data that will minimize loss, but with gradient boosting we will do so sequentially by using early learners to fit the data and later learners to fix the ‘errors’ or compute and predict the residuals made by the earlier learners. You stop just before over fitting the data.")
        self.basicWidget.backtoMain.clicked.connect(self.startMainWidget)
        self.setCentralWidget(self.basicWidget)
        self.show()

    def startMainWidget(self, genreList):
        ''' Method to show the main widget templet that lets you choose classifiers, genres, and update the cache 

                Input:  None
                Output: None
        '''
        # Set title, style and widget   
        self.setWindowTitle("OBDW")
        self.setStyleSheet('background-color: rgb(27, 27, 27);')
        self.mainWidget = MainWidget(genreList)

        #set button functionality 
        self.mainWidget.cancelButton.clicked.connect(self.close)
        self.userClassifier = ''
        self.userGenres = []
        self.updateCache = False
        self.mainWidget.okButton.clicked.connect(self.handleOK)
        self.mainWidget.cacheButton.clicked.connect(self.handleCache)

        # Set the widget and show
        self.setCentralWidget(self.mainWidget)
        self.show()


    def handleCache(self):
        ''' Method to pop up a Qdialog box asking is they reall wanna update the cache and then set the variable updateCache

                Input:  None
                Output: None
        '''
        message = '<div><b style="color: gray;">'+'Are you sure you want to refresh the cache?'+'</b></div>'
        warning = '<br><div><b style="color: gray;">'+'This action will run in the background, but still may take a few minutes to complete'+'</b></div>'
        choice = QMessageBox.question(self, 'Refresh cache',
                                            message+warning,
                                            QMessageBox.Yes | QMessageBox.Cancel)
        if choice == QMessageBox.Yes:
            self.updateCache = True
        else:
            self.updateCache = False
            pass
       
    
    def handleOK(self):
        ''' Method to set the info the user put into the gui

                Input:  None
                Output: None
        '''
        # Update genere and classifier
        items = self.mainWidget.genreTable.selectedItems()
        for item in items:
            self.userGenres.append(item.text())
        self.userClassifier = self.mainWidget.classifierCombo.currentText()
        self.close()

    def grabUserInfo(self):
        ''' Method to grab user info (ie, what they select for genres, classifiers, and cache)

                Input:  None
                Output: 3D list of strings
        '''
        return([self.userGenres, self.userClassifier, self.updateCache])
