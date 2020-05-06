import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import pandas as pd
from multiprocessing import Process, Queue, Pool, Manager
import threading
import sys
import requests
from bs4 import BeautifulSoup

#
# chrome_options = Options()
# chrome_options.add_argument(" - incognito ")
# driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
# driver = webdriver.Chrome(driver_path, options=chrome_options)
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


# def create_csv_file(self):
#     # Here I created CSV file with desired header.
#     rowHeaders = ["Title", "Price in Rupees", 'Delivery', 'Stars']
#     self.file_csv = open('Flipkart_output.csv', 'w', newline='', encoding='utf-8')
#     self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
#     # Writeheader is pre-defined function to write header
#     self.mycsv.writeheader()

# pages = 3
# url = 'https://www.amazon.in/'

#
# def getdata(start_url):
#     # page_html = self.driver.page_source
#     # self.soup = BeautifulSoup(page_html, 'html.parser')
#     current = 0
#     urls=driver.get(start_url)
#     data = {}
#     df = pd.DataFrame(columns=['Title', 'Price', 'Stock', 'Star'])
#     dictionary = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
#     while current<pages:
#         mobile = driver.find_element_by_class_name("div.sg-col-inner")
#         for mobiles in mobile:
#             for i in mobiles.find_element_by_class_name('div.sg-col-inner'):
#                 data['Title'] = i.find_element_by_class_name("img")[0].get_attribute('alt')
#                 data['Price'] = i.find_element_by_class_name("div.sg-col-inner span.a-price-symbol span.a-price-whole")[0].text
#                 data['Delivery'] = i.find_element_by_class_name("div.sg-col-inner span.a-text-bold")[0].text
#                 data['Star'] = i.find_element_by_class_name("div.a-row a-size-small span.a-icon-alt")[0].text
#                 # data['Star'] = [v for k,v in dictionary.items() if k in data['Star']]
#                 df = df.append(data, ignore_index=True)
#
#         next = driver.find_element_by_class_name('a-last')[0].click()
#         current += 1
#         df.index += 1
#     return df
#
#
# output = getdata(url, pages)
# output.to_excel('test.xlsx')
# output.to_csv('test.csv')
# print(output)


startTime = time.time()
qcount = 0
products = []  # List to store name of the product
prices = []  # List to store price of the product
ratings = []  # List to store ratings of the product
no_pages = 20


def get_data(pageNo, q):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    r = requests.get("https://www.amazon.com/s?k=laptops&page=" + str(pageNo), headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    # print(soup.encode('utf-8')) # uncomment this in case there is some non UTF-8 character in the content and
    # you get error

    for d in soup.findAll('div', attrs={
        'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
        name = d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        price = d.find('span', attrs={'class': 'a-offscreen'})
        rating = d.find('span', attrs={'class': 'a-icon-alt'})
        all = []

        if name is not None:
            all.append(name.text)
        else:
            all.append("unknown-product")

        if price is not None:
            all.append(price.text)
        else:
            all.append('$0')

        if rating is not None:
            all.append(rating.text)
        else:
            all.append('-1')
        q.put(all)
        # print("---------------------------------------------------------------")


results = []
if __name__ == "__main__":
    m = Manager()
    q = m.Queue()  # use this manager Queue instead of multiprocessing Queue as that causes error
    p = {}
    if sys.argv[1] in ['t', 'p']:
        for i in range(1, no_pages):
            if sys.argv[1] in ['t']:
                print("starting thread: ", i)
                p[i] = threading.Thread(target=get_data, args=(i, q))
                p[i].start()
            elif sys.argv[1] in ['p']:
                print("starting process: ", i)
                p[i] = Process(target=get_data, args=(i, q))
                p[i].start()
        # join should be done in seperate for loop
        # reason being that once we join within previous for loop, join for p1 will start working
        # and hence will not allow the code to run after one iteration till that join is complete, ie.
        # the thread which is started as p1 is completed, so it essentially becomes a serial work instead of
        # parallel
        for i in range(1, no_pages):
            p[i].join()
    else:
        pool_tuple = [(x, q) for x in range(1, no_pages)]
        with Pool(processes=8) as pool:
            print("in pool")
            results = pool.starmap(get_data, pool_tuple)

    while q.empty() is not True:
        qcount = qcount + 1
        queue_top = q.get()
        products.append(queue_top[0])
        prices.append(queue_top[1])
        ratings.append(queue_top[2])

    print("total time taken: ", str(time.time() - startTime), " qcount: ", qcount)
    # print(q.get())
    df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Ratings': ratings})
    print(df)
    df.to_csv('products.csv', index=False, encoding='utf-8')
# getdata(driver).to_excel(r'C:\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\test.xlsx')
# getdata(driver).to_csv(r'C:\Users\Abcd\PycharmProjects\selenium-scrapy-beautifulsoap\tests.csv')

# sigo = driver.find_element_by_class_name('nav-text')
# sigo.click()


