import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd


chrome_options = Options()
chrome_options.add_argument(" - incognito ")
driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
driver = webdriver.Chrome(driver_path, options=chrome_options)
driver.get('https://www.amazon.in')

elem = driver.find_element_by_id('nav-link-accountList')
elem.click()

email = driver.find_element_by_id('ap_email')
email.send_keys('vishal7696nda@gmail.com')

cont = driver.find_element_by_id('continue')
cont.click()

time.sleep(2)
pasw = driver.find_element_by_id('ap_password')
pasw.send_keys('admin@123')

log = driver.find_element_by_id('signInSubmit')
log.click()

elem = driver.find_element_by_id('nav-link-accountList')
elem.click()

time.sleep(2)
search = driver.find_element_by_id('twotabsearchtextbox')
search.send_keys('all mobiles under Rs10000')

search2 = driver.find_element_by_class_name('nav-input')
search2.click()
pages = 3


# def create_csv_file(self):
#     # Here I created CSV file with desired header.
#     rowHeaders = ["Title", "Price in Rupees", 'Delivery', 'Stars']
#     self.file_csv = open('Flipkart_output.csv', 'w', newline='', encoding='utf-8')
#     self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
#     # Writeheader is pre-defined function to write header
#     self.mycsv.writeheader()


def getdata(self):
    page_html = self.driver.page_source
    self.soup = BeautifulSoup(page_html, 'html.parser')
    current = 0
    data = {}
    df = pd.DataFrame(columns=['Title', 'Price', 'Stock', 'Star'])
    dictionary = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
    while current<pages:
        mobile = driver.find_element_by_class_name("s-include-content-margin s-border-bottom s-latency-cf-section")
        for mobiles in mobile:
            for i in mobiles.find_element_by_class_name('sg-col-inner'):
                data['Title'] = i.find_element_by_class_name("a-size-medium a-color-base a-text-normal")
                data['Price'] = i.find_element_by_class_name("a-price-whole")
                data['Delivery'] = i.find_element_by_class_name("a-text-bold")
                data['Star']= i.find_element_by_class_name("a-icon a-icon-star-small a-star-small-3-5 aok-align-bottom")
                data['Star'] = [v for k,v in dictionary.items() if k in data['Star']]
                df = df.append(data, ignore_index=True)
            current+=1
        next = driver.find_element_by_class_name('a-last')[0].click()
        return df

getdata(driver,pages).to_excel('C:\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\test.xlsx')
getdata(driver,pages).to_csv('C:\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\tests.csv')

sigo = driver.find_element_by_class_name('nav-text')
sigo.click()


