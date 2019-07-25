#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QComboBox, QTextEdit, QDesktopWidget, QScrollArea, QColorDialog,\
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractScrollArea, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPalette, QColor


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QVBoxLayout(self)
        exitLayout = QHBoxLayout()
        cacheLayout = QVBoxLayout()
        genreLayout = QVBoxLayout()
        classLayout = QVBoxLayout()
        # get screen size to make obj reletive instread of fixed
        sizeObject = QDesktopWidget().screenGeometry(-1)
        width = sizeObject.width()
        height = sizeObject.height()

        # label for cache
        cacheLable = QLabel(
            "Update Music Cache: Updating the music cache means you will pull new music from Spotify and update the databse")
        cacheLable.setAlignment(Qt.AlignCenter)

        # button to update cache
        cacheButton = QPushButton("Update Cache")
        cacheButton.setFixedSize(QSize(width/14, height/30))
        cacheButton.clicked.connect(self.handleCache)

        # label for genre
        genreLable = QLabel(
            "Update Your Genres: Updating your genres means you will be recommended more music in these genres")
        genreLable.setAlignment(Qt.AlignCenter)

        # list for genres
        genreList = QListWidget()
        genreList.setSelectionMode(QListWidget.MultiSelection)
        genres = ['r-n-b', 'soul', 'rock', 'rap']
        for genre in genres:
            item = QListWidgetItem(genre)
            item.setTextAlignment(Qt.AlignCenter)
            genreList.addItem(item)
        genreList.setFixedWidth(width/12)
        genreList.setStyleSheet("""
            QListWidget{background-color:transparent; color:grey;}
            QListWidget::item:selected{background-color:transparent; color:red;}
            """)

        # label for classifier
        classifierLable = QLabel(
            "Update Your Classifier: Updating your classifier will change the algorithm used to get your recommendations. Please see the 'Help' tab to learn more.")
        #classifierLable.setWordWrap(True)
        classifierLable.setAlignment(Qt.AlignCenter)

        # Combo box to select classifier
        self.classifierCombo = QComboBox()
        self.classifierCombo.setFixedWidth(width/10)
        self.classifierCombo.addItem("K-Nearest Neighbors")
        self.classifierCombo.addItem("RBF SVM")
        self.classifierCombo.addItem("Gradient Boosting ")

        # Way to cancel and exit GUI
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedSize(QSize(width/18, height/25))

        # Way to save options selected
        okButton = QPushButton("OK")
        okButton.setFixedSize(QSize(width/18, height/25))
        okButton.clicked.connect(self.handleOK)

        # first layout to hold the main widget stuff
        mainLayout.addStretch(0)
        cacheLayout.addWidget(cacheLable)
        cacheLayout.addWidget(cacheButton)
        cacheLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(cacheLayout)
        mainLayout.addStretch(0)
        genreLayout.addWidget(genreLable)
        genreLayout.addWidget(genreList)
        genreLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(genreLayout)
        mainLayout.addStretch(0)
        classLayout.addWidget(classifierLable)
        classLayout.addWidget(self.classifierCombo)
        classLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(classLayout)
        mainLayout.addStretch(0)
        mainLayout.addLayout(exitLayout)

        mainLayout.setAlignment(Qt.AlignRight)

        # second layout for exiting cleanly
        exitLayout.addWidget(okButton)
        exitLayout.addWidget(self.cancelButton)
        exitLayout.setAlignment(Qt.AlignRight)
        # setting up stylesheets for labels, buttons, ect...
        labelStyle = """
            padding: 2%;
            text-align: left;
            color: gray;
            font-size: 14px;
            border-radius: 3px;
            font:helvetica;
        """
        cacheLable.setStyleSheet(labelStyle)
        genreLable.setStyleSheet(labelStyle)
        classifierLable.setStyleSheet(labelStyle)

        buttonStyle = """
            border: .5px solid balck;
            color: gray;
            font-size: 12px;
            font:helvetica;
            border-radius: 3px;
            
        """
        okButton.setStyleSheet(buttonStyle)
        self.cancelButton.setStyleSheet(buttonStyle)
        cacheButton.setStyleSheet(buttonStyle)
        
        self.classifierCombo.setStyleSheet("background-color: rgb(33,33,33);border:.5px solid black;")

    def handleCache(self):
        print('@ cache')


    def handleOK(self):
        # update genere and classifier
        print('@ OK')
