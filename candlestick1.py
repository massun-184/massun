#参考:https://non-dimension.com/candlechart-with-plotly/#toc1
#ローソク足チャート

import pandas as pd
import numpy as np
import plotly.graph_objects as go

#csvファイルの読み込み
df = pd.read_csv("7203-トヨタ自動車.csv",encoding = "shift_jis")
df = df.drop(["Unnamed: 0","出来高","終値調整"], axis = 1)
#print(df)

x = np.arange(len(df["日付"]))

interval = 20
vals = [df.index[i*interval] for i in range(len(df)//interval+1)]
labels = [df.loc[i*interval,"日付"] for i in range(len(df)//interval +1)]
#print(vals)
#print(labels)

fig = go.Figure(
    data = go.Candlestick(
        x = x,
        open = df["始値"],
        high = df["高値"],
        low = df["安値"],
        close = df["終値"],
        hovertext = ["日付:{}<br>始値:{}<br>高値:{}<br>安値:{}<br>終値:{}"
            .format(df.loc[i,"日付"],df.loc[i,"始値"],df.loc[i,"高値"],df.loc[i,"安値"],df.loc[i,"終値"]) for i in range(len(df))] ,
        hoverinfo = "text"
    ),
    layout = go.Layout(
        xaxis = dict(
            ticktext = labels,
            tickvals = vals,
            tickangle = -45
        ),
    )
)
fig.show()