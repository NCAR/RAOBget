###############################################################################
# Method to handle printing messages. Either print to terminal, or if in gui
# mode, print to status message window.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor


def printmsg(log, msg):
    """ If a QPlainTextEdit instance is passed to this method, it will
    return the msg to that instance to be displayed in the text window
    in the GUI. For this to work, all print messages in the rest of the
    code should use printmsg instead of directly calling print() """
    if log == "":
        print(msg)
    else:
        text_format = QTextCharFormat()
        error = re.compile(r'ERROR', re.IGNORECASE)
        if error.match(msg):
            text_format.setForeground(QBrush(QColor('red')))
            log.setCurrentCharFormat(text_format)
        else:
            text_format.setForeground(QBrush(QColor('black')))
            log.setCurrentCharFormat(text_format)

        log.appendPlainText(msg)
