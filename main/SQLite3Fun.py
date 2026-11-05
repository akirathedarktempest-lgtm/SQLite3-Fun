import sqlite3

class DataBase:
    def __init__(self,dbName:str):
        self.dbName=dbName

    def INT(self):
        return "INTEGER"
    def TEXT(self):
        return "TEXT"
    def BLOB(self):
        return "BLOB"
    def NULL(self):
        return "NULL"
    def REAL(self):
        return "REAL"

    def PRIMARY_KEY(self):
        return "PRIMARY KEY"
    def UNIQUE(self):
        return "UNIQUE"
    def NOT_NULL(self):
        return "NOT NULL"
    def DEAULT(self,arg):
        return f"DEFAULT ({arg})"
    def CHECK(self,first_arg,comparision:str,second_arg):
        if type(first_arg) is str:
            first_arg=f'"{first_arg}'
        if type(second_arg) is str:
            second_arg=f'"{second_arg}'
        if comparision==">":
            return f"CHECK ({first_arg}>{second_arg})"
        elif comparision=="<":
            return f"CHECK ({first_arg}<{second_arg})"
        elif comparision==">=":
            return f"CHECK ({first_arg}>={second_arg})"
        elif comparision=="<=":
            return f"CHECK ({first_arg}<={second_arg})"
        elif comparision=="<>":
            return f"CHECK ({first_arg}<>{second_arg})"
        else:
            raise "Wrong comparision :("

    def CreateDB(self):
        if self.dbName.endswith(".db") or self.dbName.endswith(".sqlite3"):
            connect=sqlite3.connect(self.dbName)
            connect.close()
            return self.dbName
        else:
            connect=sqlite3.connect(f"{self.dbName}.db")
            connect.close()
            return f"{self.dbName}.db"

    def CreateTable(self,table_name:str,*argu):
        for w in table_name:
            if w in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                pass
            else:
                raise
        statement=""
        for a in argu:
            if type(a) is list or type(a) is tuple:
                name=a[0]
                statement+=f"{name} "
                for u in a:
                    if u==name:
                        continue
                    else:
                        statement+=f"{u} "
                if a==argu[-1]:
                    pass
                else:
                    statement+=","
            else:
                raise
        db=self.CreateDB()
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        cursor.execute(f"CREATE TABLE {table_name}({statement})")
        connect.close()
