import test.test_scraper
import test.test_details
import test.test_data_storage
from project.scraper import Scraper
from project.details import Details
from project.data_storage import Storage
import pathlib as pl
import unittest
import random

class ProjectTestCase(unittest.TestCase):
    
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {path}")

    def test_project(self):
        scrape = Scraper()
        link_list = scrape.scrape_all()
        random_link = random.choice(link_list)
        extraction = Details(random_link)
        details_dict = extraction.extract_all_data()
        store = Storage(details_dict)
        store.download_all_data()
        product_id = details_dict["Stock Code"]
        image_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{product_id}/images/{product_id}.jpg"
        self.assertIsFile(pl.Path(image_path))

if __name__ == '__main__':   
    unittest.main(verbosity=2)