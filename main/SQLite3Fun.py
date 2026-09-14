import sqlite3

class DataBase:
    def __init__(self,dbName:str):
        self.dbName=dbName#database name

    def __close(self,commit):
        commit.close()#this function is there to close the database, you can't use it outside, private function

    def CreateDB(self):#creates the database
        if self.dbName.endswith(".db") or self.dbName.endswith(".sqlite3"):
            connect=sqlite3.connect(self.dbName)
            self.__close(connect)
        else:
            connect=sqlite3.connect(f"{self.dbName}.db")
            self.__close(connect)
