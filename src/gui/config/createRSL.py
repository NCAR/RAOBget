###############################################################################
# Methods to manipulate the create RSL station list metadata display
# in the GUI. The name of the created RSL file is not displayed in the GUI.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QLabel, QPushButton
from gui.RSLcreator import RSLCreator


class CreateRSL():

    def __init__(self, request, log=""):
        """ This class creates a button which launches a RSLCreator """
        self.log = log
        self.request = request

    def create(self, box, row):
        """ Create the Create station list button """
        lbl = QLabel("-or-")
        box.addWidget(lbl, row, 0)
        create = QPushButton("Create/Edit station list")
        create.clicked.connect(self.createRSL)
        create.setToolTip('Create a list of stations for which to download ' +
                          'soundings')
        box.addWidget(create, row, 1, 1, 2)

    def createRSL(self):
        """ Call dialog box to create a station list """
        self.creator = RSLCreator(self.request, self.log)
        self.creator.show()
