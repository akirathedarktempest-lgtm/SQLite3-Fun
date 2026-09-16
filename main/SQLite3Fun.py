import sqlite3

class DataBase:
    def __init__(self,dbName:str):
        self.dbName=dbName

    def CreateDB(self):
        if self.dbName.endswith(".db") or self.dbName.endswith(".sqlite3"):
            connect=sqlite3.connect(self.dbName)
            connect.close()
            return self.dbName
        else:
            connect=sqlite3.connect(f"{self.dbName}.db")
            connect.close()
            return f"{self.dbName}.db"

    def CreateTable(self,table:str,columns):
        if type(columns) is list or type(columns) is tuple:
            create=""
            for i in columns:
                if type(i) is list or type(columns) is tuple:
                    if len(i)==2:
                        if i==columns[-1]:
                            create+=f"{i[0]} {i[1]})"
                        else:
                            create+=f"{i[0]} {i[1]},"
                    else:
                        raise sqlite3.OperationalError(f"Can only have two arguments. For example\nids INT\nNot {i[0], i[1]}")
                else:
                    raise sqlite3.OperationalError("Must be given in list or tuple. For example\n[\"column_name\" \"INT\"]")
            database=self.CreateDB()
            connect=sqlite3.connect(database)
            cursor=connect.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({create}")
            connect.close()#makes a simple table, but will need many changes and error handling here

"""
from SQLite3Fun import DataBase
database=DataBase("project.db")
database.CreateTable("table1",[["name","TEXT"],["ids","INT"]])
#this will make a database named project.db, and then a table with two columns name (having text, str type) and ids (having number, integer)
"""
