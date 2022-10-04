# import requests
# from bs4 import BeautifulSoup

# html_request = requests.get(test_link)
# html_string = html_request.content
# soup = BeautifulSoup(html_string, 'html.parser')
# # print(soup.prettify())

# print(soup)

# details = soup.find("table", {"id": "productDetails_techSpec_section_1"})

# print(details)

# https://www.amazon.co.uk/Razer-Blade-17-Display-Chamber/dp/B09Q6CVSW3/ref=sr_1_3?keywords=laptop&qid=1664886688&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-3&th=1
# https://www.amazon.co.uk/ASUS-Vivobook-E510MA-Microsoft-included/dp/B09X63GB82/ref=sr_1_10?crid=2GEDTE88DVY5K&keywords=laptop&qid=1664898174&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C62&sr=8-10&th=1

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def extract_text_data(URL):
    driver.get(URL)

    required_details = ["Brand", "Standing screen display size", "Screen Resolution", "RAM Size", "Item Weight"]
    initial_values = [None] * 5
    # Initialize the detail dictionary with empty values
    details_dict = {required_details[i]: initial_values[i] for i in range(5)}

    details_table = driver.find_element(By.XPATH, '//*[@id="productDetails_techSpec_section_1"]')
    name_list = details_table.find_elements(By.XPATH, '//th[@class = "a-color-secondary a-size-base prodDetSectionEntry"]')
    value_list = details_table.find_elements(By.XPATH, '//td[@class = "a-size-base prodDetAttrValue"]')

    detail_list_length = len(name_list)
    
    for index_1 in range(detail_list_length):
        if name_list[index_1].text == "Resolution":
            details_dict["Screen Resolution"] = value_list[index_1].text
        for index_2 in range(5):
            if name_list[index_1].text == required_details[index_2]:
                details_dict[required_details[index_2]] = value_list[index_1].text

    print(details_dict)

extract_text_data("https://www.amazon.co.uk/Lenovo-IdeaPad-Notebook-DDR4-SDRAM-802-11ax/dp/B0B4T3H79X/ref=sr_1_40?crid=2E1T6L3YWDF37&keywords=laptop&qid=1664901597&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C162&sr=8-40")
extract_text_data("https://www.amazon.co.uk/Razer-Blade-17-Display-Chamber/dp/B09Q6CVSW3/ref=sr_1_3?keywords=laptop&qid=1664886688&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-3&th=1")
extract_text_data("https://www.amazon.co.uk/ASUS-Vivobook-E510MA-Microsoft-included/dp/B09X63GB82/ref=sr_1_10?crid=2GEDTE88DVY5K&keywords=laptop&qid=1664898174&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sprefix=laptop%2Caps%2C62&sr=8-10&th=1")

# productDetails_detailBullets_sections1

# Brand
# Screen size
# Res
# Weight
# RAM

