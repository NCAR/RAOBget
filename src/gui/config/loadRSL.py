###############################################################################
# Methods to manipulate the load RSL station list metadata display in the GUI.
# The selected RSL file is not displayed in the GUI.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import logging
from PyQt5.QtWidgets import QLabel, QPushButton
from gui.fileselector import FileSelector
from lib.messageHandler import printmsg


class LoadRSL():

    def __init__(self, request, log=""):
        """ This class creates a button which launches a FileSelector """
        self.log = log
        self.request = request

        self.label = "Load RSL station list"

    def create(self, box, row, stnm):
        """ Create the Load station list button """
        self.stnm = stnm
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        self.load = QPushButton(self.label)
        self.load.clicked.connect(self.loadRSL)
        self.load.setToolTip('Load a list of stations from a file')
        box.addWidget(self.load, row, 1, 1, 2)

    def loadRSL(self):
        """ Call dialog box to load a station list """

        # Call dialog box to select a raob station list (rsl) file
        # Once selected, code will loop through contents
        self.loader = FileSelector("loadRsl")
        self.request.set_rsl(self.loader.get_file())
        if (self.request.get_rsl() == ""):
            printmsg(self.log, "WARNING: Station list not loaded. Please " +
                               "select a station/station list.")
        else:
            self.load.setText(self.request.get_rsl())
            logging.info("RAOB station list set to " +
                         self.request.get_rsl())

        # When load an RSL file, set stnm to empty in request and reset display
        # text to empty.
        self.request.set_stnm('')
        self.stnm.setText('')

    def get_default_label(self):
        """ Return the default label for the load RSL button """
        return(self.label)

    def get_button(self):
        """
        This is used to pass a reference to load RSL button to the stnm class
        so it can reset the RSL button label to the default when a station is
        chosen to override a previous RSL file selection.
        """
        return(self.load)
