# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 20:15:27 2018

@author: chenxi
"""
from numpy import *

def loadDataSet():   #加载数据函数
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():#直接读取全部数据作为list，然后对每个元素进行处理
        lineArr = line.strip().split()#去空格、分割
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])#将1.0，lineArr的第一、二个元素（转换为float类型）加入到dataMat列表
        labelMat.append(int(lineArr[2]))#获取标签
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))#inx回归系数与特征的乘积

def gradAscent(dataMatIn, classLabels):#梯度提升方法
    dataMatrix = mat(dataMatIn)             #将数据列表转化为矩阵np.mat
    labelMat = mat(classLabels).transpose() #将标签列表转化为矩阵
    m,n = shape(dataMatrix)#获取dataMatrix行数和列数，m为行数，shape(datamatrix)[0]表示获得datmat的行数，
    alpha = 0.001#步长为0.001
    maxCycles = 500#循环次数
    weights = ones((n,1))    #初始化系数矩阵，初始化为1
    for k in range(maxCycles):              #
        h = sigmoid(dataMatrix*weights)     #
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
    
    
if __name__=="__main__":
    m=array([[1,2],[8,9],[5,6]])
    a,b=shape(m)
    print(a,b)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    