###############################################################################
# Code related to creating the configEditor section of the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox
# Import metadata handlers
from gui.config.mode import Mode
from gui.config.freq import Freq
from gui.config.type import Type
from gui.config.stnm import Stnm
from gui.config.loadRSL import LoadRSL
from gui.config.createRSL import CreateRSL
from gui.config.btime import BTime
from gui.config.etime import ETime
from gui.config.now import Now
# from lib.messageHandler import printmsg
# If want to print status messages, use printmsg(self.log, msg)


class GUIconfig():

    def __init__(self, log, raob):

        self.log = log
        self.raob = raob

        # Instantiate the various request metadata handlers
        self.mode = Mode(self.raob.request, self.log)
        self.freq = Freq(self.raob.request, self.log)
        self.type = Type(self.raob.request, self.log)
        self.stnm = Stnm(self.raob.request, self.log)
        self.loadRSL = LoadRSL(self.raob.request, self.log)
        self.createRSL = CreateRSL(self.raob.request, self.log)
        self.btime = BTime(self.raob.request, self.log)
        self.etime = ETime(self.raob.request, self.log)
        self.now = Now(self.raob.request, self.log)

    def createConfigEditor(self, widget, layout):
        """ Lay out area where users can define metadata specifying which
        RAOBs to download """

        self.widget = widget
        self.request = self.raob.request.get_request()

        # Create the configuration box in the root layout of the software
        editor = QGroupBox("Configuration")
        layout.addWidget(editor, 0, 0)

        # Create a grid layout for inside the configuration box
        box = QGridLayout()
        lbl = QLabel("Set mode to MTP or CATALOG to format and name " +
                     "files as required by these specific applications.")
        lbl.setWordWrap(True)
        box.addWidget(lbl, 0, 0, 1, 2)
        self.mode.create(box, 1)  # Create and place the mode dropdown
        self.freq.create(box, 2)  # Create and place the frequency dropdown
        self.type.create(box, 3)  # Create and place the type dropdown
        lbl = QLabel("In CATALOG operational mode, ftp params will have to " +
                     "be set via a config file. Use File->Load config menu " +
                     "option.")
        lbl.setWordWrap(True)
        lbl.setStyleSheet('color: Blue')
        box.addWidget(lbl, 4, 0, 1, 2)

        # Create and place the station list layout in the configuration box
        station = QGroupBox("Station selection")
        box.addWidget(station, 5, 0, 1, 2)
        stnbox = QGridLayout()
        # Usage info to users
        lbl = QLabel("Enter a single station to download, interactively " +
                     "create a list of stations to download from a recent" +
                     " GEMPAK station list, or load an existing station list")
        lbl.setWordWrap(True)
        stnbox.addWidget(lbl, 0, 0, 1, 3)
        self.stnm.create(stnbox, 1, self.loadRSL)
        self.loadRSL.create(stnbox, 2, self.stnm)
        self.createRSL.create(stnbox, 3)
        station.setLayout(stnbox)

        # Create and place the time period selection box inside the config box
        time = QGroupBox("Time Period selection")
        box.addWidget(time, 6, 0, 1, 2)
        timebox = QGridLayout()
        # Usage info to users
        lbl = QLabel("The Wyoming interface only allows downloading a month " +
                     "of data at a time so begin and end year and month must" +
                     " be the same.")
        lbl.setWordWrap(True)
        timebox.addWidget(lbl, 0, 0, 1, 3)
        self.btime.create(timebox, 1)
        self.etime.create(timebox, 2)
        self.now.create(timebox, 3)
        time.setLayout(timebox)

        # Place the grid layout in the configration box
        editor.setLayout(box)

    def updateMode(self, text):
        """ Update the mode displayed in the GUI to show the value in text """
        self.mode.update(text)

    def updateFreq(self, text):
        """ Update the freq displayed in the GUI to show the value in text """
        self.freq.update(text)

    def updateType(self, text):
        """ Update the type displayed in the GUI to show the value in text """
        self.type.update(text)

    def updateStnm(self, text):
        """ Update the type displayed in the GUI to show the value in text """
        self.stnm.update(text)

    def updateBtime(self, text):
        """ Update the type displayed in the GUI to show the value in text """
        self.btime.update(text)

    def updateEtime(self, text):
        """ Update the type displayed in the GUI to show the value in text """
        self.etime.update(text)
        now = self.now.get_button()
        now.setText(self.now.get_default_label())
