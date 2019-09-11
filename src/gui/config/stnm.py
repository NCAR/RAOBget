###############################################################################
# Methods to manipulate the station number/id metadata display in the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from lib.messageHandler import printmsg


class Stnm():

    def __init__(self, request, log=""):
        """ The station is displayed in a textbox (QLineEdit) """
        self.stnm = QLineEdit()
        self.log = log
        self.request = request

    def create(self, box, row, loadRSL):
        """ Create the Stnm text input field """
        self.loadRSL = loadRSL
        lbl = QLabel("Station ID")
        box.addWidget(lbl, row, 0)
        self.stnm.setToolTip("Enter char or numeric id of station to " +
                             "download and click 'Set'")
        box.addWidget(self.stnm, row, 1)
        use = QPushButton("Set")
        use.clicked.connect(self.set)
        box.addWidget(use, row, 2)

    def set(self):
        """ Set the station to the value entered in the input field

        NEED TO ADD DATA VALIDATION HERE
        """
        textboxValue = self.stnm.text()
        self.request.set_stnm(textboxValue)
        printmsg(self.log, "Station set to " + textboxValue)

        # Since just manually set a station, need to set rsl to '' or
        # any defined rsl file will override user station selection
        self.request.set_rsl('')
        self.reset_loadRSLlabel()

    def update(self, text):
        """
        Update the station number/id displayed in the GUI

        Requires:
            The station number/id to be displayed
        """
        self.setText(text)
        self.reset_loadRSLlabel()

    def setText(self, text):
        """
        Set the text displayed in the GUI. This method is also called by
        loadRSL so when an RSL file is selected to override a previously
        set station, the text in the GUI can be cleared.
        """
        self.stnm.setText(text)

    def reset_loadRSLlabel(self):
        """ Reset the label on the load RSL station list button """
        rsl = self.loadRSL.get_button()
        rsl.setText(self.loadRSL.get_default_label())
