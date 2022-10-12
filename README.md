# Data-Collection-Pipeline

This is a project to make a web-scraper for scraping information about laptops from box.co.uk. It finds the details of 420 laptops on box and stores the information in my personal directory.

## Milestone 1

I chose the box website to scrape laptop data from, since it shows a wide variety of brands of laptop and gives a varied dataset. Using Selenium I created methods within a class to navigate box's pages, while collecting the links to each product on display (420 links).
  
```python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Scraper:
    '''
    This class is used to collect all the URLs of product listings on box for the first 20 pages of laptops.

    Parameters:
    ----------
    URL: str
        The URL of box's laptop section
    
    Attributes:
    ----------
    link_list: list
        The list of URLs of all the product pages

    Methods:
    -------
    open_webpage()
        Opens the Amazon front page
    get_links()
        Finds all the product links in the page and stores them in the list
    go_to_page(page_number)
        Moves to the given page number
    scrape_all()
        Collects the product links from all 20 pages on box and stores them in the list.
    '''
    def __init__(self, URL = "https://www.box.co.uk/laptops"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.link_list = []
        time.sleep(1)

    def __open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(3)

    def __get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "product-list  "]')
        product_list_1 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item "]')
        product_list_2 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item middle"]')
        product_list = product_list_1 + product_list_2
        for product in product_list:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        time.sleep(1)

    def __go_to_page(self, page_number):
        self.URL = f"https://www.box.co.uk/laptops/page/{page_number}"
        self.driver.get(self.URL)
        time.sleep(1)

    def scrape_all(self, number_of_pages = 20):
        Scraper.__open_webpage(self)
        # Get the first page's links
        Scraper.__get_links(self)
        for page_number in range(2, number_of_pages + 1):
            Scraper.__go_to_page(self, page_number)
            Scraper.__get_links(self)
        return self.link_list
        time.sleep(10)

if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_all(20)
    print(scrape.link_list)
    print(f'There are {len(scrape.link_list)} properties in this page')
```

## Milestone 2

For this milestone I created methods to scrape the text and image details off each product's webpage. I stored these details in a dictionary, along with a unique UUID to identify each product. Getting the technical details was a bit tricky since the table on box had inconsistent positioning for its variables, so I had to use multiple if statements within a for loop to track the desired details.

```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import uuid

class Details:
    '''
    This class is used to find all of the text and image data required from a laptop product page on box.

    Parameters:
    ----------
    URL: str
        The URL of the laptop's page on box.
    
    Attributes:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the laptop

    Methods:
    -------
    extract_price()
        Finds the price of the laptop
    click_specifications()
        Clicks the specifications tab on the laptop page
    extract_technical_data()
        Finds the four pieces of technical data in the specifications table
    extract_stock_code()
        Finds the stock code of the laptop
    extract_img_data
        Finds the url of the first image of the laptop
    assign_uuid()
        Generates a random uuid for the laptop
    extract_all_data()
        Puts all the above data into the details dictionary
    '''
    def __init__(self, URL):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.driver.get(URL)
        time.sleep(1)
        self.required_details = ["Price", "Screen Size", "Resolution", "Storage", "RAM", "Stock Code", "Image", "UUID"]
        self.initial_values = ["Unknown"] * 8
        self.details_dict = {self.required_details[i]: self.initial_values[i] for i in range(8)}

    def __extract_price(self):
        price = self.driver.find_element(By.XPATH, '//span[@class="pq-price"]').text
        return price

    def __click_specifications(self):
        self.driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        spec_button = self.driver.find_element(By.XPATH, '//p[@data-id = "Specifications"]')
        spec_button.click()
        time.sleep(1)

    def __extract_technical_data(self):

        details_table = self.driver.find_element(By.XPATH, '//*[@id="p-specifications"]')
        specs = details_table.find_elements(By.XPATH, '//td[@class = "speccol"]')
        names = specs[::2]
        values = specs[1::2]
        for index_1 in range(len(names)):
            if names[index_1].text == "Screen":
                screen_specs = values[index_1].text
                screen_size = screen_specs.split('"')[0]
                self.details_dict["Screen Size"] = screen_size + " Inches"
            if names[index_1].text == "Screen Resolution":
                self.details_dict["Resolution"] = values[index_1].text
            if names[index_1].text == "Total Storage":
                total_storage = values[index_1].text
                storage_amount = total_storage[:total_storage.index('B') + 1]
                self.details_dict["Storage"] = storage_amount
            if names[index_1].text == "RAM":
                ram_full = values[index_1].text
                ram_amount = ram_full[:ram_full.index('B') + 1]
                self.details_dict["RAM"] = ram_amount

        return self.details_dict
    
    def __extract_stock_code(self):
        stock_code_string = self.driver.find_element(By.XPATH, '//p[@class="p-reference p-mancode"]').text
        stock_code = stock_code_string[stock_code_string.index(':') + 2: stock_code_string.index('|') - 1]
        return stock_code

    def __extract_img_data(self):
        img_location = self.driver.find_element(By.XPATH, '//img[@class="p-image-button pq-images-small pq-images-show"]')
        img = img_location.get_attribute("src")
        return img

    def __assign_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def extract_all_data(self):
        self.details_dict["Price"] = Details.__extract_price(self)
        Details.__click_specifications(self)
        self.details_dict = Details.__extract_technical_data(self)
        self.details_dict["Stock Code"] = Details.__extract_stock_code(self)
        self.details_dict["Image"] = Details.__extract_img_data(self)
        self.details_dict["UUID"] = Details.__assign_uuid(self)
        return self.details_dict

if __name__ == '__main__':
    test_URL = "https://www.box.co.uk/Apple-MacBook-Pro-14-M1-Pro-Chip-16GB-R_3986819.html"
    extraction = Details(test_URL)
    extraction.extract_all_data()
    print(extraction.details_dict)
```

I also created data storage functions to store product details, as well as a saved image, in my own directory.

```python
import os

path = "C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data"
if not os.path.exists(path):
    os.mkdir(path)

import details
import json

def create_product_folder(URL):
    path = "C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data"
    details_dict = details.extract_all_data(URL)
    print(details_dict)
    product_id = details_dict["ASIN"]
    product_path = path + f"/{product_id}"
    print(product_path)
    print(product_id)
    if not os.path.exists(product_path):
        os.mkdir(product_path)
    with open(f"{product_path}/data.json", 'w') as fp:
        json.dump(details_dict, fp)

import requests

def create_image_folder(details_dict):
    product_id = details_dict["ASIN"]
    image_url = details_dict["Image"]
    path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{product_id}"
    image_folder_path = path + f"/images"
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)
    
    image_file_path = image_folder_path + f"/{product_id}"
    print(image_file_path)
    image_data = requests.get(image_url).content
    with open(image_file_path + '.jpg', 'wb') as handler:
        handler.write(image_data)
```
## Milestone 3

In this milestone I created unit tests for each of my project's 3 main files. The Scraper test made sure the list of links were all from the box website:

```python
from project.scraper import Scraper
import unittest

class ScraperTestCase(unittest.TestCase): 

    def setUp(self, URL = "https://www.box.co.uk/laptops"):
        scrape = Scraper()     
        self.link_list = scrape.scrape_all()

    def test_scrape_all(self):
        non_website_list = list(filter(lambda x: x[:22] != 'https://www.box.co.uk/', self.link_list))
        self.assertEqual(len(non_website_list), 0)

if __name__ == '__main__':   
    unittest.main(verbosity=2)
```
The Details test made sure that the outputted dictionary had all 8 required details, and none of them were left unknown:

```python
from project.details import Details
import unittest

class DetailsTestCase(unittest.TestCase):

    def setUp(self, URL = ""):
        extraction = Details(URL)
        detail_dict = extraction.extract_all_data("https://www.box.co.uk/Acer-Aspire-1-Microsoft-365-Intel-Cele_3213588.html")
        self.values = detail_dict.values()

    def test_extract_all_data(self):
        expected_length = 8
        actual_length = len(self.values)
        self.assertEqual(expected_length, actual_length)
        self.assertNotIn("Unknown", self.values)

if __name__ == '__main__':       
    unittest.main(verbosity=2)
```
And the Data storage test checked to see if all the information was successfully stored in my personal directory:

```python
from project.data_storage import Storage
import unittest
import pathlib as pl

class StorageTestCase(unittest.TestCase):

    def setUp(self, details_dict = {'Price': '£312.49', 'Screen Size': '12 Inches', 'Resolution': '1366 x 912', 'Storage': '32GB', 'RAM': '4GB', 'Stock Code': '6520758', 'Image': 'https://www.box.co.uk/image?id=4539297&quality=90&maxwidth=760&maxheight=520', 'UUID': 'f30001ea-4088-4ccc-bf36-871bb272713f'}):
        store = Storage(details_dict)
        store.download_all_data()
        self.product_id = details_dict["Stock Code"]
        self.image_url = details_dict["Image"]
        self.product_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{self.product_id}/"

    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {path}")

    def assertIsFolder(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError(f"Folder does not exist: {path}")

    def test_download_all_data(self):
        path = self.product_path
        path_1 = path
        path_2 = path + "data.json"
        path_3 = path + "images/"
        path_4 = path + f"images/{self.product_id}.jpg"
        self.assertIsFolder(pl.Path(path_1))
        self.assertIsFile(pl.Path(path_2))
        self.assertIsFolder(pl.Path(path_3))
        self.assertIsFile(pl.Path(path_4))

if __name__ == '__main__':      
    unittest.main(verbosity=2)
```

## Conclusions