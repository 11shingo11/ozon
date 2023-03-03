from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


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

url = "https://www.ozon.ru/category/zaryadnye-ustroystva-i-dok-stantsii-15920/?tf_state=GJ08ZsZ9qHRGDbbs88min8pawFi2Gl1vPiBeNZjHsrq9Dnl7cUrRcInNrg%3D%3D"

driver.get(url)
time.sleep(25)
