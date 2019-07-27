# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:51:01 2018

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
        a=b.find_all('p')
        for each in a:
            print(each.string)
    
    
    
    
    
""" 



    b=BeautifulSoup(str(targets_url[0]))
        a=b.find_all('a')
        for each in a:
            print(each.string)
   

    for i in range(len(targets_url)):
        b=BeautifulSoup(str(targets_url[i]))
        a=b.find_all('a')
        for each in a:
            print(each.string)
    
  
/html/body/div/div[5]/div/div/div/div/div[2]/div[2]/ul/li[1]/div[3]/p[2]
/html/body/div/div[5]/div/div/div/div/div[2]/div[2]/ul/li[1]/div[3]/p[1]         
/html/body/div/div[5]/div/div/div/div/div[2]/div[2]/ul/li[1]/div[3]/p[4]



    list_name = []
    for each in targets_url:
        list_name.append(each.a.get('href')+each.a.get('target'))
    #print(list_name)

    import pandas as pd
    #字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'电影名':list_name})

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("test2.csv",index=False,sep=',')
"""  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    