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
import sys
import argparse

from textlist import RAOBtextlist

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

    def get_request(self):

        return(self.request)

    def retrieve(self):

        if (self.request['raobtype'] == 'TEXT:LIST'):
            textlist = RAOBtextlist()
            textlist.retrieve_textlist(self.request)
        else:
            print('RAOB type '+self.request['raobtype']+' not implemented yet')
            exit(1)


def parse():
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
    args = parser.parse_args()

    return(args)


def main(args):

    # Parse command line arguments
    args = parse()

    raob = RAOBget()

    # Set requested station to values requested via command line
    raob.set_region(args)
    raob.set_type(args)
    raob.set_year(args)
    raob.set_month(args)
    raob.set_begin(args)
    raob.set_end(args)
    raob.set_stnm(args)

    # Retrieve requested data/imagery
    raob.retrieve()


if __name__ == "__main__":

    main(sys.argv)
