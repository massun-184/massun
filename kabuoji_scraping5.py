#参考:https://non-dimension.com/kabuka-scraping/#toc9
#参考2:https://gammasoft.jp/blog/excel-vlookup-by-python/
#証券コードダウンロード先:https://www.jpx.co.jp/markets/statistics-equities/misc/01.html
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime 
import time
import openpyxl

#指定したコードの有無の検索
def code_name(input_code):
    masters = []
    for code in code_list:
        if code[0] in input_code:
            masters.append(code)

    masters_code = []
    for master in masters:
        masters_code.append(master[0])
    #print(masters_code)

    for ic in input_code:
        if ic not in masters_code:
            print("指定したコードの銘柄はありません:{}".format(ic))

    #print(masters)
    return(masters)

#指定したコードの株価を取得
def get_kabuka(code,year):
    dfs = []
    for y in year:
        try:
            print(y)
            url = 'https://kabuoji3.com/stock/{}/{}/'.format(code,y)
            #header情報
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0;Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/87.0.4280.66 \
                Safari/537.36"
            }
            #HTMLを取得
            response = requests.get(url,headers = headers)
            soup = BeautifulSoup(response.content, "html.parser")
            #<tr>タグをリストに格納
            tag = soup.find_all("tr")
            #見出しを取得
            head = [h.text for h in tag[0].find_all("th")]
            #日付、始値、高値、安値、終値、出来高、終値調整のデータを取得
            data = []
            for i in range(1,len(tag)):
                data.append([d.text for d in tag[i].find_all("td")])
            #取得したデータをデータフレーム化
            df = pd.DataFrame(data, columns = head)
            #テキストデータから日付をタイムスタンプに、他はfloatにする
            df["日付"] = [datetime.strptime(i,"%Y-%m-%d") for i in df["日付"]]
            col = ["始値","高値","安値","終値","出来高","終値調整"]
            for c in col:
                df[c] = df[c].astype(float)
            #各年のデータフレームを一つのリストにまとめる
            dfs.append(df)
        #例外処理ーデータがないとき
        except IndexError:
            print("No data")
            #サーバ負荷軽減のため、次に移行前に一時停止
            time.sleep(1)
    return dfs

#取得したデータフレームを連結
def concatenate(dfs):
    #連結する
    data = pd.concat(dfs,axis=0)
    #開始列を初期化
    data = data.reset_index(drop=True)
    col = ['始値','高値','安値','終値','出来高','終値調整']
    for c in col:
        data[c] = data[c].astype(float)
    return data

#コードリストの取り込み
code_list = []
#※↓ダウンロードしたデータファイルは「.xls」なので「.xlsx」に変換すること
wb = openpyxl.load_workbook("shoukencode.xlsx")
ws = wb["Sheet1"]
for row in ws.iter_rows(min_row=2,max_col=3,min_col=2):
    values = []
    for c in row:
        values.append(c.value)
    #print(values)
    code_list.append(values)
#print(code_list)

#コード手入力
#input_code = list(map(int,input("コードを入力してください:").split()))
input_code = [7203,9999]
cn = code_name(input_code)

#取得したい年を入力(複数年可能)
#year = list(map(int,input("取得したい年を入力してください:").split()))
year = [2018,2019,2020]

for j in cn:
    k = j[0]
    v = j[1]
    print(k,v)
    dfs = get_kabuka(k,year)
    data = concatenate(dfs) 
    #複数のデータフレームをcsvで保存(エンコード:JIS) 
    data.to_csv('{}-{}.csv'.format(k,v), encoding="shift-jis")