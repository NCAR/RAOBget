###############################################################################
# Code to display a GUI to select a file
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget


class FileSelector(QMainWindow):

    def __init__(self):
        """ Set the initial GUI window size here """
        # The QMainWindow class provides a main application window
        super().__init__()

        # Set the initial size of the window created. It is user resizeable
        self.left = 100     # Pixel distance from left of screen to open window
        self.top = 100      # Pixel distance from top of screen to open window
        self.width = 500    # Pixel width of window
        self.height = 500   # Pixel height of window

        # Create the GUI
        self.initWindow()

    def initWindow(self):
        """ Create the GUI """
        # Set window title
        self.setWindowTitle('Select a file')

        # Set where GUI will appear on screen (x locn, y locn, width, ht)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def createMenuBar(self):
        """ Create the menu bar and add options and dropdowns """
        # A Menu bar will show menus at the top of the QMainWindow
        menubar = self.menuBar()


class Widget(QWidget):

    def __init__(self):
        super().__init__()
        # Configure layout
        # Add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        layout = QGridLayout(self)

        # Add an image window to hold the skewt
        self.createImageWindow(layout)

    def createImageWindow(self, layout):
        """ Add an image window to hold the Skewt image """
        image = QLabel()
        layout.addWidget(image, 0, 0, 1, 3)
        image.setWindowTitle("RAOB Skewt")
        image.show()
