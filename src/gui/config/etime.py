###############################################################################
# Methods to manipulate the end time metadata display in the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from lib.messageHandler import printmsg


class ETime():

    def __init__(self, request, log=""):
        """ The end time is displayed in a textbox (QLineEdit) """
        self.etime = QLineEdit('yyyymmddhh')
        self.log = log
        self.request = request
        self.requestMetadata = self.request.get_request()

    def create(self, box, row):
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
        use.clicked.connect(self.set)
        box.addWidget(use, row, 2)

    def set(self):
        """ Set the ending of the time range to download """

        # Now that user has entered text, set the color of the text to black
        self.etime.setStyleSheet("color: black")
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
            if self.requestMetadata['year'] != year:
                printmsg(self.log, "Begin and end year and month must match" +
                         " Please reenter and click 'Set'")
                return()

            month = textboxvalue[4:6]
            if self.requestMetadata['month'] != month:
                printmsg(self.log, "Begin and end year and month must match" +
                         " Please reenter and click 'Set'")
                return()

            # End date must be areater than begin date
            day = textboxvalue[6:8]
            hr = textboxvalue[8:10]
            if self.requestMetadata['begin'] > str(day) + str(hr):
                printmsg(self.log, "End day/hr must be after begin day/hr" +
                         " Please reenter and click 'Set'")
                return()

            # Parse entered date into end day, hr and assign to
            # request metadata
            self.request.set_end(day, hr)
            logging.info("End (ddhh) set to " + day + hr)

            # Since sucessfully set a begin date, ensure that now flag is false
            self.request.set_now(False)

    def update(self, text):
        """
        Update the etime displayed in the GUI

        Requires:
            The etime to be displayed
        """
        self.etime.setStyleSheet("color: black")
        self.etime.setText(text)
