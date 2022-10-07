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

def do_whole_extraction(URL):
    extraction = Details(URL)
    extraction.extract_all_data()
    print(extraction.details_dict)
    return extraction.details_dict

# Tests
# "https://www.amazon.co.uk/Lenovo-IdeaPad-Notebook-DDR4-SDRAM-802-11ax/dp/B0B4T3H79X/ref=sr_1_40?crid=2E1T6L3YWDF37&keywords=laptop&qid=1664901597&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C162&sr=8-40")
# "https://www.amazon.co.uk/Razer-Blade-17-Display-Chamber/dp/B09Q6CVSW3/ref=sr_1_3?keywords=laptop&qid=1664886688&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-3&th=1"
# "https://www.amazon.co.uk/ASUS-Vivobook-E510MA-Microsoft-included/dp/B09X63GB82/ref=sr_1_10?crid=2GEDTE88DVY5K&keywords=laptop&qid=1664898174&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C62&sr=8-10&th=1")
URL = "https://www.amazon.co.uk/HUAWEI-Matebook-16s-i9-12900H-Processor/dp/B0B56RJGSR/ref=sr_1_19?keywords=laptop&qid=1664919140&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-19"

if __name__ == '__main__':
    do_whole_extraction(URL)