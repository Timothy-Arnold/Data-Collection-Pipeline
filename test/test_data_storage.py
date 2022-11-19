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