import requests
from bs4 import BeautifulSoup
import re
import sys
import time

crawledList  = list()
pattern1     = "^https?://"
repattern1   = re.compile(pattern1)
pattern2     = "[^/]+$"
repattern2   = re.compile(pattern2)
pattern3     = "^/"
repattern3   = re.compile(pattern3)
counter      = 0
sleepTime    = 1
exportFileName='list.txt'

class Page:
    global crawledList
    rootURL=None
    # url=None
    # type=1 #0->CrawlAllURLs, 1->CrawlSameRootURLs
    links=list()

    def FindMyLinks(self):
        #linksにそのページ内のリンクを格納する。
        time.sleep(sleepTime)
        data=requests.get(self.url)
        soup=BeautifulSoup(data.text,"html.parser")
        aList=soup.select('a')
        for a in aList:
            hrefValue=a['href']
            if hrefValue != None:
                if repattern1.match(hrefValue):
                    Page.links.append(hrefValue)
                else:
                    Page.links.append(repattern2.sub('',self.url)+repattern3.sub('',hrefValue))

    def CompareLink(self,lines,link):
        judge=True
        for line in lines:
            line = line.replace('\n','')
            if line == link:
                judge= False
                return judge
        return judge

    def Check(self):
        global counter
        global exportFileName
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
                with open(exportFileName,'a+') as f:
                    f.seek(0)
                    lines=f.readlines()
                    print('Comparing : '+link)
                    if self.CompareLink(lines,link):
                        counter += 1
                        print('write '+link)
                        f.write(link+'\n')
        elif self.type==1:
            for link in Page.links:
                if Page.rootURL in link:
                    crawledJudge=False
                    for crawled in crawledList:
                        if crawled == link:
                            crawledJudge=True
                            break
                    if not crawledJudge:
                        Page(link,self.type)
                    #リストをファイルに書き込む
                with open('list.txt','a+') as f:
                    f.seek(0)
                    lines=f.readlines()
                    if self.CompareLink(lines,link):
                        counter += 1
                        print('write '+link)
                        f.write(link+'\n')

    def __init__(self,url,type):
        self.url=url
        self.type=type
        if Page.rootURL == None:
            Page.rootURL=url
        crawledList.append(url)
        self.FindMyLinks()
        self.Check()

def CrawlSameRootURLs(root):
    print('crawlSameRootURLs')
    Page(root,1)


def CrawlAllURLs(root):
    print('crawlAllURLs')
    Page(root,0)

if __name__ == '__main__':
    if len(sys.argv)>=2:
        if len(sys.argv)>=3:
            exportFileName=sys.argv[2]
        CrawlSameRootURLs(sys.argv[1])
        print('Add '+str(counter)+' URLs')
        # sleepTime=2
        # CrawlAllURLs(sys.argv[1])
    else:
        print('Enter domain as a first argument (and enter export file name as a second argument)')
