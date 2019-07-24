from PyQt5.QtWidgets import QScrollBar
from mainWidget import MainWidget

# Class just to change stylesheet of sthe scrollbar


class ScrollBar(QScrollBar):
    def __init__(self, color, parent=None, *args, **kwargs):
        super().__init__(*args, parent, **kwargs)
        self.pickColor(color)

    # background: qlineargradient(x1:0, y1:0, x2:0 y2:1, stop:0 #b4b4b4, stop:1 #AD568A);
    def pickColor(self, color):
        # old way of changing the scrollbar with combobox
        '''colorSelection = {"Pink": "#AD568A", "Blue": "#365C87", "Green": "#56673A",
                          "Gray": "#4E555C", "Purple": " #6A477C", "Red": "#862C2F"}
        selectColor = colorSelection[color]'''

        self.setStyleSheet("""
            QScrollBar:horizontal {
                border: 1px solid black;
                background:"""+color+""";
                height: 15px;
                margin: 0px 16px 0px 16px;
            }
            QScrollBar::handle:horizontal {
                background: lightgray;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                border: 1px solid black;
                background: lightgray;
                width: 15px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                image: url('./rightArrow.png');
            }
            QScrollBar::sub-line:horizontal {
                border: 1px solid black;
                background: lightgray;
                width: 15px;
                subcontrol-position: left;
                subcontrol-origin: margin;
                image: url('./leftArrow.png');
            }

            QScrollBar:vertical {
                border: 1px solid black;
                background:"""+color+""";
                width: 15px;
                margin: 16px 0px 16px 0px;
            }
            QScrollBar::handle:vertical {
                min-height: 20px;
                background: lightgray;
            }
            QScrollBar::add-line:vertical {
                border: 1px solid black;
                background: lightgray;
                height: 15px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                image: url('./downArrow.png');
            }
            QScrollBar::sub-line:vertical {
                border: 1px solid black;
                background: lightgray;
                height: 15px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                image: url('./upArrow.png');
            }"""
                           )
