import time
from selenium import webdriver
from scraper import Scraper
from details import Details
from data_storage import Storage

def do_full_scrape():
    scrape = Scraper()
    link_list = scrape.scrape_all()
    print(link_list)
    time.sleep(30)
    # Initialize list of detail_dict's
    details_dict_list = []
    driver = webdriver.Chrome()
    for link in link_list:
        driver.get(link)
        time.sleep(2)
        try:
            extraction = Details(driver)
            details_dict = extraction.extract_all_data()
            print(details_dict)
            details_dict_list.append(details_dict)
        except:
            pass
    number_of_products = len(details_dict_list)
    print(f"{number_of_products} laptops have been scraped")
    for details_dict in details_dict_list:
        store = Storage(details_dict)
        store.download_all_data()
    print("All Finished!")

if __name__ == '__main__':
    do_full_scrape()

# import boto3

# s3 = boto3.client("s3")