import unittest
from project.details import Details
from selenium import webdriver

class DetailsTestCase(unittest.TestCase):

    def setUp(self, URL = ""):
        driver = webdriver.Chrome()
        test_URL = "https://www.box.co.uk/Acer-Aspire-1-Microsoft-365-Intel-Cele_3213588.html"
        driver.get(test_URL)
        extraction = Details(driver)
        detail_dict = extraction.extract_all_data()
        self.values = detail_dict.values()

    def test_extract_all_data(self):
        expected_length = 8
        actual_length = len(self.values)
        self.assertEqual(expected_length, actual_length)
        self.assertNotIn("Unknown", self.values)

if __name__ == '__main__':       
    unittest.main(verbosity=2)