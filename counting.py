from ast import While
from datetime import date, datetime
from glob import glob
from PyQt5 import QtCore, QtGui, QtWidgets
import openpyxl
import pandas as pd
import PannelCalc
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
def FindingClient(): #거래처 찾기
    files = pd.read_csv("client.csv", sep=",")
    code,leng =[],[]
    for c,n in files.iterrows():
        code.append(n)
    files.row
    # print(leng)    
    # print(code[0][1]) 

