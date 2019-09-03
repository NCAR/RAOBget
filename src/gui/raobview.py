###############################################################################
# Code to display a GUI front-end to RAOBget
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
from PyQt5.QtWidgets import QMainWindow, QAction
from gui.raobwidget import Widget
from gui.fileselector import FileSelector
from lib.config import config


class RAOBview(QMainWindow):

    def __init__(self, raob):
        """ Set the initial GUI window size here """

        self.raob = raob

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
        self.setWindowTitle('RAOBget - a utility to download soundings from ' +
                            'the University of Wyoming sounding archive')

        # Set where GUI will appear on screen (x locn, y locn, width, ht)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set central widget. A QMainWindow must have a central widget. It can
        # also have a menu bar, status bar, toolbars, and dock widgets which
        # appear in a standard layout
        self.widget = Widget(self.raob)
        self.setCentralWidget(self.widget)

        # Get a pointer to the log message window
        self.log = self.widget.get_log()

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
        # This has to be self.editor (not just editor) to avoid garbage
        # collection or the GUIconfig window won't appear.

        # Call dialog box to select the configuration file
        self.loader = FileSelector("config")

        # Load the configuration into the raob request
        self.raob.request.set_config(self.loader.get_file())
        configfile = config(self.log)
        configfile.read(self.raob.request)

    def saveConfig(self):
        """ Actions to take when the 'save config' menu item is selected """
        print("Need to implement save a configuration file")

        # Call dialog box to edit the configuration
