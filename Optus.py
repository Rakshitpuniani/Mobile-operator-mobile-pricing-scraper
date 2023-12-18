import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
Optus = {"Name":[], 'storage':[], "price":[], "Status":[]}
urls = 'https://www.optus.com.au/mobile/phones'
Telstra = {"Name":[], 'storage':[], "price":[], "Status":[]}
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(urls)
load_button = driver.find_element(By.XPATH,  "//a[contains(@href, 'javascript:void(0)') and contains(@role, 'link') and contains(@tabindex, '0')]")


while True:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", load_button)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(2)
        load_button.click()
        time.sleep(2)
    except:
        break
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")
mobile_links = []
remove_words = ['budget','/5g-mobile', 'offer']
# for link in driver.find_elements(By.XPATH, "//a[contains(@href, '/mobile/phones/')]"):
#     href = link.get_attribute("href")
for link in soup.find_all('a'):
    href = link.get('href')
    if href and '/mobile/phones/' in href and all(x not in href for x in remove_words):
        if 'https://www.optus.com.au/' in href:
            mobile_links.append(href)
        elif 'https://offer.optus.com' in href:
            mobile_links.append(href)
        else:
            mobile_links.append('https://www.optus.com.au/'+href)
mobile_url = []
for link in mobile_links:
    if '?contractLength=36' in link:
        mobile_url.append(link.strip('?contractLength=36'))
    else:
        mobile_url.append(link)
mobile_link = set(mobile_url)

print(len(mobile_link))
for url in mobile_link:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    name = soup.find('h1').text
    container = soup.find(class_=re.compile('CapacitySwatchstyle__Swatches$'))
    storage_cap = []
    if container is not None:
        for div in container:
            try:
                storage = div.text
                storage_cap.append(storage)
            except Exception as e:
                print(f"Error extracting storage: {e}")
    time.sleep(1)
    print(name)
    if len(storage_cap) == 1:
        price = round(float(soup.find(class_ = re.compile('ProductPrice__PriceDetail$')).text.strip('per month').strip('$'))*36,2)
        Optus['Name'].append(name)
        Optus['storage'].append(storage_cap[0])
        Optus['price'].append(price)
        Optus['Status'].append('Contract')
    elif len(storage_cap) != 0 and len(storage_cap) != 1:
        for storage_op in reversed(storage_cap):
            driver.find_element(By.CSS_SELECTOR, "[data-auto-id="+"'"+storage_op+"'"+"]").click()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            price = round(float(soup.find(class_=re.compile('ProductPrice__PriceDetail$')).text.strip('per month').strip('$')) * 36, 2)
            Optus['Name'].append(name)
            Optus['storage'].append(storage_op)
            Optus['price'].append(price)
            Optus['Status'].append('Contract')


# Prepaid
url = 'https://www.optus.com.au/prepaid/phones'
while True:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", load_button)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(2)
        load_button.click()
        time.sleep(2)
    except:
        break
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")
containers = soup.find_all('div', class_ = re.compile('MobileDevicestyle__MobileDeviceWrapper$'))
for div in containers:
    name = div.find('h4').text
    price = div.find('span', class_ = 'price')
    Optus['Name'].append(name)
    Optus['storage'].append("")
    Optus['price'].append(price)
    Optus['Status'].append('Prepaid')

Optus_df = pd.DataFrame(Optus)
Optus_df.to_csv("Output/Optus_phone_prices.CSV")
driver.quit()





