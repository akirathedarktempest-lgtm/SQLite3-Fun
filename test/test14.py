from SQLite3Fun import DataBase, AlterTable

db=DataBase("testing")
db.CreateTable("hello",("name",db.TEXT()),("id",db.INT(),db.PRIMARY_KEY()))
alter=AlterTable()
alter.ADD_COLUMN(db.CreateDB(),"hello","numbers",db.ANY())
AlterTable().DROP_COLUMN(db.CreateDB(),"hello","numbers")
