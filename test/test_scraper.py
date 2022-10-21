import unittest
from project.scraper import Scraper

class ScraperTestCase(unittest.TestCase): 

    def setUp(self, URL = "https://www.box.co.uk/laptops"):
        scrape = Scraper()     
        self.link_list = scrape.scrape_all()

    def test_scrape_all(self):
        self.assertEqual(len(self.link_list), 315)
        non_website_list = list(filter(lambda x: x[:22] != 'https://www.box.co.uk/', self.link_list))
        self.assertEqual(len(non_website_list), 0)

if __name__ == '__main__':   
    unittest.main(verbosity=2)