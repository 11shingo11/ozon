from random import randrange
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
base_url="https://www.ozon.ru/category/zaryadnye-ustroystva-i-dok-stantsii-15920/"
url = "https://www.ozon.ru/category/zaryadnye-ustroystva-i-dok-stantsii-15920/"
i = 1
Base = declarative_base()

class Charger(Base):
    __tablename__ = 'chargers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    comments = Column(String)
    price = Column(Integer)
    url = Column(String)
    raiting = Column(String)

engine = create_engine('postgresql://postgres:2312@localhost:5432/ozon')
# metadata = MetaData()
#
# my_table = Table('chargers', metadata, autoload_with=engine)
# with engine.connect() as conn:
#     conn.execute(my_table.delete())
Session = sessionmaker(bind=engine)
session = Session()
idnum = 0
while i < 279:
    driver.get(url)
    time.sleep(randrange(2, 3))
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    # в зависимости от карточки товара название этого класса(class='y4j j5y') может меняться параметры внутри этого
    # элемента при проверкке на другой категории полностью совпали.
    for el in driver.find_elements(By.CSS_SELECTOR, "div[class='y6j jy7']"):
        reviews = 0
        raiting = 0
        try:
            items = []
            for item in el.find_elements(By.CSS_SELECTOR, "span[class='e4f']"):
                items.append(item)
            for item in items:
                if item == items[0]:
                    raiting = float(item.text)
                    # print(raiting)
                if item == items[1]:
                    reviews = int(item.text.split(' ')[1])
                    # print(reviews)
            # тут происходит отбор товаров по кол-ву отзывов, а далее по оценке, только после прохождения отбора по двум
            # критериям товар занесется в бд
            if reviews > 1500:
                if raiting >= 4.8:
                     idnum += 1
                     product_url = el.find_element(By.CSS_SELECTOR, "a[class='tile-hover-target j4v v4j']").get_attribute("href")
                     product_name = el.find_element(By.CSS_SELECTOR, "a[class='tile-hover-target j4v v4j']").text
                     # print(product_name)
                     product_price = el.find_element(By.CSS_SELECTOR, "div[class='aa2-a0']").text.split("₽")[0]
                     charger = Charger(
                        id=idnum,
                        name=product_name,
                        comments=reviews,
                        price=product_price,
                        url=product_url,
                        raiting=raiting
                     )
                     session.add(charger)
                else:
                    # logging.error(Exception)
                    pass
            else:
                # logging.error(Exception)
                pass
        except Exception as e:
            pass

    i += 1
    print("link number:",i)
    next_url = f"{base_url}?page={i}"
    url = next_url
session.commit()

