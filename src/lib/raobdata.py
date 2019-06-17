###############################################################################
# Class defining dictionary to hold RAOB request metadata and associated
# access methods
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from datetime import datetime


class RAOBdata():

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
            'freq': "12",    # Freq to look for RAOBs. Default is every 12 hrs
            'rsl': "",       # Name of file containing list of stations to
                             # retrieve data for
            'config': "",    # Name of config file
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

    def set_freq(self, args):
        self.request['freq'] = args.freq

    def set_config(self, args):
        self.request['config'] = args.config

    def set_prov(self, args):  # Set provenance of RAOB to retrieve
        """
        Set request from all the metadata specificed on the command line.
        Calls individual set_ methods for each argument.
        Doesn't set stnm because that is set in raobget.get to either a
        single station, or looping over stns from rsl file.
        """
        self.set_region(args)
        self.set_type(args)
        self.set_year(args.year)
        self.set_month(args.month)
        self.set_begin(args.bday, args.bhr)
        self.set_end(args.eday, args.ehr)
        self.set_freq(args)
        self.set_test(args)
        self.set_mtp(args)
        self.set_catalog(args)
        if args.catalog is True and args.config == '':
            print("ERROR: --config option required if --catalog is set")
            exit(1)
        self.set_config(args)
        self.set_now(args)

    def get_request(self):
        """ Return request metadata dictionary """

        return(self.request)

    def set_time_now(self):
        """ Set request time to most recent 12 hour (UTC) RAOB unless freq is
        set higher. """
        time = datetime.utcnow()
        self.set_year(str(time.year))
        self.set_month('{:02d}'.format(time.month))
        for hr in range(0, 24, int(self.request['freq'])):
            if time.hour > hr and time.hour <= hr+int(self.request['freq']):
                hour = hr

        self.set_begin('{:02d}'.format(time.day), '{:02d}'.format(hour))
        self.set_end('{:02d}'.format(time.day), '{:02d}'.format(hour))
