#実行すると2時間半はかかります
from bs4 import BeautifulSoup
import requests
import os
import time
from pathlib import Path
import re
import datetime

dt_now = str(datetime.datetime.now())

#プログラムファイルのある場所にフォルダ「img」を作成
folder = Path("img")
folder.mkdir(exist_ok=True)

#print(os.getcwd())
os.chdir("img")
#print(os.getcwd())

#まずはリンクへ行くためのリスト取得
url1 = "https://xn--dckc6bvei9bwqrc2008dk17a.gamerch.com/"
soup = BeautifulSoup(requests.get(url1).content,"lxml")
tag = soup.find_all("ul")
t_list1 = []
for i in range(len(tag)):
    t_list1.append([t.text for t in tag[i].find_all("li")])
#print(t_list1[8])
#print(t_list1[9])
t_list2 = []
for j in t_list1[8]:
    t_list2.append(j.split("(")[0])
#print(t_list2)
for k in t_list1[9]:
    t_list2.append(k.split("(")[0])
#print(t_list2)


#さらに次のページに行くためのタグを取得
for pg_tag in t_list2:
    print("START TIME:" + dt_now)
    print(pg_tag)
    url2 = "https://xn--dckc6bvei9bwqrc2008dk17a.gamerch.com/{}".format(pg_tag)
    #print(url2)
    soup2 = BeautifulSoup(requests.get(url2).content,"lxml")
    tag2 = soup2.find_all("tr")
    t_list3 = []
    for l in range(1,len(tag2)):
        tok = []
        for t in tag2[l].find_all("td"):
            tok.append(t.text)
        #print(len(tok)) 
        if len(tok) == 6 or len(tok) == 7:
            t_list3.append(tok)
    #print(t_list3)
    #print(len(t_list3))
    #print(t_list3[4][2])
    if len(t_list3) == 0:
        pass
    else:
        t_list4 = []
        for m in range(len(t_list3)):
            nn = [t_list3[m][1],t_list3[m][2]]
            t_list4.append(nn)

    #print(len(t_list4))

    #さらに画像のあるページから画像をDL
    for page in t_list4:
        try:
            url3 = "https://xn--dckc6bvei9bwqrc2008dk17a.gamerch.com/{}".format(page[1])
            soup3 = BeautifulSoup(requests.get(url3).content,"lxml")
            tag3 = soup3.find_all("img")
            #print(tag3)
            img_list = []
            for img in tag3:
                img_list.append(img["src"])
            #print(img_list[1])

            file_name = page[0] + "_" + page[1] + ".png"
            response = requests.get(img_list[1])
            image = response.content
            print(page)
            with open(file_name, "wb") as aaa:
                aaa.write(image)
            time.sleep(1)
        except:
            print("ダウンロードできませんでした")
    print("next")

print("complete")