import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
urls = 'https://www.telstra.com.au/mobile-phones/mobiles-on-a-plan'
Telstra = {"Name":[], 'storage':[], "price":[], "Status":[]}
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(urls)
load_button = driver.find_element(By.ID, "buttonLoadMore")
while True:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", load_button)
        time.sleep(1)
        load_button.click()
        time.sleep(1)
    except:
        break
soup = BeautifulSoup(driver.page_source, "html.parser")
mobile_links = []
remove_words = ['samsung#phones','iphone#phones','compare-iphones','compare-samsung']
for link in soup.find_all('a'):
    href = link.get('href')
    if href and '/mobile-phones/mobiles-on-a-plan/' in href and all(x not in href for x in remove_words):
        mobile_links.append(href)
mobile_link = set(mobile_links)
Telstra_url = []
for link in mobile_link:
    Telstra_url.append('https://www.telstra.com.au' + link)
for url in Telstra_url:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    name = url.split('/')[len(url.split('/')) - 1].replace("-", " ")
    container = soup.find(class_=re.compile('^device-product__butons-container'))
    container_web = driver.find_elements(By.CLASS_NAME, 'device-product__button-option')
    storage_options = container.find_all('label')
    if len(storage_options) == 1:
        Telstra['Name'].append(name)
        Telstra['storage'].append(container.find('label').text)
        Telstra['price'].append(round(
            float(soup.find('span', {'data-mobile-product-total': "data-mobile-product-total"}).text.strip('$')) * 36,
            2))
        Telstra['Status'].append('Contract')

    else:
        Telstra['Name'].append(name)
        Telstra['storage'].append(container.find('label').text)
        Telstra['price'].append(round(
            float(soup.find('span', {'data-mobile-product-total': "data-mobile-product-total"}).text.strip('$')) * 36,
            2))
        Telstra['Status'].append('Contract')
        for storage_op in range(len(storage_options) - 1, 0, -1):
            stor_temp = str(storage_options[storage_op].text.strip())
            for op in container_web:
                ops = str(op.text.strip())
                if stor_temp == ops:
                    op.click()
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    storage = ops
                    price = round(float(
                        soup.find('span', {'data-mobile-product-total': "data-mobile-product-total"}).text.strip(
                            '$')) * 36,
                                  2)
                    Telstra['Name'].append(name)
                    Telstra['storage'].append(storage)
                    Telstra['price'].append(price)
                    Telstra['Status'].append('Contract')
                    break


Print(Telstra)

