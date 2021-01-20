import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def req():
    s = requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"})
    r = s.get("https://www.chronodrive.com/magasins-chronodrive")
    soup = BeautifulSoup(r.text, 'html.parser')
    # txt = open("chronomags.txt","w+",encoding='utf-8')
    # txt.write(r.text)
    parse(soup)

def parse(soup):
    drivecol = soup.findAll('ul','drive-col')
    mags = []
    for col in drivecol:
        li = col.findAll('li',recursive=False)
        for l in li:
            # Extraction de la région
            h2 = l.find('div','h2-like')
            region = h2.a.text.replace('\n','')
            for a in l.findAll('a','drive-link'):
                # Extraction de l'id magasin, la ville et le lien
                id = re.search('[0-9]{4}',a.get('href').replace('\n','')).group(0)
                ville = a.text.replace('\n','')
                lien = a.get('href').replace('\n','')
                mags.append([id,lien,region,ville])
    saveMags(mags)

def saveMags(mags):
    df = pd.DataFrame(mags,columns=['id','link','region','ville'])
    df.to_excel('chronodrive_magasins.xlsx')

req('')
