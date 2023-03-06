from random import randrange

import openpyxl as openpyxl
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

s = Service(executable_path='path_to_chromedriver')
driver = webdriver.Chrome(service=s, options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
  '''
})
url = input("please input your url: ")
rait_filter = float(input("input filter for product raiting: "))
comment_filter = int(input("input filter for num comments: "))
if url.endswith('/'):
    base_url = f"{url}?"
else:
    base_url = f"{url}&"



i = 1
def conn(url, row, idnum, name_class):
    driver.get(url)
    time.sleep(randrange(2, 3))
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(randrange(1, 3))
    # print('found ', len(driver.find_elements(By.CSS_SELECTOR, f"div[class='{name_class}']")), ' elements')
    row, idnum = parse(name_class=name_class, row=row, idnum=idnum)
    return row, idnum


    # в зависимости от карточки товара название этого класса(class='y4j j5y') может меняться параметры внутри этого
    # элемента при проверкке на другой категории полностью совпали.
def parse(name_class, row, idnum, i=1):
    for el in driver.find_elements(By.CSS_SELECTOR, f"div[class='{name_class}']"):
        i += 1
        reviews = 0
        raiting = 0
        try:
            for item in el.find_elements(By.CSS_SELECTOR, "span[class='e4f']"):
                try:
                    reviews = int(item.text.split(' ')[1])
                    # print(reviews)
                except:
                    try:
                        raiting = float(item.text)
                        # print(raiting)
                    except:
                        pass
            if reviews > comment_filter:
                if raiting >= rait_filter:
                    idnum += 1
                    product_url = el.find_element(By.CSS_SELECTOR, "a[class='tile-hover-target j4v v4j']").get_attribute("href")
                    product_name = el.find_element(By.CSS_SELECTOR, "a[class='tile-hover-target j4v v4j']").text
                    # print(product_name)
                    product_price = el.find_element(By.CSS_SELECTOR, "div[class='aa2-a0']").text.split("₽")[0]
                    worksheet['A' + str(row)] = idnum
                    worksheet['B' + str(row)] = raiting
                    worksheet['C' + str(row)] = product_name
                    worksheet['D' + str(row)] = product_price
                    worksheet['E' + str(row)] = reviews
                    worksheet['F' + str(row)] = product_url
                    row += 1
                    # print("add one")
                    workbook.save('test.xlsx')
        except:
            print("not add")
            continue

    return row, idnum


h = 1
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet['A1'] = 'id'
worksheet['B1'] = 'raiting'
worksheet['C1'] = 'product_name'
worksheet['D1'] = 'product_price'
worksheet['E1'] = 'rewies'
worksheet['F1'] = 'product_url'
row = 2
idnum = 0
driver.get(url)
try:
    products_num = int(driver.find_element(By.CSS_SELECTOR, "div[class='oe']").text.split(' ')[0])
except:
    products_num = int(driver.find_element(By.CSS_SELECTOR, "div[class='faa2']").text.split(' ')[4])
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(2)
name_class = str(driver.find_element(By.CSS_SELECTOR, "div[class='kl2']").get_attribute('innerHTML').split('"')[1])
products_on_page = (int(len(driver.find_elements(By.CSS_SELECTOR, f"div[class='{name_class}']"))))
pages = int(products_num/products_on_page)+2

while h != pages:
    print(url)
    row, idnum = conn(url, row=row, idnum=idnum, name_class=name_class)
    h += 1
    next_url = f"{base_url}page={h}"
    url = next_url
    # print(row, idnum)

driver.close()
driver.quit()
