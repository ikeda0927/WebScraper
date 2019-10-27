import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import openpyxl as px
import glob

sleepTime=1
resultFile='result.txt'
pattern=None
repattern=None
urlListFileName=None
tags=None
excelFile='result.xlsx'
patternList=None
repatternList=list()
exportAsExcel=False

def FindFromFile(url,data,stringListFile):
    if stringListFile:
        if data:
            if not repattern:
                SetRegularExpressionFromFile(stringListFile)
            result=repattern.findall(str(data.text))#GETしたレスポンス内に含まれる検索対象文字列の取得
            if len(result)>0:
                with open(resultFile,'a') as f3:
                    f3.write(url+' : '+str(len(result))+'\n')
def WriteToExcel(url,data):
    global pattern
    global patternList
    global repatternList
    global excelFile
    if(len(repatternList)==0):
        patternList=pattern.split('|')
        for p in patternList:
            repatternList.append(re.compile(p))
    try:
        book = px.load_workbook(excelFile)
        sheet = book.active
    except FileNotFoundError:
        book = px.Workbook()
        sheet = book.active
        sheet['A1'].value='url'
        index=66
        for pat in patternList:
            sheet[chr(index)+'1'].value=pat
            index+=1
    columnNum=1
    while True:
        if sheet['A'+str(columnNum)].value==None:
            break
        columnNum+=1
    rowAlp=65
    sheet['A'+str(columnNum)].value=url
    for i in range(len(repatternList)):
        sheet[chr(rowAlp+i+1)+str(columnNum)].value=len(repatternList[i].findall(str(data.text)))
    book.save(excelFile)

def Find(data):
    if data and repattern:
        result=repattern.findall(str(data.text))#GETしたレスポンス内に含まれる検索対象文字列の取得
        return len(result)
    return 0

def FineWithTags(data):

    None

def SetRegularExpressionFromFile(stringListFile):
    global pattern
    global repattern
    stringList=None
    with open(stringListFile,'r') as f1:#検索対象文字列の取得
        strings=f1.read()
    pattern=strings.replace('\n','|')#正規表現に変換
    pattern=re.sub('\|$','',pattern)#正規表現の修正
    repattern= re.compile(pattern)#正規表現のコンパイル

def SetRegularExpressionFromArg(str):
    global pattern
    global repattern
    pattern=str.replace(',','|')#正規表現に変換
    pattern=re.sub('\|$','',pattern)#正規表現の修正
    repattern= re.compile(pattern)#正規表現のコンパイル

def SetRegularExpressionFromFileAndArg(stringListFile,str):
    None

def FindStrings(urlListFile):
    print('FindStrings')
    urlList=None
    with open(urlListFile,'r') as f2:#文字列検索対象URLの取得
        urlList=f2.readlines()
    print('Pattern : '+pattern)
    for url in urlList:
        time.sleep(sleepTime)#Dos攻撃にならないように
        url=url.replace('\n','')
        print('ACCESS : '+url)
        data=requests.get(url)#取得
        # print('type : '+str(type(data)))
        # result=repattern.findall(str(data.text))#GETしたレスポンス内に含まれる検索対象文字列の取得
        # if len(result)>0:
        #     with open(resultFile,'a') as f3:
        #         f3.write(url+' : '+str(len(result))+'\n')
        result=Find(data)
        if result>0:
            with open(resultFile,'a') as f3:
                f3.write(url+' : '+str(result)+'\n')
            if exportAsExcel:
                WriteToExcel(url,data)

def ShowHelp():
    print('-u [str]\n\tURLリスト指定(必須)\n-s [str]\n\t走査対象文字列のコマンドライン指定(-rを指定しているなら省略可)\n-r [str]\n\t走査対象文字列ファイルの指定(-sを指定しているなら省略可)\n-e [str]\n\t出力ファイル名指定\n-t [str]\n\t文字列走査対象タグの指定\n-ex [str]\n\t指定した名前のエクセルで出力')

if __name__ == '__main__':
    if len(sys.argv)>=2:
        for i in range(1,len(sys.argv),2):
            if sys.argv[i]=='-t':
                tags=sys.argv[i+1].split(',')
                print('未実装')
            elif sys.argv[i]=='-s':
                if len(sys.argv)>=i+2:
                    temp=sys.argv[i+1]
                    SetRegularExpressionFromArg(temp)
            elif sys.argv[i]=='-e':
                if len(sys.argv)>=i+2:
                    temp=sys.argv[i+1]
                    resultFile=temp
            elif sys.argv[i]=='-r':
                if len(sys.argv)>=i+2:
                    temp=sys.argv[i+1]
                    SetRegularExpressionFromFile(temp)
            elif sys.argv[i]=='-u':
                if len(sys.argv)>=i+2:
                    temp=sys.argv[i+1]
                    urlListFileName=temp
            elif sys.argv[i]=='-ex':
                if len(sys.argv)>=i+2:
                    temp=sys.argv[i+1]
                    if not temp in '.xlsx':
                        temp+='.xlsx'
                    excelFile=temp
                    exportAsExcel=True
        if repattern and urlListFileName:
            #処理時間測定開始
            startTime=time.time()
            #処理開始
            FindStrings(urlListFileName)
            #処理終了時間
            endTime=time.time()
            #処理時間
            processingTime=endTime-startTime
            print('processing time : '+ str(processingTime)+'s')
            h=processingTime//3600
            processingTime-=3600*h
            m=processingTime//60
            processingTime-=60*m
            s=processingTime
            print(str(h)+'h '+str(m)+'m '+str(round(s,1))+'s')
            # sleepTime=2
            # CrawlAllURLs(sys.argv[1],exportFileName)
        else:
            ShowHelp()
    else:
        ShowHelp()
