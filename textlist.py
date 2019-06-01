###############################################################################
# Code specific to retrieving TEXT:LIST formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import wget

from region import RAOBregion
from type import RAOBtype


class RAOBtextlist:

    def __init__(self):

        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def get_url_textlist(self, request):

        url = "http://weather.uwyo.edu/cgi-bin/sounding?"
        url += "region=" + self.region[request['region']]
        url += "&TYPE=" + self.type[request['raobtype']]
        url += "&YEAR=" + request['year']
        url += "&MONTH=" + request['month']
        url += "&FROM=" + request['begin']
        url += "&TO=" + request['end']
        url += "&STNM=" + request['stnm']
        print(url)

        return(url)

    def set_outfile_textlist(self, request):

        # Build output filename
        self.outfile = request['stnm'] + request['year'] + \
                request['month'] + request['begin'] + ".txt"

    def get_outfile_textlist(self):

        return(self.outfile)

    def retrieve_textlist(self, request):

        url = self.get_url_textlist(request)

        # Check if filename already exists. wget will fail if it does.
        # Since they don't change, only download new ones.
        self.set_outfile_textlist(request)
        outfile = self.get_outfile_textlist()

        if not os.path.isfile(outfile):
            # Check if online - if not, exit gracefully
            # TBD
            # if (offline):
            #    system("cp data/726722019052812.ctrl 726722019052812.txt")

            # Get requested URL. I can't recall what wget returns
            # as filename.
            filename = wget.download(url, outfile)
            print("\n", filename)

        return(self.get_outfile_textlist())
