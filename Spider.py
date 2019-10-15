import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import FindStrings

crawledList  = list()
pattern1     = "^https?://"
repattern1   = re.compile(pattern1)
pattern2     = "^https?://[^/]+/"
repattern2   = re.compile(pattern2)
pattern3     = "^/"
repattern3   = re.compile(pattern3)
counter      = 0
sleepTime    = 1
stringListFile=None
# exportFileName='list.txt'

class Page:
    global crawledList
    rootURL=None
    # url=None
    # type=1 #0->CrawlAllURLs, 1->CrawlSameRootURLs
    links=list()

    def FindMyLinks(self):#linksにそのページ内のリンクを格納する。
        time.sleep(sleepTime)#Dos攻撃にならないように
        print('ACCESS : '+self.url)
        self.data=requests.get(self.url)#取得
        soup=BeautifulSoup(self.data.text,"html.parser")
        aList=soup.select('a')#aタグ取得
        for a in aList:
            try:
                hrefValue=a['href']#href属性の取得
            except KeyError:
                continue
            if hrefValue != None:
                if repattern1.match(hrefValue):#取得したhrefの値が絶対パスの場合->そのまま
                    Page.links.append(hrefValue)
                else:#取得したhrefの値が相対パスの場合->絶対パスに変換
                    Page.links.append(repattern2.match(self.url).group()+repattern3.sub('',hrefValue))
                    # Page.links.append(repattern2.sub('',self.url)+repattern3.sub('',hrefValue))

    def CompareLink(self,lines,link):
        judge=True
        for line in lines:
            line = line.replace('\n','')
            if line == link:
                judge= False
                return judge
        return judge

    def Write(self,link):
        global counter
        with open(self.exportFileName,'a+') as f:
            f.seek(0)
            lines=f.readlines()
            # print('Comparing : '+link)
            if self.CompareLink(lines,link):
                counter += 1
                print('WRITE  : '+link)
                f.write(link+'\n')

    def WriteAndFind(self,link,data,stringListFile):
        global counter
        with open(self.exportFileName,'a+') as f:
            f.seek(0)
            lines=f.readlines()
            # print('Comparing : '+link)
            if self.CompareLink(lines,link):
                counter += 1
                print('WRITE  : '+link)
                f.write(link+'\n')
                FindStrings.Find(link,data,stringListFile)

    def Check(self):
        global stringListFile
        # global exportFileName
        if self.type==0:
            for link in Page.links:
                crawledJudge=False
                for crawled in crawledList:
                    if crawled == link:
                        crawledJudge=True
                        break
                if not crawledJudge:
                    Page(link,self.type)
                #リストをファイルに書き込む
                Self.Write(link)
        elif self.type==1:
            for link in Page.links:
                if Page.rootURL in link:#URLがスクリプト実行時に指定したURLで始まるかの確認
                    crawledJudge=False
                    for crawled in crawledList:
                        if crawled == link:#もし既にアクセスしていたなら新たにPageインスタンスを作成しない
                            crawledJudge=True
                            break
                    if not crawledJudge:
                        Page(link,self.type,self.exportFileName)
                    #リストをファイルに書き込む
                self.Write(link)
        elif self.type==2:
            for link in Page.links:
                if Page.rootURL in link:#URLがスクリプト実行時に指定したURLで始まるかの確認
                    crawledJudge=False
                    for crawled in crawledList:
                        if crawled == link:#もし既にアクセスしていたなら新たにPageインスタンスを作成しない
                            crawledJudge=True
                            break
                    if not crawledJudge:
                        Page(link,self.type,self.exportFileName)
                    #リストをファイルに書き込む
                self.WriteAndFind(link,self.data,stringListFile)

    def __init__(self,url,type,exportFileName):
        self.url=url
        self.type=type
        self.exportFileName=exportFileName
        # self.data=None
        if Page.rootURL == None:
            Page.rootURL=url
        #アクセスした（これからする）URLリストに追加
        crawledList.append(url)
        #自ページ内のリンクを取得
        self.FindMyLinks()
        #取得したリンクがまだリストに記載されていなければリストに出力する。
        self.Check()

def CrawlSameRootURLs(root,exportFileName):
    print('crawlSameRootURLs')
    Page(root,1,exportFileName)

def CrawlSameRootURLsAndScrape(root,exportFileName,myStringListFile):
    global stringListFile
    print('crawlSameRootURLs')
    stringListFile=myStringListFile
    Page(root,2,exportFileName)

def CrawlAllURLs(root,exportFileName):
    print('crawlAllURLs')
    Page(root,0,exportFileName)

if __name__ == '__main__':
    if len(sys.argv)>=2:
        exportFileName='list.txt'
        if len(sys.argv)>=3:
            exportFileName=sys.argv[2]
        #処理時間測定開始
        startTime=time.time()
        #処理開始
        # CrawlSameRootURLs(sys.argv[1],exportFileName)
        if len(sys.argv)>=4:
            CrawlSameRootURLsAndScrape(sys.argv[1],exportFileName,sys.argv[3])
        else:
            CrawlSameRootURLs(sys.argv[1],exportFileName)
        #処理終了時間
        endTime=time.time()
        #追加項目数の表示
        print('Add '+str(counter)+' URLs')
        #処理時間
        processingTime=endTime-startTime
        print('processing time : '+ str(processingTime)+'s')
        h=processingTime//3600
        processingTime-=3600*h
        m=processingTime//60
        processingTime-=60*m
        s=processingTime
        print(str(h)+'h '+str(m)+'m '+str(s)+'s')
        # sleepTime=2
        # CrawlAllURLs(sys.argv[1],exportFileName)
    else:
        print('Enter domain as a first argument (and enter export file name as a second argument)')
