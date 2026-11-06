from SQLite3Fun import DataBase

db=DataBase("test.db")
db.CreateTable("checking",("name",db.TEXT(),db.UNIQUE()),("age",db.INT(),db.CHECK("age","<",18,True)),("adm_no",db.INT(),db.PRIMARY_KEY(),db.NOT_NULL()))
