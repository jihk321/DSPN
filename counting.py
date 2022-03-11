from ast import While
from datetime import date, datetime
from glob import glob
from pprint import pprint
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import openpyxl
import pandas as pd
import PannelCalc
import main 
from csv import writer
import os.path

sale = 0
leng, num, coil, itemnum = [], [], [], []
coilsum = 0.0
logx = 0  # log(table) 행 값
logy = 0  # log(table) 열 값

def today():
    tdate = str(date.today())
    tdate = tdate.replace("-", "")
    tdate = tdate.replace("2022", "22")
    return tdate

def WritingDate():
    day = date.today()
    day = day.strftime("%m-%d")
    return day
    
def excelling(num, name, data):
    if os.path.isfile(f"{name}.csv"):
        with open(f"{name}.csv",'a',encoding= 'utf-8-sig',newline='') as file_w:
            for i in range(0,num,1):
                writer_object = writer(file_w)
                a = data.loc[i]

                writer_object.writerow(a)
        # data.to_clipboard()
    else:
        data.to_csv(f"{name}.csv",index= False,encoding= 'utf-8-sig')


# excelling()
def FindingClient(find_name): #거래처 찾기
    if len(find_name) > 1:
        # start = time.time()
        # with open("client.csv","r",encoding= 'utf-8-sig') as files:
        files = pd.read_csv("client.csv",header=0,sep=",",low_memory=False)
        # files.dropna(inplace = True) # 빈값 버리기
        # search_num = (files['거래처명'].str.find(find_name))
        search_num = files[files['거래처명'].str.contains(find_name,na=False)]
        a = search_num.index.tolist
        
        search_name = search_num['거래처명'].values

        index_num = []

        # for i in range(0,8205,1) : 
        #     if search_num[i] == True :
        #         index_num.append(i)

        # search_name = []

        # for i in index_num[0:5] :
        #     id = files.loc[i][1]
        #     search_name.append(id)

        # search_name = search_name[0:5]
        # print(search_name[0:5])
        # end = time.time()
        # print(f"{end - start:.5f} sec")
        return search_name[0:5]

# FindingClient("주식")

def findbuja(find_name,color): #부자재 찾기
    files = pd.read_csv("부자재.csv", sep=",", low_memory=False)
    search_num = files[files['품목'].str.contains(find_name,na=False)]
        
    search_name = search_num[search_num['규격'].str.contains(color,na=False)]
    re_name = search_name['규격'].values
    return re_name[0:5]

# findbuja("2단후레슁","링클브라운")