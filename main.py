from random import randrange
import openpyxl as openpyxl
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
# определяем параметры для запуска вебдрайвера, чтобы сайт думал, что запрос посылает реальный пользователь
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
# вводим данные для старта программы
url = input("enter your url: ")
rate_filter = float(input("enter a decimal number from 0 to 5 for filtrating by product rating(for example 4.8): "))
comment_filter = int(input("enter value for filtrating by num comments: "))
table_name = input("enter the names for the table where the data will be saved: ")
if url.endswith('/'):
    base_url = f"{url}?"
else:
    base_url = f"{url}&"
i = 1


# определяем функцию для запуска вебдрайвера и начала выполнения парсинга
def conn(url, row, idnum, name_class):
    driver.get(url)
    time.sleep(randrange(2, 3))
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(randrange(1, 3))
    row, idnum = parse(name_class=name_class, row=row, idnum=idnum)
    return row, idnum


# определяем функцию парсинга нужной информации, проверяем наличие нужных элементов на странице
def parse(name_class, row, idnum, i=1):
    for el in driver.find_elements(By.CSS_SELECTOR, f"div[class='{name_class}']"):
        i += 1
        reviews = 0
        rating = 0
        # находим элементы, содержащие информацию об оценке товара и количестве отзывов, получаем нужные значения
        try:
            for item in el.find_elements(By.CSS_SELECTOR, "span[class='e4f']"):
                try:
                    reviews = int(item.text.split(' ')[1])
                except:
                    try:
                        rating = float(item.text)
                    except:
                        pass
            # сортируем товары по заданным условиям, если товар проходит проверку - данные записываются в таблицу
            if reviews > comment_filter:
                if rating >= rate_filter:
                    idnum += 1
                    product_url = el.find_element(By.CSS_SELECTOR,
                                                  "a[class='tile-hover-target j4v v4j']").get_attribute("href")
                    product_name = el.find_element(By.CSS_SELECTOR, "a[class='tile-hover-target j4v v4j']").text
                    product_price = el.find_element(By.CSS_SELECTOR, "div[class='aa2-a0']").text.split("₽")[0]
                    worksheet['A' + str(row)] = idnum
                    worksheet['B' + str(row)] = rating
                    worksheet['C' + str(row)] = product_name
                    worksheet['D' + str(row)] = product_price
                    worksheet['E' + str(row)] = reviews
                    worksheet['F' + str(row)] = product_url
                    row += 1
                    workbook.save(f'{table_name}.xlsx')
        except:
            continue

    return row, idnum


# задаем структуру таблицы
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
# получаем данные о названиях классов, нужных для парсинга страницы, и количестве страниц с товарами
driver.get(url)
try:
    products_num = int(driver.find_element(By.CSS_SELECTOR, "div[class='oe']").text.split(' ')[0])
except:
    products_num = int(driver.find_element(By.CSS_SELECTOR, "div[class='faa2']").text.split(' ')[4])
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(2)
name_class = str(driver.find_element(By.CSS_SELECTOR, "div[class='kl2']").get_attribute('innerHTML').split('"')[1])
products_on_page = (int(len(driver.find_elements(By.CSS_SELECTOR, f"div[class='{name_class}']"))))
pages = int(products_num / products_on_page) + 2
# запускаем цикл парсинга с перебором всех имеющихся на заданной ссылке страниц с товарами
while h != pages:
    row, idnum = conn(url, row=row, idnum=idnum, name_class=name_class)
    h += 1
    next_url = f"{base_url}page={h}"
    url = next_url
# закрываем вебдрайвер и заканчиваем выполнение программы
driver.close()
driver.quit()
