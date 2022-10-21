from os import link
import random
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
        number_of_pages = 3
        scrape = Scraper(number_of_pages)
        link_list = scrape.scrape_all()
        self.assertEqual(len(link_list), 21 * number_of_pages)
        random_index = random.randint(0, 21 * number_of_pages - 2)
        random_link = link_list[random_index]
        driver = webdriver.Chrome()
        driver.get(random_link)
        try:
            extraction = Details(driver)
            details_dict = extraction.extract_all_data()
        except:
            random_link = link_list[random_index + 1]
            driver.get(random_link)
            try:
                extraction = Details(driver)
                details_dict = extraction.extract_all_data()
            except Exception as e:
                print("Two consecutive links didn't work: ", e)
        driver.quit()
        store = Storage(details_dict)
        store.download_all_data()
        product_id = details_dict["Stock Code"]
        image_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{product_id}/images/{product_id}.jpg"
        self.assertIsFile(pl.Path(image_path))

if __name__ == '__main__':   
    unittest.main(verbosity=2)