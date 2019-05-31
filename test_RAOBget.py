#!/usr/local/bin/python3
import unittest

from RAOBget import RAOBget


# Set default values for testing that match test data.
class options():
    region = 'North America'
    raobtype = 'TEXT:LIST'
    year = "2019"
    month = "05"
    bday = "28"
    bhr = "12"
    eday = "28"
    ehr = "12"
    stnm = "72672"


class TestRAOBstation_list(unittest.TestCase):

    def setUp(self):

        self.raob = RAOBget()

        # Set requested station to default values
        self.option = options()

        self.raob.set_type(self.option)
        self.raob.set_region(self.option)
        self.raob.set_year(self.option)
        self.raob.set_month(self.option)
        self.raob.set_begin(self.option)
        self.raob.set_end(self.option)
        self.raob.set_stnm(self.option)

    def test_TEXT_LIST(self):

        ctrlurl = "http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&" + \
                  "TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&" + \
                  "STNM=72672"

        url = self.raob.get_url_textlist()
        self.assertEqual(url, ctrlurl)

        outfile = self.raob.retrieve_textlist()

        # Compare retrieved text file to control file
        ctrlfile = "data/726722019052812.ctrl"
        with open(ctrlfile) as ctrl, open(outfile) as out:
            self.assertTrue([row1 for row1 in ctrl] == [row for row in out],
                            "files " + ctrlfile + " and " + outfile +
                            " differ ")
        ctrl.close()
        out.close()


if __name__ == "__main__":

    unittest.main()
