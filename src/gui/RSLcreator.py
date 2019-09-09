###############################################################################
# Code to display a GUI to create a file with a list of stations to download
# RAOBs for (an RSL file).
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QGridLayout, \
                            QListWidget, QPushButton
from lib.raobroot import getrootdir
from lib.stationlist import RAOBstation_list
from gui.fileselector import FileSelector


class RSLWidget(QWidget):
    # Need a signal to send back to RSLCreator when RSLWidget is closed to tell
    # it to close the parent window.
    signal = pyqtSignal()

    def __init__(self, station_list):
        """ Initialize the RSLCreator widget inside the creator main window """
        super().__init__()

        layout = QGridLayout(self)

        # Create a QListWidget to hold the source station list
        self.textbox = QListWidget(self)
        self.textbox.show()
        self.textbox.setDragEnabled(True)
        layout.addWidget(self.textbox, 0, 0, 4, 1)

        # If the user cancelled out of selecting a source station list, or
        # requested a non-existent one, capture the error here and warn them.
        # Otherwise, display stations in textbox
        error = re.compile("^ERROR:")
        if isinstance(station_list, str) and error.match(station_list):
            self.textbox.addItem(station_list)
        else:
            for stn in station_list:
                if stn['id'] == "        ":  # Use number instead of missing id
                    stn['id'] = stn['number']
                self.textbox.addItem(stn['id'])

        # Add another window to display additional metadata to help user
        # select stations, or have mouseover show metadata. Ask Julie what she
        # needs to make selection.
        # NOT YET IMPLEMENTED

        # Create a QListWidget to hold the selected stations to be saved to
        # the RSL file.
        self.rslbox = QListWidget(self)
        self.rslbox.setAcceptDrops(True)
        layout.addWidget(self.rslbox, 0, 2, 4, 1)

        # Add arrows that move stuff back and forth between boxes
        select = QPushButton('->', self)
        layout.addWidget(select, 0, 1)
        select.clicked.connect(self.select_station)

        remove = QPushButton('<-', self)
        layout.addWidget(remove, 1, 1)
        remove.clicked.connect(self.remove_station)

        # Add a Save button to save RSL
        save = QPushButton('Save', self)
        layout.addWidget(save, 3, 1)
        save.clicked.connect(self.saveRSL)

    def select_station(self, item):  # item is a pointer to a QListWidgetItem
        """ Transfer a station from the master list to the RSL list """
        print("Not yet implemented")

    def remove_station(self):
        print("Not yet implemented")
        # self.rslbox.takeItem(self.rslbox.currentRow()))

    def saveRSL(self):
        """ Save the list of values out of the GUI (rslbox) """

        # Call dialog box to select the file to save the RSL list to
        self.loader = FileSelector("saveRsl")
        self.outfile = self.loader.get_file()

        # Write the RSL list to the open file
        fp = open(self.outfile, 'w')
        for item in range(self.rslbox.count()):
            fp.write(str(self.rslbox.item(item).data(0)).strip() + "\n")
        fp.close()

        # After save, if successful, set RSL to new station list file
        print("Set station list to RSL file " + self.get_rsl_filename() +
              " not yet implemented. Use 'Load station list' to load " +
              "newly created RSL file.")

        # close window
        self.signal.emit()
        self.close()

    def get_rsl_filename(self):
        return(self.outfile)


class RSLCreator(QMainWindow):

    def __init__(self):
        """ Set the initial GUI window size here and initialize the UI """
        super().__init__()

        self.title = 'RSL Creator'
        self.left = 200
        self.top = 100
        self.width = 500
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Open a dialog to let the user select the source list of stations to
        # choose from when creating their RSL file.
        rootdir = getrootdir() + "/config"
        filefilter = "station list files (*.tbl, *.TBL)"
        # Move this to a menu File-> Load option and use default because
        # the list will likely only rarely change.
        # NOT YET IMPLEMENTED
        self.filename = self.initDialog(rootdir, filefilter)

        # Read in the contents of the source list of stations.
        stationList = RAOBstation_list()
        self.station_list = stationList.read(self.filename)

        # Create the GUI that will allow selecting stations from the source
        # list to be included in the RSL file.
        self.win = RSLWidget(self.station_list)
        self.setCentralWidget(self.win)
        self.win.signal.connect(self.close_win)
        self.win.show()

    def close_win(self):
        self.close()

    def get_rsl_filename(self):
        return(self.win.get_rsl_filename)

    def initDialog(self, rootdir, filefilter):
        """
        Instantiate the file dialog used to select the source station list
        """
        # When use native dialogs, get an error that Class
        # FIFinderSyncExtensionHost is implemented twice. Googling seems to
        # indicate this is an incompatability with the latest Mac OS's, so for
        # now disable Native Dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # getOpenFileName returns the complete path to the selected file, and a
        # string containing the filter used. Ignore the filter return.
        # If user selects cancel, returns None.
        filename, _ = QFileDialog.getOpenFileName(self, "Select a master " +
                                                  "RAOB station list file",
                                                  rootdir, filefilter,
                                                  options=options)

        return(filename)
