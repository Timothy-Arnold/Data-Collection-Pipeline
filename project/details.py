import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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
        Finds the Title of the movie
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
    def __init__(self, driver):
        self.driver = driver
        required_details = ["Title", "Tomatometer", "Audience Score", "US Box Office", "Release Date (Streaming)", "Age Rating", "Time of Scrape", "Image", "UUID"]
        initial_values = ["Unknown"] * 9
        self.details_dict = {required_details[i]: initial_values[i] for i in range(9)}

    def __extract_title(self):
        title_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board > h1")')
        title = title_location.text
        original_release_date_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board > p")')
        original_release_date = original_release_date_location.text[0:4]
        full_title = f"{title} ({original_release_date})"
        return full_title

    def __extract_scores(self):
        tomatometer_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board").shadowRoot.querySelector("div > div.scores-container > div.tomatometer-container > div > score-icon-critic").shadowRoot.querySelector("div > span.percentage")')
        tomatometer = tomatometer_location.text
        audience_score_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board").shadowRoot.querySelector("div > div.scores-container > div.audience-container > div > score-icon-audience").shadowRoot.querySelector("div > span.percentage")')
        audience_score = audience_score_location.text
        return tomatometer, audience_score

    def __extract_technical_data(self):
        details_table = self.driver.find_element(By.XPATH, '//ul[@class="content-meta info"]')
        categories = details_table.find_elements(By.XPATH, '//li[@class="meta-row clearfix"]')
        for category in categories:
            name = category.text.split(":")[0]
            if name == "Rating":
                age_rating_full = category.text.split(":")[1][1:]
                self.details_dict["Age Rating"] = age_rating_full.split()[0]
            if name == "Release Date (Streaming)":
                self.details_dict["Release Date (Streaming)"] = category.text.split(":")[1][1:]
            if name == "Box Office (Gross USA)":
                self.details_dict["US Box Office"] = category.text.split(":")[1][1:]
        return self.details_dict

    def __set_time_of_scrape(self):
        current_time = time.ctime()
        return current_time

    def __extract_img_data(self):
        img_location = self.driver.find_element(By.XPATH, '//img[@class="posterImage"]')
        img = img_location.get_attribute("src")
        return img

    def __assign_uuid(self):
        UUID = str(uuid.uuid4())
        return UUID

    def extract_all_data(self):
        self.details_dict["Tomatometer"] = Details.__extract_scores(self)[0]
        self.details_dict["Audience Score"] = Details.__extract_scores(self)[1]
        self.details_dict["Title"] = Details.__extract_title(self)
        self.details_dict = Details.__extract_technical_data(self)
        self.details_dict["Image"] = Details.__extract_img_data(self)
        self.details_dict["Time of Scrape"] = Details.__set_time_of_scrape(self)
        self.details_dict["UUID"] = Details.__assign_uuid(self)
        return self.details_dict

if __name__ == '__main__':
    chromeOptions = Options()
    chromeOptions.headless = False
    driver = webdriver.Chrome(options=chromeOptions)
    test_URL = "https://www.rottentomatoes.com/m/where_the_crawdads_sing"
    driver.get(test_URL)
    time.sleep(4)
    extraction = Details(driver)
    details_dict = extraction.extract_all_data()
    driver.quit()
    print(details_dict)