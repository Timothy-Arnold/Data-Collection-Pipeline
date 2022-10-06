# Data-Collection-Pipeline

This is a project to make a...

## Milestone 1

I chose the Amazon website to scrape laptop data from, since it shows a wide variety of brands of laptop and gives a varied dataset. Using Selenium I created methods within a class to navigate Amazon's pages, while collecting the links to each product on display (Around 300 links).
  
```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, URL = "https://www.amazon.co.uk/"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.link_list = []
    def open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(2)
    def input_search(self, search_string):
        search = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys(search_string)
        search.send_keys(Keys.RETURN)
        time.sleep(1)
    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(By.ID, "sp-cc-accept")
            accept_cookies_button.click()
        except:
            pass
    def get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "s-main-slot s-result-list s-search-results sg-row"]')
        product_list = product_container.find_elements(By.XPATH, '//div[@class = "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"]')
        for product in product_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        time.sleep(1)
    def next_page(self):
        next_button = self.driver.find_element(By.XPATH, '//a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        next_button.send_keys(Keys.RETURN)
        time.sleep(1)

def scrape():
    scrape = Scraper()
    scrape.open_webpage()
    scrape.accept_cookies()
    scrape.input_search("laptop")
    # Get first page's links
    scrape.get_links()
    for page in range(18):
        scrape.next_page()
        scrape.get_links()
    print(scrape.link_list)
    print(f'There are {len(scrape.link_list)} properties in this page')
    time.sleep(60)

if __name__ == '__main__':
    scrape()
```

## Milestone 2

For this milestone I created methods to scrape the text and image details off each amazon product's webpage. I stored these details in a dictionary, along with a unique UUID to identify each product. Getting the the technical details was a bit tricky since the table on amazon had inconsistent positioning for its variables, so I had to use a nested for loop to track the desired details. The for loop also has a check specifically for Resolution, since some products had variable name "Resolution", and others had variable name "Screen Resolution".

```python
class Details:
    def __init__(self, URL):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.driver.get(URL)
        self.required_details = ["Price", "Brand", "Standing screen display size", "Screen Resolution", "RAM Size", "Item Weight", "ASIN", "Image", "UUID"]
        self.initial_values = ["Unknown"] * 9
        self.details_dict = {self.required_details[i]: self.initial_values[i] for i in range(9)}

    def extract_text_data(self, URL):
        # Sometimes the first page opens with an error message, needs to be reloaded
        # possible_error_location = driver.find_element(By.XPATH, '//*[@class="celwidget"]')
        # possible_error = possible_error_location.find_element(By.XPATH, '//div[@class="a-alert-content"]')
        # print(possible_error.text)
        if EC.presence_of_element_located((By.XPATH, '//*[@class="a-alert-content"]')):
            self.driver.get(URL)
            time.sleep(1)
        
        price_location = self.driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]')
        price_pound = price_location.find_element(By.XPATH, '//span[@class="a-price-whole"]').text
        price_penny = price_location.find_element(By.XPATH, '//span[@class="a-price-fraction"]').text
        price = f"£{price_pound}.{price_penny}"

        self.details_dict["Price"] = price

        details_table = self.driver.find_element(By.XPATH, '//*[@id="productDetails_techSpec_section_1"]')
        name_list = details_table.find_elements(By.XPATH, '//th[@class = "a-color-secondary a-size-base prodDetSectionEntry"]')
        value_list = details_table.find_elements(By.XPATH, '//td[@class = "a-size-base prodDetAttrValue"]')
        
        for index_1 in range(len(name_list)):
            if name_list[index_1].text == "Resolution":
                self.details_dict["Screen Resolution"] = value_list[index_1].text
            for index_2 in range(1,7):
                if name_list[index_1].text == self.required_details[index_2]:
                    self.details_dict[self.required_details[index_2]] = value_list[index_1].text

        return self.details_dict

    def extract_img_data(self):
        img_location = self.driver.find_element(By.XPATH, '//*[@id="landingImage"]')
        img = img_location.get_attribute("src")
        return img

    def assign_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

def extract_all_data(URL):
    extraction = Details(URL)
    time.sleep(1)
    extraction.details_dict = extraction.extract_text_data(URL)
    extraction.details_dict["Image"] = extraction.extract_img_data()
    extraction.details_dict["UUID"] = extraction.assign_uuid()
    return extraction.details_dict
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

## Conclusions