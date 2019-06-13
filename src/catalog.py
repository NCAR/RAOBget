###############################################################################
# Code specific to downloading GIF:SKEWT images from the University of Wyoming
# Radiosonde Archive for import into the EOL field catalog
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os


def to_ftp(outfile):
    # STUB UNTIL I TALK TO SCOT
    # ftp_server = "catalog.eol.ucar.edu"
    # ftp_dir = "/net/iftp2/pub/incoming/catalog/relampago"
    ftp_dir = "../ftp"

    # Move downloaded image to dest file in ftp_dir
    os.rename(outfile, ftp_dir + "/" + outfile)

    # if ftp_server, connect and put new file to server
