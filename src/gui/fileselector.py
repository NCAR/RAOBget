###############################################################################
# Code to display a GUI to select a file
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, \
     QLineEdit, QPlainTextEdit, QPushButton


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

        # Set central widget. A QMainWindow must have a central widget.
        # Pass the MainWindow to the Widget so we can close the main window
        # from the widget when the cancel button is selected.
        self.widget = Widget(self)
        self.setCentralWidget(self.widget)


class Widget(QWidget):

    def __init__(self, window):
        super().__init__()

        # Save the parent window as self.window
        self.window = window

        # Configure layout
        # Add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        layout = QGridLayout(self)

        # Copy layout of other RAF file selection dialog windows

        lbl = QLabel("Filter")
        layout.addWidget(lbl, 0, 0, 1, 4)

        filtertext = QLineEdit()
        filtertext.setToolTip("Enter a regex path to look for file")
        layout.addWidget(filtertext, 1, 0, 1, 4)
        # filterpath = filtertext.text()

        lbl = QLabel("Directories")
        layout.addWidget(lbl, 2, 0, 1, 2)
        lbl = QLabel("Files")
        layout.addWidget(lbl, 2, 2, 1, 2)

        selector = QPlainTextEdit()
        selector.setReadOnly(True)  # Can I still highlight and choose?
        layout.addWidget(selector, 3, 0, 1, 2)
        selector = QPlainTextEdit()
        selector.setReadOnly(True)  # Can I still highlight and choose?
        layout.addWidget(selector, 3, 2, 1, 2)

        lbl = QLabel("Enter file name:")
        layout.addWidget(lbl, 4, 0, 1, 4)

        self.filetext = QLineEdit()
        self.filetext.setToolTip("Enter a file to look for")
        layout.addWidget(self.filetext, 5, 0, 1, 4)

        ok = QPushButton("OK")
        layout.addWidget(ok, 6, 0, 1, 1)
        ok.clicked.connect(self.set_filename)

        fileFilter = QPushButton("Filter")
        layout.addWidget(fileFilter, 6, 1, 1, 1)
        fileFilter.clicked.connect(self.filterList)

        cancel = QPushButton("Cancel")
        layout.addWidget(cancel, 6, 2, 1, 1)
        cancel.clicked.connect(self.cancel)

        fileHelp = QPushButton("Help")
        fileHelp.setDisabled(True)
        layout.addWidget(fileHelp, 6, 3, 1, 1)

    def filterList(self):
        print("Need to code filtering list")

    def set_filename(self):
        print("Filename set to " + self.filetext.text())

    def cancel(self):
        self.window.close()
