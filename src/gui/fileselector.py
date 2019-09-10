###############################################################################
# Code to display a GUI to select a file
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from lib.raobroot import getrootdir


class FileSelector(QMainWindow):

    def __init__(self, filetype):
        """ Set the initial GUI window size here """
        # The QMainWindow class provides a main application window
        super().__init__()

        rootdir = getrootdir() + "/config"

        # Set the file type filter
        config = re.compile("^.*Config")
        rsl = re.compile("^.*Rsl")

        if config.match(filetype):
            filefilter = "config files (*.yml, *.YML)"
        elif rsl.match(filetype):
            filefilter = "RSL Files (*.rsl, *.RSL)"
        else:
            print("Software engineer goofed - called filetype that hasn't" +
                  " been coded. Contact SE for code changes.")

        # Create the GUI
        load = re.compile("load")
        save = re.compile("save")
        if load.match(filetype):
            self.filename = self.initDialog(rootdir, filefilter)
        elif save.match(filetype):
            self.filename = self.initSaveAs(rootdir, filefilter)

    def initSaveAs(self, rootdir, filefilter):
        # When use native dialogs, get an error that Class
        # FIFinderSyncExtensionHost is implemented twice. Googling seems to
        # indicate this is an incompatability with the latest Mac OS's, so for
        # now disable Native Dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # getSaveFileName returns the complete path to the selected file, and a
        # string containing the filter used. Ignore the filter return.
        # If user selects cancel, returns None.
        filename, _ = QFileDialog.getSaveFileName(self, "Select a file",
                                                  rootdir, filefilter,
                                                  options=options)

        # QFileDialog returns the complete path to the file. We want to only
        # save the relative path in the request, starting with config so
        # remove the value of getrootdir() from the filename
        return(filename.replace(getrootdir() + "/", ''))

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
        # If user selects cancel, returns None.
        filename, _ = QFileDialog.getOpenFileName(self, "Select a file",
                                                  rootdir, filefilter,
                                                  options=options)

        # QFileDialog returns the complete path to the file. We want to only
        # save the relative path in the request, starting with config so
        # remove the value of getrootdir() from the filename
        return(filename.replace(getrootdir() + "/", ''))

    def get_file(self):
        return(self.filename)
