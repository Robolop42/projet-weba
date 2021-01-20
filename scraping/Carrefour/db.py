import mysql.connector

def DB():
    db = mysql.connector.connect(
    host="172.28.100.14",
    database="Project",
    user="project",
    password="]weCRJnL84"
    )
    return(db)