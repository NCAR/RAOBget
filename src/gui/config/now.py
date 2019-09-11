###############################################################################
# Methods to manipulate the "set time to now" button display in the GUI.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QPushButton
from lib.messageHandler import printmsg


class Now():

    def __init__(self, request, log=""):
        """ This class creates a button which launches an RSLCreator """
        self.log = log
        self.request = request

        self.label = "Return most recent RAOB"

    def create(self, box, row):
        """ Create a button to set time to now """
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        self.createRAOB = QPushButton(self.label)
        self.createRAOB.clicked.connect(self.set)
        self.createRAOB.setToolTip('Set the time to download to now. Returns' +
                                   ' most recent RAOB for selected station')
        box.addWidget(self.createRAOB, row, 1, 1, 2)

    def set(self):
        self.request.set_now(True)
        self.createRAOB.setText("Time set to now")
        printmsg(self.log, "Time to retrieve set to now")

    def get_default_label(self):
        return(self.label)

    def get_button(self):
        return(self.createRAOB)
