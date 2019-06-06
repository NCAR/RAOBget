###############################################################################
# Code specific to retrieving GIF:SKEWT formatted data from the University of
# Wyoming Radiosonde Archive.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os
from rwget import RAOBwget


class RAOBgifskewt:

    def __init__(self):

        self.rwget = RAOBwget()

    def set_outfile_html(self, request):
        self.outfile_html = request['stnm'] + request['year'] + \
            request['month'] + request['begin'] + request['end'] + \
            ".html"

    def get_outfile_html(self):

        return(self.outfile_html)

    def set_outfile_gif(self, request):
        platform = "SkewT"
        # Get prod from where??? - maybe from the HTML file?
        prod = "test"
        self.outfile_gif = "upperair." + platform + request['year'] + \
            request['month'] + request['begin'] + "." + prod + ".gif"

    def get_outfile_gif(self):

        return(self.outfile_gif)

    def get_gif_url(self, request):

        url = "http://weather.uwyo.edu/upperair/images/"
        url += request['year']
        url += request['month']
        url += request['begin'] + "."
        url += request['stnm'] + ".skewt.parc.gif"
        print(url)

        return(url)

    def retrieve(self, request):

        # SKEWT's are downloaded in two steps.
        # The first request generates the skewt on the website and downloads an
        # HTML wrapper with a reference to the gif image that is still on the
        # website. The second request downloads the gif image.

        # Create first request URL from request metadata
        url = self.rwget.get_url(request)

        # Create output filename from request metadata
        self.set_outfile_html(request)

        # If in test mode, copy file from data dir to simulate download...
        if request['test'] is True:
            os.system('cp data/7267220190528122812.skewt ' +
                      '7267220190528122812.txt')

        # ...else download data
        else:
            self.rwget.get_data(url, self.get_outfile_html())

        # Now download the gif image directly
        url = self.get_gif_url(request)

        # Create output filename from request metadata
        self.set_outfile_gif(request)

        self.rwget.get_data(url, self.get_outfile_gif())

        return(self.get_outfile_gif())
