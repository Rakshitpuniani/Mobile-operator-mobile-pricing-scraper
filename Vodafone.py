import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re

# Contract
urls = 'https://www.vodafone.com.au/mobile/mobile-phones'
driver = webdriver.Chrome()
vodafone = {"Name":[], 'storage':[], "price":[], "Status":[]}
def read_page(urls):
    driver.get(urls)
    # Parse the HTML content of the response
    scroll_pause_time = 1  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break
    # Fetch the data using BeautifulSoup after all data is loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup
soup = read_page(urls)
mobile_links = []
remove_words = ['www.vodafone.com.au']
for link in soup.find_all('a'):
    href = link.get('href')
    if href and '/mobile/mobile-phones/' in href and all(x not in href for x in remove_words):
        mobile_links.append(href)
mobile_link = set(mobile_links)
vodafone_url = []
for link in mobile_link:
    vodafone_url.append('https://www.vodafone.com.au' + link)
for url in vodafone_url:
    response = requests.get(url, verify = False)
    soup = BeautifulSoup(response.content, 'html.parser')
    storage = []
    name = url.split('/')[len(url.split('/')) - 1].replace("-", " ")
    storage_space = soup.find_all('input', {'name': 'capacity'})
    for st in storage_space:
        storage = st['id']
        driver.get(url+'?capacity='+storage)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = round(float(soup.find(class_=re.compile('^Pricestyles__Amount')).text.strip())*36,2)
        vodafone['Name'].append(name)
        vodafone['storage'].append(storage)
        vodafone['price'].append(price)
        vodafone['Status'].append('Contract')

# Prepaid
urls = 'https://www.vodafone.com.au/prepaid/mobile-phones'
driver.get(urls)
soup = read_page(urls)
container = soup.find('div', {'data-testid':"device-listing"})
sp1 = container.find_all("a",href=True)
for models in sp1:
    try:
        name = models.find(class_=re.compile('^RichText__Root')).text
        price = models.find(class_=re.compile('^Pricestyles__Amount')).text
        vodafone['Name'].append(name)
        vodafone['storage'].append("")
        vodafone['price'].append(price)
        vodafone['Status'].append('Prepaid')
    except:
        print(models.get('href'))
vodafone_df = pd.DataFrame(vodafone)
vodafone_df.to_csv("Output/vodafone_phone_prices.CSV")
driver.quit()





