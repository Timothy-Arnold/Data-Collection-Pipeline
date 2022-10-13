from scraper import Scraper
from details import Details
from data_storage import Storage

def do_full_scrape():
    scrape = Scraper()
    link_list = scrape.scrape_all()
    for link in link_list[:10]:
        extraction = Details(link)
        details_dict = extraction.extract_all_data()
        store = Storage(details_dict)
        store.download_all_data()

if __name__ == '__main__':
    do_full_scrape()