###############################################################################
# Code specific to downloading GIF:SKEWT images from the University of Wyoming
# Radiosonde Archive for import into the EOL field catalog
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import shutil
from ftplib import FTP
from lib.config import config


def to_ftp(outfile, request, log=""):
    """
    return: status messages
    """

    # Get the user specified ftp status and dirs from the YAML config file
    # given on the command line. If there is no config file, then can't ftp/cp.
    # Let user know and return.
    configfile = config(log)
    if os.path.exists(os.path.join(os.getcwd(), request.get_config())):
        configfile.read(request)
    else:
        return("WARNING: No config file defined so ftp status not set." +
               " Downloaded files are in working dir.")

    # Have a config file. Get ftp status, or warn user not set
    ftp_status = configfile.get_ftp_status()

    if ftp_status is True:  # USER IS REQUESTING FTP TO FTP SERVER AND DIR
        ftp_server = configfile.get_ftp_server()
        if ftp_server is None:
            return("Could not FTP files")
        ftp_dir = configfile.get_ftp_dir()
        if ftp_dir is None:
            return("Could not FTP files")

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

    elif ftp_status is False:

        cp_dir = configfile.get_cp_dir()
        if cp_dir is None:
            return("Could not copy files")

        # Move downloaded image to dest file in ftp_dir
        shutil.copyfile(outfile, cp_dir + "/" + outfile)
        return("copied " + outfile + " to " + cp_dir)

    else:  # ftp_status is None
        return("No FTP status set - files not copied or ftp'd")
