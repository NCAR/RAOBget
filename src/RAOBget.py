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

    # Instantiate RAOB class
    raob = RAOBget()

    args = raob.get_args()

    if args.gui is True:
        # Every GUI app must have exactly one instance of QApplication. The
        # QApplication class manages the GUI application's control flow and
        # main settings.
        app = QApplication([])

        # Instantiate the RAOBview GUI
        viewer = RAOBview(raob)
        viewer.show()

        # Run the application until the user closes it.
        app.exec_()

    else:

        raob.get(args)


if __name__ == "__main__":

    main()
