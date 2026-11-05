from SQLite3Fun import DataBase

database=DataBase("texting.db")
database.CreateTable("testing",("names",database.TEXT(),database.PRIMARY_KEY()),("AGE",database.INT()))
#import sqlite3

"""conn=sqlite3.connect("texting.db")
cursor=conn.cursor()
cursor.execute("INSERT INTO testing VALUES (?,?)",["adi",18])
conn.commit()
print("done")"""

"""conn=sqlite3.connect("texting.db")
cursor=conn.cursor()
cursor.execute("SELECT * FROM testing")
data=cursor.fetchall()
print(data)"""
#tested, works!
