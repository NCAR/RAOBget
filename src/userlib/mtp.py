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
from lib.raobroot import getrootdir


def test_dates(request):
    # The MTP VB6 requires only one RAOB per file. Enforce this by requiring
    # begin and end to be equal.
    if request['begin'] != request['end']:
        print("ERROR: Begin and end day/hour must be equal in MTP mode")
        print("begin = " + request['begin'] + "; end = " + request['end'])
        exit(1)


def set_outfile(request):
    # The MTP VB6 code requires that only the begin date be given in the RAOB
    # filename.
    return(request['stnm'] + request['year'] +
           request['month'] + request['begin'] + ".txt")


def strip_html(request, outfile):

    # Strip unneeded HTML from the retrieved data.
    # The VB6 MTP sofware strips part of the HTML from the downloaded RAOB
    # file. We are preserving this format here for backward compatibility
    # so RAOBman VB code will still work.

    out = open(outfile)
    temp = open(outfile + '.temp', 'w')

    # Loop over RAOBS in file
    line = out.readline()
    while line != '':
        if (line.rstrip() == '<HTML>'):  # Beginning of new RAOB
            # Add double quote before <HTML> on first line
            temp.write('"' + line)
        else:
            print("ERROR: RAOB textlist file " + outfile +
                  " does not begin with <HTML>")
            print(line.rstrip())
            return()

        # Remove <TITLE>, <LINK>, and <BODY> lines
        while line[0:4] != '<H2>' and line != '':
            line = out.readline()

        # Search for SECOND </PRE>, keep everything before and including it
        while line[0:6] != '</PRE>' and line != '':
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
                    print("\nObs time " + obstime + " and filename " +
                          outfile + " don't match. Fixing...\n")
                    outfile = request['stnm'] + "20" + \
                        obstime[0:8] + ".txt"
                    print("New filename is " + outfile)
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
    os.rename(outfile + '.temp', getrootdir() + '/mtp/' + outfile)
