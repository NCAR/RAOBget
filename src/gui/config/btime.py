###############################################################################
# Methods to manipulate the begin time metadata display in the GUI
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from lib.messageHandler import printmsg


class BTime():

    def __init__(self, request, log=""):
        """ The begin time is displayed in a textbox (QLineEdit) """
        self.btime = QLineEdit('yyyymmddhh')
        self.log = log
        self.request = request

    def create(self, box, row):
        """ Create the begin time input field """
        lbl = QLabel("Begin time")
        box.addWidget(lbl, row, 0)
        # Set the color of the suggested text to grey
        self.btime.setStyleSheet("color: grey")
        self.btime.setToolTip("Enter the beginning of the timerange to " +
                              "download (YYYYMMDDHH) and click 'Set'")
        box.addWidget(self.btime, row, 1)
        use = QPushButton("Set")
        use.clicked.connect(self.set)
        box.addWidget(use, row, 2)

    def set(self):
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
            self.request.set_year(year)

            month = textboxvalue[4:6]
            self.request.set_month(month)

            day = textboxvalue[6:8]
            hr = textboxvalue[8:10]
            self.request.set_begin(day, hr)
            logging.info("year set to " + year + ", month set to " +
                         month + ", begin (ddhh) set to " + day + hr)

    def update(self, text):
        """
        Update the btime displayed in the GUI

        Requires:
            The btime to be displayed
        """
        self.btime.setStyleSheet("color: black")
        self.btime.setText(text)
