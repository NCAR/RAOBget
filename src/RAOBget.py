###############################################################################
# Stub to call RAOBget class - allows command line operation of script
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from lib.raobget import RAOBget

def main():

    # Instantiate RAOB class
    raob = RAOBget()
    raob.get()


if __name__ == "__main__":

    main()
