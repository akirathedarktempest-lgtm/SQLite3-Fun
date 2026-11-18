import sqlite3

class DataBase:
    def __init__(self,dbName:str):
        self.dbName=dbName

    def DROP_TABLE(self,table_name:str):
        try:
            db=self.CreateDB()
            connect=sqlite3.connect(db)
            cursor=connect.cursor()
            cursor.execute(f"DROP TABLE {table_name}")
            connect.commit()
            connect.close()
        except Exception as e:
            raise Error(e)

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
    def ANY(self):
        return "ANY"

    def PRIMARY_KEY(self):
        return "PRIMARY KEY"
    def UNIQUE(self):
        return "UNIQUE"
    def NOT_NULL(self):
        return "NOT NULL"
    def DEAULT(self,arg):
        try:
            if type(arg) is bytes:
                h=arg.hex()
                arg=f"X'{h}'"
            elif type(arg) is str:
                arg="'arg'"
            elif type(arg) is list or type(arg) is set or type(arg) is tuple:
                raise TypeError(f"Invalid type error: {type(arg)}")
            else:
                pass
            return f"DEFAULT ({arg})"
        except Exception as e:
            raise Exception(e)
        
    def CHECK(self,*arg:Where|tuple|list):
        try:
            if type(arg) is list or type(arg) is tuple:
                statement=""
                for a in arg:
                    statement+=a
                return f"CHECK({statement})"
            else:
                raise "Invalid type!"
        except Exception as e:
            raise Exception(e)

    def CreateDB(self):
        for s in self.dbName:
            if s==".":
                if s==self.dbName[-3]:
                    if self.dbName.endswith(".db"):
                        continue
                    else:
                        pass
                elif s==self.dbName[-8]:
                    if self.dbName.endswith(".sqlite3"):
                        continue
                    else:
                        pass
                else:
                    pass
            if s in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1023456789_ ":
                pass
            else:
                raise Error(f"Invalid database name '{s}'")
        if self.dbName.endswith(".db") or self.dbName.endswith(".sqlite3"):
            connect=sqlite3.connect(self.dbName)
            connect.close()
            return self.dbName
        else:
            connect=sqlite3.connect(f"{self.dbName}.db")
            connect.close()
            return f"{self.dbName}.db"

    def CreateTable(self,table_name:str,*argu,may_exist=False):
        try:
            db=self.CreateDB()
            connect=sqlite3.connect(db)
            for w in table_name:
                if w in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                    pass
                else:
                    raise Error("Invalid table name error!")
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
                            raise Error("Invalid column name!")
                    statement+=f"{name} "
                    for u in a:
                        if type(u) is not str:
                            raise TypeError(f"Expecting a str but got {type(u)}")
                        if u in constrain:
                            continue
                        if u==name:
                            continue
                        else:
                            statement+=f"{u} "
                        if u.upper()==self.BLOB() or u.upper()==self.INT() or u.upper()==self.REAL() or u.upper()==self.NULL() or u.upper()==self.TEXT() or u.upper()==self.ANY():
                            dt+=1
                        else:
                            constrain.append(u)
                    if a==argu[-1]:
                        pass
                    else:
                        statement+=","
                else:
                    raise TypeError(f"Expected a list or tuple but got {type(a)}")
                if dt>1:
                    raise Error(f"A column can only have one have one type, got {dt} instead!")
                else:
                    pass
            cursor=connect.cursor()
            if may_exist is True:
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({statement})")
            else:
                cursor.execute(f"CREATE TABLE {table_name}({statement})")
            connect.close()
        except Exception as e:
            raise Error(e)

    class AlterTable:

        def RENAME_TABLE(self,dbname:str,table_old_name:str,table_new_name:str):
            try:
                dbname=DataBase(dbname).CreateDB()
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"ALTER TABLE {table_old_name} RENAME TO {table_new_name}")
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

        def RENAME_COLUMN(self,dbname:str,table_name:str,old_column_name:str,new_column_name:str):
            try:
                dbname=DataBase(dbname).CreateDB()
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

        def DROP_COLUMN(self,dbname:str,table_name:str,column_name:str):
            try:
                dbname=DataBase(dbname).CreateDB()
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

        def ADD_COLUMN(self,dbname:str,table_name:str,column_name:str,datatype:str,constrains:tuple=None):
            try:
                dbname=DataBase(dbname).CreateDB()
                con=""
                dty=""
                if constrains is None:
                    con=""
                else:
                    if type(constrains) is not list and type(constrains) is not tuple:
                        raise TypeError(f"Expected list or tuple but got {type(constrains)}")
                    else:
                        for c in constrains:
                            if c.upper()=="PRIMARY KEY" or c.upper()=="UNIQUE":
                                raise Error("You can't add a column with PRIMARY KEY or UNIQUE")
                            elif c.upper()=="NOT NULL":
                                for co in constrains:
                                    n=1
                                    if "DEFAULT" in co.upper():
                                        n=0
                                        break
                                    else:
                                        pass
                                if n==1:
                                    raise Error("NOT NULL without DEFAULT is invalid")
                                else:
                                    con+="NOT NULL "
                            else:
                                con+=F"{c} "
                if type(datatype) is str:
                    if datatype.upper()=="TEXT" or datatype.upper()=="INT" or datatype.upper()=="INTEGER" or datatype.upper()=="BLOB" or datatype.upper()=="REAL" or datatype.upper()=="NULL" or datatype.upper()=="ANY":
                        pass
                    else:
                        raise Error("Invalid datatype for sqlite3")
                else:
                    raise TypeError(f"Expected str but got {type(datatype)}")
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {datatype} {con}")
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

    class Update:
        def __init__(self):
            pass

        def __str(self,content:str):
            try:
                return content.replace("/s/","'")
            except Exception as e:
                raise Error(e)

        def UPDATE(self,dbname:str,table_name:str,column:str,set:str,where:str=None):
            try:
                dbname=DataBase(dbname).CreateDB()
                if where is None:
                    where=""
                elif type(where) is str:
                    where=self.__str(where)#i was keeping __str(set) not __set(where)...lol, but problem solved
                    where=f" WHERE {where}"
                else:
                    raise Error("Invalid datatype of WHERE clause")
                set=self.__str(set)
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"UPDATE {table_name} SET {column}={set}{where}")
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

    class Insert:
        def __init__(self):
            pass

        def INSERT(self,dbname:str,table_name:str,insert:tuple|list,all_columns:bool=True,specific_column:tuple|list=None):
            try:
                dbname=DataBase(dbname).CreateDB()
                if specific_column is None:
                    if all_columns is False:
                        raise Error("Specific columns is None and all columns false is invalid!")
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
                            raise Error(f"Expected tuple or list but got {type(specific_column)}")
                        if all_columns is True:
                            raise Error("Inserted specific columns but all column True is invalid!")
                        else:
                            specific=""
                            for sc in specific_column:
                                if type(sc) is str:
                                    pass
                                else:
                                    raise Error(f"Column name expected to be str but got {type(sc)}")
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
                        raise Error("Number of inserted values is not equal to the number of the columns")
                else:
                    raise Error("Unknown error")
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(f"{statement}",insert)
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

    class Delete:
        def __init__(self):
            pass

        def __str(self,content:str):
            try:
                return content.replace("/s/","'")
            except Exception as e:
                raise Error(e)

        def DELETE(self,dbname:str,table_name:str,where:tuple|list=None):
            try:
                dbname=DataBase(dbname).CreateDB()
                if where is None:
                    statement=f"DELETE FROM {table_name}"
                else:
                    if type(where) is list or type(where) is tuple:
                        pass
                    else:
                        raise
                    wh=""
                    for w in where:
                        if type(w) is str:
                            wh+=w
                        else:
                            raise Error(f"Expected str but got {type(w)}")
                    where=self.__str(wh)
                    statement=f"DELETE FROM {table_name} WHERE {where}"
                connect=sqlite3.connect(dbname)
                cursor=connect.cursor()
                cursor.execute(statement)
                connect.commit()
                connect.close()
            except Exception as e:
                raise Error(e)

    class Select:
        def __init__(self):
            pass

        class OrderBy:
            def __init__(self):
                pass

            def ORDER_BY(self,column:str,by:str="ASC"):
                try:
                    if by.upper()=="ASC" or by.upper()=="DESC":
                        return f"ORDER BY {column} {by.upper()}"
                    else:
                        raise Error("Invalid by!")
                except Exception as e:
                    raise Error(e)

        class GroupBy:
            def __init__(self):
                pass

            def GROUP_BY(self,column:str,having:bool=False,aggregate_comparision=None):
                try:
                    if aggregate_comparision is not None and having is False:
                        raise Error("Having false and using aggregate is invalid")
                    else:
                        if having is False and aggregate_comparision is None:
                            h=""
                        else:
                            h=f" HAVING {aggregate_comparision}"
                        return f"GROUP BY {column}{h}"
                except Exception as e:
                    raise Error(e)

            def HAVING(self,aggregate:str,value,comparision:str="="):
                try:
                    if comparision=="=" or comparision=="<>" or comparision==">" or comparision=="<" or comparision=="<=" or comparision==">=":
                        if type(value) is list or type(value) is tuple or type(value) is set or type(value) is dict:
                            raise Error("Invalid type!")
                        elif type(value) is bytes:
                            v=value.hex()
                            value=f"X'{v}'"
                        elif type(value) is str:
                            value=f"'{value}'"
                        else:
                            value=value
                        return f"{aggregate} {comparision} {value}"
                    else:
                        raise "Invalid comparision sign!"
                except Exception as e:
                    raise Error(e)

        class Aggregate:

            def __init__(self):
                pass

            def COUNT(self,column:str="*",distinct:bool=False,filter:tuple|list=None):
                try:
                    if filter is None:
                        f=""
                    else:
                        f=" FILTER (WHERE "
                        if type(filter) is list or type(filter) is tuple:
                            pass
                        else:
                            raise Error(f"Expected list or tuple but got {type(filter)}")
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
                except Exception as e:
                    raise Error(e)

            def AVG(self,column:str,distinct:bool=False,filter:tuple|list=None):
                try:
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
                                raise Error(f"Expected list or tuple but got {type(filter)}")
                        if distinct is True:
                            return f'AVG(DISTINCT {column}){f}'
                        else:
                            return f"AVG({column}){f}"
                    else:
                        raise Error(f"Expected column name to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

            def MAX(self,column:str,distinct:bool=False,filter:tuple|list=None):
                try:
                    if filter is None:
                        f=""
                    else:
                        if type(filter) is list or type(filter) is tuple:
                            f=" FILTER (WHERE "
                            for fi in filter:
                                f+=f"{fi}"
                            f+=")"
                        else:
                            raise Error(f"Expected list or tuple but got {type(filter)}")
                    if type(column) is str:
                        if distinct is True:
                            return f"MAX(DISTINCT {column}){f}"
                        else:
                            return f"MAX({column}){f}"
                    else:
                        raise Error(f"Expected column to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

            def MIN(self,column:str,distinct:bool=False,filter:tuple|list=None):
                try:
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
                                raise Error(f"Expected filter to be list or tuple but got {type(filter)}")
                        if distinct is True:
                            return f"MIN(DISTINCT {column}){f}"
                        else: 
                            return f"MIN({column}){f}"
                    else:
                        raise Error(f"Expected column to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

            def TOTAL(self,column:str,distinct:bool=False,filter:tuple|list=None):
                try:
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
                                raise Error(f"Expected filter to be list or tuple but got {type(filter)}")
                        if distinct is True:
                            return f"TOTAL(DISTINCT {column}){f}"
                        else:
                            return f"TOTAL({column}){f}"
                    else:
                        raise Error(f"Expected column to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

            def SUM(self,column:str,distinct:bool=False,filter:tuple|list=None):
                try:
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
                                raise Error(f"Expected filter to be list or tuple but got {type(filter)}")
                        if distinct is True:
                            return f"SUM(DISTINCT {column}){f}"
                        else:
                            return f"SUM({column}){f}"
                    else:
                        raise Error(f"Expected column to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

            def GROUP_CONCAT(self,column:str,separator:str=",",distinct:bool=False,filter:tuple|list=None,order_by:Select.OrderBy=None):
                try:
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
                                raise Error(f"Expected filter to be list or tuple but got {type(filter)}")
                        if order_by is None:
                            order=""
                        else:
                            order=f" {order_by}"
                        if distinct is True:
                            d+="DISTINCT "
                        else:
                            d=""
                        if separator==",":
                            return f"GROUP_CONCAT({d}{column}{order}){f}"
                        else:
                            if type(separator) is str:
                                if d=="":
                                    return f"GROUP_CONCAT({d}{column},{separator}{order}){f}"
                                else:
                                    raise Error("You can't use separator with distinct")
                            else:
                                raise Error(f"Expected separator to be str but got {type(separator)}")
                    else:
                        raise Error(f"Expected column to be str but got {type(column)}")
                except Exception as e:
                    raise Error(e)

        class Fetch:
            def __init__(self):
                pass

            def FETCHALL(self,dbname:str,table_name:str,columns:Column="*",where:Where=None,group_by:Select.GroupBy=None,order_by=None):
                try:
                    if where is None:
                        w=""
                    else:
                        w=" WHERE "
                        for wh in where:
                            w+=wh
                    if group_by is None:
                        gb=""
                    else:
                        gb=f" {group_by}"
                    if order_by is None:
                        ob=""
                    else:
                        ob=f" {order_by}"
                    dbname=DataBase(dbname).CreateDB()
                    connect=sqlite3.connect(dbname)
                    cursor=connect.cursor()
                    cursor.execute(f"SELECT {columns} FROM {table_name}{w}{gb}{ob}")
                    data=cursor.fetchall()
                    connect.close()
                    return data
                except Exception as e:
                    raise Error(e)

            def FETCHONE(self,dbname:str,table_name:str,columns:Column="*",where:Where=None,group_by:Select.GroupBy=None,order_by=None):
                try:
                    if where is None:
                        w=""
                    else:
                        w=" WHERE "
                        for wh in where:
                            w+=wh
                    if group_by is None:
                        gb=""
                    else:
                        gb=f" {group_by}"
                    if order_by is None:
                        ob=""
                    else:
                        ob=f" {order_by}"
                    dbname=DataBase(dbname).CreateDB()
                    connect=sqlite3.connect(dbname)
                    cursor=connect.cursor()
                    cursor.execute(f"SELECT {columns} FROM {table_name}{w}{gb}{ob}")
                    data=cursor.fetchone()
                    connect.close()
                    return data
                except Exception as e:
                    raise Error(e)

            def FETCHMANY(self,dbname:str,table_name:str,columns:Column="*",size:int=1,where:Where=None,group_by:Select.GroupBy=None,order_by=None):
                try:
                    if where is None:
                        w=""
                    else:
                        w=" WHERE "
                        for wh in where:
                            w+=wh
                    if group_by is None:
                        gb=""
                    else:
                        gb=f" {group_by}"
                    if order_by is None:
                        ob=""
                    else:
                        ob=f" {order_by}"
                    dbname=DataBase(dbname).CreateDB()
                    connect=sqlite3.connect(dbname)
                    cursor=connect.cursor()
                    cursor.execute(f"SELECT {columns} FROM {table_name}{w}{gb}{ob}")
                    data=cursor.fetchmany(size)
                    connect.close()
                    return data
                except Exception as e:
                    raise Error(e)
                
    class Where:
        def __init__(self):
            pass

        def COMPARISION(self,column_name:str,value,comparision:str='='):
            try:
                if type(value) is str:
                    value=f'"{value}"'
                elif type(value) is bytes:
                    h=value.hex()
                    value=f"X'{h}'"
                elif type(value) is list or type(value) is dict or type(value) is set or type(value) is tuple:
                    raise Error("Invalid type!")
                else:
                    pass
                if comparision ==">=" or comparision =="<=" or comparision =="=" or comparision =="<>" or comparision==">" or comparision =="<":
                    return f"{column_name} {comparision} {value}"
                else:
                    raise Error(f"Invalid comparision sign {comparision}")
            except Exception as e:
                raise Error(e)

        def AND(self):
            return " AND "
        def OR(self):
            return " OR "
        def NOT(self):
            return " NOT "

        def IN(self,column:str,values:tuple|list):
            try:
                if type(values) is list or type(values) is tuple:
                    pass
                else:
                    raise Error(f"Expectd list or tuple but got {type(values)}")
                statement=""
                for v in values:
                    if type(v) is str:
                        statement+=f"'{v}'"
                    elif type(v) is bytes:
                        b=v.hex()
                        statement+=f"X'{b}'"
                    elif type(v) is list or type(v) is dict or type(v) is set:
                        raise Error("Invalid type!")
                    else:
                        statement+=f"{v}"
                    if v==values[-1]:
                        pass
                    else:
                        statement+=","
                return f"{column} IN ({statement})"
            except Exception as e:
                raise Error(e)

        def LIKE(self,column:str,islike,escape:str=None):
            try:
                like=""
                if type(islike) is list or type(islike) is dict or type(islike) is set:
                    raise Error("Invalid type!")
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
            except Exception as e:
                raise Error(e)

        def IS_NULL(self,column:str):
            return f"{column} IS NULL"
        def IS_NOT_NULL(self,column:str):
            return f"{column} IS NOT NULL"

    class Column:
        def COLUMN(self,*columns:str):
            try:
                col=""
                for c in columns:
                    col+=c
                    if c==columns[-1]:
                        pass
                    else:
                        col+=","
                return col
            except Exception as e:
                raise Error(e)

AlterTable=DataBase.AlterTable
Update=DataBase.Update
Insert=DataBase.Insert
Select=DataBase.Select
Aggregate=DataBase.Select.Aggregate
Where=DataBase.Where
Column=DataBase.Column
Delete=DataBase.Delete

class Error(Exception):
    pass

if "__main__"==__name__:
    pass
