from SQLite3Fun import DataBase,Where,Select,Insert

db=DataBase("meowwwwwww.db")
insert=Insert()
where=Where()
select=Select()
db.CreateTable("meowww",("id",db.INT(),db.PRIMARY_KEY(),db.NOT_NULL()),("cat_name",db.TEXT(),db.UNIQUE()))
w="w"
for i in range(3):
    n=i+1
    insert.INSERT(db.CreateDB(),"meowww",(i,f"meow{w*n}"))
d2=select.Fetch().FETCHALL(db.CreateDB(),"meowww")
d1=select.Fetch().FETCHALL(db.CreateDB(),"meowww",where=where.COMPARISION("id",1,"="))
print(d1)
print(d2)