import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.logitech.com/en-gb/products/mice.html")
html = response.content
html = BeautifulSoup(html, 'html.parser')

print(html.find_all("div"))

#class Scraper:

