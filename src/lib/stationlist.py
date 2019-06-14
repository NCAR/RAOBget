###############################################################################
#
# This python dictionary stores the list of stations available via the
# University of Wyoming Radiosonde data archive. The station identifier (id or
# number) is used in the retrieval URL, e.g.
#   http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&STNM=72672...
#
# Written in Python 3
#
# COPYRIGHT:   University Corporation for Atmospheric Research, 2019
###############################################################################
import os

RAOBstation = {
        'id': "",           # 8-character station identifier
        'number': "",       # 5-digit station number
        'description': "",  # 30-character station description
        'state': "",        # 2-character state abbreviation
        'country': "",      # 2-character country abboreviation
        'lat': "",          # 5-digit latitiude (+-degrees.hundredths)
        'lon': "",          # 6-digit latitiude (+-degrees.hundredths)
        'elev': "",         # 5 digit elevation (meters)
}


class RAOBstation_list:

    def __init__(self):
        self.station = RAOBstation
        self.station_list = []

    def read(self, station_list_file):

        # Make sure station_list_file exists
        if not os.path.isfile(station_list_file):
            print("ERROR: station list file " + station_list_file +
                  " doesn't exist")
            exit(1)

        infile = open(station_list_file)
        for line in infile:

            # Skip HTML/XML
            if (line[0] != '<'):

                # Parse line and put into dictionary
                self.station['id'] = line[0:8]
                self.station['number'] = line[10:15]
                self.station['description'] = line[16:46]
                self.station['state'] = line[49:51]
                self.station['country'] = line[52:54]
                self.station['lat'] = line[55:60]
                self.station['lon'] = line[61:67]
                self.station['elev'] = line[68:73]

                # Copy dictionary into array (so get a copy, not a pointer)
                self.station_list.append(self.station.copy())

                # print(line.rstrip().split())

        infile.close()

    def get_by_id(self, stnid):

        # ID need to be 8 chars so right pad with spaces if needed
        if (len(stnid) < 8):
            stnid = stnid.ljust(8)

        return(list(filter(lambda station: station['id'] == stnid,
               self.station_list)))

    # Select station by station number
    def get_by_stnm(self, number):

        return(list(filter(lambda station: station['number'] == number,
               self.station_list)))


if __name__ == "__main__":
    # Older GEMPAK list from MJ
    #station_list_file = "../../config/station-query.html"

    # GEMPAK list from Larry Ooolman as of 2019. This is the list he uses with
    # the UWyo website.
    station_list_file = "../../config/snstns.tbl"

    stationList = RAOBstation_list()
    stationList.read(station_list_file)
