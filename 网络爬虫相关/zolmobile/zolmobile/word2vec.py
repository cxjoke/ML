# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:41:21 2018

@author: chenxi
"""

import jieba,re,os  
from gensim.models import word2vec  
import logging    
#jieba.load_userdict("data\\userdict.txt")    
  
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO,filename='test_01.log')    
filename = '词库.txt'   #测试文本  
pre,ext = os.path.splitext(filename)   #输入文件分开前缀，后缀   pre=test_01   ext=.txt  
corpus = pre + '_seg' + ext    #训练语料为按行分词后的文本文件    corpus=test_01_seg.txt  
fin = open(filename,encoding='utf8').read().strip(' ').strip('\n').replace('\n\n','\n')   #strip()取出首位空格，和换行符，用\n替换\n\n  
stopwords = set(open('test_01停用词.txt',encoding='utf8').read().strip('\n').split('\n'))   #读入停用词  

text = ' '.join([x for x in jieba.lcut(fin) if x not in stopwords and len(x)>1 and x != '\n'])  #去掉停用词中的词，去掉长度小于等于1的词  
print(text)     
results = re.sub('[（）：:？“”《》，。！·、\d ]+',' ',text)  #去标点  
open(corpus,'w+',encoding='utf8').write(results)   #按行分词后存为训练语料  