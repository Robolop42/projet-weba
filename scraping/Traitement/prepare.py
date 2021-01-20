import pandas as pd

chrono = pd.read_csv('carrefour_csv2.csv', sep=";",header=None)
# chrono.columns = ['id','enseigne','shopUrl','ville']
# chrono['id']=chrono['id'].astype(str)
print(chrono.dtypes)

# print(chrono.head())
# print('juste en dessous')
for i in range(len(chrono[1])):
    print(chrono[0][i])

print("""INSERT INTO Magasins(id,enseigne,shopUrl,ville) values (%s,%s,%s,%s)""",[(chrono[0][i],chrono[1][i],chrono[2][i],chrono[3][i]) for i in range(len(chrono[1]))])

