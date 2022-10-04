import requests
from bs4 import BeautifulSoup

test_link = "https://www.amazon.co.uk/Razer-Blade-17-Display-Chamber/dp/B09Q6CVSW3/ref=sr_1_3?keywords=laptop&qid=1664886688&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-3"

html_request = requests.get(test_link)
html_string = html_request.content
soup = BeautifulSoup(html_string, 'html.parser')
# print(soup.prettify())

print(soup)

details = soup.find("table", {"id": "productDetails_techSpec_section_1"})

print(details)