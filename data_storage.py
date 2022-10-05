import os

path = "C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data"
if not os.path.exists(path):
    os.mkdir(path)

import details
import json

def create_product_folder(URL):
    path = "C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data"
    details_dict = details.extract_all_data(URL)
    print(details_dict)
    product_id = details_dict["ASIN"]
    product_path = path + f"/{product_id}"
    print(product_path)
    print(product_id)
    if not os.path.exists(product_path):
        os.mkdir(product_path)
    with open(f"{product_path}/data.json", 'w') as fp:
        json.dump(details_dict, fp)
    
# def download_image

# Tests
# create_product_folder("https://www.amazon.co.uk/Lenovo-IdeaPad-Notebook-DDR4-SDRAM-802-11ax/dp/B0B4T3H79X/ref=sr_1_40?crid=2E1T6L3YWDF37&keywords=laptop&qid=1664901597&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C162&sr=8-40")
# create_product_folder("https://www.amazon.co.uk/HUAWEI-Matebook-16s-i9-12900H-Processor/dp/B0B56RJGSR/ref=sr_1_19?keywords=laptop&qid=1664919140&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-19")

import requests

def create_image_folder(details_dict):
    product_id = details_dict["ASIN"]
    image_url = details_dict["Image"]
    path = f"C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data/{product_id}"
    image_folder_path = path + f"/images"
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)
    
    image_file_path = image_folder_path + f"/{product_id}"
    print(image_file_path)
    image_data = requests.get(image_url).content
    with open(image_file_path + '.jpg', 'wb') as handler:
        handler.write(image_data)

create_image_folder({"Price": "\u00a3818.98", "Brand": "Lenovo", "Standing screen display size": "15.6 Inches", "Screen Resolution": "1920x1080 Pixels", "RAM Size": "8 GB", "Item Weight": "2.25 kg", "ASIN": "B0B4T3H79X", "Image": "https://m.media-amazon.com/images/I/51oIDiA4I6L._AC_SY450_.jpg", "UUID": "dd2c937a-6c69-4473-a3fa-c7c4b031a2c6"})
