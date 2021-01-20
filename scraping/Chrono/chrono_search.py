from db import DB
import requests

from headers import setHeaders

from bs4 import BeautifulSoup
import re

# from timer import timer
from time import sleep
import random
import pandas as pd

from temp_save import save_result
import logging

def timer():
    chrono = pd.read_excel("chronodrive_magasins.xlsx") 
    mags = chrono['id']
    mags = [mag for mag in chrono['id']]
    random.shuffle(mags)

    headers = setHeaders()
    
    for mag in mags     :
        header = random.choice(headers)
        timeout = random.randint(5,30)
        print('scrapping chronodrive number : ' + str(mag) + '\n')
        ###### NOT SURE ABOUT THIS ######
        req('Bonduelle',str(mag),header)
        print("\nGoing to sleep for : "+str(timeout)+'s\n')
        sleep(timeout) 

def req(query, shopId, header):
    s = requests.Session()
    s.headers.update(header)
    cookies = {'chronoShop': 'shopId='+shopId}
    r = s.get("https://www.chronodrive.com/search/"+query,cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    parse(soup,shopId)

def parse(soup,shopId):
    articles = soup.findAll('article','item')
    result = []
    for article in articles:
        # Prix
        prix = article.find("span",{"class":"item-goodPrice"})
        prix = float(re.sub(",",".",re.sub("<.+?>|€|\n", "", str(prix))))
        # Nom
        nom = article.find("div",{"class":"item-desc"})
        nom = re.sub("<.+?>", "", str(nom)).lower()
        # Item Quantity
        divqty = article.find("div",{"class":"item-qtyPrice"})

        qty = re.sub('.+>|<| ','',re.findall('qtyCapacity">.+<',str(divqty))[0])

        ppqty = float(re.sub(",",".",re.sub("\n| €.+","",re.findall("\n[0-9].+\n",str(divqty))[0])))
        result.append(['Chronodrive',shopId,nom,'none',qty,prix,ppqty])
        print(prix,nom,qty,ppqty)
    save_result(result)

# def save(prix,nom,qty,ppqty,shopId):
#     db=DB()
#     c = db.cursor()
#     c.execute("""INSERT INTO Articles_temp(nom,description,prix,quantite,ppqty) VALUES (%s,%s,%s,%s,%s)""", (nom,shopId,prix,qty,ppqty))
#     db.commit()

def main():
    # req('Bonduelle','1016')
    timer()

if __name__ == "__main__":
    main()