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

if __name__ == '__main__':   
    unittest.main()