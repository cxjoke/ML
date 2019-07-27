# -*- coding: utf-8 -*-
"""
Created on Wed May  2 19:40:38 2018

@author: chenxi
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

def htmls(url):
    headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
            }
    req = requests.get(url = url,headers = headers)#获取html地址
    req.encoding = 'GBK'#因为该网站采用GNK编码，如果使用utf-8就会出现乱码
    html1 = req.text#转化成可识别的文本格式
    bf = BeautifulSoup(html1,"html.parser")
    return(bf)

   
    
    
def getparm(url): 
    bf=htmls(url)
    gyq=[]
    water=[]
    bluetooth=[]
    fun=[]
    lists=bf.select('.category-param-list li')
    for function in lists:
        if'感应器' in function.text:
            gyq.append(function.text.rstrip('\n感应器\n'))
        if'防水防尘' in function.text:
            water.append(function.text)
        if'蓝牙' in function.text:
            bluetooth.append(function.text)
        if'特性功能' in function.text:
            fun.append(function.text)
    return gyq,water,bluetooth,fun
"""
    for function in functions:
        if'防水防尘' in function.text:
            print(function.text)

    for function in functions:
        if'特性功能' in function.text:
            kg.append(function.text)
    return kg
"""    



    
if __name__ == '__main__':
    function1=[]
    url = 'http://detail.zol.com.cn/1157/1156337/param.shtml'
    a,b,c,d=getparm(url)
    #字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'电影名':a,'导演':b,'主演':c,'类型':d})
#dataframe = pd.DataFrame({'类型':types})
    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("cs.csv",index=False,sep=',')
   
  
    