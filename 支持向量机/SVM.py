# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 10:33:40 2019

@author: chenxi
"""

def loaddataset(filename):
    datamat=[];lablemat=[]
    fr=open(filename)
    for line in fr.readlines:
        linear=line.strip().split('\t')#strip() 方法用于移除字符串头尾指定的字符(默认为空格或换行符)或字符序列,此处用于删除空格。split(str="", num=string.count(str))参数str -- 分隔符,默认为所有的空字符,包括空格、换行(\n)、制表符(\t)等。
        datamat.append(float(linear[0]),float(linear[1])) 
        lablemat.append(float(linear[0]))
    return(datamat,labelmat)





def selectjran(i,m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return(j)

def clialpha(aj,h,l):
    if aj>h:
        return h
    if aj<l:
        return l
    else:
        return aj









if __name__=='__main__':
