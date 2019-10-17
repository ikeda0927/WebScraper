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
maxSearchURLNum=None
maxSearchURLNumCounter=0
minDetectedURLNum=None
minDetectedURLNumCounter=0
TIMEOUT=3
connectionTimeOut=TIMEOUT
readTimeOut=TIMEOUT
mode=1
maxDepth=998
exportFileName='list.txt'

class Page:
    global crawledList
    rootURL=None
    links=list()

    def getResponse(self,url):
        global connectionTimeOut
        global readTimeOut
        with requests.Session() as sess:
            resp = sess.get(url, stream=True,timeout=(connectionTimeOut,readTimeOut), allow_redirects=True)
            # 画像とかpdfは取らないようにcontent-typeがtextのもののみ選ぶ処理
            if not 'content-type' in resp.headers or not 'text' in resp.headers['content-type']:
                resp=None
                return resp
        return resp

    def FindMyLinks(self):#linksにそのページ内のリンクを格納する。
        time.sleep(sleepTime)#Dos攻撃にならないように
        print('ACCESS : '+self.url)
        try:
            self.data=self.getResponse(self.url)
        except requests.exceptions.Timeout:
            self.data=None
            print('Request Timeout : '+self.url)
        if not self.data:
            return False
        soup=BeautifulSoup(self.data.text,"html.parser")
        aList=soup.select('a')#aタグ取得
        self.data=None
        soup=None
        for a in aList:
            try:
                hrefValue=a['href']#href属性の取得
            except KeyError:
                continue
            if hrefValue != None:
                judge=True
                if repattern1.match(hrefValue):#取得したhrefの値が絶対パスの場合->そのまま
                    for link in Page.links:
                        if link ==hrefValue:
                            judge=False
                            break
                    for crawled in crawledList:
                        if crawled==hrefValue:
                            judge=False
                            break
                    if judge:
                        Page.links.append(hrefValue)
                else:#取得したhrefの値が相対パスの場合->絶対パスに変換
                    hrefValue=repattern2.match(self.url).group()+repattern3.sub('',hrefValue)
                    for link in Page.links:
                        if link ==hrefValue:
                            judge=False
                            break
                    for crawled in crawledList:
                        if crawled==hrefValue:
                            judge=False
                            break
                    if judge:
                        Page.links.append(hrefValue)
        return True

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
        global minDetectedURLNumCounter
        with open(self.exportFileName,'a+') as f:
            f.seek(0)
            lines=f.readlines()
            if self.CompareLink(lines,link):
                counter += 1
                print('WRITE  : '+link)
                print('     depth='+str(self.depth))
                f.write(link+'\n')
                minDetectedURLNumCounter=len(lines)+1

    def WriteAndFind(self,link,data,stringListFile):
        global counter
        global minDetectedURLNumCounter
        with open(self.exportFileName,'a+') as f:
            f.seek(0)
            lines=f.readlines()
            if self.CompareLink(lines,link):
                counter += 1
                print('WRITE  : '+link)
                f.write(link+'\n')
                minDetectedURLNumCounter=len(lines)+1
                FindStrings.Find(link,data,stringListFile)

    def Check(self):
        global stringListFile
        global mode
        if mode==0:
            for link in Page.links:
                crawledJudge=False
                for crawled in crawledList:
                    if crawled == link:
                        crawledJudge=True
                        break
                if not crawledJudge:
                    Page(link,self.exportFileName,self.depth)
                #リストをファイルに書き込む
                Self.Write(link)
        elif mode==1:
            for link in Page.links:
                if Page.rootURL in link:#URLがスクリプト実行時に指定したURLで始まるかの確認
                    crawledJudge=False
                    for crawled in crawledList:
                        if crawled == link:#もし既にアクセスしていたなら新たにPageインスタンスを作成しない
                            crawledJudge=True
                            break
                    if not crawledJudge:
                        Page(link,self.exportFileName,self.depth)
                    #リストをファイルに書き込む
                self.Write(link)
        elif mode==2:
            for link in Page.links:
                if Page.rootURL in link:#URLがスクリプト実行時に指定したURLで始まるかの確認
                    crawledJudge=False
                    for crawled in crawledList:
                        if crawled == link:#もし既にアクセスしていたなら新たにPageインスタンスを作成しない
                            crawledJudge=True
                            break
                    if not crawledJudge:
                        Page(link,self.exportFileName,self.depth)
                    #リストをファイルに書き込む
                self.WriteAndFind(link,self.data,stringListFile)

    def __init__(self,url,exportFileName,depth):
        global maxSearchURLNum
        global maxSearchURLNumCounter
        self.url=url
        self.exportFileName=exportFileName
        self.depth=depth+1
        if Page.rootURL == None:
            Page.rootURL=re.sub('[^/]*$','',url)
        #アクセスした（これからする）URLリストに追加
        crawledList.append(url)
        for crawled in crawledList:
            try:
                Page.links.remove(crawled)
            except ValueError:
                None
        # 自ページ内のリンクを取得
        if maxSearchURLNum and minDetectedURLNum:
            if maxSearchURLNum>maxSearchURLNumCounter and minDetectedURLNum>minDetectedURLNumCounter:
                judge=self.FindMyLinks()
        elif maxSearchURLNum:
            if maxSearchURLNum>maxSearchURLNumCounter:
                judge=self.FindMyLinks()
        elif minDetectedURLNum:
            if minDetectedURLNum>minDetectedURLNumCounter:
                judge=self.FindMyLinks()
        else:
            judge=self.FindMyLinks()
        maxSearchURLNumCounter+=1
        if judge and self.depth<maxDepth:
            #取得したリンクがまだリストに記載されていなければリストに出力する。
            self.Check()

def CrawlSameRootURLs(root,exportFileName):
    print('crawlSameRootURLs')
    mode=1
    Page(root,exportFileName,-1)

def CrawlSameRootURLsAndScrape(root,exportFileName,myStringListFile):
    global stringListFile
    print('crawlSameRootURLs')
    stringListFile=myStringListFile
    mode=2
    Page(root,exportFileName,-1)

def CrawlAllURLs(root,exportFileName):
    print('crawlAllURLs')
    mode=0
    Page(root,exportFileName,-1)

def ShowHelp():
    print('-u [str]\n\tターゲットURL（必須）\n-dm [int]\n\t発見URL数の最大値\n-sm [int]\n\t検索対象URL数の最大値\n-sl [float]\n\tリクエスト送信時の待ち時間\n-ct [int] \n\tConnection Timeout(秒)\n-rt [int]\n\tRead Timeout\n-e [str]\n\t出力ファイル名\n-d [int]\n\t検索時の深さ指定')

if __name__ == '__main__':
    if len(sys.argv)>=2:
        targetUrl=None
        for i in range(1,len(sys.argv),2):
            if sys.argv[i]=='-dm':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1:
                        minDetectedURLNum=temp
                print('minDetectedURLNum='+str(minDetectedURLNum))
            elif sys.argv[i]=='-sm':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1:
                        maxSearchURLNum=temp
                print('maxSearchURLNum='+str(maxSearchURLNum))
            elif sys.argv[i]=='-sl':
                if len(sys.argv)>=i+2:
                    temp=float(sys.argv[i+1])
                    if temp>=1:
                        sleepTime=temp
                print('sleepTime='+str(sleepTime))
            elif sys.argv[i]=='-ct':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1:
                        connectionTimeOut=temp
                print('connectionTimeout='+str(connectionTimeOut))
            elif sys.argv[i]=='-rt':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1:
                        readTimeOut=temp
                print('readTimeout='+str(readTimeOut))
            elif sys.argv[i]=='-m':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1:
                        mode=temp
                print('mode='+str(mode))
            elif sys.argv[i]=='-e':
                if len(sys.argv)>=i+2:
                    exportFileName=sys.argv[i+1]
                print('exportFileName='+exportFileName)
            elif sys.argv[i]=='-h':
                ShowHelp()
            elif sys.argv[i]=='-d':
                if len(sys.argv)>=i+2:
                    temp=int(sys.argv[i+1])
                    if temp>=1 and temp<999:
                        maxDepth=temp
                print('maxDepth='+str(maxDepth))
            elif sys.argv[i]=='-u':
                if len(sys.argv)>=i+2:
                    targetUrl=sys.argv[i+1]
                print('maxDepth='+str(maxDepth))
        if not targetUrl:
            ShowHelp()
        else:
            #処理期間測定開始
            startTime=time.time()
            #処理開始
            CrawlSameRootURLs(targetUrl,exportFileName)
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
    else:
        ShowHelp()
