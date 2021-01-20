import re
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from db import DB
import logging
import mysql

db=DB() #init DB
def clean(x): #This function cleans the product name
    x=re.sub(r'é|è',r'e',x) #Eliminate all french accents
    x=re.sub(r'à|â',r'a',x)
    x=re.sub(r':|-',r'',x) #Eliminate : or -
    x=re.sub(r'  |   ',r' ',x)#Clean double spaces
    x=re.sub(r'ees|ee|es','e',x)#Kind of tokenize
    x=re.sub(r'bonduelle','',x)#Get rid of the brand (present in every product)
    x=x.strip()#Remove extra spaces
    return(x)

def get_ngrams(text, n ):
    n_grams = ngrams(word_tokenize(text), n) #Makes ngrams
    return [ ' '.join(grams) for grams in n_grams] #return a list of ngrams

def init_products(db):
    c = db.cursor()
    chrono=[]
    carrefour=[]
    try:
        c.execute("""SELECT nom,poids,id FROM Produits""")
        resp = c.fetchall()
    except Exception as e:
        logging.warning(e)

    for r in resp:
        if 'bonduelle' in r[0]:
            if r[0][0:11] == 'bonduelle :':
                chrono.append([r[0],r[1],r[2]])
            else:
                if float(r[1])>0:
                    carrefour.append([r[0],round(float(r[1])*1000,0),r[2]])
    
    for prod in chrono: #Cleaning product weight
        x = re.sub('kg','000',prod[1])
        x = re.sub('g|G','',x)
        prod[1] = float(x)

    return(chrono,carrefour)

def verify():
    #Append products into lists
    chrono,carrefour=init_products(db)
    sim=0
    relations=[]
    for prodch in chrono: #For each product in chronodrive
        for prodca in carrefour: #For each product in carrefour
            similarite=0
            if prodca[1] - 5 <= prodch[1] <= prodca[1]+5: #If the weight is approx the same
                ch1 = clean(prodch[0]) #Clean each product
                ca1 = clean(prodca[0])
                if ' ' in  ca1: #If there is at least 2 words
                    n1 = get_ngrams(ch1,2) #The get 2-grams
                    n2 = get_ngrams(ca1,2)
                    count=0
                    for el in n1: #for each ngram 
                        if el in n2: #if ngram is found in ngrams from carrefour
                            count+=1 #append count
                            similarite = count/((len(n1)+len(n2))/2) #compute similarity
                elif ch1==ca1: #If the product is only one word, is it the same?
                    similarite = 1
                    count+=1 
                
                if (similarite >= 0.25): #If there is a similarity
                    sim+=1
                    print('\nsimilarité : ','{:.2%}'.format(similarite)) 
                    print(ch1,ca1)
                    try:
                        n1
                    except:
                        print(n1,20)
                    else:
                        print("No n1 n2")
                    print([prodch[2],prodca[2]])
                    if (input('Est-ce le même ? Y/N\n') == 'Y'): #Requieres human interaction to confirm

                        relations.append([prodch[2],prodca[2]])
                        print('Ajouté aux relations\n')   

    print(sim)
    print(len(relations))
    print(relations)

def save_results(relations):
    db = mysql.connector.connect(
        # host="172.28.100.14",
        database="Project",
        user="project",
        password="]weCRJnL84"
    )


    print("bordel")
    print("""INSERT INTO Relations(chronodrive,carrefour) values (%s,%s)""",[(rel[0],rel[1]) for rel in relations]) #Prints the SQL query
    c=db.cursor()
    try:
        c.executemany("""INSERT INTO Relations(chronodrive,carrefour) values (%s,%s)""",[(rel[0],rel[1]) for rel in relations]) #KO
    except Exception as e:
        logging.warning(e)

verify()