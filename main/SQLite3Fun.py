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
    def CHECK(self,first_arg,comparision:str,second_arg, is_first_column_name=False,is_second_column=False):
        if is_first_column_name is True:
            first_arg=first_arg
        else:
            if type(first_arg) is str:
                first_arg=f'"{first_arg}'
            else:
                first_arg=first_arg
        if is_second_column is True:
            second_arg=second_arg
        else:
            if type(second_arg) is str:
                second_arg=f'"{second_arg}'
            else:
                second_arg=second_arg
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
        elif comparision=="=":
            return f"CHECK ({first_arg}={second_arg})"
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

    def CreateTable(self,table_name:str,*argu,may_exist=False):
        for w in table_name:
            if w in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                pass
            else:
                raise
        statement=""
        for a in argu:
            dt=0
            constrain=[]
            if type(a) is list or type(a) is tuple:
                name=a[0]
                for n in name:
                    if n in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                        pass
                    else:
                        raise "Wrong name"
                statement+=f"{name} "
                for u in a:
                    if u in constrain:
                        continue
                    if u==name:
                        continue
                    else:
                        statement+=f"{u} "
                    if u.upper()==self.BLOB() or u.upper()==self.INT() or u.upper()==self.REAL() or u.upper()==self.NULL() or u.upper()==self.TEXT():
                        dt+=1
                    else:
                        constrain.append(u)
                if a==argu[-1]:
                    pass
                else:
                    statement+=","
            else:
                raise
        if dt>1:
            raise
        else:
            pass
        db=self.CreateDB()
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        if may_exist is True:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({statement})")
        else:
            cursor.execute(f"CREATE TABLE {table_name}({statement})")
        connect.close()

    class AlterTable:

        def RENAME_TABLE(self,dbname:str,table_old_name:str,table_new_name:str):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"ALTER TABLE {table_old_name} RENAME TO {table_new_name}")
            connect.commit()
            connect.close()

        def RENAME_COLUMN(self,dbname:str,table_name:str,old_column_name:str,new_column_name:str):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
            connect.commit()
            connect.close()

        def DROP_COLUMN(self,dbname:str,table_name:str,column_name:str):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
            connect.commit()
            connect.close()

        def ADD_COLUMN(self,dbname:str,table_name:str,column_name:str,*datatype,constrains:str=None):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            con=""
            if "PRIMARY KEY" in constrains.upper() or "UNIQUE" in constrains.upper() or "NOT NULL" in constrains.upper():
                raise "Invalid Constrain"
            elif constrains:
                con+=constrains
            else:
                con=""
            dt=0
            dty=""
            for d in datatype:
                if d.upper()=="REAL" or d.upper=="TEXT" or d.upper()=="INT" or d.upper()=="INTEGER" or d.upper()=="NULL" or d.upper()=="BLOB":
                    dt+=1
                    dty+=d.upper()
                else:
                    raise
            if dt>1:
                raise "Only one datatype"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {dty} {con}")
            connect.commit()
            connect.close()

    class Update:
        def __init__(self):
            pass

        def UPDATE(self,dbname:str,table_name:str,column:str,set:str,where:bool=False):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            if where==False:
                where=""
            elif where==True:
                where=f"WHERE {where}"
            else:
                raise
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"UPDATE {table_name} SET {column}={set} {where}")
            connect.commit()
            connect.close()

AlterTable=DataBase.AlterTable
Update=DataBase.Update
#we are making this AlterTable to use it properly, it is is object right now 
