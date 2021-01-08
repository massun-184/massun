from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime 
import time
import openpyxl
import numpy as np
import plotly.graph_objects as go
import talib as ta

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
            #df["日付"] = [datetime.strptime(i,"%Y-%m-%d") for i in df["日付"]]
            col = ["始値","高値","安値","終値","出来高","終値調整"]
            #print(df["日付"])
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
def codelistget():
    code_list = []
    #※↓ダウンロードしたデータファイルは「.xls」なので「.xlsx」に変換すること
    wb = openpyxl.load_workbook("shoukencode.xlsx")
    ws = wb["Sheet1"]
    for row in ws.iter_rows(min_row = 2,max_col = 3,min_col = 2):
        values = []
        for c in row:
            values.append(c.value)
        #print(values)
        code_list.append(values)
    #print(code_list)
    return code_list

code_list = codelistget()
#コード手入力
input_code = list(map(int,input("コードを入力してください:").split()))
#input_code = [7203] #一個だけ
cn = code_name(input_code)

#取得したい年を入力(複数年可能)
#year = list(map(int,input("取得したい年を入力してください:").split()))
year = [2019,2020]

k = cn[0][0]
v = cn[0][1]
print(k,v)


dfs = get_kabuka(k,year)
data = concatenate(dfs) 
""" 
for j in cn:
    k = j[0]
    v = j[1]
    print(k,v)
    dfs = get_kabuka(k,year)
    data = concatenate(dfs) 
    #複数のデータフレームをcsvで保存(エンコード:JIS) 
    #data.to_csv('{}-{}.csv'.format(k,v), encoding="shift-jis")
 """
#print(k,v)
#print(data)

#ここからローソク足チャート作成
#data = data.drop(["出来高","終値調整"], axis = 1)
#print(data)

x = np.arange(len(data["日付"]))

#x軸に描写する間隔と日付
interval = 20
vals = [data.index[i*interval] for i in range(len(data)//interval+1)]
labels = [data.loc[i*interval,"日付"] for i in range(len(data)//interval +1)]
#print(vals)
#print(labels)

fig = go.Figure(
    data = go.Candlestick(
        x = x,
        open = data["始値"],
        high = data["高値"],
        low = data["安値"],
        close = data["終値"],
        hovertext = ["日付:{}<br>始値:{}<br>高値:{}<br>安値:{}<br>終値:{}"
            .format(data.loc[i,"日付"],data.loc[i,"始値"],data.loc[i,"高値"],data.loc[i,"安値"],data.loc[i,"終値"]) for i in range(len(data))] ,
        hoverinfo = "text",
        name = "ローソク足"
    ),
    layout = go.Layout(
        xaxis = dict(
            ticktext = labels,
            tickvals = vals,
            tickangle = -45
        ),
        yaxis = dict(
            title = "株価[円]",
            side = "left"
        )
    )
)



#移動平均線(5日平均,25日平均,75) 
SMA = [5,25,75]
for day in SMA:
    sma = "{}日平均".format(day)
    data[sma] = ta.SMA(data["終値"], timeperiod = day)
    fig.add_trace(
        go.Scatter(
            x = x,
            y = data[sma],
            mode = "lines",
            name = sma,
            hovertext = ["日付:{}".format(data.loc[i,"日付"]) for i in range(day,len(dfs))],
            #hoverinfo = "text",
        ),
        #row = 1,
        #col = 1,
    )

data['丸坊主'] = ta.CDLMARUBOZU(data['始値'],data['高値'],data['安値'],data['終値']) * data['高値'] / 100
#data['Engulfing_Pattern'] = ta.CDLENGULFING(data['始値'],data['高値'],data['安値'],data['終値']) * data['終値'] / 100
data['カラカサ線'] = ta.CDLHAMMER(data['始値'],data['高値'],data['安値'],data['終値']) * data['高値'] / 100
data['トンボ'] = ta.CDLDRAGONFLYDOJI(data['始値'],data['高値'],data['安値'],data['終値']) * data['高値'] / 100    
pattern_list = list(data.loc[:,'丸坊主':'トンボ'].columns)
label_list = [m + '_label' for m in list(data.loc[:,'丸坊主':'トンボ'].columns)]
data[pattern_list] = data[pattern_list].where(~(data[pattern_list] == 0.0), np.nan)

 # 売り買いラベルの作成
data[label_list] = data[pattern_list]
data[label_list] = data[label_list].where(~(data[label_list] > 0), 1)
data[label_list] = data[label_list].where(~(data[label_list] < 0), -1)
data[label_list] = data[label_list].where(~(data[label_list] == 1), 'b')
data[label_list] = data[label_list].where(~(data[label_list] == -1), 's')

# 発生価格の絶対値化
data[pattern_list] = data[pattern_list].abs()

for pattern in list(data.loc[:,'丸坊主':'トンボ'].columns):
    fig.add_trace(go.Scatter(x=x, y=data[pattern],mode='markers+text',text=data[label_list],textposition="top center",name=pattern,
                                marker = dict(size = 9),opacity=0.8))

fig.show()