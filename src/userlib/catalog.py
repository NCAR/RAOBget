###############################################################################
# Code specific to downloading GIF:SKEWT images from the University of Wyoming
# Radiosonde Archive for import into the EOL field catalog
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
from ftplib import FTP
from lib.config import config
from lib.raobroot import getrootdir


def to_ftp(outfile, request):
    """
    return: status messages
    """

    # Get the user specified ftp status and dirs from the YAML config file
    # given on the command line
    configfile = config()
    configfile.read(getrootdir() + "/" + request['config'])
    ftp_status = configfile.get_ftp_status()

    if ftp_status is True:  # USER IS REQUESTING FTP TO FTP SERVER AND DIR
        ftp_server = configfile.get_ftp_server()
        ftp_dir = configfile.get_ftp_dir()

        # Connect to server and put new file
        # ftp = FTP(ftp_server,'USERNAME','PASSWORD')
        try:
            ftp = FTP(ftp_server, 'anonymous', '')
            ftp.cwd(ftp_dir)
            f = open(outfile, 'rb')
            ftp.storbinary(f'STOR ' + outfile, f)
            ftp.quit()
            return("FTPd " + outfile + " to " + ftp_server + "/" + ftp_dir)
        except Exception:
            return("ERROR: FTP transfer failed for file " + outfile)

    else:

        cp_dir = configfile.get_cp_dir()

        # Move downloaded image to dest file in ftp_dir
        os.system("cp " + outfile + " " + cp_dir + "/" + outfile)
        return("copied " + outfile + " to " + cp_dir)
