###############################################################################
# Code to display a GUI to select a file
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from lib.raobroot import getrootdir
from lib.filemanager import FileManager


class FileSelector(QMainWindow):

    def __init__(self, filetype):
        """ Set the initial GUI window size here """
        # The QMainWindow class provides a main application window
        super().__init__()

        rootdir = getrootdir() + "/config"
        if (filetype == "config"):
            filefilter = "config files (*.yml, *.YML)"
        elif (filetype == "rsl"):
            filefilter = "RSL Files (*.rsl, *.RSL)"
        else:
            print("Software engineer goofed - called filetype that hasn't" +
                  " been coded. Contact SE for code changes.")

        # Create the GUI
        filename = self.initDialog(rootdir, filefilter)

        filemgr = FileManager()
        if (filetype == "config"):
            filemgr.readYMLfile(filename)
        elif (filetype == "rsl"):
            filemgr.readRSLfile(filename)
        else:
            print("Software engineer goofed - called filetype that hasn't" +
                  " been coded. Contact SE for code changes.")

    def initDialog(self, rootdir, filefilter):
        """ Instantiate the file dialog """
        # When use native dialogs, get an error that Class
        # FIFinderSyncExtensionHost is implemented twice. Googling seems to
        # indicate this is an incompatability with the latest Mac OS's, so for
        # now disable Native Dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # getOpenFileName returns the complete path to the selected file, and a
        # string containing the filter used. Ignore the filter return.
        filename, _ = QFileDialog.getOpenFileName(self, "Select a file",
                                                  rootdir, filefilter,
                                                  options=options)

        return(filename)
