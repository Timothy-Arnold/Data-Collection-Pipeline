from project.details import Details
import unittest

class DetailsTestCase(unittest.TestCase):

    def setUp(self, URL = ""):
        extraction = Details(URL)
        detail_dict = extraction.extract_all_data("https://www.box.co.uk/Acer-Aspire-1-Microsoft-365-Intel-Cele_3213588.html")
        self.values = detail_dict.values()

    def test_extract_all_data(self):
        expected_length = 8
        actual_length = len(self.values)
        self.assertEqual(expected_length, actual_length)
        self.assertNotIn("Unknown", self.values)

if __name__ == '__main__':       
    unittest.main(verbosity=2)