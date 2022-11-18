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
        movie_title_underscores = self.details_dict["Title"].replace(" ", "_")
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
    test_details_dict = {'Title': 'What Is a Woman? (2022)', 'Tomatometer': '83%', 'Audience Score': '96%', 'US Box Office': 'Unknown', 'Release Date (Streaming)': 'Jun 1, 2022', 'Age Rating': 'Unknown', 'Time of Scrape': 'Fri Nov 18 18:21:43 2022', 'Image': 'https://resizing.flixster.com/Lc4GOUXt1W-E0RgG6CCvLL-tclk=/206x305/v2/https://resizing.flixster.com/6cMwGg4yBwCUKoDOsoeWay-5nBo=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzL2E2ZWQyZTllLWVhZmMtNGI2YS1hM2UyLTg1YjI1MTgwY2JiNi5qcGc=', 'UUID': '6f79e62e-0248-40f4-92c3-c5561d01f75f'}
    store = Storage(test_details_dict)
    store.download_all_data()
    print("Done!")