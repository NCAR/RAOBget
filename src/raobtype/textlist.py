###############################################################################
# Code specific to retrieving TEXT:LIST formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os

import userlib.mtp
from lib.rwget import RAOBwget
# from lib.messageHandler import printmsg
# If want to print status messages, use printmsg(self.log, msg)


class RAOBtextlist():

    def __init__(self, log=""):

        self.log = log
        self.rwget = RAOBwget(log)

    def get_url(self, request):
        """
        Generate the request URL for a TEXT:LIST request
        """

        request.set_type("TEXT:LIST")
        url = self.rwget.get_url(request, self.log)

        return(url)

    def set_outfile(self, request):
        """
        Build output filename for TEXT:LIST file. If --mtp option is set will
        create a filename to meet mtp-specific requirements.

        Parameters:
            request: a RAOBrequest dictionary of request metadata
        """
        if request.get_mtp() is True:
            self.outfile = userlib.mtp.set_outfile(request)
        else:
            self.outfile = request.get_stnm() + request.get_year() + \
                request.get_month() + request.get_begin() + request.get_end() \
                + ".txt"

    def get_outfile(self):
        """
        Returns:
            self.outfile: the name of the file to which the received data
            should be saved
        """

        return(self.outfile)

    def retrieve(self, app, request, log=""):
        """
        Retrieves the requested data from the U Wyoming archive

        Parameters:
            request: A dictionary containing the metadata for the
                     request.

        Returns:
            outfile: The name of the retrieved file.
        """

        # Create output filename from request metadata
        self.set_outfile(request)
        outfile = self.get_outfile()

        # If in test mode, copy file from data dir to simulate download...
        if request.get_test() is True:
            if request.get_mtp() is True:
                os.system('cp data/726722019052812.ctrl 726722019052812.txt')
            else:
                os.system('cp data/7267220190528122812.ctrl ' +
                          '7267220190528122812.txt')

        # ...else download data
        else:
            # Create request URL from request metadata
            url = self.get_url(request)
            if app is not None:      # Force the GUI to redraw so log
                app.processEvents()  # messages, etc are displayed

            status = self.rwget.get_data(url, outfile)

            if request.get_mtp() is True and status:
                userlib.mtp.strip_html(request, outfile)

        return(status, outfile)
