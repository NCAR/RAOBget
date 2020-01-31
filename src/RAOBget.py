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

# To turn on additional messages for debugging, etc, uncomment these lines
# import logging
# logging.basicConfig(level=logging.INFO)


def main():
    """ Instantiate a RAOB class and call in either GUI mode or command-line
        mode """

    # Instantiate RAOB class
    raob = RAOBget()

    # Get arguments from command line
    args = raob.get_args()

    # Set either the command line or default args as the request
    status = raob.set_args(args)
    if not status:  # status returned False, so something went wrong
        exit(1)

    if args.gui is True:  # Run in GUI mode
        # Every GUI app must have exactly one instance of QApplication. The
        # QApplication class manages the GUI application's control flow and
        # main settings.
        app = QApplication([])

        # Instantiate the RAOBview GUI. Pass a pointer to the QApplication
        # so we can force the GUI to redraw when needed.
        viewer = RAOBview(raob, app)
        viewer.show()

        # Run the application until the user closes it.
        app.exec_()

    else:  # Run in command line mode. There is no QApplication, so pass None

        # Call method to retrieve raobs.
        raob.get(None, None)


if __name__ == "__main__":

    main()
