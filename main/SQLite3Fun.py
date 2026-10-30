vimport sqlite3

class DataBase:
    def __init__(self,dbName:str):
        self.dbName=dbName

    INT="INTEGER"
    TEXT="TEXT"
    BLOB="BLOB"
    NULL="NULL"
    REAL="REAL"

    PRIMARY_KEY="PRIMARY KEY"
    UNIQUE="UNIQUE"
    FOREGIN_KEY="FOREGIN KEY"
    NOT_NULL="NOT NULL"
    CHECK="CHECK"
    DEFAULT="DEFAULT"

    def CreateDB(self):
        if self.dbName.endswith(".db") or self.dbName.endswith(".sqlite3"):
            connect=sqlite3.connect(self.dbName)
            connect.close()
            return self.dbName
        else:
            connect=sqlite3.connect(f"{self.dbName}.db")
            connect.close()
            return f"{self.dbName}.db"
