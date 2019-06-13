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

from datetime import datetime
from raobtype.textlist import RAOBtextlist
from raobtype.gifskewt import RAOBgifskewt


class RAOBget():

    def __init__(self):
        """
        Initialize a RAOBrequest dictionary to hold request metadata
        """

        RAOBrequest = {  # Default station used in testing. Will be overwritten
                         # with requested station in normal usage.
            'region': '',    # Region identifier
            'raobtype': '',  # Retreived data/imagery type indentifier
            'year': "",      # Year to retrieve data for
            'month': "",     # Month to retrieve data for
            'begin': "",     # Begin day/hour (ddhh) to retrieve data for
            'end': "",       # End day/hour (ddhh) to retrieve data for
            'stnm': "",      # Station number to retrieve data for
            'rsl': "",       # Name of file containing list of stations to
                             # retrieve data for
            'test': False,   # Run in test/dev mode
            'mtp': False,    # MTP-specific processing
            'catalog': False,  # catalog-specific processing
            'now': False,    # Set requested date/time to current time,
                             # i.e. retrieve current RAOB.
        }

        self.request = RAOBrequest  # dictionary to hold all URL components

    def set_region(self, args):
        self.request['region'] = args.region

    def set_type(self, args):
        self.request['raobtype'] = args.raobtype

    def set_year(self, year):
        self.request['year'] = year

    def set_month(self, month):
        self.request['month'] = month

    def set_begin(self, bday, bhr):
        self.request['begin'] = bday+bhr

    def set_end(self, eday, ehr):
        self.request['end'] = eday+ehr

    def set_test(self, args):
        self.request['test'] = args.test

    def set_mtp(self, args):
        self.request['mtp'] = args.mtp

    def set_catalog(self, args):
        self.request['catalog'] = args.catalog

    def set_now(self, args):
        self.request['now'] = args.now

    def set_stnm(self, args):
        self.request['stnm'] = args.stnm

    def set_prov(self, args):  # Set provenance of RAOB to retrieve
        """ Set request from all the metadata specificed on the command line.
        Calls individual set_ methods for each argument.
        """
        self.set_region(args)
        self.set_type(args)
        self.set_year(args.year)
        self.set_month(args.month)
        self.set_begin(args.bday, args.bhr)
        self.set_end(args.eday, args.ehr)
        self.set_test(args)
        self.set_mtp(args)
        self.set_catalog(args)
        self.set_now(args)

    def read_rsl(self, args):  # read RAOB Station List (RSL) file
        """ Read a optional provided list of raob stations to request data for
        """
        rsl = open(args.rsl)
        stnlist = rsl.readlines()
        rsl.close()
        return([line.rstrip() for line in stnlist])

    def get_request(self):
        """ Return request metadata dictionary """

        return(self.request)

    def set_time_now(self):
        """ Set request time to most recent 12 hour (UTC) RAOB """
        time = datetime.utcnow()
        self.set_year(str(time.year))
        self.set_month('{:02d}'.format(time.month))
        if time.hour > 0 and time.hour <= 12:
            hour = 0
        else:
            hour = 12

        self.set_begin('{:02d}'.format(time.day), '{:02d}'.format(hour))
        self.set_end('{:02d}'.format(time.day), '{:02d}'.format(hour))

    def retrieve(self):
        """ Retrieve data for requested RAOB type """

        # If option --now is set, set year, month, begin, and end to current
        # date/time
        if self.request['now'] is True:
            self.set_time_now()

        if (self.request['raobtype'] == 'TEXT:LIST'):
            textlist = RAOBtextlist()
            textlist.retrieve(self.request)
        elif (self.request['raobtype'] == 'GIF:SKEWT'):
            gifskewt = RAOBgifskewt()
            gifskewt.retrieve(self.request)
        else:
            print('RAOB type '+self.request['raobtype']+' not implemented yet')
            exit(1)


def parse():
    """ Define command line arguments which can be provided"""
    parser = argparse.ArgumentParser(
            description="Script to download various formats of RAOB " +
                        "data/imagery from the University of Wyoming " +
                        "Radiosonde Archive")
    parser.add_argument('--region', type=str, default='',
                        help='Region for which to download sonde info. ' +
                        'Not required. Download will fail if region does not' +
                        'match station location. Defaults to not defined.')
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
                        help='Station number for which to request data...')
    parser.add_argument('--rsl', type=str, default='',
                        help='RSL file from which to read list of stations' +
                        'to request')
    parser.add_argument('--test', action="store_true",
                        help='Run in testing mode using local sample data ' +
                        'file 726722019052812.txt. Used for offline dev')
    parser.add_argument('--mtp', action="store_true",
                        help='Download one RAOB per file, reformat HTML, ' +
                        'and rename file to match MTP requirements. In mtp ' +
                        'mode begin and end times must be the same.')
    parser.add_argument('--catalog', action="store_true",
                        help='Download gif images for catalog use. Rename ' +
                        'to match catalog filename requirements.')
    parser.add_argument('--now', action="store_true",
                        help='Set requested date/time to current date/time')
    args = parser.parse_args()

    return(args)


def main(args):

    # Parse command line arguments
    args = parse()

    # Instantiate RAOB class
    raob = RAOBget()

    # Set requested region, type, and date to values requested via command line
    raob.set_prov(args)

    # Did user request a single station via --stnm, or a list of stations
    # via an RSL file
    if (args.rsl == ''):
        raob.set_stnm(args)
        raob.retrieve()  # Retrieve requested data/imagery for a single station
    else:
        stnlist = raob.read_rsl(args)
        for stn in stnlist:  # Loop through a list of stations
            args.stnm = stn
            raob.set_stnm(args)
            raob.retrieve()


if __name__ == "__main__":

    main(sys.argv)
