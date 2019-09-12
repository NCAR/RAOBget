###############################################################################
# Code specific to retrieving GIF:SKEWT formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
import re

import userlib.catalog
from lib.rwget import RAOBwget
from lib.stationlist import RAOBstation_list
from lib.raobroot import getrootdir
from lib.messageHandler import printmsg


class RAOBgifskewt():

    def __init__(self, log=""):

        self.log = log
        self.rwget = RAOBwget(log)

    def set_outfile_html(self, request):
        """ Build output filename for GIF:SKEWT data file. """
        self.outfile_html = request.get_stnm() + request.get_year() + \
            request.get_month() + request.get_begin() + request.get_end() + \
            ".html"

    def get_outfile_html(self):
        """
        Returns:
            self.outfile_html: the name of the file to which the received data
            should be saved
        """

        return(self.outfile_html)

    def get_url(self, request):
        """
        Generate the request URL for a GIF:SKEWT request
        """
        request.set_type("GIF:SKEWT")
        return(self.rwget.get_url(request, self.log))

    def get_station_info(self, request):
        """ Read in the station metadata for the given station id/number """
        station_list_file = getrootdir() + "/" + request.get_stnlist_file()

        stationList = RAOBstation_list(self.log)
        stationList.read(station_list_file)
        if request.get_stnm().isdigit():
            station = stationList.get_by_stnm(request.get_stnm())
        else:
            station = stationList.get_by_id(request.get_stnm())

        # Should only get back one, unique station. If not, warn user
        if (len(station) != 1):
            printmsg(self.log, "WARNING: Found more than one station " +
                     "matching request['stnm']")
            for i in range(len(station)):
                printmsg(self.log, str(station[i]))
            printmsg(self.log, "Returning first station found")

        return(station[0])

    def get_prod(self, request):
        """ Build the product name required by the field catalog """

        # Open the HTML file and read in the <TITLE> line
        out = open(self.get_outfile_html())
        line = out.readline()
        while '<TITLE>' not in line:
            line = out.readline()
        if '<TITLE>' in line:
            m = re.search(request.get_stnm()+' (.*) [Sounding]',
                          line)
            if m:
                prod = m.group(1).replace(" ", "_")

                # Get station metadata for use in reformatting product name
                station = self.get_station_info(request)

                # If we found the station by the number, then the id will still
                # be in the title. Remove it.
                if station['id'].rstrip() in prod:
                    prod = prod.replace(station['id'].rstrip()+"_", "")

                # I have seen some products with protected shell characters.
                # Remove them here.
                prod = prod.replace("(", "")  # Remove open parenthesis
                prod = prod.replace(")", "")  # Remove close parenthesis
                # ... add more as needed here ...

                # For international skewts, set the product name to
                # "Station_Name_CC" where CC is the two letter country code.
                # For US stations use "Station_Name_ST" where ST it the two
                # letter state code.
                if (station['country'] == 'US'):
                    prod += "_" + station['state']
                else:
                    prod += "_" + station['country']

            else:
                printmsg(self.log, "WARNING: Couldn't find product name. " +
                         "Setting to temp")
                prod = "temp"

        out.close()

        return(prod)

    def set_outfile_gif(self, request):
        """
        Build output filename for GIF:SKEWT image.

        Parameters:
            request: a RAOBrequest dictionary of request metadata
        """
        platform = "SkewT"

        self.outfile_gif = "upperair." + platform + '.' + request.get_year() \
            + request.get_month() + request.get_begin() + "00." + \
            self.get_prod(request) + ".gif"

    def get_outfile_gif(self):
        """
        Returns:
            self.outfile_gif: the name of the file to which the received image
            should be saved
        """

        return(self.outfile_gif)

    def get_gif_url(self, request):

        url = "http://weather.uwyo.edu/upperair/images/"
        url += request.get_year()
        url += request.get_month()
        url += request.get_begin() + "."
        url += request.get_stnm() + ".skewt.parc.gif"

        return(url)

    def retrieve(self, app, request, log=""):
        """
        Retrieves the requested data from the U Wyoming archive

        Parameters:
            request: A dictionary containing the metadata for the
                     request.

        Returns:
            outfile: The name of the retrieved file.
        """

        # SKEWT's are downloaded in two steps.
        # The first request generates the skewt on the website and downloads an
        # HTML wrapper with a reference to the gif image that is still on the
        # website. The second request downloads the gif image.

        # Create first request URL from request metadata
        url = self.get_url(request)
        if app is not None:      # Force the GUI to redraw so log
            app.processEvents()  # messages, etc are displayed

        # Create output filename from request metadata
        self.set_outfile_html(request)

        # If in test mode, copy file from data dir to simulate download...
        if request.get_test() is True:
            os.system('cp ' + getrootdir() +
                      '/test/data/7267220190528122812.html.ctrl' +
                      ' 7267220190528122812.html')
            status = False

        # ...else download data
        else:
            status = self.rwget.get_data(url, self.get_outfile_html())
            if app is not None:      # Force the GUI to redraw so log
                app.processEvents()  # messages, etc are displayed

        # If site returned good html file and thus generated gif
        if status:
            # Download the gif image directly
            url = self.get_gif_url(request)

            # Create output filename from request metadata
            self.set_outfile_gif(request)
            outfile = self.get_outfile_gif()
            if app is not None:      # Force the GUI to redraw so log
                app.processEvents()  # messages, etc are displayed

            # Download gif image
            status = self.rwget.get_data(url, outfile)
            if app is not None:      # Force the GUI to redraw so log
                app.processEvents()  # messages, etc are displayed

        else:
            if request.get_test() is True:
                os.system('cp ' + getrootdir() + '/test/data/' +
                          'upperair.SkewT.201905280000.Riverton_WY.gif.ctrl' +
                          ' upperair.SkewT.201905280000.Riverton_WY.gif')
            outfile = "upperair.SkewT.201905280000.Riverton_WY.gif"

        # If running in catalog mode, ftp files to catalog dir
        if request.get_catalog() is True and status:
            status = userlib.catalog.to_ftp(outfile, request, self.log)
            printmsg(self.log, status)
            if app is not None:      # Force the GUI to redraw so log
                app.processEvents()  # messages, etc are displayed

        return(outfile)

    def cleanup(self):
        """ Remove now-irrelevant html file """
        if os.path.isfile(self.get_outfile_html()):
            os.system('rm ' + self.get_outfile_html())
            printmsg(self.log, 'Removed ' + self.get_outfile_html())
