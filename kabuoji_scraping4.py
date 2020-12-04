#参考:https://non-dimension.com/kabuka-scraping/#toc9
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime 
import time

#指定したコードの株価を取得
def get_kabuka(code):
    dfs = []
    #取得したい年を入力(複数年可能)
    #year = list(map(int,input().split()))
    year = [2018,2019,2020]
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
    """ col = ['始値','高値','安値','終値','出来高','終値調整']
    for c in col:
        data[c] = data[c].astype(float) """
    return data

#作成したコードリスト(銘柄コードと銘柄名記載)を読み込む
code_list = pd.read_csv('code_list.csv')
#print(code_list.loc[0])


for i in range(len(code_list)):
    k = code_list.loc[i,'code']
    v = code_list.loc[i,'name']
    print(k,v)
    dfs = get_kabuka(k)
    data = concatenate(dfs) 
    #複数のデータフレームをcsvで保存(エンコード:JIS) 
    data.to_csv('{}-{}.csv'.format(k,v), encoding="shift-jis")