import os

path = "C:/Users/timcy/Documents/Aicore/Data-Collection-Pipeline/raw_data"
if not os.path.exists(path):
    os.mkdir(path)

import details

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
    with open(f"{product_path}/data.json", 'w') as f:
        f.write(str(details_dict))

create_product_folder("https://www.amazon.co.uk/Lenovo-IdeaPad-Notebook-DDR4-SDRAM-802-11ax/dp/B0B4T3H79X/ref=sr_1_40?crid=2E1T6L3YWDF37&keywords=laptop&qid=1664901597&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C162&sr=8-40")