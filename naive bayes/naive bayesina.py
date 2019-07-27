# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:49:29 2018

@author: chenxi
"""
import numpy as np
import re
import feedparser
import random
def fenci(filename):
    fr=open(filename)
    lists=fr.read()
    
    listword=re.split(lists)
    
    print(listword)
   
    
        
      
def loaddataset():
    postinglist=[['my','dog','has','flae','problem','help','plaese'],
                 ['maybe','not','take','him','to','dog','park','stupid'],
                 ['my','dog','is','so','cute','i','love','him'],
                 ['stop','posting','stupid','worthless','garbage',],
                 ['mr','licks','ate','my','steak','how','to','stop','him'],
                 ['qiut','buying','worthless','dog','food','stupid']]
    classvec=[0,1,0,1,0,1]
    return postinglist,classvec

def createvocablist(dataset):#功能是创建一个不重复的词汇表
    vocabset=set([])#创建出来的是一个集合，
    for document in dataset:
        vocabset =vocabset | set(document)#set(document)不重复的提取出所有的词，并且加入到vocabset集里面去
    return list(vocabset)


def bagofwords2vecmn(vocablist,inputset):#生成分类向量，当所输入的文章中的词在vocablist中出现时，就将其对应的向量设置为1，否则维持原来的不变
    returnvec=[0]*len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnvec[vocablist.index(word)] +=1
    return returnvec




    
def trainnbo(trainmatrix,traincategory):#输入训练样本和属性（分类）标记
    numtraindocs=len(trainmatrix)#计算训练样本的样本数
    numwords=len(trainmatrix[0])#
    pabusive=sum(traincategory)/float(numtraindocs)#计算p（c）的概率（比重）这里面指的是分类为1的比重，因为求和之后为0的不考虑
    p0num=np.ones(numwords);p1num=np.ones(numwords)
    p0denom=2.0;p1denom=2.0
    for i in range(numtraindocs):
        if traincategory[i]==1:
            p1num +=trainmatrix[i]#如果说归为1类，那么把这个训练样本的向量和原先已有的向量加和，保证了同一位置（表示同一单词）的数量的叠加，起到计数的作用
            p1denom +=sum(trainmatrix[i])
        else:
            p0num +=trainmatrix[i]
            p0denom +=sum(trainmatrix[i])
    np.set_printoptions(threshold=np.inf)
    print(p0num)
    print(p1num)
    p1vect=np.log(p1num/p1denom)#p1num是一个向量，而怕denom是一个数，除了之后计算得到的是每一个单词出现在不同类别的概率
    p0vect=np.log(p0num/p0denom)
    return p0vect,p1vect,pabusive
    
'''
3 针对算法的部分改进

1)计算概率时，需要计算多个概率的乘积以获得文档属于某个类别的概率，即计算p(w0|ci)*p(w1|ci)*...p(wN|ci)，然后当其中任意一项的值为0，那么最后的乘积也为0.为降低这种影响，
    采用拉普拉斯平滑，在分子上添加a(一般为1)，分母上添加ka(k表示类别总数)，即在这里将所有词的出现数初始化为1，并将分母初始化为2*1=2

#p0Num=ones(numWords);p1Num=ones(numWords)
#p0Denom=2.0;p1Denom=2.0
2)解决下溢出问题

　　正如上面所述，由于有太多很小的数相乘。计算概率时，由于大部分因子都非常小，最后相乘的结果四舍五入为0,造成下溢出或者得不到准确的结果，所以，我们可以对成绩取自然对数，
  即求解对数似然概率。这样，可以避免下溢出或者浮点数舍入导致的错误。同时采用自然对数处理不会有任何损失。

#p0Vect=log(p0Num/p0Denom);p1Vect=log(p1Num/p1Denom)
'''  
    
def classifynb(vec2classify,p0vec,p1vec,pclass1):
    p1=sum(vec2classify*p1vec)+np.log(pclass1)
    p0=sum(vec2classify*p0vec)+np.log(1-pclass1)
    if p1>p0:
        return 1
    else:
        return 0
    
def testingnb():#测试算法
    listoposts,listclasses=loaddataset()
    myvocablist=createvocablist(listoposts)
    trainmat=[]
    for postdoc in listoposts:
        trainmat.append(bagofwords2vecmn(myvocablist,postdoc))#利用词袋模型生成所需的向量
    p0v,p1v,pab=trainnbo(trainmat,listclasses)#计算每一类中，出现的词语属于该类的概率，生成模型
    testentry=['love','my','dalmation']#测试信息
    thisdoc=np.array(bagofwords2vecmn(myvocablist,testentry))
    print(testentry,'classified as',classifynb(thisdoc,p0v,p1v,pab))



def textparse(bigstring):
    listoftokens=re.split(r'\W*',bigstring)#利用除字符和数字之外的字符串进行分割,\w是转义字符的意思，为了保持原有的意思所以需要加上“r”来表示
    return[tok.lower()for tok in listoftokens if len(tok)>2]#保留字符长度超过两个的字符串，并且将字母设置为小写


def spamtest():
    doclist=[]
    classlist=[]
    fulltext=[]
    for i in range(1,26):
        wordlist=textparse(open(r'C:\Users\chenxi\Desktop\python.py\朴素贝叶斯\spam\%d.txt'%i).read())#文件夹中ham都是正常文章，spam都是广告
        doclist.append(wordlist)#做单个的词向量
        fulltext.extend(wordlist)#fulltext是在做词库
        classlist.append(1)#生成类别标签
        wordlist=textparse(open(r'C:\Users\chenxi\Desktop\python.py\朴素贝叶斯\ham\%d.txt'%i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist=createvocablist(doclist)    
    print(doclist)
    trainingset=range(50)
    testset=[]
    for i in range(10):#交叉验证
        randindex=int(random.uniform(0,len(trainingset)))#利用uniform函数随机生成一个在0到len范围之间的随机实数，用于随机选取十个数据集
        testset.append(trainingset[randindex])#这里用的是append函数，说明这十个测试集在一个testset中，每个测试样本为一个数据集
        del(trainingset[randindex])
    trainmat=[];trainclasses=[]
    for docindex in trainingset:
        trainmat.append(bagofwords2vecmn(vocablist,doclist[docindex]))#原代码前面已经改成了bagofwords2vecmn，而他还在用setofwords2vec很明显用词袋比词集合理
        trainclasses.append(classlist[docindex])
    p0v,p1v,pspam=trainnbo(np.array(trainmat),np.array(trainclasses))
    errorcount=0
    for docindex in testset:
        wordvector=bagofwords2vecmn(vocablist,doclist[docindex])
        if classifynb(np.array(wordvector),p0v,p1v,pspam) != classlist[docindex]:
            errorcount +=1
    print('the error rate is:%s'%(float(errorcount/len(testset))))#这曾经少打了一个括号，让我声泪俱下

    
def calmostfreq(vocablist,fulltext):
    import operator
    freqdict={}
    for token in vocablist:
        freqdict[token]=fulltext.count(token)
    sortedfreq=sorted(freqdict.items(),key=operator.itemgetter(1),reverse=True)
    return sortedfreq[0:30]



def localwords(feed1,feed0):
    import feedparser
    doclist=[]
    classlist=[]
    fulltext=[]
    minlen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minlen):
        wordlist=textparse(feed1['entries'][i]['summary'])
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(1)
        wordlist=textparse(feed0['entries'][i]['summary'])
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist=createvocablist(doclist)
    top30words=calmostfreq(vocablist,fulltext)
    for pairw in top30words:
        if pairw[0]in vocablist:vocablist.remove(pairw[0])
    trainingset=range(2*minlen);testset=[]
    for i in range(20):
        randindex=int(random.uniform(0,len(trainingset))) 
        testset.append(trainingset[randindex])
        del(trainingset[randindex])
    trainmat=[];trainclasses=[]
    for docindex in trainingset:
        trainmat.append(bagofwords2vecmn(vocablist,doclist[docindex]))
        trainclasses.append(classlist[docindex])
    p0v,p1v,pspam=trainnbo(np.array(trainmat),np.array(trainclasses))
    errorcount=0
    for docindex in testset:
        wordvector=bagofwords2vecmn(vocablist,doclist[docindex])
        if classifynb(np.array(wordvector),p0v,p1v,pspam) != classlist[docindex]:
            errorcount +=1
    print('the error rate is:%s'%(float(errorcount/len(testset))))
    return vocablist,p0v,p1v            



if __name__=='__main__':
    ny=feedparser.parser('http://newyork.craigslist.org/stp/index.rss')
    sf=feedparser.parser('http://sfbay.craigslist.org/stp/index.rss')
    vocablist,psf,pny=localwords(ny,sf)

      
