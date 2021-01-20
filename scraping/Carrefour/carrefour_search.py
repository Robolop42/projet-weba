from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.options import Options

import re
from bs4 import BeautifulSoup

import random
from time import sleep

import pandas as pd

from db import DB
from temp_save import save_result
import logging
path = '../chromedriver2.exe'

def timer():
    carrefour = pd.read_excel("carrefour_magasins.ods")
    mags = [i for i in range(len(carrefour.index))]
    random.shuffle(mags)

    # headers = setHeaders()
    
    for mag in mags:
        timeout = random.randint(30,90) #Setting timeout between requests
        print('scrapping carrefour : ' + str(mag) + '\n')
        connect('Bonduelle',carrefour['Ville'][mag],str(mag+1),carrefour['shopUrl'][mag]) #Lauching connect function
        print("\nGoing to sleep for : "+str(timeout)+'s\n') 
        sleep(timeout) #Sleeping untill next mag

def write(text,uinput):
    for char in text:
            n = random.randrange(1, 7, 1) / 10
            sleep(n)
            uinput.send_keys(char)
            #change here

def connect(query,mag, shopId,shopUrl):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("window-size=1280,800")

    # For older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    #For ChromeDriver version 79.0.3945.16 or over
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(chrome_options=options,executable_path=path)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    magasin = re.sub(' ','+',mag)
    driver.get('https://duckduckgo.com/?q=carrefour+drive+'+magasin+'&va=b&t=hc&ia=places')

    sleep(random.uniform(4,7))
    mag = driver.find_element_by_xpath('//a[@href="'+shopUrl+'"]')
    mag.click()

    sleep(random.uniform(3,5))

    #Accepting cookies
    driver.find_element_by_id('footer_tc_privacy_button').click()
    sleep(random.uniform(3,5))
    #Entering the shop
    choose = driver.find_element_by_xpath('//span[contains(text(),"CHOISIR CE DRIVE")]')
    choose.click()


    sleep(random.uniform(4,7))

    #Search
    search = driver.find_element_by_id("search-bar-input")
    search.click()
    sleep(random.uniform(1,3))
    write(query,search)

    sleep(random.uniform(1.5,4))
    button_search = driver.find_elements_by_class_name("button-search")[0]
    button_search.click()

    #Make it a soup then parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parse(soup,shopId)
    driver.close()

def parse(soup,shopId):
    articles = soup.findAll('article','ds-product-card')
    result = []
    #Constructing result list
    for article in articles:
        # Prix 
        prix = article.find("span",{"class":"product-card-price__price--final"})
        prix = float(re.sub("\n|<.+?>| |€","",re.sub(",", ".", str(prix))))
        # Nom
        nom = article.find("h2",{"class":"ds-title--medium"})
        nom = re.sub("<.+?>|\n", "", str(nom)).lower().strip() 
        # Item Quantity
        divqty = article.find("div",{"class":"ds-product-card__perunitlabel"})
        ppqty = re.sub('<.+>|[a-zA-Z]|/|€','',str(divqty)).strip()
        try:
            ppqty = float(ppqty)
            qty = prix/ppqty
        except:
            ppqty = 0
            qty = 0
        result.append(['Carrefour',shopId,nom,'none',qty,prix,ppqty])
    #Saving with temp_save.py
    # save_result(result)
    print(result)

def main():
    # req('Bonduelle','1016')
    timer()

if __name__ == "__main__":
    main()