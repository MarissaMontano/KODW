from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QListWidget, QListWidgetItem,\
    QLabel, QComboBox, QTextEdit, QDesktopWidget, QTableView, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractScrollArea



class BasicWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizeObject = QDesktopWidget().screenGeometry(-1)
        width = sizeObject.width()
        height = sizeObject.height()

        basicLayout = QVBoxLayout(self)
        exitLayout = QHBoxLayout()

        # Qlabel for name of classifier 
        self.classLable = QLabel()
        self.classLable.setAlignment(Qt.AlignLeft)

        # Qlabel for info about classifier 
        self.classInfo = QLabel()
        self.classInfo.setWordWrap(True)
        self.classInfo.setAlignment(Qt.AlignLeft)

        # set label styles 
        labelStyle = """
            padding: 2%;
            text-align: left;
            color: gray;
            font-size: 14px;
            border-radius: 3px;
            font:helvetica;
        """
        self.classLable.setStyleSheet(labelStyle)
        self.classInfo.setStyleSheet(labelStyle)

        # Set button styles 
        self.backtoMain = QPushButton('Back')
        buttonStyle = """
            border: .5px solid balck;
            color: gray;
            font-size: 12px;
            font:helvetica;
            border-radius: 3px;
            
        """
        self.backtoMain.setStyleSheet(buttonStyle)
        self.backtoMain.setFixedSize(QSize(width/18, height/25))
        
        # Set final layout of the basic widget
        basicLayout.addStretch(0)
        basicLayout.addWidget(self.classLable)
        basicLayout.addWidget(self.classInfo)
        basicLayout.addStretch(0)
        exitLayout.addWidget(self.backtoMain)
        exitLayout.setAlignment(Qt.AlignRight)
        basicLayout.addLayout(exitLayout)
        basicLayout.addStretch(0)
        basicLayout.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(self.size())
