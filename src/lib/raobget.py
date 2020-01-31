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
import time
import argparse

from raobtype.textlist import RAOBtextlist
from raobtype.gifskewt import RAOBgifskewt
from lib.raobdata import RAOBdata
from lib.rsl import RSL
from lib.messageHandler import printmsg
from lib.config import config


class RAOBget():

    def __init__(self, log=""):
        """
        Initialize a RAOBrequest dictionary to hold request metadata
        """

        self.request = RAOBdata()  # dictionary to hold all URL components

    def parse(self):
        """ Define command line arguments which can be provided"""
        parser = argparse.ArgumentParser(
            description="Script to download various formats of RAOB " +
                        "data/imagery from the University of Wyoming " +
                        "Radiosonde Archive. Defaults to value in brackets." +
                        "WARNING: If an argument is provided in the config " +
                        "file and as a command line argument or via the GUI," +
                        " the used argument value may be hard to predict. " +
                        "Please provide each argument only once.",
            epilog="For NCAR/EOL field catalog use " +
                   "the command: python3 RAOBget.py --config " +
                   "config/catalog.yml [--stnm <station number> or --rsl " +
                   "<RSL file>] --freq <[3,6,12]>")
        parser.add_argument('--region', type=str, default='',
                            help='Region for which to download sonde info. ' +
                            'Not required. Download will fail if region does' +
                            ' not match station location. [''] ')
        parser.add_argument('--raobtype', type=str, default='',
                            help='Data/image type to request - ' +
                            'TEXT:LIST or GIF:SKEWT. [TEXT:LIST]')
        parser.add_argument('--year', type=str, default='',
                            help='Year to request data [2019]')
        parser.add_argument('--month', type=str, default='',
                            help='Month to request data [05]')
        parser.add_argument('--bday', type=str, default='',
                            help='Begin day (dd) to request data UTC [28]')
        parser.add_argument('--bhr', type=str, default='',
                            choices=['00', '03', '06', '09',
                                     '12', '15', '18', '21'],
                            help='Begin hour (hh) to request data UTC [12]')
        parser.add_argument('--eday', type=str, default='',
                            help='End day (dd) to request data UTC [28]')
        parser.add_argument('--ehr', type=str, default='',
                            choices=['00', '03', '06', '09',
                                     '12', '15', '18', '21'],
                            help='End hour (hh) to request data UTC [12]')
        parser.add_argument('--now', action="store_true",
                            help='Set requested date/time to current ' +
                            'date/time' [False])
        parser.add_argument('--stnm', type=str, default='',
                            help='Station number for which to request ' +
                            'data... [72672]')
        parser.add_argument('--freq', type=str, default='',
                            choices=['3', '6', '12'],
                            help='Frequency to look for RAOBs [12]')
        parser.add_argument('--rsl', type=str, default='',
                            help='RSL file from which to read list of ' +
                            'stations to request ['']')
        parser.add_argument('--config', type=str, default='',
                            help='Path to YAML config file. Required if ' +
                            '--catalog set ['']')
        parser.add_argument('--test', action="store_true",
                            help='Run in testing mode using local sample ' +
                            'data file 726722019052812.txt. Used for offline' +
                            ' dev [False]')
        parser.add_argument('--mtp', action="store_true",
                            help='Download one RAOB per file, reformat HTML,' +
                            ' and rename file to match MTP requirements. In ' +
                            'mtp mode begin and end times must be the same. ' +
                            '[False]')
        parser.add_argument('--mtpdir', type=str, default='./mtp',
                            help='Directory to write downloaded mtp data ' +
                            '[../mtp]')
        parser.add_argument('--catalog', action="store_true",
                            help='Download gif images for catalog use. ' +
                            'Rename to match catalog filename requirements.' +
                            ' Requires that --config be set. [False]')
        parser.add_argument('--gui', action="store_true",
                            help='Start RAOBget in GUI mode [False]')
        parser.add_argument('--station_list_file', type=str,
                            default='config/snstns.tbl', help='Path to file ' +
                            'containing station lat/lon, etc. ' +
                            '[config/snstns.tbl] (snstns.tbl was received' +
                            'from U Wyoming June 2019.')
        args = parser.parse_args()

        return(args)

    def get_args(self):
        # Parse command line arguments
        args = self.parse()

        return(args)

    def set_args(self, args):
        """
        Populate the request with values from the command line or from a config
        file.
        """
        # Set requested region, type, and date to values requested via command
        # line
        status = self.request.set_prov(args)

        # If --config supplied, set request to values in config file
        if self.request.get_config() != '':
            configfile = config()
            status = configfile.read(self.request)

        return(status)

    def get(self, widget, app, log=""):
        """ Method to retrieve RAOBS

        Parameters:
            args: a dictionary of command line arguments/defaults
            app: if in GUI mode, a pointer to the QApplication, else
                 app is None

        Returns:
            N/A

        """
        self.log = log  # pointer to GUI log, if running in GUI mode
        self.widget = widget
        args = self.get_args()

        # If args are all empty, warn user.
        empty = True
        request = self.request.get_request()
        for key in request.keys():
            if key != 'station_list_file' and key != 'mtpdir':
                if str(request[key]).lower() == 'true':
                    empty = False
                elif str(request[key]).lower() != 'false' and \
                        request[key] != '':
                    empty = False

        if empty:
            printmsg(log, "ERROR: Request is empty. Set some metadata or" +
                          " load a config file and rerun.")
            return()

        # If option --now is set, set year, month, begin, and end to current
        # date/time
        if self.request.get_now() is True:
            self.request.set_time_now()

        # If user has requested more than one RAOB, loop over the requested
        # frequency
        printmsg(log, "Getting RAOBs from: '" + self.request.get_year() +
                 self.request.get_month() + self.request.get_begin() +
                 "' to '" + self.request.get_year() +
                 self.request.get_month() + self.request.get_end() + "'")
        if self.request.get_begin() == self.request.get_end():
            # printmsg(log, "Single Day:" + self.request.get_begin() +
            #          ' - ' + self.request.get_end())
            self.stn_loop(app)
        else:
            if self.request.get_end() < self.request.get_begin():
                printmsg(log, "ERROR: Requested end time must be >= " +
                         "requested begin time")
            else:
                # Get RAOBs for first day requested
                begin = self.request.get_begin()
                bday = begin[0:2]
                bhr = begin[2:4]
                end = self.request.get_end()
                eday = end[0:2]
                ehr = end[2:4]
                for hr in range(int(bhr), 24,
                                int(self.request.get_freq())):
                    # get RAOBs
                    self.request.set_begin(bday, '{:02d}'.format(hr))
                    self.request.set_end(bday, '{:02d}'.format(hr))
                    # printmsg(log, "Day 1:" + self.request.get_begin() +
                    #          ' - ' + self.request.get_end())
                    self.stn_loop(app)
                # Get RAOBs for second to second-to-last day
                for day in range(int(bday) + 1, int(eday)):
                    for hr in range(0, 24, int(self.request.get_freq())):
                        # get RAOBs
                        self.request.set_begin('{:02d}'.format(day),
                                               '{:02d}'.format(hr))
                        self.request.set_end('{:02d}'.format(day),
                                             '{:02d}'.format(hr))
                        # printmsg(log, self.request.get_begin() + ' - ' +
                        #          self.request.get_end())
                        self.stn_loop(app)
                # Get RAOBs for last day requested
                for hr in range(0, int(ehr)+1,
                                int(self.request.get_freq())):
                    # get RAOBs
                    self.request.set_begin(eday, '{:02d}'.format(hr))
                    self.request.set_end(eday, '{:02d}'.format(hr))
                    # printmsg(log, "Last:" + self.request.get_begin() +
                    #          ' - ' + self.request.get_end())
                    self.stn_loop(app)

    def test_rsl(self, rslfile):
        if os.path.exists(rslfile):
            return(True)
        else:
            return(False)

    def stn_loop(self, app):
        if self.request.get_mtp() is True and \
                self.request.get_type() == "GIF:SKEWT":
            printmsg(self.log, 'ERROR: Requested GIF:SKEWT plots in ' +
                     'MTP mode. Check configuration.')
            return()

        # If TEXT:LIST, change the image to a canvas
        if (app is not None) and (self.request.get_type() == 'TEXT:LIST'):
            self.widget.resetImageWindow()

        # Did user request a single station via --stnm, or a list of stations
        # via an RSL file
        if (self.request.get_rsl() == ''):
            # Stnm already set
            # Retrieve requested data/imagery for a single stn
            self.retrieve(app)
        else:
            rslfile = os.path.join(os.getcwd(), self.request.get_rsl())
            if self.test_rsl(rslfile):
                rsl = RSL()
                stnlist = rsl.read_rsl(rslfile)
                # If use requests more than 50 stns, break them up so don't
                # overwhelm UWyo server.
                if len(stnlist) > 30:
                    count = 0
                for stn in stnlist:  # Loop through a list of stations
                    status = self.request.set_stnm(stn)
                    if not status:
                        printmsg(self.log, "WARNING: Requested station "
                                 + stn + " not valid. Update RSL station" +
                                 " list. Skipping and continuing...")
                        continue
                    status = self.retrieve(app)
                    if not status:
                        printmsg(self.log, "Skipping station and continuing")
                    if len(stnlist) > 30:
                        count = count+1
                        if count % 10 == 0:
                            printmsg(self.log, 'Sleeping for 30 seconds to ' +
                                     'avoid overwhelming UWyo server')
                            time.sleep(30)
                printmsg(self.log, "Done retrieving RAOBs from: '" +
                         self.request.get_year() + self.request.get_month() +
                         self.request.get_begin() + "' to '" +
                         self.request.get_year() + self.request.get_month() +
                         self.request.get_end() + "'")
            else:
                printmsg(self.log, 'ERROR: File ' + rslfile +
                         ' does not exist. Check for typo and rerun.')

    def retrieve(self, app):
        """ Retrieve data for requested RAOB type """

        if (self.request.get_type() == 'TEXT:LIST'):
            textlist = RAOBtextlist(self.log)
            (status, outfile) = textlist.retrieve(app, self.request, self.log)
            # If in GUI mode and successfully downloaded a text file, create a
            # skewT and display it in the GUI
            if status and (app is not None):
                self.widget.createSkewt(outfile)
                app.processEvents()
        elif (self.request.get_type() == 'GIF:SKEWT'):
            gifskewt = RAOBgifskewt(self.log)
            (status, outfile) = gifskewt.retrieve(app, self.request, self.log)
            gifskewt.cleanup()
            # If in GUI mode and successfully downloaded a gif image, display
            # it in the GUI
            if status and (app is not None):
                self.widget.setImage(outfile)
                app.processEvents()
        else:
            printmsg(self.log, "RAOB type '" + self.request.get_type() +
                     "' not implemented yet")
            status = False

        return(status)
