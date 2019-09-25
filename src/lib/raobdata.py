###############################################################################
# Class defining dictionary to hold RAOB request metadata and associated
# access methods
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from datetime import datetime
from lib.raobroot import getrootdir
from lib.stationlist import RAOBstation_list


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
            'mtpdir': "",    # Dir to write RAOBs for MTP use
            'catalog': False,  # catalog-specific processing
            'now': False,    # Set requested date/time to current time,
                             # i.e. retrieve current RAOB.
            'ftp': False,    # Ftp data to catalog site, or cp to local dir?
            'ftp_server': "",  # If ftp is True, need ftp_server and ftp_dir
            'ftp_dir': "",
            'cp_dir': "",    # If ftp is False, need dir to cp files to
            'station_list_file': "",  # List of RAOB station locations,
                             # description, etc. Used to assign metadata to
                             # retrieved RAOB. Give path relative to RAOBget
                             # dir.
        }

        self.request = RAOBrequest  # dictionary to hold all URL components

        # Load a station list so we can validate stnm requests
        self.stationList = RAOBstation_list()
        self.stationList.read(getrootdir() + "/config/snstns.tbl")

    def set_key(self, key, value):
        self.request[key] = value

    def get_keys(self):
        return(self.request.keys())

    def set_region(self, region):
        self.request['region'] = region

    def get_region(self):
        return(self.request['region'])

    def set_type(self, raobtype):
        self.request['raobtype'] = raobtype

    def get_type(self):
        return(self.request['raobtype'])

    def set_year(self, year):
        self.request['year'] = year

    def get_year(self):
        return(self.request['year'])

    def set_month(self, month):
        self.request['month'] = month

    def get_month(self):
        return(self.request['month'])

    def set_begin(self, bday, bhr):
        self.request['begin'] = bday+bhr

    def get_begin(self):
        return(self.request['begin'])

    def set_end(self, eday, ehr):
        self.request['end'] = eday+ehr

    def get_end(self):
        return(self.request['end'])

    def set_test(self, test):
        self.request['test'] = test

    def get_test(self):
        return(self.request['test'])

    def set_mtp(self, mtp):
        self.request['mtp'] = mtp

    def get_mtp(self):
        return(self.request['mtp'])

    def set_mtp_dir(self, mtpdir):
        self.request['mtpdir'] = mtpdir

    def get_mtp_dir(self):
        return(self.request['mtpdir'])

    def set_catalog(self, catalog):
        self.request['catalog'] = catalog

    def get_catalog(self):
        return(self.request['catalog'])

    def set_now(self, now):
        self.request['now'] = now

    def get_now(self):
        return(self.request['now'])

    def set_stnm(self, stnm):
        self.request['stnm'] = stnm
        # This code tests if the station requested is valid by comparing it to
        # the stations in the master list received from UWyo. If that list gets
        # out of date with the UWyo website, comment out the next 5 lines to
        # turn off validation.
        if stnm != "" and not self.stationList.get_by_stnm(stnm) and \
           not self.stationList.get_by_id(stnm):
            return(False)
        else:
            return(True)

    def get_stnm(self):
        return(self.request['stnm'])

    def set_rsl(self, rsl):
        self.request['rsl'] = rsl

    def get_rsl(self):
        return(self.request['rsl'])

    def set_freq(self, freq):
        self.request['freq'] = freq

    def get_freq(self):
        return(self.request['freq'])

    def set_config(self, config):
        self.request['config'] = config

    def get_config(self):
        return(self.request['config'])

    def set_stnlist_file(self, station_list_file):
        self.request['station_list_file'] = station_list_file

    def get_stnlist_file(self):
        return(self.request['station_list_file'])

    def set_prov(self, args):  # Set provenance of RAOB to retrieve
        """
        Set request from all the metadata specificed on the command line.
        Calls individual set_ methods for each argument.
        Doesn't set stnm because that is set in raobget.get to either a
        single station, or looping over stns from rsl file.
        """
        self.set_region(args.region)
        self.set_type(args.raobtype)
        self.set_stnm(args.stnm)
        self.set_rsl(args.rsl)
        self.set_year(args.year)
        self.set_month(args.month)
        self.set_begin(args.bday, args.bhr)
        self.set_end(args.eday, args.ehr)
        self.set_freq(args.freq)
        self.set_test(args.test)
        self.set_mtp(args.mtp)
        self.set_mtp_dir(args.mtpdir)
        self.set_catalog(args.catalog)
        if args.catalog is True and args.config == '':
            print("ERROR: --config option required if --catalog is set")
            exit(1)
        self.set_config(args.config)
        self.set_stnlist_file(args.station_list_file)
        self.set_now(args.now)

    def get_request(self):
        """ Return request metadata dictionary """

        return(self.request)

    def get_dict(self):
        """ Return request dictionary contents """
        return(dict(self.request))

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
