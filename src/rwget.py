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

from util.region import RAOBregion
from raobtype.raobtype import RAOBtype


class RAOBwget:

    def __init__(self):
        """
        Initialize instances of the region dictionary and data/imagery type
        dictionary. These are used to convert the user-supplied commandline
        arguments to the specific format needed in the URL
        """

        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def get_url(self, request):
        """
        Create the URL string from the request metadata that will be used
        to retrieve the data from the uwyo archive

        Parameters:
            request: a RAOBrequest dictionary of request metadata

        Returns:
            url: the generated URL
        """

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
        """
        Send the generated URL to the uwyo website and receive back a file
        containing the requested data or imagery.

        Parameters:
            url: the url containing the request
            outfile: the name of the file to which the received data should be
                     saved

        Returns:
            boolean: True/False success indicator

        """

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
            urllib.request.urlretrieve(url, outfile)

            # Test if text/html file contains good data
            if "gif" not in outfile:
                out = open(outfile)
                line = out.readline()
                while line != '':
                    if "Can't get" in line:
                        print('ERROR: Website says "' + line.rstrip() + '"')
                        os.system('rm ' + outfile)
                        out.close()
                        return(False)
                    elif 'Sorry, unable to generate' in line:
                        print(line.rstrip() + ". Retrieved file contains" +
                              " error message - gif was got generated.")
                        os.system('rm ' + outfile)
                        out.close()
                        return(False)
                    else:
                        line = out.readline()
                out.close()

            print("\nRetrieved ", outfile)

            return(True)  # Downloaded new data
