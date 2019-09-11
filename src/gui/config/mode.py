###############################################################################
# Methods to manipulate the mode (default, mtp, catalog, etc) metadata
# display in the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QComboBox
from lib.messageHandler import printmsg


class Mode():

    def __init__(self, request, log=""):
        """ The mode is displayed in a dropdown (QComboBox) """
        self.comboBox = QComboBox()
        self.log = log
        self.request = request

    def create(self, box, row):
        """
        Create and place the mode dropdown into the configuration
        section of the GUI
        """
        lbl = QLabel("Mode")
        box.addWidget(lbl, row, 0)
        self.comboBox.addItem("Default")
        self.comboBox.addItem("MTP")
        self.comboBox.addItem("CATALOG")
        self.comboBox.activated[str].connect(self.set)
        self.comboBox.setToolTip('Select the mode to run in')
        box.addWidget(self.comboBox, row, 1)

    def set(self, text):
        """ Save the mode selected in the GUI to the metadata dictionary """
        if text == "MTP":
            self.request.set_mtp(True)
            printmsg(self.log, "Mode set to MTP")
        if text == "CATALOG":
            self.request.set_catalog(True)
            printmsg(self.log, "Mode set to Catalog")

    def update(self, text):
        """
        Update the mode displayed in the GUI

        Requires:
            The mode to be displayed
        """
        self.comboBox.setCurrentText(text)
