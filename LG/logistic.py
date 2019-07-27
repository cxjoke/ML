# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 20:15:27 2018

@author: chenxi
"""
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import random



def loadDataSet():   #加载数据函数
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():#直接读取全部数据作为list，然后对每个元素进行处理
        lineArr = line.strip().split()#去空格、分割
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])#将1.0，lineArr的第一、二个元素（转换为float类型）加入到dataMat列表
        labelMat.append(int(lineArr[2]))#获取标签
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))#inx回归系数与特征的乘积

def gradAscent(dataMatIn, classLabels):#梯度提升方法
    dataMatrix = np.mat(dataMatIn)             #将数据列表转化为矩阵np.mat
    labelMat = np.mat(classLabels).transpose() #将标签列表转化为矩阵，transpose()为转置函数
    m,n = np.shape(dataMatrix)#获取dataMatrix行数和列数，m为行数，shape(datamatrix)[0]表示获得datmat的行数，
    alpha = 0.001#步长为0.001
    maxCycles = 500#循环次数
    weights = np.ones((n,1))    #初始化系数矩阵，初始化为1,n是dataMatrix列数，即特征个数
    weights_array = np.array([])
    for k in range(maxCycles):              #
        h = sigmoid(dataMatrix*weights)     #矩阵内部的元素相乘并相加，然后输入到sigmod函数并返回值，最后形成一个列向量，每一列代表一个样本的z=w1x1+w2x2通过sigmod函数之后获得的值                            
        error = (labelMat - h)              #错误率代表样本标签和sigmod函数的差值，{0,1}，距离越远，说明错的越大
        weights = weights + alpha * dataMatrix.transpose()* error #通  过逻辑回归的似然函数求参数最优值，采用梯度上升法最后获得的迭代公式为α*（y-h（x））x
        weights_array = np.append(weights_array,weights)
    weights_array=weights_array.reshape(maxCycles,n)
    return weights




def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])#获得分类为1的横纵坐标
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])#获得分类为0的横纵坐标
    fig = plt.figure()
    ax = fig.add_subplot(111)#将画布分割成1行1列，图像画在从左到右从上到下的第1块
    #画点
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')#分类为1的画入图中  s是大小，c为颜色
    ax.scatter(xcord2, ycord2, s=30, c='green')
    #画线
    x = np.arange(-3.0, 3.0, 0.1)   #x的坐标从-3到3，步长为0.1
    y = (-weights[0]-weights[1]*x)/weights[2]#0=w0x0+w1x1+w2x2
    y1=y.transpose()
    ax.plot(x, y1 )
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()   


def stogradacent0(datamatrix,classlebels):
   
    m,n=np.shape(datamatrix)
    alpha=0.01
    weights=np.ones(n)
    x=[]
    for i in range(m):
        h=sigmoid(sum(weights*datamatrix[i]))
        error=classlebels[i]-h
        weights=weights+alpha*error*datamatrix[i]
        x.append([i,weights[0],weights[1],weights[2]])
    return weights,x





def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = np.shape(dataMatrix)
    weights = np.ones(n)   #初始化权重矩阵
   # weights_array=np.array([])
    for j in range(numIter):#迭代次数
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    #随着i，j的增大，步长逐渐减小，更加精细 
            randIndex = int(random.uniform(0,len(dataIndex)))#每次都是随机选取样本来作为更新权重矩阵的数据,不放回抽样，因为每次抽完之后就把该数据删除
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
           # weights_array=np.append(weights_array,weights,axis=0)
            del(dataIndex[randIndex])
    #weights_array=weights_array.reshape(numIter*m,n)
    return weights


 
def plotWeights(weights_array1,weights_array2):
    #设置汉字格式,windows自带的汉字
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    #将fig画布分隔成1行1列,不共享x轴和y轴,fig画布的大小为(13,8)
    #当nrow=3,nclos=2时,代表fig画布被分为六个区域,axs[0][0]表示第一行第一列
    fig, axs = plt.subplots(nrows=3, ncols=2,sharex=False, sharey=False, figsize=(20,10))
    x1 = np.arange(0, len(weights_array1), 1)
    #绘制w0与迭代次数的关系
    axs[0][0].plot(x1,weights_array1[:,0])
    axs0_title_text = axs[0][0].set_title(u'梯度上升算法：回归系数与迭代次数关系',FontProperties=font)
    axs0_ylabel_text = axs[0][0].set_ylabel(u'W0',FontProperties=font)
    plt.setp(axs0_title_text, size=20, weight='bold', color='black') 
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][0].plot(x1,weights_array1[:,1])
    axs1_ylabel_text = axs[1][0].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][0].plot(x1,weights_array1[:,2])
    axs2_xlabel_text = axs[2][0].set_xlabel(u'迭代次数',FontProperties=font)
    axs2_ylabel_text = axs[2][0].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black') 
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')


    x2 = np.arange(0, len(weights_array2), 1)
    #绘制w0与迭代次数的关系
    axs[0][1].plot(x2,weights_array2[:,0])
    axs0_title_text = axs[0][1].set_title(u'改进的随机梯度上升算法：回归系数与迭代次数关系',FontProperties=font)
    axs0_ylabel_text = axs[0][1].set_ylabel(u'W0',FontProperties=font)
    plt.setp(axs0_title_text, size=20, weight='bold', color='black') 
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][1].plot(x2,weights_array2[:,1])
    axs1_ylabel_text = axs[1][1].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][1].plot(x2,weights_array2[:,2])
    axs2_xlabel_text = axs[2][1].set_xlabel(u'迭代次数',FontProperties=font)
    axs2_ylabel_text = axs[2][1].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black') 
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')

    plt.show()           
    
    
    
def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0  #以0.5为分类线，大于0.5分类为1
    else: return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):#获取样本特征数据，转化为float数据类型
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)#获取样本特征数据，
        trainingLabels.append(float(currLine[21]))#获取样本标签
    trainWeights = stocGradAscent1(np.array(trainingSet), trainingLabels,500)#获得样本特征权值
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(np.array(lineArr), trainWeights))!= int(currLine[21]):#计算分类错误数量
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print ("the error rate of this test is: %f" % errorRate)
    return errorRate

def multiTest():
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest()
    print ("after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))   )
 
    






if __name__=="__main__":
    multiTest()
    
    
'''
#对比改进的梯度下降算法和未改进的梯度下降算法的回归系数与迭代次数之间的关系  
if __name__=="__main__":    
    dataMat,labelMat=loadDataSet()
    weights0,a0=gradAscent(np.array(dataMat),labelMat)
    weights,a=stocGradAscent1(np.array(dataMat),labelMat)
    plotWeights(a0,a)   
'''  

    
    
    
    
    
    
    
    
    
    
    
    
    