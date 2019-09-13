###############################################################################
# GUI-specific unit tests
#
## Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import unittest
from lib.raobget import RAOBget
from gui.configedit import GUIconfig
from PyQt5.QtWidgets import QApplication, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

class TESTgui(unittest.TestCase):

    def setUp(self):
        self.raob = RAOBget()
        self.app = QApplication([])
        self.best = None

    def test_default(self):
        '''Test the GUI in its default state'''
        layout = QGridLayout()
        config = GUIconfig("", self.raob)
        config.createConfigEditor(self, layout)
        timebox = QGridLayout()
        # Test default begin time
        self.bset = config.btime.create(timebox, 1)
        self.assertEqual(config.btime.getText(),"yyyymmddhh")
        # Test if color is grey - this is set via a style sheet. Haven't
        # figure out how to test this yet. 

    def test_Btime(self):
        '''Test changes to the Begin time field'''
        # Test mouse click on 'Set' with nothing in the box.
        # Should print error message and text should still be yyyymmddhh
        QTest.mouseClick(self.bset, Qt.LeftButton)
        self.assertEqual(config.btime.getStatus(), False)
        self.assertEqual(config.btime.getText(),"yyyymmddhh")
        # Test if color is black - once figure out. See comment above.

        # Set text to a invalid date and test mouse click on 'Set'
        # Text is box is updated, but should print error message
        config.btime.update("20190505")
        status = QTest.mouseClick(self.bset, Qt.LeftButton)
        self.assertEqual(config.btime.getStatus(), False)
        self.assertEqual(config.btime.getText(),"20190505")
        # Test if color is black - once figure out. See comment above.

        # Set text to a valid date and test mouse click on 'Set'
        # Text is box is updated and status is OK
        config.btime.update("2019050512")
        QTest.mouseClick(self.bset, Qt.LeftButton)
        self.assertEqual(config.btime.getStatus(), True)
        # Test if color is black - once figure out. See comment above.
