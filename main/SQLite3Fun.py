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
            if "PRIMARY KEY" in constrains.upper() or "UNIQUE" in constrains.upper():
                raise "Invalid Constrain"
            elif "NOT NULL" in constrains.upper():
                if "DEFAULT" in constrains.upper():
                    pass
                else:
                    raise
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

        def __str(self,content:str):
            return content.replace("/s/","'")

        def UPDATE(self,dbname:str,table_name:str,column:str,set:str,where:str=None):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            if where is None:
                where=""
            elif type(where) is str:
                where=self.__str(where)#i was keeping __str(set) not __set(where)...lol, but problem solved
                where=f"WHERE {where}"
            else:
                raise
            set=self.__str(set)
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"UPDATE {table_name} SET {column}={set} {where}")
            connect.commit()
            connect.close()

    class Insert:
        def __init__(self):
            pass

        def INSERT(self,dbname:str,table_name:str,insert:tuple|list,all_columns:bool=True,specific_column:tuple|list=None):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            if specific_column is None:
                if all_columns is False:
                    raise
                else:
                    question=f""
                    for ins in insert:
                        if ins==insert[-1]:
                            question+=f"?"
                        else:
                            question+=f"?,"
                    statement=f"INSERT INTO {table_name} VALUES ({question})"
            elif specific_column is not None:
                if len(insert)==len(specific_column):
                    if type(specific_column) is list or type(specific_column) is tuple:
                        pass
                    else:
                        raise
                    if all_columns is True:
                        raise
                    else:
                        specific=""
                        for sc in specific_column:
                            if type(sc) is str:
                                pass
                            else:
                                raise
                            if sc==specific_column[-1]:
                                specific+=f"{sc}"
                            else:
                                specific+=f"{sc},"
                        question=""
                        for ins in insert:
                            if ins==insert[-1]:
                                question+="?"
                            else:
                                question+="?,"
                        statement=f"INSERT INTO {table_name}({specific}) VALUES ({question})"
                else:
                    raise
            else:
                raise "Unknown error"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(f"{statement}",insert)
            connect.commit()
            connect.close()

    class Delete:
        def __init__(self):
            pass

        def __str(self,content:str):
            return content.replace("/s/","'")

        def DELETE(self,dbname:str,table_name:str,where=None):
            if dbname.endswith(".db") or dbname.endswith(".sqlite3"):
                dbname=dbname
            else:
                dbname=f"{dbname}.db"
            if where is None:
                statement=f"DELETE FROM {table_name}"
            else:
                if type(where) is str:
                    pass
                else:
                    raise
                where=self.__str(where)
                statement=f"DELETE FROM {table_name} WHERE {where}"
            connect=sqlite3.connect(dbname)
            cursor=connect.cursor()
            cursor.execute(statement)
            connect.commit()
            connect.close()

    class Select:
        def __init__(self):
            pass

        class OrderBy:
            def __init__(self):
                pass

            def ORDER_BY(self,column:str,by:str="ASC"):
                if by.upper()=="ASC" or by.upper()=="DESC":
                    return f"ORDER BY {column} {by.upper()}"
                else:
                    raise "Invalid by!"

        class Aggregate:

            def __init__(self):
                pass

            def COUNT(self,column:str="*",distinct:bool=False,filter:tuple|list=None):
                if filter is None:
                    f=""
                else:
                    f=" FILTER (WHERE "
                    if type(filter) is list or type(filter) is tuple:
                        pass
                    else:
                        raise
                    for fi in filter:
                        f+=f"{fi}"
                    f+=")"
                if column.upper()=="*":
                    return f"COUNT(*){f}"
                else:
                    if distinct is True:
                        return f"COUNT(DISTINCT {column}){f}"
                    else:
                        return f"COUNT({column}){f}"

            def AVG(self,column:str,distinct:bool=False,filter:tuple|list=None):
                if type(column) is str:
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is tuple or type(filter) is list:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise
                    if distinct is True:
                        return f'AVG(DISTINCT {column}){f}'
                    else:
                        return f"AVG({column}){f}"
                else:
                    raise

            def MAX(self,column:str,distinct:bool=False,filter:tuple|list=None):
                if filter is None:
                    f=""
                else:
                    if type(filter) is list or type(filter) is tuple:
                        f=" FILTER (WHERE "
                        for fi in filter:
                            f+=f"{fi}"
                        f+=")"
                    else:
                        raise
                if type(column) is str:
                    if distinct is True:
                        return f"MAX(DISTINCT {column}){f}"
                    else:
                        return f"MAX({column}){f}"
                else:
                    raise

            def MIN(self,column:str,distinct:bool=False,filter:tuple|list=None):
                if type(column) is str:
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is list or type(filter) is tuple:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise
                    if distinct is True:
                        return f"MIN(DISTINCT {column}){f}"
                    else: 
                        return f"MIN({column}){f}"
                else:
                    raise

            def TOTAL(self,column:str,distinct:bool=False,filter:tuple|list=None):
                if type(column) is str:
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is list or type(filter) is tuple:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise
                    if distinct is True:
                        return f"TOTAL(DISTINCT {column}){f}"
                    else:
                        return f"TOTAL({column}){f}"
                else:
                    raise

            def SUM(self,column:str,distinct:bool=False,filter:tuple|list=None):
                if type(column) is str:
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is list or type(filter) is tuple:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise
                    if distinct is True:
                        return f"SUM(DISTINCT {column}){f}"
                    else:
                        return f"SUM({column}){f}"
                else:
                    raise

            def GROUP_CONCAT(self,column:str,separator:str=",",distinct:bool=False,filter:tuple|list=None,order_by:Select.OrderBy=None):
                if type(column) is str:
                    d=""
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is list or type(filter) is tuple:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise
                    if order_by is None:
                        order=""
                    else:
                        order=f" {order_by}"
                    if distinct is True:
                        d+="DISTINCT "
                    else:
                        d=""
                    if separator==",":
                        return f"GROUP_CONCAT({d}{column}){f}{order}"
                    else:
                        if type(separator) is str:
                            if d=="":
                                return f"GROUP_CONCAT({d}{column},{separator}){f}{order}"
                            else:
                                raise "You can't use separator with distinct"
                        else:
                            raise
                else:
                    raise
    class Where:
        def __init__(self):
            pass

        def COMPARISION(self,column_name:str,value,comparision:str='='):
            if type(value) is str:
                value=f'"{value}"'
            elif type(value) is bytes:
                h=value.hex()
                value=f"X'{h}'"
            elif type(value) is list or type(value) is dict or type(value) is set:
                raise "Invalid type!"
            else:
                pass
            if comparision ==">=" or comparision =="<=" or comparision =="=" or comparision =="<>" or comparision==">" or comparision =="<":
                return f"{column_name} {comparision} {value}"
            else:
                raise "Invalid comparision"

        def AND(self):
            return " AND "
        def OR(self):
            return " OR "
        def NOT(self):
            return " NOT "

        def IN(self,column:str,values:tuple|list):
            statement=""
            for v in values:
                if type(v) is str:
                    statement+=f"'{v}'"
                elif type(v) is bytes:
                    b=v.hex()
                    statement+=f"X'{b}'"
                elif type(v) is list or type(v) is dict or type(v) is set:
                    raise "Invalid type!"
                else:
                    statement+=f"{v}"
                if v==values[-1]:
                    pass
                else:
                    statement+=","
            return f"{column} IN ({statement})"

        def LIKE(self,column:str,islike,escape:str=None):
            like=""
            if type(islike) is list or type(islike) is dict or type(islike) is set:
                raise "Invalid type!"
            elif type(islike) is str:
                like+=f"'{islike}'"
            elif type(islike) is bytes:
                h=islike.hex()
                like+=f"X'{h}'"
            else:
                like+=f"{islike}"
            if escape is None:
                statement=f"{column} LIKE {like}"
            else:
                statement=f"{column} LIKE {like} ESCAPE '{escape}'"
            return statement

AlterTable=DataBase.AlterTable
Update=DataBase.Update
Insert=DataBase.Insert
Select=DataBase.Select
Aggregate=DataBase.Select.Aggregate
Where=DataBase.Where

if "__main__"==__name__:
    pass
