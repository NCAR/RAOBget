###############################################################################
# Code to display the central widget of the RAOBget GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import logging
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget, \
     QFrame, QPlainTextEdit
from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
from gui.configedit import GUIconfig
from lib.messageHandler import printmsg
from raobtype.skewt import Skewt

# from PIL import Image
# from resizeimage import resizeimage


class Widget(QWidget):

    def __init__(self, raob, app):
        super().__init__()

        self.app = app
        self.initWidget(raob)

    def initWidget(self, raob):
        # Make raob accessible throughout this file
        self.raob = raob

        # Configure layout
        # Add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        self.layout = QGridLayout(self)

        # Add a log message window
        self.log = self.createLogMessageWindow()

        # Add configuration editor window
        self.config = GUIconfig(self.log, raob)
        self.config.createConfigEditor(self, self.layout)

        # Add an image window to hold the skewt
        self.createImageWindow()

        # Add a button to begin retrieving RAOBs
        self.createRetrieveButton()

    def configGUI(self):
        return(self.config)

    def get_log(self):
        """ Return a pointer to the log message window """
        return(self.log)

    def createRetrieveButton(self):
        retrieve = QPushButton("Retrieve RAOBs")
        self.layout.addWidget(retrieve, 2, 0)
        retrieve.clicked.connect(self.clickRetrieve)
        retrieve.setToolTip('Click to start downloading RAOBs')
        retrieve.show()

    def createImageWindow(self):
        """ Add an image window to hold the Skewt image """
        self.image = QLabel()
        self.layout.addWidget(self.image, 0, 1, 1, 2)
        pixmap = self.getImage()
        # This was an attempt to resize from [800,640] to [600,480]. Image
        # quality is unacceptably low. gif's don't resize well.
        # pixmap_resized = pixmap.scaled(600, 480, Qt.KeepAspectRatio)
        # image.setPixmap(pixmap_resized)
        self.image.setPixmap(pixmap)
        self.image.show()

    def getImage(self, gifimage='./gui/message.gif'):
        """ Return the image associated with the latest downloaded RAOB data.
        Defaults to usage message on initialization.
        """
        self.pixmap = \
            QPixmap(gifimage)
        return(self.pixmap)

    def resetImageWindow(self):
        # Am I creating a bunch of widgets on top of each other, or
        # replacing the previous one??
        self.layout.removeWidget(self.image)
        self.skewt = Skewt(self.app)
        self.skewt.set_fig()
        self.skewt.set_canvas()
        self.canvas = self.skewt.get_canvas()
        self.layout.addWidget(self.canvas, 0, 1, 1, 2)

    def setImage(self, outfile):
        self.image.setPixmap(QPixmap(outfile))

    def createLogMessageWindow(self):
        """ Add a log message window """
        log = QPlainTextEdit()
        log.setReadOnly(True)
        self.layout.addWidget(log, 1, 0, 1, 3)
        log.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        printmsg(log, "Status and error messages will appear here")
        log.show()
        return(log)

    def clickRetrieve(self):
        """ Actions to take when the 'Begin retrieval' button is selected """
        printmsg(self.log, "Begin retrieval")
        logging.info(str(self.raob.request.get_request()))
        self.raob.get(self, self.app, self.log)

    def createSkewt(self, outfile):
        """ Create a skewt image from a downloaded TEXT:LIST data file """
        self.skewt.clear()
        rdat = self.skewt.read_data(outfile)
        self.skewt.create_skewt(rdat)
        self.canvas = self.skewt.get_canvas()
        self.canvas.draw()
        self.skewt.close()
        self.app.processEvents()
