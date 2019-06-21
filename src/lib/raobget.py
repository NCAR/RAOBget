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
import argparse

from raobtype.textlist import RAOBtextlist
from raobtype.gifskewt import RAOBgifskewt
from lib.raobdata import RAOBdata
from lib.rsl import RSL


class RAOBget():

    def __init__(self):
        """
        Initialize a RAOBrequest dictionary to hold request metadata
        """

        self.request = RAOBdata()  # dictionary to hold all URL components

    def retrieve(self, request):
        """ Retrieve data for requested RAOB type """

        if (request['raobtype'] == 'TEXT:LIST'):
            textlist = RAOBtextlist()
            textlist.retrieve(request)
        elif (request['raobtype'] == 'GIF:SKEWT'):
            gifskewt = RAOBgifskewt()
            gifskewt.retrieve(request)
            gifskewt.cleanup()
        else:
            print('RAOB type '+request['raobtype']+' not implemented yet')
            exit(1)

    def parse(self):
        """ Define command line arguments which can be provided"""
        parser = argparse.ArgumentParser(
            description="Script to download various formats of RAOB " +
                        "data/imagery from the University of Wyoming " +
                        "Radiosonde Archive. For NCAR/EOL field catalog use " +
                        "the command: \n\npython3 RAOBget.py --catalog --now" +
                        " --config config/project.yml --raobtype GIF:SKEWT " +
                        "[--stnm <station number> or --rsl " +
                        "<station_list_file>] --freq <[3,6,12]>")
        parser.add_argument('--region', type=str, default='',
                            help='Region for which to download sonde info. ' +
                            'Not required. Download will fail if region does' +
                            'not match station location. Defaults to not ' +
                            'defined.')
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
                            choices=['00', '03', '06', '09',
                                     '12', '15', '18', '21'],
                            help='Begin hour (hh) to request data UTC')
        parser.add_argument('--eday', type=str, default='28',
                            help='End day (dd) to request data UTC')
        parser.add_argument('--ehr', type=str, default='12',
                            choices=['00', '03', '06', '09',
                                     '12', '15', '18', '21'],
                            help='End hour (hh) to request data UTC')
        parser.add_argument('--stnm', type=str, default='72672',
                            help='Station number for which to request data...')
        parser.add_argument('--freq', type=str, default='12',
                            choices=['3', '6', '12'],
                            help='Frequency to look for RAOBs')
        parser.add_argument('--rsl', type=str, default='',
                            help='RSL file from which to read list of ' +
                            'stations to request')
        parser.add_argument('--config', type=str, default='',
                            help='Path to YAML config file. Required if ' +
                            '--catalog set')
        parser.add_argument('--test', action="store_true",
                            help='Run in testing mode using local sample ' +
                            'data file 726722019052812.txt. Used for offline' +
                            ' dev')
        parser.add_argument('--mtp', action="store_true",
                            help='Download one RAOB per file, reformat HTML,' +
                            ' and rename file to match MTP requirements. In ' +
                            'mtp mode begin and end times must be the same.')
        parser.add_argument('--catalog', action="store_true",
                            help='Download gif images for catalog use. ' +
                            'Rename to match catalog filename requirements.' +
                            ' Requires that --config be set.')
        parser.add_argument('--now', action="store_true",
                            help='Set requested date/time to current ' +
                            'date/time')
        parser.add_argument('--gui', action="store_true",
                            help='Start RAOBget in GUI mode')
        args = parser.parse_args()

        return(args)

    def get_args(self):
        # Parse command line arguments
        args = self.parse()

        return(args)

    def get(self, args):
        # Set requested region, type, and date to values requested via command
        # line
        self.request.set_prov(args)

        # If option --now is set, set year, month, begin, and end to current
        # date/time
        request = self.request.get_request()
        if request['now'] is True:
            self.request.set_time_now()

        # If user has requested more than one RAOB, loop over the requested
        # frequency
        print("Getting RAOBs from:" + request['year'] + request['month'] +
              request['begin'] + " to " + request['year'] + request['month'] +
              request['end'])
        if request['begin'] == request['end']:
            self.stn_loop(args, request)
        else:
            if request['end'] < request['begin']:
                print("ERROR: Requested end time must be >= requested begin" +
                      "time")
            else:
                # Get RAOBs for first day requested
                day = args.bday
                for hr in range(int(args.bhr), 24, int(request['freq'])):
                    # get RAOBs
                    self.request.set_begin(day, '{:02d}'.format(hr))
                    self.request.set_end(day, '{:02d}'.format(hr))
                    # print("Day 1:",request['begin'] + ' - ' + request['end'])
                    self.stn_loop(args, request)
                # Get RAOBs for second to second-to-last day
                for day in range(int(args.bday) + 1, int(args.eday)):
                    for hr in range(0, 24, int(request['freq'])):
                        # get RAOBs
                        self.request.set_begin('{:02d}'.format(day),
                                               '{:02d}'.format(hr))
                        self.request.set_end('{:02d}'.format(day),
                                             '{:02d}'.format(hr))
                        # print(request['begin'] + ' - ' + request['end'])
                        self.stn_loop(args, request)
                # Get RAOBs for last day requested
                day = args.eday
                for hr in range(0, int(args.ehr)+1, int(request['freq'])):
                    # get RAOBs
                    self.request.set_begin(day, '{:02d}'.format(hr))
                    self.request.set_end(day, '{:02d}'.format(hr))
                    # print("Last:" + request['begin'] + ' - ' +
                    # request['end'])
                    self.stn_loop(args, request)

    def stn_loop(self, args, request):
        # Did user request a single station via --stnm, or a list of stations
        # via an RSL file
        if (args.rsl == ''):
            self.request.set_stnm(args.stnm)
            # Retrieve requested data/imagery for a single stn
            self.retrieve(request)
        else:
            rsl = RSL()
            stnlist = rsl.read_rsl(args)
            for stn in stnlist:  # Loop through a list of stations
                args.stnm = stn
                self.request.set_stnm(args.stnm)
                self.retrieve(request)
