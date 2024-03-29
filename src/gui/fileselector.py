###############################################################################
# Code to display a GUI to select a file
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
import os

from PyQt5.QtWidgets import QMainWindow, QFileDialog


class FileSelector(QMainWindow):

    def __init__(self, filetype):
        """ Set the initial GUI window size here """
        # The QMainWindow class provides a main application window
        super().__init__()

        rootdir = os.getcwd()

        # Set the file type filter
        config = re.compile("^.*Config")
        rsl = re.compile("^.*Rsl")
        dir = re.compile("dir")

        if config.match(filetype):
            filefilter = "config files (*.yml, *.YML)"
        elif rsl.match(filetype):
            filefilter = "RSL Files (*.rsl, *.RSL)"
        elif not dir.match(filetype):
            print("Software engineer goofed - called filetype that hasn't" +
                  " been coded. Contact SE for code changes.")

        # Create the GUI
        load = re.compile("load")
        save = re.compile("save")
        if load.match(filetype):
            self.filename = self.initDialog(rootdir, filefilter)
        elif save.match(filetype):
            self.filename = self.initSaveAs(rootdir, filefilter)
        elif dir.match(filetype):
            self.filename = self.initGetDir(rootdir)

    def initSaveAs(self, rootdir, filefilter):
        """ Instantiate the file dialog to select a file to save to """
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
                                                  os.path.join(rootdir,
                                                               "config"),
                                                  filefilter,
                                                  options=options)

        if filename == "":
            # When user hits Cancel, QFileDialog returns an empty string
            return(filename)
        else:
            # QFileDialog returns the complete path to the file. We want to
            # only save the relative path in the request, starting with
            # config so remove the value of rootdir from the filename.
            return(os.path.relpath(filename, start=rootdir))

    def initDialog(self, rootdir, filefilter):
        """ Instantiate the file dialog to select a file to load """
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
                                                  os.path.join(rootdir,
                                                               "config"),
                                                  filefilter,
                                                  options=options)

        if filename == "":
            # When user hits Cancel, QFileDialog returns an empty string
            return(filename)
        else:
            # QFileDialog returns the complete path to the file. We want to
            # only save the relative path in the request, starting with
            # config so remove the value of rootdir from the filename.
            return(os.path.relpath(filename, start=rootdir))

    def initGetDir(self, rootdir):
        """ Instantiate the file dialog to select a dir """
        # When use native dialogs, get an error that Class
        # FIFinderSyncExtensionHost is implemented twice. Googling seems to
        # indicate this is an incompatability with the latest Mac OS's, so for
        # now disable Native Dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        dir = QFileDialog.getExistingDirectory(self,
                                               "Select a directory",
                                               os.path.join(rootdir),
                                               options=options)

        if dir == "":
            # When user hits Cancel, QFileDialog returns an empty string
            return(dir)
        else:
            # QFileDialog returns the complete path to the file. We want to
            # only save the relative path in the request, starting with
            # config so remove the value of rootdir from the filename.
            return(dir)

    def get_file(self):
        return(self.filename)
