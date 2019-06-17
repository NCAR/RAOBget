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


class config():

    def read(self, yamlfile):
        if not os.path.isdir(yamlfile):
            infile = open(yamlfile)
            self.projConfig = yaml.load(infile, Loader=yaml.BaseLoader)
            # for key, value in self.projConfig.items():
            #     print(key + ": " + str(value))

            infile.close()
        else:
            self.projConfig = {'station_list_file': 'config/snstns.tbl'}

    def get_stnlist_file(self):
        if 'station_list_file' in self.projConfig.keys():
            return(getrootdir() + "/" + self.projConfig['station_list_file'])
        else:
            print("ERROR: station list metadata file not defined. " +
                  "Add 'station_list_file: path' to  config file and rerun.")
            exit(1)

    def get_ftp_status(self):
        if 'ftp' in self.projConfig.keys():
            if self.projConfig['ftp'] == "False":
                return(False)
            if self.projConfig['ftp'] == "True":
                return(True)
        else:
            print("ERROR: ftp status not defined. " +
                  "Add 'ftp: True/False' to  config file and rerun.")
            exit(1)

    def get_cp_dir(self):
        if 'cp_dir' in self.projConfig.keys():
            return(self.projConfig['cp_dir'])
        else:
            print("ERROR: Directory to cp files to not defined. " +
                  "Add 'cp_dir: path' to  config file and rerun.")
            exit(1)

    def get_ftp_server(self):
        if 'ftp_server' in self.projConfig.keys():
            return(self.projConfig['ftp_server'])
        else:
            print("ERROR: ftp server not defined. " +
                  "Add 'ftp_server: path' to  config file and rerun.")
            exit(1)

    def get_ftp_dir(self):
        if 'ftp_dir' in self.projConfig.keys():
            return(self.projConfig['ftp_dir'])
        else:
            print("ERROR: Directory to ftp files to not defined. " +
                  "Add 'ftp_dir: path' to  config file and rerun.")
            exit(1)
