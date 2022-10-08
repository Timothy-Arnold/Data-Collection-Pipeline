from project.scraper import Scraper
import unittest

class ScraperTestCase(unittest.TestCase): 

    def setUp(self, URL = "https://www.amazon.co.uk/"):
        scrape = Scraper()     
        self.link_list = scrape.scrape_all()

    def test_scrape_all(self):
        minimum_length = 200
        actual_length = len(self.link_list)
        self.assertGreaterEqual(actual_length, minimum_length)
        non_website_list = list(filter(lambda x: x[:8] != 'https://', self.link_list))
        self.assertEqual(len(non_website_list), 0)

if __name__ == '__main__':   
    unittest.main(verbosity=2)