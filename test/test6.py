from SQLite3Fun import DataBase,Insert

DB=DataBase("sua")
DB.CreateTable("sua_sua",("id",DB.INT(),DB.PRIMARY_KEY()),("name",DB.TEXT()))
Insert().INSERT(DB.CreateDB(),"sua_sua",(1,">.< sua"))
Insert().INSERT(DB.CreateDB(),"sua_sua",(2,"sua..."))
