import os
import json
import requests
import boto3

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
        self.product_id = self.details_dict["Stock Code"]
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

    def upload_data(self):
        s3_client = boto3.client("s3")
        s3_client.upload_file(f"../raw_data/{self.product_id}/images/{self.product_id}.jpg", "aicore-box-datalake", f"{self.product_id}.jpg")
        s3_client.upload_file(f"../raw_data/{self.product_id}/data.json", "aicore-box-datalake", f"{self.product_id}.json")

if __name__ == '__main__':
    test_details_dict = {'Price': '£229.99', 'Screen Size': '14 Inches', 'Resolution': '1366 x 768', 'Storage': '64GB', 'RAM': '4GB', 'Stock Code': '79519411', 'Image': 'https://www.box.co.uk/image?id=4603979&quality=90&maxwidth=760&maxheight=520', 'UUID': '1ff86a83-6316-4cfb-a9ad-47ca1daa6390'}
    store = Storage(test_details_dict)
    store.download_all_data()
    store.upload_data()
    print("Done!")