from project.data_storage import Storage
import unittest
import pathlib as pl

class StorageTestCase(unittest.TestCase):

    def setUp(self, details_dict = {'Price': '£299.00', 'Brand': 'CHUWI', 'Standing screen display size': '14 Inches', 'Screen Resolution': '2160x1440 Pixels', 'RAM Size': '8 GB', 'Item Weight': '1.5 kg', 'ASIN': 'B08NPCBGSZ', 'Image': 'https://m.media-amazon.com/images/I/61GmFJrsGwL._AC_SX679_.jpg', 'UUID': '83cbd88b-449b-4740-865c-d7c2292e215d'}):
        store = Storage(details_dict)
        store.download_all_data()
        self.product_id = details_dict["ASIN"]
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
    unittest.main()