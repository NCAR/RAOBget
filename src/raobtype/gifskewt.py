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


class RAOBgifskewt():

    def __init__(self):

        self.rwget = RAOBwget()

    def set_outfile_html(self, request):
        self.outfile_html = request['stnm'] + request['year'] + \
            request['month'] + request['begin'] + request['end'] + \
            ".html"

    def get_outfile_html(self):

        return(self.outfile_html)

    def get_url(self, request):
        request['raobtype'] = "GIF:SKEWT"
        return(self.rwget.get_url(request))

    def get_station_info(self, stnm):
        """ Read in the station metadata for the given station id/number """
        station_list_file = '../config/snstns.tbl'
        stationList = RAOBstation_list()
        stationList.read(station_list_file)
        if stnm.isdigit():
            station = stationList.get_by_stnm(stnm)
        else:
            station = stationList.get_by_id(stnm)

        # Should only get back one, unique station. If not, warn user
        if (len(station) != 1):
            print("WARNING: Found more than one station matching " + stnm)
            for i in range(len(station)):
                print(station[i])
            print("Returning first station found")

        return(station[0])

    def get_prod(self, request):
        """ Build the product name required by the field catalog """

        # Open the HTML file and read in the <TITLE> line
        out = open(self.get_outfile_html())
        line = out.readline()
        while '<TITLE>' not in line:
            line = out.readline()
        if '<TITLE>' in line:
            m = re.search(request['stnm']+' (.*) [Sounding]',
                          line)
            if m:
                prod = m.group(1).replace(" ", "_")

                # Get station metadata for use in reformatting product name
                station = self.get_station_info(request['stnm'])

                # If we found the station by the number, then the id will still
                # be in the title. Remove it.
                if station['id'].rstrip() in prod:
                    prod = prod.replace(station['id'].rstrip()+"_", "")

                # For international skewts, set the product name to
                # "Station_Name_CC" where CC is the two letter country code.
                # For US stations use "Station_Name_ST" where ST it the two
                # letter state code.
                if (station['country'] == 'US'):
                    prod += "_" + station['state']
                else:
                    prod += "_" + station['country']

            else:
                print("WARNING: Couldn't find product name. Setting to temp")
                prod = "temp"

        out.close()

        return(prod)

    def set_outfile_gif(self, request):
        platform = "SkewT"

        self.outfile_gif = "upperair." + platform + '.' + request['year'] + \
            request['month'] + request['begin'] + "00." + \
            self.get_prod(request) + ".gif"

    def get_outfile_gif(self):

        return(self.outfile_gif)

    def get_gif_url(self, request):

        url = "http://weather.uwyo.edu/upperair/images/"
        url += request['year']
        url += request['month']
        url += request['begin'] + "."
        url += request['stnm'] + ".skewt.parc.gif"

        return(url)

    def retrieve(self, request):

        # SKEWT's are downloaded in two steps.
        # The first request generates the skewt on the website and downloads an
        # HTML wrapper with a reference to the gif image that is still on the
        # website. The second request downloads the gif image.

        # Create first request URL from request metadata
        url = self.get_url(request)

        # Create output filename from request metadata
        self.set_outfile_html(request)

        # If in test mode, copy file from data dir to simulate download...
        if request['test'] is True:
            os.system('cp data/7267220190528122812.skewt ' +
                      '7267220190528122812.txt')

        # ...else download data
        else:
            status = self.rwget.get_data(url, self.get_outfile_html())

        # If site returned good html file and thus generated gif
        if status:

            # Download the gif image directly
            url = self.get_gif_url(request)

            # Create output filename from request metadata
            self.set_outfile_gif(request)
            outfile = self.get_outfile_gif()

            # Download gif image
            status = self.rwget.get_data(url, outfile)

            # Remove now-irrelevant html file
            os.system('rm ' + self.get_outfile_html())
            print('Removed ' + self.get_outfile_html())

            # If running in catalog mode, ftp files to catalog dir
            if request['catalog'] is True and status:
                userlib.catalog.to_ftp(outfile)

            return(self.get_outfile_gif())
