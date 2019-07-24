from PyQt5.QtGui import QDialog
from PyQt5.QtWidgets import QMessageBox, QPushButton
from mainWidget import MainWidget

# Class class to make a custom dialog box


class BoringDialog(QMessageBox):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, parent, **kwargs)
        self.setText('What do you want to do?')
        self.addButton(QPushButton("Quit"), QMessageBox.YesRole)
        self.addButton(QPushButton("Retry"), QMessageBox.NoRole)
        self.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
