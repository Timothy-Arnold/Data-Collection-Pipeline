import json
import os
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
        self.movie_title = self.details_dict["Title"].replace(" ", "_")
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
    test_details_dict = {'Title': 'BLADE RUNNER 2049 (2017)', 'Tomatometer': '88%', 'Audience Score': '81%', 'US Box Office': '$91.5M', 'Release Date (Streaming)': 'Jan 16, 2018', 'Age Rating': 'R', 'Time of Scrape': 'Fri Nov 18 16:47:09 2022', 'Image': 'https://resizing.flixster.com/9jMsWgVxmznwSXln9X7Y4XgYxhw=/206x305/v2/https://resizing.flixster.com/VP4CyK9NQFu-6UWzqpy-qY-5vtY=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzljMzEwZGY4LThjOTEtNGRhZS05MThmLTRkNDhkOWE2Njc0My53ZWJw', 'UUID': 'fcb08b0e-6419-4606-9c26-35ec6d2acac1'}
    store = Storage(test_details_dict)
    store.download_all_data()
    print("Done!")