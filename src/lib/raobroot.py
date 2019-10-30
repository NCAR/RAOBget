###############################################################################
# Function to identify the project root dir so all hardcoded paths can
# be relative to that dir.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os


def getrootdir():
    """ Return a rootdir variable that is hold the root dir of the checkout """
    rootdir = os.path.dirname(os.path.dirname(os.path.dirname(
              os.path.abspath(__file__))))
    return(rootdir)
