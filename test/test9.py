from SQLite3Fun import Where

data=Where()
print(data.COMPARISION("hell",b'hello',"<>"))
print(data.IN("hell",["city","state"]))
print(data.LIKE("hell","/%h/%","/"))
