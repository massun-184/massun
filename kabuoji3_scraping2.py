#指定した銘柄の価格データを取得
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import sqlite3
import time

#銘柄コードを入力
#code = format(int(input("銘柄コードを入力してください:")),"04")
code = 7203
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

#<tr>タグをリストに格納
tag = soup.find_all("tr")
#print(len(tag))

#見出しを取得(内包表記)
head = [h.text for h in tag[0].find_all("th")]
""" head = []  #上と同じ
for h in tag[0].find_all("th"):
    head.append(h.text)
print(head) """

#日付、始値、高値、安値、終値、出来高、終値調整のデータを取得(内包表記)
data = []
for i in range(1,len(tag)):
    data.append([d.text for d in tag[i].find_all("td")])
"""     data2 = [] #上と同じ
    for d in tag[i].find_all("td"):
        data2.append(d.text)
    data.append(data2) """
#print(data)

#取得したデータをデータフレーム化
df = pd.DataFrame(data, columns = head)
#print(df)

#テキストデータから日付をタイムスタンプに、他はfloatにする
#df["日付"] = [datetime.strptime(i,"%Y-%m-%d") for i in df["日付"]]
""" dfs = []
for i in df["日付"]: #多分上と同じ
    dfs.append(datetime.strptime(i,"%Y-%m-%d"))
df["日付"] = dfs """
#print(df["日付"])

col = ["始値","高値","安値","終値","出来高","終値調整"]
for c in col:
    df[c] = df[c].astype(float)
    #print(df[c])

#データフレームをsqlファイルに変換
#実行する度、同じデータが入れ込まれるので注意
file_name = "kabuoji2.db"
conn = sqlite3.connect(file_name)

df.to_sql("トヨタ自動車", conn, if_exists = "append", index = None)

conn.close()
