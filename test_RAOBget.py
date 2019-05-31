import unittest

from RAOBget import RAOBget


class TestRAOBstation_list(unittest.TestCase):

    def setUp(self):

        self.raob = RAOBget()

    def test_TEXT_LIST(self):

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
