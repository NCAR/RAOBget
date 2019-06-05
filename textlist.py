###############################################################################
# Code specific to retrieving TEXT:LIST formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import wget
import urllib.request

from region import RAOBregion
from type import RAOBtype


class RAOBtextlist:

    def __init__(self):

        self.region = RAOBregion    # Instance of region dictionary
        self.type = RAOBtype    # Instance of data/imagery type dictionary

    def get_url_textlist(self, request):

        url = "http://weather.uwyo.edu/cgi-bin/sounding?"
        if (request['region'] != ''):
            url += "region=" + self.region[request['region']]
        url += "&TYPE=" + self.type[request['raobtype']]
        url += "&YEAR=" + request['year']
        url += "&MONTH=" + request['month']
        url += "&FROM=" + request['begin']
        url += "&TO=" + request['end']
        url += "&STNM=" + request['stnm']
        # print(url)

        return(url)

    def set_outfile_textlist(self, request):

        # Build output filename
        self.outfile = request['stnm'] + request['year'] + \
                request['month'] + request['begin'] + ".txt"

    def get_outfile_textlist(self):

        return(self.outfile)

    def retrieve_textlist(self, request):

        url = self.get_url_textlist(request)

        # Check if filename already exists. wget will fail if it does.
        # Since they don't change, only download new ones.
        self.set_outfile_textlist(request)
        outfile = self.get_outfile_textlist()

        # Add if test just copy from data dir logic here
        if request['test'] is True:
            print(request['test'])
            os.system('cp data/726722019052812.txt .')
        else:

            if os.path.isfile(outfile):
                print("Already downloaded file with name " + outfile +
                      ". Remove this file to re-download.")
            else:
                # Check if online - if not, exit gracefully
                try:
                    urllib.request.urlopen(url)
                except Exception as e:
                    print("Can't connect to weather.uwyo.edu. Use option " +
                          "--test for testing with offline sample data files.")
                    print(str(e))
                    exit(1)

                # Get requested URL.
                wget.download(url, outfile)
                self.strip_html(request)

        return(self.get_outfile_textlist())

    def strip_html(self, request):

        # Strip unneeded HTML from the retrieved data.
        # The VB6 MTP sofware strips part of the HTML from the downloaded RAOB
        # file. We are preserving this format here for backward compatibility
        # so RAOBman VB code will still work.

        out = open(self.outfile)
        temp = open(self.outfile + '.temp', 'w')

        # Loop over RAOBS in file
        line = out.readline()
        while line != '':
            if (line.rstrip() == '<HTML>'):  # Beginning of new RAOB
                # Add double quote before <HTML> on first line
                temp.write('"' + line)
            elif (line.rstrip() == '<BODY BGCOLOR=white>'):
                # read next line and check.
                line = out.readline()
                if "Can't get" in line:
                    print("ERROR: Can't download data for station " +
                          request['stnm'])
                    os.system('rm ' + self.outfile + '.temp')
                    return()
            else:
                print("ERROR: RAOB textlist file " + self.outfile +
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
        os.rename(self.outfile + '.temp', 'final/' + self.outfile)
        print("\nRetrieved ", self.outfile)
