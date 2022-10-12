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