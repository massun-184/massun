#株式投資メモから基本情報をスクレイピング(単元数はなかった)
from bs4 import BeautifulSoup
import requests
import sqlite3

#銘柄コードを入力
#code = format(int(input("銘柄コードを入力してください:")),"04")
code = 7203
print(code)
year = 2019
url =  "https://kabuoji3.com/stock/{}/{}/".format(code, year)
#print(url)

#header情報
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0;Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/87.0.4280.66 \
    Safari/537.36"
}
#HTMLを取得
response = requests.get(url, headers = headers)
#print(response)

#HTMLを抽出
soup = BeautifulSoup(response.content, "html.parser")
#print(soup)

#銘柄名
name = soup.find("h1").text.split()[1]
print(name)
#上場市場
market = soup.find(class_="dread").text.split("（")[0]
print(market)
#業種
sector = soup.find(class_="dread").text.split("（")[1].split("）")[0]
print(sector)


meigara = [[int(code),name,market,sector],[0,"i","u","e"]]
print(meigara)

#sqliteに格納
dbname = "kabuoji.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS meigara(code INTEGER PRIMARY KEY AUTOINCREMENT,\
    name STRING,market STRING,sector STRING)")
cur.executemany("INSERT INTO meigara VALUES(?,?,?,?)",meigara)
conn.commit()
conn.close()