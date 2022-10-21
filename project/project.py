import boto3
from details import Details
from scraper import Scraper
from data_storage import Storage
import time
from selenium import webdriver

def do_full_scrape():
    '''
    Scrapes laptops from the box website.
    
    This function scrapes the first 15 pages of laptops' product page urls on the box website, then accesses these URLs to get the information of each laptop.
    It then stores this technical and image data in my local directory, as well as uploads it to an S3 bucket.

    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    '''
    scrape = Scraper(2)
    link_list = scrape.scrape_all()
    print(link_list)
    time.sleep(2)
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
        store.upload_data()
    print("All downloaded and uploaded!")

if __name__ == '__main__':
    do_full_scrape()