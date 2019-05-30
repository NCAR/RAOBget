import unittest

from stationlist import RAOBstation_list

class TestRAOBstation_list(unittest.TestCase):

    def setUp(self):

        self.stn = {
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

        }

        station_list_file = "station-query.html"

        self.stationList = RAOBstation_list()
        self.stationList.read(station_list_file)


    def test_by_index(self):
        station = self.stationList.get_by_stnm('01003')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0],self.stn['01003'])

        station = self.stationList.get_by_stnm('01015')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0],self.stn['01015'])

    def test_by_id(self):
        station = self.stationList.get_by_id('BJC')
        self.assertEqual(len(station), 1)
        self.assertDictEqual(station[0],self.stn['BJC'])

if __name__ == "__main__":

    unittest.main()
