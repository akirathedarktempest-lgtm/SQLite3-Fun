from SQLite3Fun import Where,Select,Column

GROUP=Select.GroupBy().GROUP_BY(
    "hhhh",True,Select.GroupBy().HAVING(
        Select.Aggregate().AVG
        ("hlll",True,[Where().COMPARISION("helll",12,"<")]),
            12,
            "<>"
            )
            )

print(GROUP)
column=Column().COLUMN("hell","yeahhhh",Select.Aggregate().AVG("hlll",True,[Where().COMPARISION("helll",12,"<")]))
print(f"SELECT {column} FROM tab {GROUP}")