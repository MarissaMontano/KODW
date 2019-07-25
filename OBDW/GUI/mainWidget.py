#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QListWidget, QListWidgetItem,\
    QLabel, QComboBox, QTextEdit, QDesktopWidget, QTableView, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractScrollArea
import math


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

        # table for genres
        self.genreTable = QTableWidget()

        self.genreTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.genreTable.horizontalHeader().setVisible(False)
        self.genreTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.genreTable.verticalHeader().setVisible(False)
        self.genreTable.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.genreTable.setStyleSheet("""
            QTableWidget{
                background-color: transparent;
                border: none;
            }
            QTableView{
                selection-background-color:transparent;
                selection-color:red;
                border:.5px solid black;
                color:gray;
            }""")

        genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 
                  'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 
                  'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 
                  'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop',
                  'industrial', 'iranian', 'j-dance','j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 
                  'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 
                  'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 
                  'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 
                  'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
        self.genreTable.setRowCount(math.ceil(len(genres)/10))
        self.genreTable.setColumnCount(10)
        self.genreTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.genreTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # set the table widget item in table and center the text.
        row = 0
        for i in range(len(genres)):
            if(i % 10 == 0 and i != 0):
                row += 1
            col = i % 10
            types = QTableWidgetItem(genres[i])
            types.setTextAlignment(Qt.AlignCenter)
            self.genreTable.setItem(row, col, types)
        # self.genreTable.setColumnWidth(width/14)

        # label for classifier
        classifierLable = QLabel(
            "Update Your Classifier: Updating your classifier will change the algorithm used to get your recommendations. Please see the 'Help' tab to learn more.")
        # classifierLable.setWordWrap(True)
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
        self.okButton = QPushButton("OK")
        self.okButton.setFixedSize(QSize(width/18, height/25))

        # first layout to hold the main widget stuff
        mainLayout.addStretch(0)
        cacheLayout.addWidget(cacheLable)
        cacheLayout.addWidget(cacheButton)
        cacheLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(cacheLayout)
        mainLayout.addStretch(0)
        genreLayout.addWidget(genreLable)
        genreLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(genreLayout)
        mainLayout.addWidget(self.genreTable)
        mainLayout.addStretch(0)
        classLayout.addWidget(classifierLable)
        classLayout.addWidget(self.classifierCombo)
        classLayout.setAlignment(Qt.AlignLeft)
        mainLayout.addLayout(classLayout)
        mainLayout.addStretch(0)
        mainLayout.addLayout(exitLayout)

        mainLayout.setAlignment(Qt.AlignHCenter)

        # second layout for exiting cleanly
        exitLayout.addWidget(self.okButton)
        exitLayout.addWidget(self.cancelButton)
        exitLayout.setAlignment(Qt.AlignRight)

        # Stylesheets!!!!!!!!!!!!!!!!!
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
        self.okButton.setStyleSheet(buttonStyle)
        self.cancelButton.setStyleSheet(buttonStyle)
        cacheButton.setStyleSheet(buttonStyle)

        self.classifierCombo.setStyleSheet(
            "background-color: rgb(33,33,33);border:.5px solid black;")

    def handleCache(self):
        print('@ cache')
