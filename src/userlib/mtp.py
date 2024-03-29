###############################################################################
# Code specific to naming and formatting TEXT:LIST formatted data from the
# University of Wyoming Radiosonde Archive for use with the MTP VB6 code.
#
# Hopefully when we complete the rewrite of the VB6 code, these required quirks
# can be eliminated and this code can go away.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
from lib.messageHandler import printmsg
from gui.fileselector import FileSelector


def set_dir(log, request):
    """ Ask user where to save RAOB files. """

    getdir = FileSelector("dir")
    dir = getdir.get_file()

    # If user hit cancel, set dir to previous dir (usually default)
    if not dir:
        dir = os.path.join(os.getcwd(), request.get_mtp_dir())

    printmsg(log, "RAOBs will be written to " + dir)

    request.set_mtp_dir(dir)


def set_outfile(request, dir, log):
    """ Create an output filename, including the full path """

    # If user did not select output dir, default to args default.
    if not dir:
        dir = os.path.join(os.getcwd(), request.get_mtp_dir())

    # Make sure directory exists. If not, warn user.
    if not os.path.exists(dir):
        printmsg(log, "ERROR: Directory to write MTP data does not exist: " +
                 dir + ". Choose another dir.")
        set_dir(log, request)

    # The MTP VB6 code requires that only the begin date be given in the RAOB
    # filename.
    return(request.get_mtp_dir() + '/' + request.get_stnm() +
           request.get_year() + request.get_month() + request.get_begin() +
           ".txt")


def strip_html(request, outfile, log):
    """ Strip unneeded HTML from the retrieved data. """
    # The VB6 MTP sofware strips part of the HTML from the downloaded RAOB
    # file. We are preserving this format here for backward compatibility
    # so RAOBman VB code will still work.

    status = False  # Keep track of if found any data in the file
    out = open(outfile)
    temp = open(outfile + '.temp', 'w')

    # Loop over RAOBS in file
    line = out.readline()
    while line != '':
        if (line.rstrip() == '<HTML>'):  # Beginning of new RAOB
            # Add double quote before <HTML> on first line
            temp.write('"' + line)
        else:
            printmsg(log, "ERROR: RAOB textlist file " + outfile +
                     " does not begin with <HTML>")
            printmsg(log, line.rstrip())
            return()

        # Remove <TITLE>, <LINK>, and <BODY> lines
        while line[0:4] != '<H2>' and line != '':
            line = out.readline()

        # Search for SECOND </PRE>, keep everything before and including it
        while line[0:6] != '</PRE>' and line != '':
            status = True  # Found at least one data line
            temp.write(line)
            line = out.readline()

        # Print the line with the first </PRE>
        temp.write(line)
        line = out.readline()

        # Print until, and including, the line with the second </PRE>
        while line[0:6] != '</PRE>' and line != '':
            # Check for exact obs time in data
            if "Observation time" in line:
                obstime = ''.join(filter(str.isdigit, line))
                if obstime[0:8] not in outfile:
                    printmsg(log, "\nObs time " + obstime + " and filename " +
                             outfile + " don't match. Fixing...\n")
                    outfile = request.get_stnm() + "20" + \
                        obstime[0:8] + ".txt"
                    printmsg(log, "New filename is " + outfile)
            temp.write(line)
            line = out.readline()

        temp.write(line)
        line = out.readline()

        # Remove everything until next <HTML> or until end of file.
        while line != '<HTML>' and line != '':  # not new RAOB and not EOF
            line = out.readline()

    out.close()
    temp.close()

    # move temp back to outfile
    os.replace(outfile + '.temp', outfile)

    # At this point, if status=False, file did not contain any data.
    if (status is False):
        printmsg(log, outfile + " did not contain any data.")
    return(status)
