import random
import re
import unittest
import pathlib as pl
import test.test_scraper
import test.test_details
import test.test_data_storage
from project.details import Details
from project.scraper import Scraper
from project.data_storage import Storage
from selenium import webdriver

class ProjectTestCase(unittest.TestCase):
    
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {path}")

    def test_project(self):
        scrape = Scraper()
        link_list = scrape.scrape_all()
        self.assertEqual(len(link_list), 210)
        random_index = random.randint(0, 209)
        random_link = link_list[random_index]
        driver = webdriver.Chrome()
        driver.get(random_link)
        extraction = Details(driver)
        details_dict = extraction.extract_all_data()
        driver.quit()
        store = Storage(details_dict)
        store.download_all_data()
        movie_title_underscores = details_dict["Title"].replace(" ", "_").replace("/", "_")
        movie_title = re.sub('[:;!?]', '', movie_title_underscores)
        image_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{movie_title}/images/{movie_title}.jpg"
        self.assertIsFile(pl.Path(image_path))

if __name__ == '__main__':   
    unittest.main(verbosity=2)