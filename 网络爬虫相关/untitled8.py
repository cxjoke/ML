# -*- coding: UTF-8 -*-

"""
from urllib import request

if __name__ == "__main__":
    #urllib使用使用request.urlopen()打开和读取URLs信息，返回的对象response如同一个文本对象，
    response = request.urlopen("http://www.mtime.com/top/movie/top100/index-2.html")
    #我们可以调用read()，进行读取。再通过print()，将读到的信息打印出来。但读出来代码比较乱，无法正常看，将其转化为utf-8的格式写出
    html = response.read()
    html = html.decode("utf-8")
  #  print(html)
    print(html)


    # -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    #以CSDN为例，CSDN不更改User Agent是无法访问的
    url = 'http://www.csdn.net/'
    head = {}
    #写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
 #创建Request对象
    req = request.Request(url, headers=head)
    #传入创建好的Request对象
    response = request.urlopen(req)
    #读取响应信息并解码
    html = response.read().decode('utf-8')
    #打印信息
    print(html)
"""

from urllib import request
import scrapy      
import re
from bs4 import BeautifulSoup
if __name__=="__main__":
    url='http://www.mtime.com/top/movie/top100/index-3.html'
     #创建Request对象
    req=request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19')
    response = request.urlopen(req)
    html=response.read().decode('utf-8')
    #print(html)
    soup=BeautifulSoup(html,"lxml")
    target_url=soup.find_all(class_='img_box')
    print(target_url)
    list_url=[]
    for each in target_url:
        list_url.append(each.img.get('alt'))
   
    print(list_url)
   










































