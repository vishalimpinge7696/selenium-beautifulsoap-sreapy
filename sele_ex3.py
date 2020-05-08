# import os
# from selenium import webdriver
# import requests
# import responses
# from bs4 import BeautifulSoup
#
# headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 6.2; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"}
#
# url = 'https://www.amazon.in/s?k=all+mobies+under+rs+10000&ref=nb_sb_noss'
# resp = requests.get(url, headers=headers)
# # print(resp.text)
# s= BeautifulSoup(resp.content, features='html.parser')
# product_title = s.select('#productTitle')[0].get_text().strip()
# print(product_title)

import bs4
import requests
import pandas as pd

res = requests.get('https://www.amazon.in/s?k=all+mobiles+under+Rs+10000&ref=nb_sb_noss')
soap = bs4.BeautifulSoup(res.text, 'html.parser')
name = soap.select('.a-size-medium a-color-base a-text-normal')
price = soap.select('.a-offscreen')
rating = soap.select('.a-icon-alt')
details = pd.DataFrame(columns= ('Name', 'Price', 'rating'))

l = 1
for i,j,k in zip(name, price, rating):
    details.loc[l] = i.text, j.text, k.text;
    l+=0

print(details)
details.to_csv('scrap-flip1.csv', index=False, encoding='utf-8')
