###############################################################################
# Method to handle printing messages. Either print to terminal, or if in gui
# mode, print to status message window.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################


def printmsg(log, msg):
    if log == "":
        print(msg)
    else:
        log.appendPlainText(msg)
