import os
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
driver = webdriver.Chrome(driver_path)
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

time.sleep(2)
time.sleep(2)

pages = driver.find_elements_by_css_selector('li.a-last')

def getdata(driver, pages):
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    current = 0
    data = {}
    df = pd.DataFrame(columns=['Title', 'Price', 'Star'])
    dictionary = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    # while current < pages:
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//li[not(@class="disabled")]/a[contains(text(), "Next")]'))).click()
        except TimeoutException:
            break
        all_divs = soup.findAll('div', attrs={
            'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'})
        for mobiles in all_divs:
            title = mobiles.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            price = mobiles.find('span', attrs={'class': "a-price-whole"})
            rating = mobiles.find('span', attrs={'class': 'a-icon-alt'})
            try:
                data['Title'] = title.text
            except:
                data['Title'] = '--'

            try:
                data['Price'] = price.text
            except:
                data['Price'] = '-'

            try:
                data['Star'] = rating.text
            except:
                data['Star'] = '--'

            df = df.append(data, ignore_index=True)
        # current += 1
        # next_page = driver.find_element_by_class_name('a-last')
        # next_page.click()
    return df


list_data = getdata(driver, pages)
list_data.to_csv('tests2.csv')

sigo = driver.find_element_by_class_name('nav-text')
sigo.click()


