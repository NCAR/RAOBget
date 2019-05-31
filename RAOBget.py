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
import sys
import wget
import argparse

from region import RAOBregion
from type import RAOBtype

RAOBrequest = {  # Default station used in testing. Will be overwritten with
                 # requested station in normal usage.
        'region': '',    # Region identifier
        'raobtype': '',  # Retreived data/imagery type indentifier
        'year': "",      # Year to retrieve data for
        'month': "",     # Month to retrieve data for
        'begin': "",     # Begin day/hour (ddhh) to retrieve data for
        'end': "",       # End day/hour (ddhh) to retrieve data for
        'stnm': "",      # Station number to retrieve data for
        }


class RAOBget:

    def __init__(self):

        self.request = RAOBrequest  # dictionary to hold all URL components
        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def set_region(self, args):
        self.request['region'] = args.region

    def set_type(self, args):
        self.request['raobtype'] = args.raobtype

    def set_year(self, args):
        self.request['year'] = args.year

    def set_month(self, args):
        self.request['month'] = args.month

    def set_begin(self, args):
        self.request['begin'] = args.bday+args.bhr

    def set_end(self, args):
        self.request['end'] = args.eday+args.ehr

    def set_stnm(self, args):
        self.request['stnm'] = args.stnm

    def set_outfile_textlist(self):

        # Build output filename
        self.outfile = self.request['stnm'] + self.request['year'] + \
                self.request['month'] + self.request['begin'] + ".txt"

    def get_outfile_textlist(self):
        return(self.outfile)

    def get_url_textlist(self):

        url = "http://weather.uwyo.edu/cgi-bin/sounding?"
        url += "region=" + self.region[self.request['region']]
        url += "&TYPE=" + self.type[self.request['raobtype']]
        url += "&YEAR=" + self.request['year']
        url += "&MONTH=" + self.request['month']
        url += "&FROM=" + self.request['begin']
        url += "&TO=" + self.request['end']
        url += "&STNM=" + self.request['stnm']
        print(url)

        return(url)

    def retrieve_textlist(self):

        url = self.get_url_textlist()

        # Check if filename already exists. wget will fail if it does.
        # Since they don't change, only download new ones.
        self.set_outfile_textlist()
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


def main(args):

    # Parse command line arguments
    parser = argparse.ArgumentParser(
            description="Script to download various formats of RAOB " +
                        "data/imagery from the University of Wyoming " +
                        "Radiosonde Archive")
    parser.add_argument('--region', type=str, default='North America',
                        help='Region for which to download sonde info. ' +
                        'Defaults to North America.')
    parser.add_argument('--raobtype', type=str, default='TEXT:LIST',
                        help='Data/image type to request - ' +
                        'TEXT:LIST or GIF:SKEWT')
    parser.add_argument('--year', type=str, default='2019',
                        help='Year to request data ')
    parser.add_argument('--month', type=str, default='05',
                        help='Month to request data ')
    parser.add_argument('--bday', type=str, default='28',
                        help='Begin day (dd) to request data UTC')
    parser.add_argument('--bhr', type=str, default='12',
                        choices=['00', '12'],
                        help='Begin hour (hh) to request data UTC')
    parser.add_argument('--eday', type=str, default='28',
                        help='End day (dd) to request data UTC')
    parser.add_argument('--ehr', type=str, default='12',
                        choices=['00', '12'],
                        help='End hour (hh) to request data UTC')
    parser.add_argument('--stnm', type=str, default='72672',
                        help='Station number for which to request data ')
    (args) = parser.parse_args()

    raob = RAOBget()

    # Set requested station to values requested via command line
    raob.set_region(args)
    raob.set_type(args)
    raob.set_year(args)
    raob.set_month(args)
    raob.set_begin(args)
    raob.set_end(args)
    raob.set_stnm(args)

    raob.retrieve_textlist()


if __name__ == "__main__":

    main(sys.argv)
