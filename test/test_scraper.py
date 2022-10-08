from selenium import webdriver
from project.scraper import Scraper
import unittest

class ScraperTestCase(unittest.TestCase): 
    def setUp(self, URL = "https://www.amazon.co.uk/"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.link_list = []
    def test_scrape_all(self):
        minimum_length = 200
        print(Scraper.scrape_all(self))
        actual_length = len(Scraper.scrape_all(self))
        self.assertGreaterEqual(actual_length, minimum_length)
    def tearDown(self):
        self.driver.quit()

unittest.main()