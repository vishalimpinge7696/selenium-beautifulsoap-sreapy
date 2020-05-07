import os
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
import csv

# driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
# driver = webdriver.Chrome(driver_path)
# driver.get('https://www.amazon.in')
#
# elem = driver.find_element_by_id('nav-link-accountList')
# elem.click()
#
# email = driver.find_element_by_id('ap_email')
# email.send_keys('vishal7696nda@gmail.com')
#
# cont = driver.find_element_by_id('continue')
# cont.click()
#
# time.sleep(2)
# pasw = driver.find_element_by_id('ap_password')
# pasw.send_keys('admin@123')
#
# log = driver.find_element_by_id('signInSubmit')
# log.click()
#
# elem = driver.find_element_by_id('nav-link-accountList')
# elem.click()
#
# time.sleep(2)
# search = driver.find_element_by_id('twotabsearchtextbox')
# search.send_keys('all mobiles under Rs10000')
#
# search2 = driver.find_element_by_class_name('nav-input')
# search2.click()

path = r'\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\chromedriver'

#Use Incognito mode when scraping

chrome_options = Options()
chrome_options.add_argument(" — incognito")
browser = webdriver.Chrome(path, options=chrome_options)
# pages=int(input('How Many Pages Do You Want to Scrape? '))

#define number of pages to scrape and starting URL (usually page 1)
pages=1
url='https://www.amazon.in/s?k=all+mobile+under+rs10000&qid=1588784418&ref=sr_pg_1'

#Create Function to scrape webpage

def getdata(start_url,pgs):
    current=0
    urls=browser.get(start_url)
    data={}
    df=pd.DataFrame(columns=['Title','Price','Delivery'])
    # dictionary = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
    while current<pages:
        books = browser.find_elements_by_class_name("sg-col-20-of-24 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-8-of-12 sg-col-12-of-16 sg-col-24-of-28")
        for book in books:
            for b in book.find_elements_by_class_name('s-include-content-margin s-border-bottom s-latency-cf-section'):
                data['Title'] = b.find_elements_by_class_name('a-size-medium a-color-base a-text-normal')[0].text
                data['Price'] = b.find_elements_by_class_name('a-price-whole')[0].text
                data['Delivery'] = b.find_elements_by_class_name('a-text-bold')[0].text
                # data['Star'] = b.find_elements_by_css_selector('p')[0].get_attribute('class').split()[0].text
                # data['Star'] = [v for k,v in dictionary.items() if k in data['Star']][0]
                df=df.append(data, ignore_index=True)
        next = browser.find_elements_by_class_name('a-last')[0].click()
        current+=1
        df.index += 1 #Increments the index from 0 to 1
    return df
getdata(url,pages).to_csv(r'C:\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\test.csv')

# sigo = driver.find_element_by_class_name('nav-text')
# sigo.click()


