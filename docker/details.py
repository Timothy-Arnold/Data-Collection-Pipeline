import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Details:
    '''
    This class is used to find all of the text and image data required from a movie's page on rottentomatoes.

    Parameters:
    ----------
    URL: str
        The URL of the movie's page on rottentomatoes.
    
    Attributes:
    ----------
    details_dict: dict
        The dictionary containing all the desired information about the movie

    Methods:
    -------
    extract_title()
        Finds the Title of the movie
    extract_scores()
        Finds the critic scores and audience scores
    extract_tabular_data()
        Finds the Age Rating, Streaming Release date and US Box Office of the movie from the table
    set_time_of_scrape()
        Finds the time at which the scrape was performed
    extract_img_data()
        Finds the url of the poster image of the movie
    assign_uuid()
        Generates a random uuid for the movie
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
        title = title_location.get_attribute("textContent")
        original_release_date_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board > p")')
        original_release_date = original_release_date_location.text[0:4]
        full_title = f"{title} ({original_release_date})".strip()
        return full_title

    def __extract_scores(self):
        tomatometer_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board").shadowRoot.querySelector("div > div.scores-container > div.tomatometer-container > div > score-icon-critic").shadowRoot.querySelector("div > span.percentage")')
        tomatometer = tomatometer_location.text
        audience_score_location = self.driver.execute_script('return document.querySelector("#topSection > div.thumbnail-scoreboard-wrap > score-board").shadowRoot.querySelector("div > div.scores-container > div.audience-container > div > score-icon-audience").shadowRoot.querySelector("div > span.percentage")')
        audience_score = audience_score_location.text
        return tomatometer, audience_score

    def __extract_tabular_data(self):
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
        self.details_dict["Title"] = Details.__extract_title(self)
        self.details_dict["Tomatometer"] = Details.__extract_scores(self)[0]
        self.details_dict["Audience Score"] = Details.__extract_scores(self)[1]
        self.details_dict = Details.__extract_tabular_data(self)
        self.details_dict["Image"] = Details.__extract_img_data(self)
        self.details_dict["Time of Scrape"] = Details.__set_time_of_scrape(self)
        self.details_dict["UUID"] = Details.__assign_uuid(self)
        # print(self.details_dict)
        return self.details_dict

if __name__ == '__main__':
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(options=chromeOptions)
    test_URL = "https://www.rottentomatoes.com/m/thor_ragnarok_2017"
    driver.get(test_URL)
    time.sleep(3)
    extraction = Details(driver)
    details_dict = extraction.extract_all_data()
    driver.quit()
    print(details_dict)