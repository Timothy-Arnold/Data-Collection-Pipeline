import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import uuid

class Details:
    '''
    This class is used to find all of the text and image data required from a laptop product page on Amazon.

    Parameters:
    ----------
    URL: str
        The URL of the laptop's page on Amazon.
    
    Attributes:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the laptop

    Methods:
    -------
    extract_text_data()
        Finds all the desired text data on the webpage
    extract_img_data()
        Finds the first display image of the laptop
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
        self.required_details = ["Price", "Brand", "Standing screen display size", "Screen Resolution", "RAM Size", "Item Weight", "ASIN", "Image", "UUID"]
        self.initial_values = ["Unknown"] * 9
        self.details_dict = {self.required_details[i]: self.initial_values[i] for i in range(9)}

    def __extract_text_data(self):
        if EC.presence_of_element_located((By.XPATH, '//*[@class="a-alert-content"]')):
            self.driver.get(self.URL)
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

    def __extract_img_data(self):
        img_location = self.driver.find_element(By.XPATH, '//*[@id="landingImage"]')
        img = img_location.get_attribute("src")
        return img

    def __assign_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def extract_all_data(self):
        self.details_dict = Details.__extract_text_data(self)
        self.details_dict["Image"] = Details.__extract_img_data(self)
        self.details_dict["UUID"] = Details.__assign_uuid(self)
        return self.details_dict

test_URL = "https://www.amazon.co.uk/CHUWI-GemiBook-2160x1440-Intel-Processor/dp/B08NPCBGSZ/ref=sr_1_12?crid=3E23J6SE3Y156&keywords=laptop&qid=1665235352&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C95&sr=8-12"

if __name__ == '__main__':
    extraction = Details(test_URL)
    extraction.extract_all_data()
    print(extraction.details_dict)