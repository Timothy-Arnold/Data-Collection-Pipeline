import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import uuid

from project.details import Details
import unittest

URL = "https://www.amazon.co.uk/ASUS-Vivobook-E510MA-Microsoft-included/dp/B09X63GB82/ref=sr_1_10?crid=2GEDTE88DVY5K&keywords=laptop&qid=1664898174&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C62&sr=8-10&th=1"

class DetailsTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.driver.get(URL)
        time.sleep(1)
        self.required_details = ["Price", "Brand", "Standing screen display size", "Screen Resolution", "RAM Size", "Item Weight", "ASIN", "Image", "UUID"]
        self.initial_values = ["Unknown"] * 9
        self.details_dict = {self.required_details[i]: self.initial_values[i] for i in range(9)}
    def test_extract_all_data(self):
        expected_length = 9
        print(Details.extract_all_data(self))
        actual_length = len(Details.extract_all_data(self))
        self.assertEqual(expected_length, actual_length)
    def test_extract_all_data_2(self):
        values = Details.extract_all_data(self).values()
        self.assertNotIn("Unknown", values)
        
unittest.main()