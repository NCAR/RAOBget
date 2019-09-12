###############################################################################
# Methods to manipulate the freq (to request RAOBS at) metadata display in
# the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import logging
from PyQt5.QtWidgets import QLabel, QComboBox


class Freq():

    def __init__(self, request, log=""):
        """ The freq is displayed in a dropdown (QComboBox) """
        self.comboBox = QComboBox()
        self.log = log
        self.request = request

    def create(self, box, row):
        """
        Create and place the frequency dropdown into the configuration
        section of the GUI
        """
        lbl = QLabel("Freq (hours)")
        box.addWidget(lbl, row, 0)
        self.comboBox.addItem("")
        self.comboBox.addItem("3")
        self.comboBox.addItem("6")
        self.comboBox.addItem("12")
        self.comboBox.activated[str].connect(self.set)
        self.comboBox.setToolTip('Set the frequency to attempt to download ' +
                                 'data. Less frequent data will still be ' +
                                 'downloaded')
        box.addWidget(self.comboBox, row, 1)

    def set(self, text):
        """ Save the selected reporting frequency to the metadata dictionary"""
        self.request.set_freq(text)
        logging.info("Freq set to " + text)

    def update(self, text):
        """
        Update the frequency displayed in the GUI

        Requires:
            The frequency to be displayed
        """
        self.comboBox.setCurrentText(text)
