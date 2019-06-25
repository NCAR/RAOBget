###############################################################################
# Code related to creating the configEditor section of the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QComboBox, \
     QLineEdit, QPushButton


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
        self.createMode(box, 0)  # Create and place the mode dropdown
        self.createFreq(box, 1)  # Create and place the frequency dropdown
        self.createType(box, 2)  # Create and place the type dropdown

        # Create and place the station list layout in the configuration box
        station = QGroupBox("Station selection")
        box.addWidget(station, 3, 0, 1, 2)
        stnbox = QGridLayout()
        self.createStnm(stnbox, 0)
        self.createLoadStn(stnbox, 1)
        self.createCreateStnlist(stnbox, 2)
        station.setLayout(stnbox)

        # Create and place the time period selection box inside the config box
        time = QGroupBox("Time Period selection")
        box.addWidget(time, 4, 0, 1, 2)

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
            self.widget.setMessage(self.log, "Mode set to MTP")
        if text == "GUI":
            self.raob.request.set_catalog(True)
            self.widget.setMessage(self.log, "Mode set to Catalog")

    def createFreq(self, box, row):
        """ Create and place the frequency dropdown """
        lbl = QLabel("Freq (hours)")
        box.addWidget(lbl, row, 0)
        comboBox = QComboBox()
        comboBox.addItem("3")
        comboBox.addItem("6")
        comboBox.addItem("12")
        comboBox.activated[str].connect(self.setFreq)
        box.addWidget(comboBox, row, 1)

    def setFreq(self, text):
        """ Save the selected reporting frequency to the metadata dictionary"""
        self.raob.request.set_freq(text)
        self.widget.setMessage(self.log, "Freq set to " + text)

    def createType(self, box, row):
        """ Create and place the type dropdown """
        lbl = QLabel("Data Format")
        box.addWidget(lbl, row, 0)
        comboBox = QComboBox()
        comboBox.addItem("TEXT:LIST")
        comboBox.addItem("GIF:SKEWT")
        comboBox.activated[str].connect(self.setType)
        box.addWidget(comboBox, row, 1)

    def setType(self, text):
        """ Save the selected type to the metadata dictionary"""
        self.raob.request.set_type(text)
        self.widget.setMessage(self.log, "RAOB type set to " + text)

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
        print("Load a station list")

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
        print("Create a station list")

    def createStnm(self, box, row):
        """ Create the Stnm text input field """
        lbl = QLabel("Station ID")
        box.addWidget(lbl, row, 0)
        self.stnm = QLineEdit()
        self.stnm.setToolTip("Enter char or numeric id of station to download")
        box.addWidget(self.stnm, row, 1)
        use = QPushButton("Use")
        use.clicked.connect(self.setStnm)
        box.addWidget(use, row, 2)

    def setStnm(self):
        textboxValue = self.stnm.text()
        self.raob.request.set_stnm(textboxValue)
        self.widget.setMessage(self.log, "Station set to " + textboxValue)
