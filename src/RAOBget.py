###############################################################################
# Stub to call RAOBget class - allows command line operation of script
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from lib.raobget import RAOBget
from gui.raobview import RAOBview
from PyQt5.QtWidgets import QApplication


def main():
    """ Instantiate a RAOB class and call in either GUI mode or command-line
        mode """

    # Instantiate RAOB class
    raob = RAOBget()

    # Get arguments from command line
    args = raob.get_args()

    # Set either the command line or default args as the request
    raob.set_args(args)

    if args.gui is True:  # Run in GUI mode
        # Every GUI app must have exactly one instance of QApplication. The
        # QApplication class manages the GUI application's control flow and
        # main settings.
        app = QApplication([])

        # Instantiate the RAOBview GUI
        viewer = RAOBview(raob)
        viewer.show()

        # Run the application until the user closes it.
        app.exec_()

    else:  # Run in command line mode

        # Call method to retrieve raobs
        raob.get(args)


if __name__ == "__main__":

    main()
