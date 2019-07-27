# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:51:38 2018

@author: chenxi
"""


# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = 'http://www.mtime.com/top/movie/top100/'
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    req = requests.get(url = url,headers = headers)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    targets_url = bf.find_all('div',class_='mov_con')
    for i in range(len(targets_url)):
        b=BeautifulSoup(str(targets_url[i]))
        a=b.find_all('a')
        for each in a:
            print(each.string)