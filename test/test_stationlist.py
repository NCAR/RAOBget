import unittest
import os

from lib.stationlist import RAOBstation_list


class TestRAOBstation_list(unittest.TestCase):

    def setUp(self):

        self.stnlist1 = "../config/station-query.html"
        # stations from station-query.html
        self.stn1 = {
            '01003': {
                'id': '        ', 'number': '01003',
                'description': 'HORNSUND RIVER                ',
                'state': '--', 'country': 'NO',
                'lat': ' 7700', 'lon': '  1550', 'elev': '   12'},
            '01015': {
                'id': '        ', 'number': '01015',
                'description': 'HEKKINGEN (LGT-H)             ',
                'state': '--', 'country': 'NO',
                'lat': ' 6960', 'lon': '  1783', 'elev': '   14'},
            'BJC':  {
                'id': 'BJC     ', 'number': '99999',
                'description': 'BROOMFIELD/JEFFCO             ',
                'state': 'CO', 'country': 'US',
                'lat': ' 3992', 'lon': '-10512', 'elev': ' 1724'},
            'GJT':  {
                'id': 'GJT     ', 'number': '72476',
                'description': 'GRAND JUNCTION                ',
                'state': 'CO', 'country': 'US',
                'lat': ' 3912', 'lon': '-10853', 'elev': ' 1475'},
        }

        self.stnlist2 = "../config/snstns.tbl"
        # stations from snstns.tbl
        self.stn2 = {
            'GJT':  {
                'id': 'GJT     ', 'number': '72476',
                'description': 'GRAND_JUNCTION/WALKER         ',
                'state': 'CO', 'country': 'US',
                'lat': ' 3911', 'lon': '-10853', 'elev': ' 1475'},
            '72476':  {
                'id': 'GJT     ', 'number': '72476',
                'description': 'GRAND_JUNCTION/WALKER         ',
                'state': 'CO', 'country': 'US',
                'lat': ' 3911', 'lon': '-10853', 'elev': ' 1475'},
        }
        
    def get_stns(self):

        assert(os.path.isfile(self.station_list_file))

        self.stationList = RAOBstation_list()
        self.stationList.read(self.station_list_file)

    def test_by_index(self):
        # Test first station list
        self.station_list_file = self.stnlist1
        self.get_stns()

        station = self.stationList.get_by_stnm('01003')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn1['01003'])

        station = self.stationList.get_by_stnm('01015')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn1['01015'])

    def test_by_index2(self):
        # Test second station list
        self.station_list_file = self.stnlist2
        self.get_stns()

        station = self.stationList.get_by_stnm('72476')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn2['72476'])

    def test_by_id(self):
        # Test first station list
        self.station_list_file = self.stnlist1
        self.get_stns()

        station = self.stationList.get_by_id('BJC')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn1['BJC'])

        station = self.stationList.get_by_id('GJT')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn1['GJT'])

    def test_by_id2(self):
        # Test second station list
        self.station_list_file = self.stnlist2
        self.get_stns()

        station = self.stationList.get_by_id('GJT')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0], self.stn2['GJT'])


if __name__ == "__main__":

    unittest.main()
