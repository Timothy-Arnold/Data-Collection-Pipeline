import os
import json
import requests

class Storage:
    '''
    This class is used to store product text and image data in my local directory.

    Parameters:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the laptop.
    
    Attributes:
    ----------
    details_dict: dict
        The dictionary containing all the desired details of the laptop.
    product_id: str
        The ID of the product which was scraped from it's product page.
    image_url: str
        The URL of the image of the laptop
    product_path: str
        The path on my PC where I want the details of the laptop to go.

    Methods:
    -------
    create_raw_data_folder()
        Creates a raw_data folder in the root if it doesn't already exist.
    create_product_folder()
        Creates a product folder in the raw_data folder, named by the product's ID.
    create_image_folder()
        Creates an image folder in the product folder if it doesn't already exist.
    download_image()
        Stores the image as a .jpg file in the image folder.
    download_all_data
        Executes all of the above methods.

    '''
    def __init__(self, details_dict):
        self.details_dict = details_dict
        self.product_id = self.details_dict["ASIN"]
        self.image_url = self.details_dict["Image"]
        self.product_path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{self.product_id}"

    def __create_raw_data_folder(self):
        if not os.path.exists(self.product_path):
            os.mkdir(self.product_path)

    def __create_product_folder(self):
        with open(f"{self.product_path}/data.json", 'w') as fp:
            json.dump(self.details_dict, fp)

    def __create_image_folder(self):
        image_folder_path = self.product_path + f"/images"
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)

    def __download_image(self):
        image_file_path = self.product_path + f"/images/{self.product_id}"
        image_data = requests.get(self.image_url).content
        with open(image_file_path + '.jpg', 'wb') as handler:
            handler.write(image_data)

    def download_all_data(self):
        Storage.__create_raw_data_folder(self)
        Storage.__create_product_folder(self)
        Storage.__create_image_folder(self)
        Storage.__download_image(self)

test_details_dict = {'Price': '£299.00', 'Brand': 'CHUWI', 'Standing screen display size': '14 Inches', 'Screen Resolution': '2160x1440 Pixels', 'RAM Size': '8 GB', 'Item Weight': '1.5 kg', 'ASIN': 'B08NPCBGSZ', 'Image': 'https://m.media-amazon.com/images/I/61GmFJrsGwL._AC_SX679_.jpg', 'UUID': '83cbd88b-449b-4740-865c-d7c2292e215d'}

if __name__ == '__main__':
    store = Storage(test_details_dict)
    store.download_all_data()
    print("Done!")