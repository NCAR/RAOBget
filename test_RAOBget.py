#!/usr/local/bin/python3
import unittest
import os

from RAOBget import RAOBget
from textlist import RAOBtextlist


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
    rsl = ""
    test = False
    mtp = False


class TestRAOBget(unittest.TestCase):

    def setUp(self):

        self.raob = RAOBget()

        # Set requested station to default values
        self.option = options()

        self.raob.set_prov(self.option)
        self.raob.set_stnm(self.option)

    def test_RAOB_set(self):
        request = self.raob.get_request()
        self.assertEqual(request['region'], self.option.region)
        self.assertEqual(request['raobtype'], self.option.raobtype)
        self.assertEqual(request['year'], self.option.year)
        self.assertEqual(request['month'], self.option.month)
        self.assertEqual(request['begin'],
                         self.option.bday + self.option.bhr)
        self.assertEqual(request['end'], self.option.eday + self.option.ehr)
        self.assertEqual(request['stnm'], self.option.stnm)

    def get_data(self):

        textlist = RAOBtextlist()

        ctrlurl = "http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&" + \
                  "TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&" + \
                  "STNM=72672"

        request = self.raob.get_request()
        url = textlist.get_url_textlist(request)
        self.assertEqual(url, ctrlurl)

        outfile = textlist.retrieve(request)

        return(outfile)

    def test_TEXT_LIST(self):

        # Remove files if we downloaded them before
        if os.path.isfile("7267220190528122812.txt"):
            os.system('rm 7267220190528122812.txt')

        outfile = self.get_data()
        print("\n" + outfile)

        # Compare retrieved text file to control file
        ctrlfile = "data/7267220190528122812.ctrl"
        with open(ctrlfile) as ctrl, open(outfile) as out:
            self.assertTrue([row1 for row1 in ctrl] == [row for row in out],
                            "files " + ctrlfile + " and " + outfile +
                            " differ ")
        ctrl.close()
        out.close()

    def test_mtp(self):

        # Remove files if we downloaded them before
        if os.path.isfile("726722019052812.txt"):
            os.system('rm 726722019052812.txt')

        self.option.mtp = True
        self.raob.set_prov(self.option)

        outfile = self.get_data()

        # Compare files with HTML stripped
        ctrlfile = "data/726722019052812.ctrl.mtp"
        mtpfile = "mtp/" + outfile
        with open(ctrlfile) as ctrl, open(mtpfile) as out:
            self.assertTrue([row1 for row1 in ctrl] == [row for row in out],
                            "files " + ctrlfile + " and " + mtpfile +
                            " differ ")
        ctrl.close()
        out.close()

    def test_rsl(self):
        ctrlstnlist = ['89611', 'ASLH', 'DNR', 'GJT', 'LKN', 'NCRG', 'NFFN',
                       'NKX', 'NSTU', 'NWWN', 'NZNV', 'NZPP', 'NZRN', 'NZWP',
                       'NZHK', 'NZLD', 'OAK', 'PHLI', 'PHTO', 'PKMJ', 'PTKK',
                       'PTPN', 'REV', 'SLC', 'VBG', 'VEF', 'YBBN', 'YBRK',
                       'YBTL', 'YMHB', 'YMMG', 'YMMQ', 'YMML', 'YSNF', 'YSWM']
        self.option.rsl = "data/DEEPWAVE.RSL"
        stnlist = self.raob.read_rsl(self.option)
        self.assertListEqual(stnlist, ctrlstnlist)

    def tearDown(self):

        # Remove downloaded file since it's just for testing
        if os.path.isfile("7267220190528122812.txt"):
            os.system('rm 7267220190528122812.txt')
        if os.path.isfile("726722019052812.txt"):
            os.system('rm 726722019052812.txt')
        if os.path.isfile("mtp/726722019052812.txt"):
            os.system('rm mtp/726722019052812.txt')


if __name__ == "__main__":

    unittest.main()
