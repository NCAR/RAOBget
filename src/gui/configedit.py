###############################################################################
# Code related to creating the configEditor section of the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re

from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QComboBox, \
     QLineEdit, QPushButton
from lib.messageHandler import printmsg
from gui.fileselector import FileSelector
# If want to print status messages, use printmsg(self.log, msg)


class GUIconfig():

    def createConfigEditor(self, widget, layout, log, raob):
        """ Lay out area where users can define metadata specifying which
        RAOBs to download """

        self.raob = raob
        self.widget = widget
        self.log = log
        self.request = raob.request.get_request()

        # Create the configuration box in the root layout of the software
        editor = QGroupBox("Configuration")
        layout.addWidget(editor, 0, 0)

        # Create a grid layout for inside the configuration box
        box = QGridLayout()
        lbl = QLabel("Set mode to MTP or CATALOG to format and name " +
                     "files as required by these specific applications.")
        lbl.setWordWrap(True)
        box.addWidget(lbl, 0, 0, 1, 2)
        self.createMode(box, 1)  # Create and place the mode dropdown
        self.createFreq(box, 2)  # Create and place the frequency dropdown
        self.createType(box, 3)  # Create and place the type dropdown

        # Create and place the station list layout in the configuration box
        station = QGroupBox("Station selection")
        box.addWidget(station, 4, 0, 1, 2)
        stnbox = QGridLayout()
        # Usage info to users
        lbl = QLabel("Enter a single station to download, interactively " +
                     "create a list of stations to download from a recent" +
                     " GEMPAK station list, or load an existing station list")
        lbl.setWordWrap(True)
        stnbox.addWidget(lbl, 0, 0, 1, 3)
        self.createStnm(stnbox, 1)
        self.createLoadStn(stnbox, 2)
        self.createCreateStnlist(stnbox, 3)
        station.setLayout(stnbox)

        # Create and place the time period selection box inside the config box
        time = QGroupBox("Time Period selection")
        box.addWidget(time, 5, 0, 1, 2)
        timebox = QGridLayout()
        # Usage info to users
        lbl = QLabel("The Wyoming interface only allows downloading a month " +
                     "of data at a time so begin and end year and month must" +
                     " be the same.")
        lbl.setWordWrap(True)
        timebox.addWidget(lbl, 0, 0, 1, 3)
        self.createBtime(timebox, 1)
        self.createEtime(timebox, 2)
        self.createNow(timebox, 3)
        time.setLayout(timebox)

        # Place the grid layout in the configration box
        editor.setLayout(box)

    def createMode(self, box, row):
        """ Create and place the mode dropdown """
        lbl = QLabel("Mode")
        box.addWidget(lbl, row, 0)
        comboBox = QComboBox()
        comboBox.addItem("Default")
        comboBox.addItem("MTP")
        comboBox.addItem("CATALOG")
        comboBox.activated[str].connect(self.setMode)
        comboBox.setToolTip('Select the mode to run in')
        box.addWidget(comboBox, row, 1)

    def setMode(self, text):
        """ Save the selected mode to the metadata dictionary """
        if text == "MTP":
            self.raob.request.set_mtp(True)
            printmsg(self.log, "Mode set to MTP")
        if text == "CATALOG":
            self.raob.request.set_catalog(True)
            printmsg(self.log, "Mode set to Catalog")

    def createFreq(self, box, row):
        """ Create and place the frequency dropdown """
        lbl = QLabel("Freq (hours)")
        box.addWidget(lbl, row, 0)
        comboBox = QComboBox()
        comboBox.addItem("3")
        comboBox.addItem("6")
        comboBox.addItem("12")
        comboBox.activated[str].connect(self.setFreq)
        comboBox.setToolTip('Set the frequency to attempt to download data.' +
                            ' Less frequent data will still be downloaded')
        box.addWidget(comboBox, row, 1)

    def setFreq(self, text):
        """ Save the selected reporting frequency to the metadata dictionary"""
        self.raob.request.set_freq(text)
        printmsg(self.log, "Freq set to " + text)

    def createType(self, box, row):
        """ Create and place the type dropdown """
        lbl = QLabel("Data Format")
        box.addWidget(lbl, row, 0)
        comboBox = QComboBox()
        comboBox.addItem("TEXT:LIST")
        comboBox.addItem("GIF:SKEWT")
        comboBox.activated[str].connect(self.setType)
        comboBox.setToolTip('Choose to either download data in text format,' +
                            ' or download SkewT plots as gif images.')
        box.addWidget(comboBox, row, 1)

    def setType(self, text):
        """ Save the selected type to the metadata dictionary"""
        self.raob.request.set_type(text)
        printmsg(self.log, "RAOB type set to " + text)

    def createLoadStn(self, box, row):
        """ Create the Load station list button """
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        load = QPushButton("Load station list")
        load.clicked.connect(self.loadStnlist)
        load.setToolTip('Load a list of stations from a file')
        box.addWidget(load, row, 1, 1, 2)

    def loadStnlist(self):
        """ Call dialog box to load a station list """

        # Call dialog box to select a raob station list (rsl) file
        # Once selected, code will loop through contents
        self.loader = FileSelector("rsl")
        self.raob.request.set_rsl(self.loader.get_file())
        if (self.raob.request.get_rsl() == ""):
            printmsg(self.log, "WARNING: Station list not loaded. Please " +
                               "select a station/station list.")
        else:
            printmsg(self.log, "Station list set to " +
                     self.raob.request.get_rsl())

    def createCreateStnlist(self, box, row):
        """ Create the Create station list button """
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        create = QPushButton("Create station list")
        create.clicked.connect(self.createStnlist)
        create.setToolTip('Create a list of stations for while to download ' +
                          'soundings')
        box.addWidget(create, row, 1, 1, 2)

    def createStnlist(self):
        """ Call dialog box to create a station list """
        printmsg(self.log, "Need to implement create a station list")

    def createStnm(self, box, row):
        """ Create the Stnm text input field """
        lbl = QLabel("Station ID")
        box.addWidget(lbl, row, 0)
        self.stnm = QLineEdit()
        self.stnm.setToolTip("Enter char or numeric id of station to " +
                             "download and click 'Set'")
        box.addWidget(self.stnm, row, 1)
        use = QPushButton("Set")
        use.clicked.connect(self.setStnm)
        box.addWidget(use, row, 2)

    def setStnm(self):
        """ Set the station to the value entered in the input field

        NEED TO ADD DATA VALIDATION HERE
        """
        textboxValue = self.stnm.text()
        self.raob.request.set_stnm(textboxValue)
        printmsg(self.log, "Station set to " + textboxValue)

        # Since just manually set a station, need to set rsl to '' or
        # any defined rsl file will override user station selection
        self.raob.request.set_rsl('')

    def createBtime(self, box, row):
        """ Create the begin time input field """
        lbl = QLabel("Begin time")
        box.addWidget(lbl, row, 0)
        self.btime = QLineEdit('yyyymmddhh')
        # Set the color of the suggested text to grey
        self.btime.setStyleSheet("color: grey")
        self.btime.setToolTip("Enter the beginning of the timerange to " +
                              "download (YYYYMMDDHH) and click 'Set'")
        box.addWidget(self.btime, row, 1)
        use = QPushButton("Set")
        use.clicked.connect(self.setBtime)
        box.addWidget(use, row, 2)

    def setBtime(self):
        """ Set the beginning of the time range to download """

        # Now that user has entered text, set the color of the text to black
        self.btime.setStyleSheet("color: black")
        textboxvalue = self.btime.text()

        # Validate entered data
        time = re.compile(r'[12][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-9][0-9]')
        if not time.match(textboxvalue):
            printmsg(self.log, "ERROR in entered begin time: " + textboxvalue +
                     ".  Entered time must be a 4-digit year followed by a " +
                     "2-digit month, a 2-digit day, and a 2-digit hour, e.g." +
                     "2019051012 for noon May 10th, 2019")
            printmsg(self.log, "Begin date/time not set. Please reenter and " +
                     "click 'Set'")
        else:
            # Parse entered date into year, month, day, hr and assign to
            # request metadata
            year = textboxvalue[0:4]
            self.raob.request.set_year(year)

            month = textboxvalue[4:6]
            self.raob.request.set_month(month)

            day = textboxvalue[6:8]
            hr = textboxvalue[8:10]
            self.raob.request.set_begin(day, hr)
            printmsg(self.log, "year set to " + year + ", month set to " +
                     month + ", begin (ddhh) set to " + day + hr)

    def createEtime(self, box, row):
        """ Create the end time input field """
        lbl = QLabel("End time")
        box.addWidget(lbl, row, 0)
        self.etime = QLineEdit('yyyymmddhh')
        # Set the color of the suggested text to grey
        self.etime.setStyleSheet("color: grey")
        self.etime.setToolTip("Enter the ending of the timerange to " +
                              "download (YYYYMMDDHH) and click 'Set'")
        box.addWidget(self.etime, row, 1)
        use = QPushButton("Set")
        use.clicked.connect(self.setEtime)
        box.addWidget(use, row, 2)

    def setEtime(self):
        """ Set the ending of the time range to download """

        # Now that user has entered text, set the color of the text to black
        self.btime.setStyleSheet("color: black")
        textboxvalue = self.etime.text()

        # Validate entered data
        time = re.compile(r'[12][0-9][0-9][0-9][0-1][0-9][0-3][0-9][0-9][0-9]')
        if not time.match(textboxvalue):
            printmsg(self.log, "ERROR in entered end time: " + textboxvalue +
                     ".  Entered time must be a 4-digit year followed by a " +
                     "2-digit month, a 2-digit day, and a 2-digit hour, e.g." +
                     "2019051012 for noon May 10th, 2019")
            printmsg(self.log, "Begin date/time not set. Please reenter and " +
                     "click 'Set'")
        else:
            # Site can only download one month at a time, so begin and end
            # year and month must be the same.
            year = textboxvalue[0:4]
            if self.request['year'] != year:
                printmsg(self.log, "Begin and end year and month must match" +
                         " Please reenter and click 'Set'")
                return()

            month = textboxvalue[4:6]
            if self.request['month'] != month:
                printmsg(self.log, "Begin and end year and month must match" +
                         " Please reenter and click 'Set'")
                return()

            # End date must be greater than begin date
            day = textboxvalue[6:8]
            hr = textboxvalue[8:10]
            if self.request['begin'] > str(day) + str(hr):
                printmsg(self.log, "End day/hr must be after begin day/hr" +
                         " Please reenter and click 'Set'")
                return()

            # Parse entered date into end day, hr and assign to
            # request metadata
            self.raob.request.set_end(day, hr)
            printmsg(self.log, "End (ddhh) set to " + day + hr)

    def createNow(self, box, row):
        """ Create a button to set time to now """
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        create = QPushButton("Return most recent RAOB")
        create.clicked.connect(self.Now)
        create.setToolTip('Set the time to download to now. Returns most ' +
                          'recent RAOB for selected station')
        box.addWidget(create, row, 1, 1, 2)

    def Now(self):
        self.raob.request.set_now(True)
        printmsg(self.log, "Time to retrieve set to now")
