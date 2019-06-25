###############################################################################
# Code to display the central widget of the RAOBget GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget, \
     QFrame, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from gui.configedit import GUIconfig


class Widget(QWidget):

    def __init__(self, raob):
        super().__init__()

        self.initWidget(raob)

    def initWidget(self, raob):
        # Configure layout
        # Add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        layout = QGridLayout(self)

        # Add a log message window
        self.log = self.createLogMessageWindow(layout)

        # Add configuration editor window
        self.config = GUIconfig()
        self.config.createConfigEditor(self, layout, self.log, raob)

        # Add an image window to hold the skewt
        self.createImageWindow(layout)

        # Add a button to begin retrieving RAOBs
        self.createRetrieveButton(layout)

    def createRetrieveButton(self, layout):
        retrieve = QPushButton("Retrieve RAOBs")
        layout.addWidget(retrieve, 2, 2)
        retrieve.clicked.connect(self.clickRetrieve)
        retrieve.setToolTip('Click to start downloading RAOBs')
        retrieve.show()

    def createImageWindow(self, layout):
        """ Add an image window to hold the Skewt image """
        image = QLabel()
        layout.addWidget(image, 0, 1, 1, 2)
        pixmap = self.getImage()
        pixmap_resized = pixmap.scaled(800, 640, Qt.KeepAspectRatio)
        image.setPixmap(pixmap_resized)

        image.show()

    def getImage(self):
        """ Stub - will eventually return the image associated with the latest
        downloaded RAOB data """
        self.pixmap = \
            QPixmap('../ftp/upperair.SkewT.201905280000.Riverton_WY.gif')
        return(self.pixmap)

    def createLogMessageWindow(self, layout):
        """ Add a log message window """
        log = QPlainTextEdit()
        log.setReadOnly(True)
        layout.addWidget(log, 1, 0, 1, 3)
        log.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        log.appendPlainText("Status messages will appear here")
        log.show()
        return(log)

    def setMessage(self, log, text):
        log.appendPlainText(text)

    def clickRetrieve(self):
        """ Actions to take when the 'Begin retrieval' button is selected """
        self.setMessage(self.log, "Begin retrieval")
