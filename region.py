################################################################################
#
# This python dictionary stores the list of regions available via the University
# of Wyoming Radiosonde data archive. The region identifier is used in the 
# retrieval URL, e.g.
#   http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&...
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
################################################################################

RAOBregion = {
    # Region name       : URL region identifier
    'North America'     :"naconf",
    'South America'     :"samer",
    'South Pacific'     :"pac",
    'New Zealand'       :"nz",
    'Antarctica'        :"ant",
    'Arctic'            :"np",
    'Europe'            :"europe",
    'Africa'            :"africa",
    'Southeast Asia'    :"seasia",
}

