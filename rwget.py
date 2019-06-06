###############################################################################
# Code specific to configuring and executing retrieval of data/imagery from the
# University of Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import urllib.request
import wget

from region import RAOBregion
from type import RAOBtype


class RAOBwget:

    def __init__(self):

        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def get_url(self, request):

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

    def get_data(self, url, outfile):

        # Check if filename already exists. wget will fail if it does.
        if os.path.isfile(outfile):
            print("Already downloaded file with name " + outfile +
                  ". Remove this file to re-download.")

            return(False)  # Did not download new data

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
            print("\nRetrieved ", outfile)

            return(True)  # Downloaded new data
