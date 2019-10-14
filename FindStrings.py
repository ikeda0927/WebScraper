import requests
from bs4 import BeautifulSoup
import re
import sys
import time

sleepTime=1
resultFile='result.txt'

def FindStrings(urlListFile,stringListFile):
    print('FindStrings')
    stringList=None
    urlList=None
    with open(stringListFile,'r') as f1:#検索対象文字列の取得
        strings=f1.read()
    with open(urlListFile,'r') as f2:#文字列検索対象URLの取得
        urlList=f2.readlines()
    pattern=strings.replace('\n','|')#正規表現に変換
    pattern=re.sub('\|$','',pattern)#正規表現の修正
    repattern= re.compile(pattern)#正規表現のコンパイル
    print('Pattern : '+pattern)
    for url in urlList:
        time.sleep(sleepTime)#Dos攻撃にならないように
        url=url.replace('\n','')
        print('ACCESS : '+url)
        data=requests.get(url)#取得
        # print('type : '+str(type(data)))
        result=repattern.findall(str(data.text))#GETしたレスポンス内に含まれる検索対象文字列の取得
        if len(result)>0:
            with open(resultFile,'a') as f3:
                f3.write(url+' : '+str(len(result))+'\n')

if __name__ == '__main__':
    if len(sys.argv)>=3:
        #処理時間測定開始
        startTime=time.time()
        #処理開始
        FindStrings(sys.argv[1],sys.argv[2])
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
        print('Enter URLListFile as a first argument and enter export StringListFile as a second argument')
