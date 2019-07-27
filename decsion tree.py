# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:47:56 2018

@author: chenxi
功能：机器学习实战之决策树
"""
from math import log
import operator
import numpy as np
import matplotlib.pyplot as plt
def calshannonent(dataset):   #计算信息熵
    numentries=len(dataset)
    labelcounts={}
    for featvec in dataset:               #对dataSet的每一个元素进行处理  
        currentlabel=featvec[-1]        #//将dataSet的每一个元素的最后一个元素选择出来        
        if currentlabel not in labelcounts.keys():  
            labelcounts[currentlabel]=0  #//若没有该键，则使用字典的自动添加进行添加值为0的项，取0是因为下一行代码              
        labelcounts[currentlabel] +=1    #对currentlabel计数，每有一个key：currentlabel，就在对应的key的值上加一
    shannonent=0
    for key in labelcounts:
        prob=float(labelcounts[key])/numentries
        shannonent -=prob*log(prob,2)
    return shannonent

def file2matrix(filename):
    fr=open(filename)
    lists=fr.readlines()
    listnum=[]
    for k in lists:
        listnum.append(k.strip().split(','))  
    return listnum

def splitdataset(dataset,axis,value):   #按特征选取除该特征之外的特征数据
    retdataset=[]
    for featvec in dataset:
        if featvec[axis]==value:
            reducedfeatvec=featvec[:axis]
            reducedfeatvec.extend(featvec[axis+1:])
            retdataset.append(reducedfeatvec)
            
    return retdataset

"""
选取特征的方法是计算每个特征的信息增益，然后再基于信息增益的值来选取信息增益最大的特征作为下一次决策树分类的一句，这样保证了每次选取的
特征都能最大化程度的较少数据集的信息混乱程度

具体信息增益计算方法为：
infogain=数据集信息熵+Σ该特征下每个取值对应每个分类的信息熵

"""

def choosebestfeaturetosplit(dataset):   #就算出信息增益之后选取信息增益值最高的特征作为下一次分类的标准
    numfeatures=len(dataset[0])-1     #计算特征数量，列表【0】表示列的数量，-1是减去最后的类别特征
    baseentropy=calshannonent(dataset)   #计算数据集的信息熵
    bestinfogain=0.0;bestfeature=-1
    for i in range(numfeatures):  
        featlist=[example[i] for example in dataset]
        uniquevals=set(featlist)   #确定某一特征下所有可能的取值
        newentropy=0.0
        for value in uniquevals:
            subdataset=splitdataset(dataset,i,value)#抽取在该特征的每个取值下其他特征的值组成新的子数据集
            prob=len(subdataset)/float(len(dataset))#计算该特征下的每一个取值对应的概率（或者说所占的比重）
            newentropy +=prob*calshannonent(subdataset)#计算该特征下每一个取值的子数据集的信息熵
        infogain=baseentropy-newentropy   #计算每个特征的信息增益
      #  print("第%d个特征是的取值是%s，对应的信息增益值是%f"%((i+1),uniquevals,infogain))
        if(infogain>bestinfogain):
            bestinfogain=infogain
            bestfeature=i
   # print("第%d个特征的信息增益最大，所以选择它作为划分的依据，其特征的取值为%s,对应的信息增益值是%f"%((i+1),uniquevals,infogain))
    return bestfeature



def majoritycnt(classlist):#针对所有特征都用完，但是最后一个特征中类别还是存在很大差异，比如西瓜颜色为青绿的情况下同时存在好瓜和坏瓜，无法进行划分，此时选取该类别中最多的类
#作为划分的返回值，majoritycnt的作用就是找到类别最多的一个作为返回值
    classcount={}#创建字典
    for vote in classlist:
        if vote not in classcount.keys():
            classcount[vote]=0   #如果现阶段的字典中缺少这一类的特征，创建到字典中并令其值为0
            classcount[vote] +=1 #循环一次，在对应的字典索引vote的数量上加一
        sortedclasscount=sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)#operator.itemgetter(1)是抓取其中第2个数据的值
        #利用sorted方法对class count进行排序，并且以key=operator.itemgetter(1)作为排序依据降序排序因为用了（reverse=True）,3.x以上的版本不再有iteritems而是items
        return sortedclasscount[0][0]
       
     


def createtree(dataset,labels):
    classlist=[example[-1] for example in dataset]   #提取dataset中的最后一栏——种类标签
    if classlist.count(classlist[0])==len(classlist): #计算classlist[0]出现的次数,如果相等，说明都是属于一类，不用继续往下划分
        return classlist[0]
    if len(dataset[0])==1:   #看还剩下多少个属性，如果只有一个属性，但是类别标签又多个，就直接用majoritycnt方法进行整理  选取类别最多的作为返回值
        return majoritycnt(classlist)
    bestfeat=choosebestfeaturetosplit(dataset)#选取信息增益最大的特征作为下一次分类的依据
    bestfeatlabel=labels[bestfeat]   #选取特征对应的标签
    mytree={bestfeatlabel:{}}   #创建tree字典，紧跟现阶段最优特征，下一个特征位于第二个大括号内，循环递归
    del(labels[bestfeat])   #使用过的特征从中删除
    featvalues=[example[bestfeat] for example in dataset]  #特征值对应的该栏数据
    uniquevals=set(featvalues)   #找到featvalues所包含的所有元素，同名元素算一个
    for value in uniquevals:
        sublabels=labels[:]  #子标签的意思是循环一次之后会从中删除用过的标签 ，剩下的就是子标签了
        mytree[bestfeatlabel][value]=createtree(splitdataset(dataset,bestfeat,value),sublabels)   #循环递归生成树
    return mytree



def getnumleafs(mytree):#计算叶子节点的个数（不包括中间的分支节点）
    numleafs=0
  #原代码  firststr=mytree.keys()[0]  # 获得myTree的第一个键值，即第一个特征，分割的标签 
    firststr=list(mytree.keys())[0]
    #遇到的问题是mytree.keys()获得的类型是dict_keys，而dict_keys不支持索引，我的解决办法是把获得的dict_keys强制转化为list即可
    seconddict=mytree[firststr]# 根据键值得到对应的值，即根据第一个特征分类的结果  
    for key in seconddict.keys():  #获取第二个小字典中的key
        if type(seconddict[key]).__name__=='dict':#判断是否小字典中是否还包含新的字典（即新的分支）   书上写的是.-name-但是3.0以后得版本都应该写成.__name__(两个下划线)
            numleafs +=getnumleafs(seconddict[key])#包含的话进行递归从而继续循环获得新的分支所包含的叶节点的数量
        else: numleafs +=1#不包含的话就停止迭代并把现在的小字典加一表示这边有一个分支
    return numleafs

def gettreedepth(mytree):#计算判断节点的个数
    maxdepth=0
    firststr=list(mytree.keys())[0]
    seconddict=mytree[firststr]
    for key in seconddict.keys():
        if type(seconddict[key]).__name__=='dict':
            thisdepth  = 1+gettreedepth(seconddict[key])
        else: thisdepth =1
        if thisdepth>maxdepth:
            maxdepth=thisdepth#间隔 间隔间隔得问题一定要多考虑啊啊啊啊啊啊
    return maxdepth





#使用文本注解绘制树节点
#包含了边框的类型，边框线的粗细等
decisionnode=dict(boxstyle="sawtooth",fc="0.8",pad=1)# boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细  ,pad指的是外边框锯齿形（圆形等）的大小
leafnode=dict(boxstyle="round4",fc="0.8",pad=1)# 定义决策树的叶子结点的描述属性 round4表示圆形
arrow_args=dict(arrowstyle="<-")#定义箭头属性

def plotnode(nodetxt,centerpt,parentpt,nodetype):
     # annotate是关于一个数据点的文本  
    # nodeTxt为要显示的文本，centerPt为文本的中心点，箭头所在的点，parentPt为指向文本的点  
    #annotate的作用是添加注释，nodetxt是注释的内容，
    #nodetype指的是输入的节点（边框）的形状
    createplot.ax1.annotate(nodetxt,xy=parentpt,xycoords='axes fraction',\
                           xytext=centerpt,textcoords='axes fraction',\
                           va="center",ha="center",bbox=nodetype,arrowprops=arrow_args)
    
    
'''
xOff

xOff和yOff用来记录当前要画的叶子结点的位置。
画布的范围x轴和y轴都是0到1，我们希望所有的叶子结点平均分布在x轴上。totalW记录叶子结点的个数，那么 1/totalW 正好是每个叶子结点的宽度
如果叶子结点的坐标是 1/totalW , 2/totalW, 3/totalW, …, 1 的话，就正好在宽度的最右边，为了让坐标在宽度的中间，需要减去0.5 / totalW 。所以createPlot函数中，初始化 plotTree.xOff 的值为-0.5/plotTree.totalW。这样每次 xOff + 1/totalW ，正好是下1个结点的准确位置
yOff

yOff的初始值为1，每向下递归一次，这个值减去 1 / totalD
cntrPt

cntrPt用来记录当前要画的树的树根的结点位置
在plotTree函数中，它是这样计算的
cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
numLeafs记录当前的树中叶子结点个数。我们希望树根在这些所有叶子节点的中间。
plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW
这里的 1.0 + numLeafs 需要拆开来理解，也就是
plotTree.xOff +  float(numLeafs)/2.0/plotTree.totalW +1.0/2.0/plotTree.totalW
plotTree.xOff +  1/2 * float(numLeafs)/plotTree.totalW + 0.5/plotTree.totalW
因为xOff的初始值是-0.5/plotTree.totalW ，是往左偏了0.5/plotTree.tatalW 的，这里正好加回去。这样cntrPt记录的x坐标正好是所有叶子结点的中心点
'''    
#plottree.totalw和plottree.totald是全局变量  
    
def plotmidtext(cntrpt,parentpt,txtstring):#作用是计算tree的中间位置    cntrpt起始位置,parentpt终止位置,txtstring：文本标签信息
    xmid=(parentpt[0]-cntrpt[0])/2.0+cntrpt[0]# cntrPt 起点坐标 子节点坐标   parentPt 结束坐标 父节点坐标
    ymid=(parentpt[1]-cntrpt[1])/2.0+cntrpt[1]#找到x和y的中间位置
    createplot.ax1.text(xmid,ymid,txtstring)
    
    
def plottree(mytree,parentpt,nodetxt):
    numleafs=getnumleafs(mytree)
    depth=gettreedepth(mytree)
    firststr=list(mytree.keys())[0]
    cntrpt=(plottree.xoff+(1.0+float(numleafs))/2.0/plottree.totalw,plottree.yoff)#计算子节点的坐标 
    plotmidtext(cntrpt,parentpt,nodetxt) #绘制线上的文字  
    plotnode(firststr,cntrpt,parentpt,decisionnode)#绘制节点  
    seconddict=mytree[firststr]
    plottree.yoff=plottree.yoff-1.0/plottree.totald#每绘制一次图，将y的坐标减少1.0/plottree.totald，间接保证y坐标上深度的
    for key in seconddict.keys():
        if type(seconddict[key]).__name__=='dict':
            plottree(seconddict[key],cntrpt,str(key))
        else:
            plottree.xoff=plottree.xoff+1.0/plottree.totalw
            plotnode(seconddict[key],(plottree.xoff,plottree.yoff),cntrpt,leafnode)
            plotmidtext((plottree.xoff,plottree.yoff),cntrpt,str(key))
    plottree.yoff=plottree.yoff+1.0/plottree.totald

    
def createplot(intree):
     # 类似于Matlab的figure，定义一个画布(暂且这么称呼吧)，背景为白色 
    fig=plt.figure(1,facecolor='white')
    fig.clf()    # 把画布清空 
    axprops=dict(xticks=[],yticks=[])   
    # createPlot.ax1为全局变量，绘制图像的句柄，subplot为定义了一个绘图，111表示figure中的图有1行1列，即1个，最后的1代表第一个图 
    # frameon表示是否绘制坐标轴矩形 
    createplot.ax1=plt.subplot(111,frameon=False,**axprops) 
    
    plottree.totalw=float(getnumleafs(intree))
    plottree.totald=float(gettreedepth(intree))
    plottree.xoff=-0.6/plottree.totalw;plottree.yoff=1.2;
    plottree(intree,(0.5,1.0),'')
    plt.show()
    




#测试和存储分类器

def classify(inputtree,featlabels,testvec):
    classlabel=''
    firststr=list(inputtree.keys())[0]
    seconddict=inputtree[firststr]
    featindex=featlabels.index(firststr)
    for key in seconddict.keys():
        if testvec[featindex]==key:
            if type(seconddict[key]).__name__=='dict':
                classlabel=classify(seconddict[key],featlabels,testvec)
            else:classlabel=seconddict[key] 
    return classlabel


#测试决策树分类性能'the calculte result is%s,the true result is %s'%(result,testdata[i][-1]) 
def testefficiency(inputtree,labels,testdata):
    flag=0
    for i in range(len(testdata)): 
        result=classify(inputtree,labels,testdata[i][:6])
        if(result==testdata[i][-1]): flag +=1
        print('the calculte result is%s,the true result is %s'%(result,testdata[i][-1]))
    print('the data number is %d,but the right number is %d'%(len(testdata),flag))




 #生成决策树的存储              
def storetree(inputtree,filename):
    import pickle
    fw=open(filename,'wb')
    pickle.dump(inputtree,fw)
    fw.close
def grabtree(filename):
    import pickle
    fr=open(filename,'rb')
    return pickle.load(fr)
           
      


    
if __name__ == '__main__':
    data=file2matrix('uci-cardata.txt')
    testdata=file2matrix('test.txt')
    labels=['buying','maint','doors','persons','lug_boot','safety']
    labels1=['buying','maint','doors','persons','lug_boot','safety']
    mytree=createtree(data,labels)
    print(type(mytree))
    storetree(mytree,'classifierstorge.txt')
    print(grabtree('classifierstorge.txt'))
 
    
    
    
    
 
'''    
   print(grabtree('classifierstorge.txt'))

    
    labels=['buying','maint','doors','persons','lug_boot','safety','Class Values']
    
    data1=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels1=['no surfacing','flipers']
    mytree=createtree(data,labels)
    labels3=['buying','maint','doors','persons','lug_boot','safety','Class Values'] 
    testefficiency(mytree,labels3,testdata)
    
    
    

    labels2=['no surfacing','flipers']
    car1=['vhigh','vhigh',2,2,'small','low']
    print(classify(mytree,labels3,car1))
    
 
'''


 
    










































     
