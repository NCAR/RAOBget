###############################################################################
# Use a pandas dataframe, matplotlib, and metpy to plot a skewt of the
# downloaded TEXT:LIST formatted RAOB data.
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas)

from metpy.plots import SkewT
from metpy.units import units


class Skewt():

    def __init__(self, app):
        """ Import link to GUI """
        self.app = app

    def read_data(self, datafile, mtp):
        """ Read in data from the downloaded TEXT:LIST-formatted RAOB """

        # Number of lines before title and column in files as downloaded from
        # the UWyo server.
        title_hdr_len = 3
        col_hdr_len = 6

        # For MTP data, the number of lines in the header is edited using
        # userlib.mtp.strip_html to maintain backward compatibility with the
        # VB6 code. So for the MTP data, set the number of header lines
        # differently than for data files read from the UWyo server and NOT
        # modified.
        if mtp:
            title_hdr_len = 1
            col_hdr_len = 4

        # Read in the title from the header.
        title = pd.read_fwf(datafile, header=title_hdr_len, nrows=1).columns

        # Remove the HTML
        self.title = title[0].replace('<H2>', '')
        self.title = self.title.replace('</H2>', '')

        # Read in the column names from the header. For a description, see:
        # http://weather.uwyo.edu/upperair/columns.html
        col_names = pd.read_fwf(datafile, header=col_hdr_len, nrows=1).columns
        col_names = col_names[0].split()

        # Read the data from the data file into a pandas dataframe
        # Only read in columns we need [P, T, Td], and skip header and footer
        # lines (identified by having letters or 2 or more dashes)
        header = re.compile(r'.*[A-Za-z-][A-Za-z-].*')

        # lambda function is failing with TypeError: argument of type
        # 'function' is not iterable so code workaround
        # rdat = pd.read_fwf(datafile+".plot",
        #                    skiprows=lambda x: x not in header.match(x),
        #                    usecols=[0, 2, 3], names=col_names)

        # Read in contents of data file
        f = open(datafile, 'r')
        data = f.readlines()
        f.close()

        # Create an empty data frame to hold data file
        rdat = pd.DataFrame(columns=col_names)

        # Loop through data and remove lines that match header, i.e. remove
        # header/footer.
        for line in data:
            if not header.match(line):
                # Skip lines with missing data
                if (len(line.split())) == len(col_names):
                    # Save good data lines to data frame
                    rdat = rdat.append(pd.DataFrame.from_records([tuple(
                                       line.split())], columns=col_names))

        return(rdat)

    def set_fig(self):
        """ Create a figure instance to hold the plot """
        self.fig = plt.figure(figsize=(9, 9))

    def create_skewt(self, rdat):
        """ Create the SkewT plot inside the figure instance """

        # Extract pressure from data
        P = rdat['PRES'].values * units.hPa

        # Extract temperature from data
        T = rdat['TEMP'].values * units.degC

        # Extract dewpt from data
        Td = rdat['DWPT'].values * units.degC

        skew = SkewT(self.fig, rotation=45)
        # Change to read in min/max from data arrays??
        skew.ax.set_ylim(1000, 100)
        skew.ax.set_xlim(-40, 80)
        skew.ax.set_title(self.title)
        skew.plot(P, T, 'r', linewidth=2)
        skew.plot(P, Td, 'g', linewidth=2)

        # Plot a zero degree isotherm
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

        # Add the relevant special lines
        skew.plot_dry_adiabats()
        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()

    def set_canvas(self):
        """ Link the canvas to the calling GUI (if extant) """
        # A canvas widget that displays the figure
        if self.app is not None:
            self.canvas = FigureCanvas(self.fig)

    def get_canvas(self):
        """ Return link to GUI """
        return(self.canvas)

    def clear(self):
        """ Clear a previous plot - ready to display new plot """
        self.fig.clear()

    def close(self):
        """ Be sure to close plots to free memory """
        plt.close()


if __name__ == "__main__":
    """
    This class can run independently on a TEXT:LIST file and create
    a free-standing plot window.

    Requires:
        input data file in UWyo TEXT:LIST format
    """

    # Run in MTP mode
    # datafile = "../../test/data/726722019052812.ctrl.mtp"
    # mtp = True

    # Run not in MTP mode (so could be default or CATALOG)
    datafile = "../../test/data/726722019052812.ctrl"
    mtp = False

    skewt = Skewt(None)
    rdat = skewt.read_data(datafile, mtp)
    skewt.set_fig()
    skewt.set_canvas()
    skewt.create_skewt(rdat)
    plt.show()
    skewt.close()
    skewt.clear()
