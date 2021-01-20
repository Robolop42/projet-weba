import requests
from bs4 import BeautifulSoup
import re
from db import DB

# from timer import timer
from time import sleep
import random
import pandas as pd

import logging

def save_result(result):
    db=DB()
    c = db.cursor()

    releve = [r[0:3]+r[5:8] for r in result]
    

    noms = [r[2] for r in result]
    try:
        names = tuple(noms)
        c.execute("""SELECT nom FROM Produits WHERE nom IN {}""".format(names))
        resp = c.fetchall()
    except Exception as e:
        logging.warning(e)
        resp = []
    # Adding new links
    banNames = [n[0] for n in resp]
    addProducts = [r[2:5] for r in result if r[2] not in banNames]
    try:
        c.executemany("""INSERT INTO Produits(nom,description,poids) values (%s,%s,%s)""",[tuple(r) for r in addProducts])
        db.commit()
    except Exception as e:
        logging.warning(e)

    #A PARTIR D'ICI TOUS LES NOUVEAUX PRODUITS ONT ETE AJOUTES

    #Récupérer les id des produits
    try:
        names = tuple(noms)
        c.execute("""SELECT id,nom FROM Produits WHERE nom IN {}""".format(names))
        resp = c.fetchall()
    except Exception as e:
        logging.warning(e)

    #Create list of [prodid, enseigne, mag, prix, poids, prixparquantite]
    addReleve = [[r[0],nom[0],nom[1],nom[3],nom[4]] for r in resp for nom in releve if r[1] == nom[2]]
    print(addReleve)
    try:
        c.executemany("""INSERT INTO Relevés(idArticle,enseigne,idMagasin,Prix,ppqty) values (%s,%s,%s,%s,%s)""",[tuple(r) for r in addReleve])
        db.commit()
    except Exception as e:
        logging.warning(e)

# rrr = [['cr','1001','banae','100','200g','5','10','10'],['cr','1001','banane','100','200g','5','10','10'],['cr','1001','courge','100','200g','5','10','50'],['cr','1001','prune','100','200g','5','10','10']]
# save(rrr)
