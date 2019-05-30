###############################################################################
# Script to download RAOBS from the University of Wyoming Radiosonde Archive
# by building URLs like:
#   "http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&
#       YEAR=2019&MONTH=05&FROM=2812&TO=2812&STNM=72672"
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import wget

from region import RAOBregion

RAOBrequest = {  # Default station used in testing. Will be overwritten with
                 # requested station in normal usage.
        'region': 'North America',    # Region identifier
        'type': 'TEXT%3ALIST',
        'year': "2019",
        'month': "05",
        'from': "2812",
        'to': "2812",
        'stnm': "72672",
        }


class RAOBget:

    def __init__(self):

        self.request = RAOBrequest  # dictionary to hold all URL components
        self.region = RAOBregion    # Instance of region dictionary

    def set_outfile_textlist(self):

        # Build output filename
        self.outfile = self.request['stnm'] + self.request['year'] + \
                self.request['month'] + self.request['from'] + ".txt"

    def get_outfile_textlist(self):
        return(self.outfile)

    def retrieve_textlist(self):

        url = "http://weather.uwyo.edu/cgi-bin/sounding?region="
        url += self.region[self.request['region']]
        url += "&TYPE=" + self.request['type']
        url += "&YEAR=" + self.request['year']
        url += "&MONTH=" + self.request['month']
        url += "&FROM=" + self.request['from']
        url += "&TO=" + self.request['to']
        url += "&STNM=" + self.request['stnm']
        print(url)

        # Check if filename already exists. wget will fail if it does.
        # Since they don't change, only download new ones.
        self.set_outfile_textlist()
        outfile = self.get_outfile_textlist()

        if not os.path.isfile(outfile):
            filename = wget.download(url, outfile)
            print("\n", filename)

        return(self.get_outfile_textlist())


if __name__ == "__main__":

    raob = RAOBget()
    raob.retrieve_textlist()
