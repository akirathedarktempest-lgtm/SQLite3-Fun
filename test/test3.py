from SQLite3Fun import DataBase

db=DataBase("trying")
db.CreateTable("table1",("name",db.TEXT()),may_exist=True)
alter=DataBase.AlterTable()
alter.RENAME_TABLE(db.CreateDB(),"table1","new_table")
