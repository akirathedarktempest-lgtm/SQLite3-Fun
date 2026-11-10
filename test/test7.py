from SQLite3Fun import DataBase

db=DataBase("sua.db")
db.CreateTable("sua_sua",("type",db.TEXT()),("sua",db.TEXT()),("id",db.INT(),db.PRIMARY_KEY()),may_exist=True)
db.Insert().INSERT(db.CreateDB(),"sua_sua",("cute sua","meow!",1))
db.Insert().INSERT(db.CreateDB(),"sua_sua",("angry sua",">.<",2))
print("done...?")
db.Delete().DELETE(db.CreateDB(),"sua_sua","sua=/s/meow!/s/")
#/s/ == ' or /s/=="