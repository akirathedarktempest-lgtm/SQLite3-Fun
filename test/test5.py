from SQLite3Fun import DataBase,Update
import sqlite3

db=DataBase("sua")
db.CreateTable("characters",("cuteSua",db.TEXT()),("angrySua",db.TEXT()),("silentSua",db.TEXT()),("id",db.INT(),db.PRIMARY_KEY()),may_exist=True)
connect=sqlite3.connect(db.CreateDB())
cursor=connect.cursor()
cursor.execute("INSERT INTO characters VALUES (?,?,?,?)",["sua",">.< sua","sua...",3])#didn't add insert function yet, so we are using it manually
connect.commit()
connect.close()
print("done...")
Update().UPDATE(db.CreateDB(),"characters","cuteSua",":str:(˶˃ ᵕ ˂˶) sua:str:","id=3")#problem at where condition...but i don't know why?
print("Did it work?")
connect=sqlite3.connect("sua.db")
cursor=connect.cursor()
cursor.execute("SELECT cuteSua FROM characters")
data=cursor.fetchall()
print(data)
connect.close()