###############################################################################
# Code specific to retrieving TEXT:LIST formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import mtp

from rwget import RAOBwget


class RAOBtextlist:

    def __init__(self):

        self.rwget = RAOBwget()

    def get_url_textlist(self, request):

        # In MTP mode, confirm begin and end are equal so will only get one
        # RAOB per file.
        if request['mtp'] is True:
            mtp.test_dates(request)

        url = self.rwget.get_url(request)

        return(url)

    def set_outfile_textlist(self, request):

        # Build output filename
        if request['mtp'] is True:
            self.outfile = mtp.set_outfile(request)
        else:
            self.outfile = request['stnm'] + request['year'] + \
                request['month'] + request['begin'] + request['end'] + \
                ".txt"

    def get_outfile_textlist(self):

        return(self.outfile)

    def retrieve(self, request):

        # Create request URL from request metadata
        url = self.get_url_textlist(request)

        # Create output filename from request metadata
        self.set_outfile_textlist(request)
        outfile = self.get_outfile_textlist()

        # If in test mode, copy file from data dir to simulate download...
        if request['test'] is True:
            if request['mtp'] is True:
                os.system('cp data/726722019052812.ctrl 726722019052812.txt')
            else:
                os.system('cp data/7267220190528122812.ctrl ' +
                          '7267220190528122812.txt')

        # ...else download data
        else:

            status = self.rwget.get_data(url, outfile)

            if request['mtp'] is True and status:
                mtp.strip_html(request, self.outfile)

        return(self.get_outfile_textlist())
