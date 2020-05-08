# import os
# from selenium.webdriver.common.keys import Keys
# import pandas as pd
# import time
# from selenium import webdriver as wb
# from selenium.webdriver.chrome.options import Options
#
# webD=wb.Chrome('chromedriver.exe')
# webD.get('https://www.amazon.in/')
#
# time.sleep(2)
# search = webD.find_element_by_id('twotabsearchtextbox')
# search.send_keys('all mobiles under Rs10000')
#
# search2 = webD.find_element_by_class_name('nav-input')
# search2.click()
# time.sleep(2)
#
# product=webD.find_elements_by_class_name('a-section a-spacing-none').text()
# print(product)