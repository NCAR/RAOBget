###############################################################################
# Code to read in the project yaml configuration file, which specifies the
# station list filename and location, whether to ftp data to the catalog or cp
# it to a local dir, and the server and path to ftp/cp to, e.g.
#
# station_list_file: '../../config/snstns.tbl'
# ftp: False
# cp_dir: '../ftp'
#
# Parameters:
#    station_list_file: list of stations with location, description, etc
#    ftp:               ftp data to catalog site, or cp to local dir?
#    ftp_server:        usually catalog.eol.ucar.edu
#    ftp_dir:           usually project under pub/incoming/catalog
#    cp_dir:            usually /net/iftp2/pub/incoming/catalog/<project>
#
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import yaml
from lib.raobroot import getrootdir
from lib.messageHandler import printmsg


class config():

    def __init__(self, log=""):
        self.log = log       # pointer to GUI log, if extant

    def read(self, request):
        yamlfile = request.get_config()
        if not os.path.isdir(yamlfile):
            if os.path.exists(yamlfile):
                infile = open(yamlfile)
                self.projConfig = yaml.load(infile, Loader=yaml.BaseLoader)
                # for key, value in self.projConfig.items():
                #     printmsg(self.log, key + ": " + str(value))
                infile.close()
            else:
                printmsg(self.log, "Config file not selected - can't load")
                printmsg(self.log, "ERROR: Station set to testing default \
                         - please select a station")
                return(False)
        else:
            self.projConfig = {'station_list_file': 'config/snstns.tbl'}

        # Load the configuration into the request
        self.load(request)

    def load(self, request):
        for key in self.projConfig.keys():
            # Vet that key is a valid key in request
            if key in request.get_keys():

                # Save booleans as booleans
                if self.projConfig[key] == 'True':
                    request.set_key(key, True)
                elif self.projConfig[key] == 'False':
                    request.set_key(key, False)
                else:
                    request.set_key(key, self.projConfig[key])

                printmsg(self.log, key + " set to " + self.projConfig[key])
            else:
                printmsg(self.log, "ERROR: key " + key + " in config file is" +
                         " not a valid key - skipping.")

    def get_stnlist_file(self):
        if 'station_list_file' in self.projConfig.keys():
            return(getrootdir() + "/" + self.projConfig['station_list_file'])
        else:
            printmsg(self.log, "ERROR: station list metadata file not " +
                     "defined. Add 'station_list_file: path' to  config file" +
                     "and rerun.")
            exit(1)

    def get_ftp_status(self):
        if 'ftp' in self.projConfig.keys():
            if self.projConfig['ftp'] == "False":
                return(False)
            if self.projConfig['ftp'] == "True":
                return(True)
        else:
            printmsg(self.log, "ERROR: ftp status not defined. " +
                     "Add 'ftp: True/False' to  config file and rerun.")
            exit(1)

    def get_cp_dir(self):
        if 'cp_dir' in self.projConfig.keys():
            return(self.projConfig['cp_dir'])
        else:
            printmsg(self.log, "ERROR: Directory to cp files to not defined." +
                     " Add 'cp_dir: path' to  config file and rerun.")
            exit(1)

    def get_ftp_server(self):
        if 'ftp_server' in self.projConfig.keys():
            return(self.projConfig['ftp_server'])
        else:
            printmsg(self.log, "ERROR: ftp server not defined. " +
                     "Add 'ftp_server: path' to  config file and rerun.")
            exit(1)

    def get_ftp_dir(self):
        if 'ftp_dir' in self.projConfig.keys():
            return(self.projConfig['ftp_dir'])
        else:
            printmsg(self.log, "ERROR: Directory to ftp files to not " +
                     "defined. Add 'ftp_dir: path' to  config file and rerun.")
            exit(1)
