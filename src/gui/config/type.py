###############################################################################
# Methods to manipulate the type (type of RAOB data to download) metadata
# display in the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QComboBox
from lib.messageHandler import printmsg


class Type():

    def __init__(self, request, log=""):
        """ The type is displayed in a dropdown (QComboBox) """
        self.comboBox = QComboBox()
        self.log = log
        self.request = request

    def create(self, box, row):
        """
        Create and place the type dropdown into the configuration
        section of the GUI
        """
        lbl = QLabel("Data Format")
        box.addWidget(lbl, row, 0)
        self.comboBox.addItem("")
        self.comboBox.addItem("TEXT:LIST")
        self.comboBox.addItem("GIF:SKEWT")
        self.comboBox.activated[str].connect(self.set)
        self.comboBox.setToolTip('Choose to either download data in text ' +
                                 'format, or download SkewT plots as gif ' +
                                 'images.')
        box.addWidget(self.comboBox, row, 1)

    def set(self, text):
        """ Save the selected type to the metadata dictionary"""
        self.request.set_type(text)
        printmsg(self.log, "RAOB type set to " + text)

    def update(self, text):
        self.comboBox.setCurrentText(text)
