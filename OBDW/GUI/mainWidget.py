#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QComboBox, QTextEdit, QDesktopWidget, QScrollArea, QColorDialog,\
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractScrollArea, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPalette, QColor
import pymongo
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import webbrowser


MONGO_CONNECTION = "mongodb://127.0.0.1:27017/"


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # NOTE: the order in which shit is defined is the order in the parent child chain
        # the self is really parent=self (QWidget --> QVBox)
        mainLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        colorhLayout = QHBoxLayout()
        commentColor = QHBoxLayout()
        dataHbox = QHBoxLayout()
        lastWidget = QHBoxLayout()

        # get screen size to make obj reletive instread of fixed
        sizeObject = QDesktopWidget().screenGeometry(-1)
        width = sizeObject.width()
        height = sizeObject.height()

        # set scroll bar
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(
            QRect(0, 0, width/1.8, height))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # button to say "hello _____"
        self.onButton = QPushButton("Enter")
        self.onButton.setFixedSize(QSize(width/20, height/30))
        self.onButton.clicked.connect(self.handleButtonOn)
        self.enterName = ""
        self.enterNum = ""

        # button to clear the hello statment
        self.offButton = QPushButton("Clear")
        self.offButton.setFixedSize(QSize(width/20, height/30))
        self.offButton.clicked.connect(self.handleButtonOff)

        # line to get user to input name
        self.inputLine = QLineEdit()
        self.inputLine.setFixedWidth(width/9)

        self.title = QLabel("Please Enter Your Name:")
        self.title.setAlignment(Qt.AlignCenter)

        # label to get user to change colors
        colorPrompt = QLabel("Don't like the background?")
        colorPrompt.setAlignment(Qt.AlignCenter)

        # old way of selecting colors -  combo box to chaneg colors
        '''self.combobox = QComboBox()
        self.combobox.setFixedWidth(width/11)
        self.combobox.addItem("Pink")
        self.combobox.addItem("Blue")
        self.combobox.addItem("Red")
        self.combobox.addItem("Purple")
        self.combobox.addItem("Green")
        self.combobox.addItem("Gray")'''

        # new way of choosing the background
        self.colorButton = QPushButton("Change the background")
        self.colorButton.setFixedSize(QSize(width/12, height/30))

        # text edit for color additions
        self.suggestionBox = QTextEdit()
        self.suggestionBox.setFixedSize(width/4, height/11)
        self.suggestionBox.setPlaceholderText(
            "If you have any comments or consers about the color scheme, please let me know here")

        self.subButton = QPushButton("Submmit")
        self.subButton.setMaximumHeight(height/30)
        self.subButton.setMaximumWidth(width/18)
        self.subButton.clicked.connect(self.handleButtonSub)

        self.submmitPrompt = QLabel()
        self.submmitPrompt.setAlignment(Qt.AlignCenter)
        self.submmitPrompt.setDisabled(True)

        # figure for plot of fave nums
        self.figure = Figure()
        self.figure.patch.set_facecolor('none')
        self.figure.patch.set_alpha(0)
        self.figure.set_facecolor('none')
        self.figure.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setVisible(False)

        # Table to keep track of the favorite numbers
        self.scoreTable = QTableWidget()
        self.scoreTable.horizontalHeader().setVisible(False)
        self.scoreTable.verticalHeader().setVisible(False)
        self.scoreTable.setVisible(False)
        self.scoreTable.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.scoreTable.resizeColumnsToContents()
        self.scoreTable.setStyleSheet("""
            QTableWidget{
                background-color: transparent;
            }
            QHeaderView::section{
                background-color: transparent;
            }
            QHeaderView{
                background-color: transparent;
            }
            QTableWidget QTableCornerButton::section {
                background-color: transparent;
            }"""
                                      )

        # subreddit Qlist widget
        subredditList = QListWidget()
        redditList = ["Interesting", "Kids", "Happy", "Mysteries"]
        for subreddit in redditList:
            sub = QListWidgetItem(subreddit)
            sub.setTextAlignment(Qt.AlignCenter)
            subredditList.addItem(sub)
        subredditList.setFixedWidth(width/12)
        subredditList.itemDoubleClicked.connect(self.handleList)
        subredditList.setStyleSheet("""
            QListWidget{background-color:transparent;}
            QListWidget::item:selected{background-color:transparent; color:red;}
            """)
        # first layout (make it it acroll area before you add stuff)
        mainLayout.addWidget(self.scrollArea)
        mainLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        # put everything in the "scroll area"
        mainLayout.addStretch(0)
        mainLayout.addWidget(self.title)
        mainLayout.addLayout(hLayout)
        mainLayout.addLayout(dataHbox)
        # mainLayout.addWidget(self.canvas)
        # mainLayout.addWidget(self.scoreTable)
        mainLayout.addStretch(0)
        mainLayout.addLayout(colorhLayout)
        mainLayout.addLayout(commentColor)
        mainLayout.addWidget(self.submmitPrompt)
        mainLayout.addLayout(lastWidget)
        mainLayout.addStretch(0)
        mainLayout.setAlignment(Qt.AlignCenter)

        # second layout
        hLayout.addWidget(self.inputLine)
        hLayout.addWidget(self.onButton)
        hLayout.addWidget(self.offButton)
        hLayout.setAlignment(Qt.AlignCenter)

        # third layout
        colorhLayout.addWidget(colorPrompt)
        # old way with combobox - changed to dialog box
        # self.colorhLayout.addWidget(self.combobox)
        colorhLayout.addWidget(self.colorButton)
        colorhLayout.setAlignment(Qt.AlignCenter)

        # fourth layout (hiden data)
        dataHbox.addWidget(self.canvas)
        dataHbox.addWidget(self.scoreTable)

        # fifth layout
        commentColor.addWidget(self.suggestionBox)
        commentColor.addWidget(self.subButton)
        commentColor.setAlignment(Qt.AlignCenter)

        # last layer
        lastWidget.addWidget(subredditList)
        lastWidget.setAlignment(Qt.AlignCenter)

        # setting up stylesheets for labels, buttons, ect...
        labelStyle = """
            padding: 2%;
            text-align: left;
            color: black;
            font-size: 20px;
            border-radius: 3px;
            font:helvetica;
        """

        self.title.setStyleSheet(labelStyle)
        colorPrompt.setStyleSheet(labelStyle)
        self.submmitPrompt.setStyleSheet(labelStyle)

        buttonStyle = """
            border: .5px solid ;
            color: black;
            font-size: 10px;
            font:helvetica;
            border-radius: 3px;
            
        """
        self.onButton.setStyleSheet(buttonStyle)
        self.offButton.setStyleSheet(buttonStyle)
        self.subButton.setStyleSheet(buttonStyle)
        self.colorButton.setStyleSheet(buttonStyle)

    # Method to handel hitting the enter and clear buttons
    def handleButtonOn(self):
        # still at name stage
        if self.title.text() == "Please Enter Your Name:":
            # prompt for fave number
            self.enterName = self.inputLine.text()
            self.inputLine.setText("")
            self.title.setText("Hey "+self.enterName +
                               "! What's your favorite number?")
        # now at num stage
        else:
            num = self.inputLine.text()
            self.inputLine.setText("")
            try:
                self.enterNum = int(num)
            except ValueError:
                print("Invalid number, not storing data")
        # when both fields are entered, add them to database
        if self.enterName != "" and self.enterNum != "":
            self.mongodbMatplotlib()

    def handleButtonOff(self):
        self.inputLine.setText("")
        self.title.setText("Please Enter Your Name:")
        self.enterName = ""
        self.enterNum = ""
        self.canvas.setVisible(False)

    def handleButtonSub(self):
        colorComment = self.suggestionBox.toPlainText()
        print(colorComment)
        self.suggestionBox.setText("")
        self.submmitPrompt.setEnabled(True)
        if self.enterName != "":
            self.submmitPrompt.setText(
                "Thanks for the comment "+self.enterName+", I'll work on it soon!")
        else:
            self.submmitPrompt.setText(
                "Thanks for the comment, I'll work on it soon!")

    # method to deal with mongodb - pyqt5 db - Marissa Marissa

    def mongodbMatplotlib(self):
        # connect to mongo - hardcode mongodb://127.0.0.1:27017/
        myClient = pymongo.MongoClient(MONGO_CONNECTION)

        # use database/collection if it exists, if not create it
        if "pyqt5" not in myClient.list_database_names():
            print("creating new database")
        myDb = myClient["pyqt5"]
        if "favorite_nums" not in myDb.list_collection_names():
            print("creating new collection")
        myCollect = myDb["favorite_nums"]

        # add their data
        myData = {"name": self.enterName, "nums": self.enterNum}
        myCollect.insert_one(myData)

        # find all fave nums:
        faveNums = []
        for numbers in myCollect.find({}, {"_id": 0, "name": 0}):
            faveNums.append(numbers["nums"])

        # get info for table
        tableInfo = []
        dbInfo = myCollect.find().sort("name")
        for dbLine in dbInfo:
            tableInfo.append((dbLine["name"], dbLine["nums"]))
        self.scoreTable.setVisible(True)
        self.scoreTable.setRowCount(len(tableInfo))
        self.scoreTable.setColumnCount(2)
        # set the table widget item in table and center the text.
        for i in range(len(tableInfo)):
            name = QTableWidgetItem(tableInfo[i][0])
            name.setTextAlignment(Qt.AlignCenter)
            nums = QTableWidgetItem(str(tableInfo[i][1]))
            nums.setTextAlignment(Qt.AlignCenter)
            self.scoreTable.setItem(i, 0, name)
            self.scoreTable.setItem(i, 1, nums)

        # show histogram of fav nums
        self.canvas.setVisible(True)
        self.canvas.setStyleSheet("background-color:transparent;")
        ax = self.figure.add_subplot(111)

        # discards the old histogram and plot new one
        ax.clear()
        ax.patch.set_facecolor('none')
        ax.patch.set_alpha(0)
        ax.hist(faveNums, facecolor="black", edgecolor="gray", alpha=0.4)
        ax.set_title('See how popular your favorite number is')
        ax.set_xlabel('Favorite Numbers')
        ax.set_ylabel('Count of people')
        self.canvas.draw()
        myClient.close()

    def handleList(self, link):
        # navigate to subreddit
        # link.setBackground(QColor(Qt.transparent))
        linkMapper = {"Interesting": 'https://www.reddit.com/r/interestingasfuck/', "Kids": 'https://www.reddit.com/r/KidsAreFuckingStupid/',
                      "Happy": 'https://www.reddit.com/r/HumansBeingBros/', "Mysteries": 'https://www.reddit.com/r/UnresolvedMysteries/'}
        link.setSelected(False)
        webbrowser.open(linkMapper[link.text()])
