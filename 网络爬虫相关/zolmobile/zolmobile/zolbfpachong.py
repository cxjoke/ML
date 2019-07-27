# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:48:43 2018

@author: cxjoker
功能：抓取zol上智能手环的参数数据
"""


# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup

import requests

def htmls(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
            }
    req = requests.get(url = url,headers = headers)#获取html地址
    req.encoding = 'GBK'#因为该网站采用GBK编码，如果使用utf-8就会出现乱码
    html1 = req.text#转化成可识别的文本格式
    bf = BeautifulSoup(html1,"html.parser")#请求bf实现连接跳转
    return(bf)
    


def gethref(url):#获取产品详细信息，实现翻页
    bf=htmls(url)
    h=[]
    hrefs=bf.find_all('h3')   #寻找标签为h3的内容，正则表达式寻找含有“h3”标签的数据，因为所有从列表到产品详细信息的界面的href都在h3标签之下，
    for href in hrefs:
        href1=href.find_all('a',target="_blank")#h3中标签为a，且具有属性为target="_blank"的标签，含有h3标签不一定都是跳转的href，所以用属性“target="_blank"”进行筛选
        for k in href1:#因为标签中还含有其他字符，所以需要进一步的去除留下键为href的值，获取每一页产品的多个href连接
            h.append(k["href"])
    return h
            
            
def trun2parm(url):#从产品详情连接到参数页
    bf=htmls(url)
    a=[]
    parhrefs=bf.find_all('div',class_="nav")#寻找所有div标签且属性为“class_="nav"”，因为各个栏的数据都包含在内部
    #parhrefs=bf.find_all('div',atters={'class':'navbox clearfix'})
    for parhref in parhrefs:
        parhref1=parhref.find_all('a',target="_self")#寻找所有a标签且属性为“target="_self"”，因为各个包含参数的href在该标签下
        for k in parhref1:
            a.append(k["href"])#获取标签下的href值
    parhrefs=bf.find_all('div',class_="navbox clearfix")#由于部分href存在在“'div',class_="navbox clearfix"”之下，所以需要二次抓取href连接
    for parhref in parhrefs:
        parhref1=parhref.find_all('a',target="_self")
        for k in parhref1:
            a.append(k["href"])
    if len(a)>2:
        return a[2]
    
    
    
"""    
def getparm(url): 
    bf=htmls(url)
    kg=[]
    functions=bf.select('.category-param-list li')
    for function in functions:
        if'特性功能' in function.text:
            kg.append(function.text)
    return kg
"""  
    


def xunhuan(url):
    a=gethref(url)#获取从列表式产品数据到单个产品页面的href
    k=[]   
    bf=htmls(url)  #请求url
    total=[]
    global gyq,water,bluetooth,fun#抓取的数据主要包括感应器栏、防水防尘、蓝牙功能以及特性功能
    for i in range(len(a)):
         url1= 'http://detail.zol.com.cn{}'.format(a[i])#获取每个产品的详细信息的链接
         k.append(trun2parm(url1))#实现第一次翻页
    for j in range(len(k)):
        if k[j] !=None:
            url2= 'http://detail.zol.com.cn{}'.format(k[j])#跳转到参数栏的链接
            bf=htmls(url2)
            lists=bf.select('.category-param-list li')#寻找所有的属性为param-list的li
            for function in lists:
        
                if'感应器' in function.text:#获取感应器的数据
                    gyq=function.text
                if'防水防尘' in function.text:
                    water=function.text
                if'蓝牙' in function.text:
                    bluetooth=function.text

                if'特性功能' in function.text:
                    fun=function.text
            total.append(fun)
    return total
    


        
#href=bf.select('.category-param-list li')



if __name__ == '__main__':
    a=[]
    for i in range(1,30):
        url = 'http://detail.zol.com.cn/intelligentbracelet/good_{}.html'.format(str(i))#总共有30页有效信息，故抓取30页数据即可，但是当时记得是开着电脑跑了一晚上，效率较低
        a.extend(xunhuan(url))
    file=open('fun.txt','w')
    file.write(str(a))
    file.close() 
  
  

    
