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
import urllib.request
import mtp

from region import RAOBregion
from type import RAOBtype


class RAOBtextlist:

    def __init__(self):

        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def get_url_textlist(self, request):

        # In MTP mode, confirm begin and end are equal so will only get one
        # RAOB per file.
        if request['mtp'] is True:
            mtp.test_dates(request)

        url = "http://weather.uwyo.edu/cgi-bin/sounding?"
        if (request['region'] != ''):
            url += "region=" + self.region[request['region']]
        url += "&TYPE=" + self.type[request['raobtype']]
        url += "&YEAR=" + request['year']
        url += "&MONTH=" + request['month']
        url += "&FROM=" + request['begin']
        url += "&TO=" + request['end']
        url += "&STNM=" + request['stnm']
        # print(url)

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

    def retrieve_textlist(self, request):

        url = self.get_url_textlist(request)

        # Check if filename already exists. wget will fail if it does.
        # Since they don't change (with below caveats),  only download new
        # ones.
        self.set_outfile_textlist(request)
        outfile = self.get_outfile_textlist()

        # If in test mode, copy file from data dir to simulate download
        if request['test'] is True:
            os.system('cp data/726722019052812.txt .')
        else:

            if os.path.isfile(outfile):
                print("Already downloaded file with name " + outfile +
                      ". Remove this file to re-download.")
            else:
                # Check if online - if not, exit gracefully
                try:
                    urllib.request.urlopen(url)
                except Exception as e:
                    print("Can't connect to weather.uwyo.edu. Use option " +
                          "--test for testing with offline sample data files.")
                    print(str(e))
                    exit(1)

                # Get requested URL.
                wget.download(url, outfile)
                if request['mtp'] is True:
                    mtp.strip_html(request, self.outfile)
                print("\nRetrieved ", self.outfile)

        return(self.get_outfile_textlist())
