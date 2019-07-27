# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:46:08 2018

@author: chenxi
"""

# -*- coding: utf-8 -*-  
""" 
Created on Thu Jan 18 14:37:37 2018 
 
@author: cxjoke 
功能：抓取豆瓣top250的电影名字，导演。类型等，评分，评分人数等 
"""  
 
  
# -*- coding:UTF-8 -*-  
import requests  
from lxml import etree

def jiema(url):
    headers = {  
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  
            }#定义模仿浏览器机制，实现隐蔽爬虫
    req = requests.get(url = url,headers = headers)   #获取url地址
    req.encoding = 'utf-8' #转码为utf-8
    html = req.text #转化为text
    html1=etree.HTML(html)
    return(html1)     
   




  
if __name__ == '__main__':  
    a=jiema("http://detail.zol.com.cn/1189/1188711/param.shtml")
    print(a)
   
    
"""     
    
    ranks=[]  
    names=[]  
    directors=[]  
    types=[]  
    juqing=[]  
    stars=[]  
    dd=[]  
    gg=[]  
    people=[]  
    grades=[]  
    quotes=[]  
    numbers=['0','25','50','75','100','125','150','175','200','225']  
    for number in numbers:  
        url = 'https://movie.douban.com/top250?start={}&filter='.format(number)#实现翻页功能  
         
        headers = {  
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  
            }  
        req = requests.get(url = url,headers = headers)  
        req.encoding = 'utf-8'  
        html = req.text  
        html1=etree.HTML(html)  
        rank=html1.xpath('//div[@class="item"]/div/em/text()')#x-path地址并获取文字  
        for rank1 in rank:  
            ranks.append(rank1)  
        name=html1.xpath('//div[@class="info"]/div[1]/a/span[1]/text()')  
        for name1 in name:  
            names.append(name1)  
        director=html1.xpath('//div[@class="bd"]/p[1]/text()')  
        for director1 in director:  
            directors.append(director1)  
         
        people1=html1.xpath('//div[@class="star"]/span[4]/text()')  
        for people2 in people1:  
            people.append(people2)  
        grade=html1.xpath('//div[@class="star"]/span[@class="rating_num"][@property="v:average"]/text()')  
        for grade1 in grade:  
            grades.append(grade1)  
      
  
  
        quote=html1.xpath('//p[@class="quote"]/span/text()')  
        for quote1 in quote:  
            quotes.append(quote1)  
          
   
      
        for i in directors:  
            gg.append(i.strip())  
        for k in gg:  
            dd.append("".join(k.split()))  
     
        for q in range(25):  
            juqing.append(dd[2*q-1])  
        for q in range(25):  
            stars.append(dd[2*q])  
        
import pandas as pd  
    #字典中的key值即为csv中列名  
columns1= ['豆瓣排名','电影名','剧情','导演/主演','评分','评价人数','queto']#csv会按首字母进行排序，所以加表格自己排序  
dataframe = pd.DataFrame({'豆瓣排名':ranks,'电影名':names,'剧情':juqing,'导演/主演':stars,'评分':grades,'评价人数':people,'queto':quotes})  
#dataframe = pd.DataFrame({'类型':types})  
    #将DataFrame存储为csv,index表示是否显示行名，default=True  
dataframe.to_csv("豆瓣电影top250.csv",encoding="utf_8_sig",index=False,columns=columns1)  

""" 