from project.details import Details
import unittest

class DetailsTestCase(unittest.TestCase):

    def setUp(self, URL = "https://www.amazon.co.uk/CHUWI-GemiBook-2160x1440-Intel-Processor/dp/B08NPCBGSZ/ref=sr_1_12?crid=3E23J6SE3Y156&keywords=laptop&qid=1665235352&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C95&sr=8-12"):
        extraction = Details(URL)
        detail_dict = extraction.extract_all_data()
        self.values = detail_dict.values()

    def test_extract_all_data(self):
        expected_length = 9
        actual_length = len(self.values)
        self.assertEqual(expected_length, actual_length)
        self.assertNotIn("Unknown", self.values)

if __name__ == '__main__':       
    unittest.main()