###############################################################################
# Methods related to managing an optional list of raob stations to request
# data for
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################


class RSL():

    def read_rsl(self, args):  # read RAOB Station List (RSL) file
        """ Read a optional provided list of raob stations to request data for
        """
        rsl = open(args.rsl)
        stnlist = rsl.readlines()
        rsl.close()
        return([line.rstrip() for line in stnlist])
