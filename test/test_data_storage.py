import pathlib as pl
import unittest
from project.data_storage import Storage

class StorageTestCase(unittest.TestCase):

    def setUp(self, details_dict = {'Price': '£312.49', 'Screen Size': '12 Inches', 'Resolution': '1366 x 912', 'Storage': '32GB', 'RAM': '4GB', 'Stock Code': '6520758', 'Image': 'https://www.box.co.uk/image?id=4539297&quality=90&maxwidth=760&maxheight=520', 'UUID': 'f30001ea-4088-4ccc-bf36-871bb272713f'}):
        store = Storage(details_dict)
        store.download_all_data()
        self.product_id = details_dict["Stock Code"]
        self.image_url = details_dict["Image"]
        self.product_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{self.product_id}/"

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
        path_4 = path + f"images/{self.product_id}.jpg"
        self.assertIsFolder(pl.Path(path_1))
        self.assertIsFile(pl.Path(path_2))
        self.assertIsFolder(pl.Path(path_3))
        self.assertIsFile(pl.Path(path_4))

if __name__ == '__main__':      
    unittest.main(verbosity=2)