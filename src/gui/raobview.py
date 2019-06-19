###############################################################################
#
# Code to display a GUI front-end to RAOBget
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QMainWindow, QAction, QMdiSubWindow, QLabel, \
     QPushButton, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Configure layout
        # Add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        layout = QGridLayout(self)

        # Add an image window to hold the skewt
        self.createImageWindow(layout)

        # Add a log message window
        self.createLogMessageWindow(layout)

        # Add a button to begin retrieving RAOBs
        self.createRetrieveButton(layout)

    def createRetrieveButton(self, layout):
        retrieve = QPushButton("Retrieve RAOBs")
        layout.addWidget(retrieve, 2, 2)
        retrieve.clicked.connect(self.clickRetrieve)
        retrieve.setToolTip('Click to start downloading RAOBs')
        retrieve.show()

    def createImageWindow(self, layout):
        """ Add an image window to hold the Skewt image """
        image = QLabel()
        layout.addWidget(image, 0, 0, 1, 3)
        image.setWindowTitle("RAOB Skewt")
        pixmap = self.getImage()
        image.setPixmap(pixmap)

        image.show()

    def getImage(self):
        """ Stub - will eventually return the image associated with the latest
        downloaded RAOB data """
        self.pixmap = \
            QPixmap('../ftp/upperair.SkewT.201905280000.Riverton_WY.gif')
        return(self.pixmap)

    def createLogMessageWindow(self, layout):
        """ Add a log message window """
        log = QMdiSubWindow()
        layout.addWidget(log, 1, 0, 1, 3)
        log.setWindowTitle("Status messages")
        log.show()

    def clickRetrieve(self):
        """ Actions to take when the 'Begin retrieval' button is selected """
        print("Begin retrieval")


class RAOBview(QMainWindow):

    def __init__(self):
        """ Set the initial GUI window size here """
        # The QMainWindow class provides a main application window
        QMainWindow.__init__(self)

        # Set the initial size of the window created. It is user resizeable
        self.left = 500     # Pixel distance from left of screen to open window
        self.top = 100      # Pixel distance from top of screen to open window
        self.width = 800    # Pixel width of window
        self.height = 1000  # Pixel height of window

        # Create the GUI
        self.initUI()

    def initUI(self):
        """ Create the GUI """
        # Set window title
        self.setWindowTitle('RAOBget')

        # Set where GUI will appear on screen (x locn, y locn, width, ht)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set central widget. A QMainWindow must have a central widget. It can
        # also have a menu bar, status bar, toolbars, and dock widgets which
        # appear in a standard layout
        self.widget = Widget()
        self.setCentralWidget(self.widget)

        # Configure the menu bar
        self.createMenuBar()

    def createMenuBar(self):
        """ Create the menu bar and add options and dropdowns """
        # A Menu bar will show menus at the top of the QMainWindow
        menubar = self.menuBar()

        # Mac OS treats menubars differently. To get a similar outcome, we can
        # add the following line: menubar.setNativeMenuBar(False).
        menubar.setNativeMenuBar(False)

        # Add a menu option to access config files
        fileMenu = menubar.addMenu("File")
        # In order for tooltips of actions to display, need to
        # setToolTipsVisible to True (is False by default)
        fileMenu.setToolTipsVisible(True)

        # Add a submenu option to load a config file
        loadConfig = QAction("Load config", self)
        loadConfig.setToolTip('Load a previously saved configuration file')
        loadConfig.triggered.connect(self.loadConfig)
        fileMenu.addAction(loadConfig)

        # Add a submenu option to save the current configuration
        saveConfig = QAction("Save config", self)
        saveConfig.setToolTip('Save the current configuration to a file')
        saveConfig.triggered.connect(self.saveConfig)
        fileMenu.addAction(saveConfig)

        # Add a menu option to edit configuration
        editMenu = menubar.addMenu("Edit")
        # In order for tooltips of actions to display, need to
        # setToolTipsVisible to True (is False by default)
        editMenu.setToolTipsVisible(True)

        # Add a submenu option to edit the current configuration
        editConfig = QAction("Edit config", self)
        editConfig.setToolTip('Edit the current configuration')
        editConfig.triggered.connect(self.editConfig)
        editMenu.addAction(editConfig)

        # Add a menu/submenu? option to quit
        quitButton = QAction('Quit', self)
        quitButton.setShortcut('Ctrl+Q')
        quitButton.setToolTip('Exit application')
        quitButton.triggered.connect(self.close)
        # Decide between these two menu positions
        fileMenu.addAction(quitButton)
        self.quit = menubar.addAction(quitButton)

    def loadConfig(self):
        """ Actions to take when the 'Load config' menu item is selected """
        print("Implement LOAD action here")

    def saveConfig(self):
        """ Actions to take when the 'save config' menu item is selected """
        print("Implement SAVE action here")

    def editConfig(self):
        """ Actions to take when the 'save config' menu item is selected """
        print("Implement EDIT action here")
