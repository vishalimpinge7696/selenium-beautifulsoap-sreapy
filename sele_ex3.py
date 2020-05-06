import os
from selenium import webdriver
import requests
import responses
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 6.2; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"}

url = 'https://www.amazon.in/s?k=all+mobies+under+rs+10000&ref=nb_sb_noss'
resp = requests.get(url, headers=headers)
# print(resp.text)
s= BeautifulSoup(resp.content, features='html.parser')
product_title = s.select('#productTitle')[0].get_text().strip()
print(product_title)