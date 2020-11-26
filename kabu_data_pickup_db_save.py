#銘柄名にスペースがあるとmarket情報が正しく取れないので注意
from pyquery import PyQuery
import time
import sqlite3

dbname = "kabu.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS meigara(code INTEGER PRIMARY KEY AUTOINCREMENT,name STRING,short_name STRING,market STRING,sector STRING,unit INTEGER)")

#銘柄コードを記入
code = format(7203,"04")
print(code)

url =  "https://kabutan.jp/stock/?code={}".format(code)
#print(url)

#urlのhtml？抽出
q = PyQuery(url)
#print(q)

#企業名
name = q.find("title").text().split()[0].split("（")[0].split("【")[0]
print(name)
#企業名略称
short_name = q.find("li")("span").text().split()[1].split("(")[0]
print(short_name)
#上場市場
market = q.find("#stockinfo_i1").text().split()[1]
print(market)
#業種
sector = q.find("#stockinfo_i2").text().split()[1]
print(sector)
#単元
unit = q.find("#stockinfo_i2").text().split()[3].split("株")[0]
print(unit)

meigara = [(int(code),name,short_name,market,sector,int(unit))]
print(meigara)

#sqliteに格納
cur.executemany("INSERT INTO meigara VALUES(?,?,?,?,?,?)",meigara)
conn.commit()
conn.close()
