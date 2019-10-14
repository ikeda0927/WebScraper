# WebScraper

以下のスクリプトを実行する際は全て自己責任でお願いします。

- [Spider.py](https://github.com/ikeda0927/WebScraper#spiderpy)  

### Spider.py
----
指定したURLを基にリンクを探していくCrawlerです。  

使用方法は  
~~~
Python3 Spider.py https://github.com/ikeda0927/ list.txt
~~~  

のように、  

第一引数に探したいURL、第二引数（省略可）にURLを書き出すファイル名（ファイルは存在しなくても可）を指定することで、再帰的にリンクを探しに行ってくれます。  

Spider.pyをそのまま使う場合、リンクを探す対象となるURLは指定したURLを含むもの※1となっていますが、  
Spider.pyのスクリプト中の  
~~~
CrawlSameRootURLs(sys.argv[1],exportFileName)
~~~  
を
~~~
#CrawlSameRootURLs(sys.argv[1],exportFileName)
~~~  
とし、  
~~~
#CrawlAllURLs(sys.argv[1],exportFileName)
~~~  
を
~~~
CrawlAllURLs(sys.argv[1],exportFileName)
~~~  
とすることで、  
発見した全てのURLを対象に再帰的にURLを探しに行きます。※2  

また、Spider.pyのスクリプト中の  
~~~
time.sleep(sleepTime)
~~~  
により、  

Getリクエストを送る前に1秒待つようになっていますが、  
これは短時間に多量のリクエストを送信する（Dos攻撃をしてしまう）ことを防ぐためのものとなっているので、  
絶対に消さない（また、sleepTimeを1秒より小さくしない）でください。  



---

※1 例えば、URLとしてhttps://github.com/ikeda0927/ を指定した場合は、発見したリンクの中でもhttps://github.com/ikeda0927/ から始まるものをのみを対象に再帰的にリンクを探しに行く。  
もちろん、出力されるファイルには発見した全てのリンクが記される。  

※2 実行することはお勧めしません。
