###############################################################################
#
# This python dictionary stores the list of data/imagery types available for
# retrieval via the University of Wyoming Radiosonde data archive. The type
# identifier is used in the retrieval URL, e.g.
#   http://weather.uwyo.edu/cgi-bin/sounding?type=TEXT%3ALIST&...
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################

RAOBtype = {
    # Type name: URL type identifier
    'TEXT:LIST': "TEXT%3ALIST",
    'GIF:SKEWT': "GIF%3ASKEWT",
}
