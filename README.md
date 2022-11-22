# Data-Collection-Pipeline

This is a project to make a web-scraper for scraping information about movies from rottentomatoes. It finds the details of the 210 most popular movies at home on rottentomatoes and stores the information in my personal directory.

## Milestone 1

I chose the rottentomatoes website to scrape movie data from, since it shows a wide variety of movies and has a lot of details about each movie. Using Selenium I created methods within a class to navigate the rottentomatoes "Most Popular" movie page, and get the URL's of the top 210 movies' pages.
  
```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper:
    '''
    This class is used to collect all the URLs of the first 210 movies on rottentomatoes' "Most Popular Movies at Home" page'

    Parameters:
    ----------
    URL: str
        The URL of rottentomatoes' "Most Popular Movies at Home" page
    
    Attributes:
    ----------
    link_list: list
        The list of URLs of all the movie pages' URLs
    number_of_pages: int
        The number of times the "Load more" button is clicked, to view more movies

    Methods:
    -------
    open_webpage()
        Opens the rottentomatoes "Most Popular Movies at Home" page
    click_load_more()
        Clicks the load more button at the bottom of the page to show more movies
    get_links()
        Finds all the movie links in the page and stores them in the list
    scrape_all()
        Collects the movie links from the whole extended page and stores them in the list.
    '''
    def __init__(self, number_of_load_more_clicks=2):
        chromeOptions = Options()
        chromeOptions.headless = True
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.link_list = []
        self.number_of_load_more_clicks = number_of_load_more_clicks
        time.sleep(2)

    def __open_webpage(self):
        self.driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=5")
        time.sleep(2)

    def __click_load_more(self):
        load_more_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Load more")]')
        load_more_button.click()
        time.sleep(2)

    def __get_links(self):
        print("Getting Links!")
        movie_container = self.driver.find_element(By.XPATH, '//div[@class = "discovery-tiles"]')
        movie_list = movie_container.find_elements(By.XPATH, '//a[@class = "js-tile-link"]')
        for movie in movie_list:
            # a_tag = movie.find_element(By.TAG_NAME, 'a')
            link = movie.get_attribute("href")
            self.link_list.append(link)
        time.sleep(2)

    def scrape_all(self):
        Scraper.__open_webpage(self)
        for click in range(self.number_of_load_more_clicks):
            Scraper.__click_load_more(self)
            time.sleep(2)
        Scraper.__get_links(self)
        return self.link_list

if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_all()
    print(scrape.link_list)
    print(f"{len(scrape.link_list)} laptops' urls have been scraped")
    time.sleep(5)
    scrape.driver.quit()
```

## Milestone 2

For this milestone I created methods to scrape the text and image details off each movie's webpage. I stored these details in a dictionary, along with a unique UUID to identify each movie. Getting the text details was a bit tricky since the table on rottentomatoes had inconsistent positioning for its variables (due to variables sometimes being missing), so I had to use multiple if statements within a for loop to track the desired details.

```python
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
```

I also created data storage functions to store movie details, as well as a saved image, in my own directory.

```python
import json
import os
import re
import requests

class Storage:
    '''
    This class is used to store the movies' text and image data in my local directory.

    Parameters:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the movie.
    
    Attributes:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the movie.
    movie_title: str
        The title of the movie which was scraped from its page (with its spaces replaced by underscores).
    image_url: str
        The URL of the image of the movie.
    product_path: str
        The path on my PC where I want the details of the movie to go.

    Methods:
    -------
    create_raw_data_folder()
        Creates a raw_data folder in the root if it doesn't already exist.
    create_movie_folder()
        Creates a movie folder in the raw_data folder, named by the movie's ID.
    create_image_folder()
        Creates an image folder in the movie folder if it doesn't already exist.
    download_image()
        Stores the image as a .jpg file in the image folder.
    download_all_data()
        Executes all of the above methods.
    '''
    def __init__(self, details_dict: dict):
        self.details_dict = details_dict
        movie_title_underscores = self.details_dict["Title"].replace(" ", "_").replace("/", "_")
        self.movie_title = re.sub('[:;!?]', '', movie_title_underscores)
        self.image_url = self.details_dict["Image"]
        self.product_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{self.movie_title}"

    def __create_raw_data_folder(self):
        if not os.path.exists(self.product_path):
            os.makedirs(self.product_path)

    def __create_product_folder(self):
        with open(f"{self.product_path}/data.json", 'w') as fp:
            json.dump(self.details_dict, fp)

    def __create_image_folder(self):
        image_folder_path = self.product_path + f"/images"
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)

    def __download_image(self):
        image_file_path = self.product_path + f"/images/{self.movie_title}"
        image_data = requests.get(self.image_url).content
        with open(image_file_path + '.jpg', 'wb') as handler:
            handler.write(image_data)

    def download_all_data(self):
        Storage.__create_raw_data_folder(self)
        Storage.__create_product_folder(self)
        Storage.__create_image_folder(self)
        Storage.__download_image(self)

if __name__ == '__main__':
    test_details_dict = {'Title': 'Sell/Buy/Date (2022)', 'Tomatometer': '71%', 'Audience Score': '86%', 'US Box Office': 'Unknown', 'Release Date (Streaming)': 'Nov 8, 2022', 'Age Rating': 'Unknown', 'Time of Scrape': 'Fri Nov 18 18:46:01 2022', 'Image': 'https://resizing.flixster.com/TPL6sElwV9yH--7cQGFpNjNkHoM=/206x305/v2/https://resizing.flixster.com/_rcrP2auKC_ifdihU333b8_9_GU=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzZhYmY0M2JjLTI4MzQtNDE4MS1hZDZjLWRjYjMyZTgxNWJmNy5qcGc=', 'UUID': '072c573a-01c7-4e71-ae45-abaa89f4ea10'}
    store = Storage(test_details_dict)
    store.download_all_data()
    print("Done!")
```
## Milestone 3

In this milestone I created unit tests for each of my project's 3 main files. The Scraper test made sure the list of links were all from the rottentomatoes website:

```python
import unittest
from project.scraper import Scraper

class ScraperTestCase(unittest.TestCase): 

    def setUp(self):
        scrape = Scraper()     
        self.link_list = scrape.scrape_all()

    def test_scrape_all(self):
        self.assertEqual(len(self.link_list), 210)
        non_website_list = list(filter(lambda x: x[:33] != "https://www.rottentomatoes.com/m/", self.link_list))
        self.assertEqual(len(non_website_list), 0)

if __name__ == '__main__':   
    unittest.main(verbosity=2)
```
The Details test made sure that the outputted dictionary had all 9 required details, and none of them were left unknown for this particular url:

```python
import unittest
from project.details import Details
from selenium import webdriver

class DetailsTestCase(unittest.TestCase):

    def setUp(self):
        driver = webdriver.Chrome()
        test_URL = "https://www.rottentomatoes.com/m/nobody_2021"
        driver.get(test_URL)
        extraction = Details(driver)
        detail_dict = extraction.extract_all_data()
        self.values = detail_dict.values()

    def test_extract_all_data(self):
        expected_length = 9
        actual_length = len(self.values)
        self.assertEqual(expected_length, actual_length)
        self.assertNotIn("Unknown", self.values)

if __name__ == '__main__':       
    unittest.main(verbosity=2)
```
And the Data storage test checked to see if all the data was successfully stored in my personal directory:

```python
import pathlib as pl
import re
import unittest
from project.data_storage import Storage

class StorageTestCase(unittest.TestCase):

    def setUp(self, details_dict = {'Title': 'Thor: Ragnarok (2017)', 'Tomatometer': '93%', 'Audience Score': '87%', 'US Box Office': '$315.0M', 'Release Date (Streaming)': 'Mar 6, 2018', 'Age Rating': 'PG-13', 'Time of Scrape': 'Sat Nov 19 19:21:48 2022', 
        'Image': 'https://resizing.flixster.com/JuiNcQBYggEOrN5PbIVv0fq7SJA=/206x305/v2/https://flxt.tmsimg.com/assets/p12402331_p_v8_ax.jpg', 'UUID': '453da405-8265-4aee-8220-d6ba5bdacbf5'}):
        store = Storage(details_dict)
        store.download_all_data()
        movie_title_underscores = details_dict["Title"].replace(" ", "_").replace("/", "_")
        self.movie_title = re.sub('[:;!?]', '', movie_title_underscores)
        self.image_url = details_dict["Image"]
        self.product_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{self.movie_title}/"

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
        path_4 = path + f"images/{self.movie_title}.jpg"
        self.assertIsFolder(pl.Path(path_1))
        self.assertIsFile(pl.Path(path_2))
        self.assertIsFolder(pl.Path(path_3))
        self.assertIsFile(pl.Path(path_4))

if __name__ == '__main__':      
    unittest.main(verbosity=2)
```

## Milestone 4

I then put everything into a docker container using these Dockerfile and docker-compose files:

```
FROM python:bullseye

ENV PYTHONBUFFERED 1

#Set up selenium Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN mkdir /app

WORKDIR /app

COPY scraper.py details.py project.py data_storage.py /app/

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENTRYPOINT ["python3", "project.py"]
```

```
version: '2.12.0'

services:
  test_container:
    image: scraper-lp
    ports:
      - "5432:5432"
    volumes:
      - C:\Users\timcy\Documents\Aicore\Data-Collection-Pipeline\docker\raw_data:/app/raw_data
    tty: true               # equivalent for -t
    stdin_open: true        # equivalent for -i
```

## Conclusions