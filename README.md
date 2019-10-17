# WebScraper?

以下のスクリプトを実行する際は全て自己責任でお願いします。

- [Spider.py](https://github.com/ikeda0927/WebScraper#spiderpy)  
- [FindStrings.py](https://github.com/ikeda0927/WebScraper#findstringspy)

### Spider.py
----
指定したURLを基にリンクを探していくCrawlerです。  

使用方法は  
~~~
Python3 Spider.py -u https://github.com/ikeda0927/
~~~  

のように、  

-uの後に基点となるURLを指定して実行してください。  

オプションについては引数なしで実行すると一覧が出ます。  

##### 注意  
- 再帰的にURLの取得を行っており、その再起にも限度があるので全てのURLを取得できるとは限りません...(コードを書き換えれば限度を緩くすることも可能)
- -slで指定できる数値はDos攻撃にならないためのリクエストの送信間隔なので大きい方が良いです。

### FindStrings.py
---
列挙したURLのリストと検索対象文字列のリストを基に検索対象文字列を有するページのURLを列挙し出力します。  

使用方法は  
~~~
python3 FindStrings.py -u listSample.txt -s test1,test2
~~~  
のように、  

-uにURLのリスト、-sに検索対象文字列(-rに検索対象文字列のリストファイル名)を指定して実行します。  

もし、文字列が見つかった場合はURLと見つかった個数がresult.txt(もしくは-eで指定したファイル名)に出力されます。
