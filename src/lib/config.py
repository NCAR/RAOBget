###############################################################################
# Code to read in the project yaml configuration file, which specifies the
# request metadata including, if needed, the station list filename and
# location, whether to ftp data to the catalog or cp it to a local dir, and the
# server and path to ftp/cp to, e.g.
#
# station_list_file: '../../config/snstns.tbl'
# ftp: False
# cp_dir: '../ftp'
#
# Requires:
#    A request containing the location of the config file.
#
# In --catalog mode, the following parameters are required:
#    ftp:               ftp data to catalog site, or cp to local dir?
#    ftp_server:        usually catalog.eol.ucar.edu
#    ftp_dir:           usually project under pub/incoming/catalog
#    cp_dir:            usually /net/iftp2/pub/incoming/catalog/<project>
#
# Since these parameters don't have defaults defined via the
# argparse function in lib/raobget.py (maybe this should change??), the only
# way to get them is from the config file. This class handles notifying the
# user of this requirement.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import logging
import os
import yaml
from lib.messageHandler import printmsg


class config():

    def __init__(self, log=""):
        self.log = log        # pointer to GUI log, if extant
        self.projConfig = {}  # initialize dictionary to hold yamlfile contents

    def write(self, request):
        """ Write the request metadata to a YAML config file"""

        yamlfile = request.get_config()

        if (request.get_config() == ""):
            printmsg(self.log, "ERROR: File to save config to not defined. " +
                     "Can't save")
            return(False)

        with open(yamlfile, 'w') as outfile:
            yaml.dump(request.get_dict(), outfile)

        printmsg(self.log, "Successfully saved config to " + yamlfile)

    def read(self, request):
        """ Read the contents of the YAML file into self.projConfig"""

        yamlfile = request.get_config()
        printmsg(self.log, "Reading configuration from " + yamlfile)

        # If the yamlfile is not defined, return False so code will use default
        # request (e.g, cancelled out so didn't append a file)
        if (request.get_config() == ""):
            return(False)

        elif not os.path.isdir(yamlfile):
            if os.path.exists(yamlfile):
                infile = open(yamlfile)
                self.projConfig = yaml.load(infile, Loader=yaml.BaseLoader)
                # for key, value in self.projConfig.items():
                #     printmsg(self.log, key + ": " + str(value))
                infile.close()
            else:
                printmsg(self.log, "WARNING: No config file selected")
                return(False)
        else:
            printmsg(self.log, "WARNING: Path to config file doesn't exist: " +
                     yamlfile)
            return(False)

        # Load the configuration into the request
        self.load(request)
        return(True)

    def load(self, request):
        """ Load the configuration into the request """
        for key in self.projConfig.keys():
            # Vet that key is a valid key in request so code will use default
            # request
            if key in request.get_keys():

                # Save booleans as booleans
                if str(self.projConfig[key]).lower() == 'true':
                    request.set_key(key, True)
                elif str(self.projConfig[key]).lower() == 'false':
                    request.set_key(key, False)
                else:
                    request.set_key(key, self.projConfig[key])

                logging.info(key + " set to " + self.projConfig[key])
            else:
                printmsg(self.log, "ERROR: key " + key + " in config file is" +
                         " not a valid key - skipping.")

    def clear(self, request):
        for key in request.get_keys():
            request.set_key(key, "")

    def get_ftp_status(self):
        if 'ftp' in self.projConfig.keys():
            if str(self.projConfig['ftp']).lower() == "false":
                return(False)
            if str(self.projConfig['ftp']).lower() == "true":
                return(True)
        else:
            printmsg(self.log, "ERROR: ftp status not defined. " +
                     "Add 'ftp: True/False' to  config file and rerun.")
            return(None)

    def get_cp_dir(self):
        if 'cp_dir' in self.projConfig.keys():
            return(self.projConfig['cp_dir'])
        else:
            printmsg(self.log, "ERROR: Directory to cp files to not defined." +
                     " Add 'cp_dir: path' to  config file and rerun.")
            return(None)

    def get_ftp_server(self):
        if 'ftp_server' in self.projConfig.keys():
            return(self.projConfig['ftp_server'])
        else:
            printmsg(self.log, "ERROR: ftp server not defined. " +
                     "Add 'ftp_server: path' to  config file and rerun.")
            return(None)

    def get_ftp_dir(self):
        if 'ftp_dir' in self.projConfig.keys():
            return(self.projConfig['ftp_dir'])
        else:
            printmsg(self.log, "ERROR: Directory to ftp files to not " +
                     "defined. Add 'ftp_dir: path' to  config file and rerun.")
            return(None)
