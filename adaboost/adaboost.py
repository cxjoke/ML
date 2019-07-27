# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:03:49 2019

@author: chenxi

"""

import numpy as np

import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve,auc
def loadSimpData():
    datMat = np.matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]   
    return datMat,classLabels
def showdata(datMat,Labels):
    data_plus = []                                  #正样本
    data_minus = []                                 #负样本
    for i in range(len(Labels)):
        if Labels[i]>0:
            data_plus.append(datMat[i])
        else:
            data_minus.append(datMat[i])
    data_plus_np = np.array(data_plus)                                        
    data_minus_np = np.array(data_minus)   
    plt.scatter(np.transpose(data_plus_np)[0],np.transpose(data_plus_np)[1],c="#ff1212",marker="v")
    plt.scatter(np.transpose(data_minus_np)[0],np.transpose(data_minus_np)[1],marker="<")
    plt.show()
  
"""
    单层决策树分类函数
    Parameters:
        dataMatrix - 数据矩阵
        dimen - 第dimen列，也就是第几个特征
        threshVal - 阈值
        threshIneq - 标志
    Returns:
        retArray - 分类结果
"""
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#just classify the data
    retArray =np.ones((np.shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray    



def buildStump(dataArr,classLabels,D):
    dataMatrix = np.mat(dataArr); labelMat = np.mat(classLabels).T
    
    m,n = np.shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = np.mat(np.zeros((m,1)))
    minError = np.inf #init error sum, to +infinity
    for i in range(n):#loop over all dimensions
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):#loop over all range in current dimension
            for inequal in ['lt', 'gt']: #go over less than and greater than
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)#call stump classify with i, j, lessThan
                errArr = np.mat(np.ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T*errArr  #calc total error multiplied by D
                #print("j:%d,split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (j,i, threshVal, inequal, weightedError))
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst 
   
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m = np.shape(dataArr)[0]
    D = np.mat(np.ones((m,1))/m)   #init D to all equal
    aggClassEst = np.mat(np.zeros((m,1)))
    for i in range(numIt):#numIt为迭代次数
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#build Stump
        #print "D:",D.T
        alpha = float(0.5*np.log((1.0-error)/max(error,1e-16)))#calc alpha, throw in max(error,eps) to account for error=0
        bestStump['alpha'] = alpha  
        weakClassArr.append(bestStump)                  #store Stump Params in Array
        #print "classEst: ",classEst.T
        expon = np.multiply(-1*alpha*np.mat(classLabels).T,classEst) #exponent for D calc, getting messy
        D = np.multiply(D,np.exp(expon))                              #Calc New D for next iteration
        D = D/D.sum()
        #calc training error of all classifiers, if this is 0 quit for loop early (use break)
        aggClassEst += alpha*classEst
        #print "aggClassEst: ",aggClassEst.T
       # print("fxxk:",np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T,np.ones((m,1))))
        aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T,np.ones((m,1)))#这个前面的sign函数是阶跃函数，然后对比之后获得true和false，相乘之后true*1=1，false*1=0
        errorRate = aggErrors.sum()/m
        #print ("total error: ",errorRate)
        if errorRate == 0.0: break
    return weakClassArr,aggClassEst      
def adaClassify(datToClass,classifierArr):
    dataMatrix = np.mat(datToClass)#do stuff similar to last aggClassEst in adaBoostTrainDS
    m = np.shape(dataMatrix)[0]
    aggClassEst = np.mat(np.zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])#call stump classify
        aggClassEst += classifierArr[i]['alpha']*classEst
    return aggClassEst
    #return np.sign(aggClassEst)





def loaddataset(filename):
    dataset=[]
    labels=[]
    fr=open(filename)
    for line in fr.readlines():
        arr=[]
        line_trip=line.strip().split('\t')
        for i in range(len(line_trip)-1):
            arr.append(float(line_trip[i]))
        dataset.append(arr)
        labels.append(float(line_trip[-1]))
    return dataset,labels
        



def plotROC(predStrengths, classLabels):    
    cur = (1.0,1.0) #cursor
    ySum = 0.0 #variable to calculate AUC
    numPosClas = sum(np.array(classLabels)==1.0)#真实值为正例的样本数
    yStep = 1/float(numPosClas); xStep = 1/float(len(classLabels)-numPosClas)#真实值为负例的样本数
    sortedIndicies = predStrengths.argsort()#get sorted index, it's reverse
    fig = plt.figure()#画布
    fig.clf()#清除画布
    ax = plt.subplot(111)
    #loop through all the values, drawing a line segment at each point
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delX = 0; delY = yStep;
        else:
            delX = xStep; delY = 0;
            ySum += cur[1]
        #draw line from cur to (cur[0]-delX,cur[1]-delY)
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')  
        cur = (cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
    plt.title('ROC curve for AdaBoost horse colic detection system')
    ax.axis([0,1,0,1])#坐标轴范围，第一个为x轴，第二个为y轴
    plt.show()
    print("the Area Under the Curve is: ",ySum*xStep)       

def ROC_bySKlearn(trainlabel,pre_scores):
    fpr,tpr,threshold=roc_curve(trainlabel,pre_scores)
    roc_auc=auc(fpr,tpr)
    plt.figure()

    plt.figure(figsize=(5,5))
    plt.plot(fpr,tpr,color='darkorange',lw=2,label='ROC curve (area = %0.5f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0,1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

def adaboostbysklearn(dataset,labels,dataset_test,labels_test):
    bdt=AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=2),\
                           algorithm = "SAMME", n_estimators = 50)
    bdt.fit(dataset,labels)
    pre=bdt.predict(dataset)
    errarr=np.ones((len(pre),1))
    train_err_rate=(errarr[pre==labels].sum())/len(pre)
    print('训练错误率:%0.3f',train_err_rate,'\n')
    
    pre_test=bdt.predict(dataset_test)
    errarr_test=np.ones((len(pre_test),1))
    test_err_rate=(errarr_test[pre_test==labels_test].sum())/len(pre_test)
    print('测试错误率:%0.3f',test_err_rate,'\n')
    
    train_pre_pro=bdt.predict_proba(dataset_test)
    return process_pro(train_pre_pro)

def process_pro(pre):
    pre_pro=[]
    for arr in pre:
        arr1=[]
        if(arr[0]>arr[1]):
            arr1.append(-arr[0])
        else:
            arr1.append(arr[1])
        pre_pro.append(arr1)
    pre_pro_matrix=np.matrix(pre_pro)
    #print(pre_pro_matrix)
    return pre_pro_matrix
    
if __name__=='__main__':

   # datMat,classLabels=loadSimpData()
    
    dataset_train,labels_train=loaddataset("horseColicTraining2.txt")  
    dataset_test,labels_test=loaddataset("horseColicTest2.txt") 
    weakClassArr,aggClassEst=adaBoostTrainDS(dataset_train,labels_train,numIt=50)
    aggClassEst_test=adaClassify(dataset_test,weakClassArr)
   # labels_pre=adaClassify(dataset_test,weakClassArr)
    test_pre_pro=adaboostbysklearn(dataset_train,labels_train,dataset_test,labels_test)
    #pre_pro_matrix=process_pro(train_pre_pro)
    ROC_bySKlearn(labels_test,aggClassEst_test)
    
    #np.set_printoptions(threshold=np.inf)
    
    print("通过SKlearn训练的结果")
    ROC_bySKlearn(labels_test,test_pre_pro)
    
    
   # errarr=np.mat(np.ones((67,1)))
   # a=errarr[labels_pre!=np.mat(labels_test).T]
    #np.set_printoptions(threshold=np.inf)
    #print(aggClassEst)
   # print(a.sum())
    #print((errarr[labels_pre!=np.mat(labels_test).T].sum())/67)
    
   
   
#aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T,np.ones((m,1)))
    
 
    
    
    
    
    
    
    
    
    
    
    