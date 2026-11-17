from SQLite3Fun import DataBase,Delete,Where,Insert,Select

db=DataBase("hell.db")
db.CreateTable("hello",("name",db.TEXT(),db.UNIQUE()),("id",db.INT(),db.PRIMARY_KEY()))
num=1
for i in range(3):
    Insert().INSERT(db.CreateDB(),"hello",(f"a{i}",num))
    num+=1
select=Select().Fetch().FETCHALL(db.CreateDB(),"hello")
print(select)
Delete().DELETE(db.CreateDB(),"hello",[Where().COMPARISION("id",1)])
select=Select().Fetch().FETCHALL(db.CreateDB(),"hello")
print(select)