import openpyxl
""" from pprint import pprint """
""" from operator import itemgetter """

# リスト
code_list = []

# エクセルファイルの取り込み
wb = openpyxl.load_workbook("shoukencode.xlsx")
ws = wb["Sheet1"]
for row in ws.iter_rows(min_row=2,max_col=3,min_col=2):
    values = []
    for c in row:
        values.append(c.value)
    #print(values)
    code_list.append(values)
#pprint(code_list)

#入力したコードをここから検索
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

#input_code = [10080,9999,7203]
input_code = list(map(int,input("コードを入力してください:").split()))
cn = code_name(input_code)
print(cn)