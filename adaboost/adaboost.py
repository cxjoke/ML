# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:48:14 2018

@author: chenxi
功能：实现机器学习实战得adaboost算法
"""
import numpy as np
import matplotlib.pyplot as plt
def loadsimpdata():
    datmat=np.matrix([   #构建样本矩阵
            [1.,2.1],
            [2.,1.1],
            [1.3,1.],
            [1.,1.],
            [2.,1.]     
                   ])
    classlabels=[1.0,1.0,-1.0,-1.0,1.0]
    return datmat,classlabels
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
def stumpclassify(datamatrix,dimen,threshval,threshineq):
    retarray=np.ones((np.shape(datamatrix)[0],1)) 
    #构建1矩阵，shape(datamatrix)[0]表示获得datmat的行数，如果是(datamatrix)[1]则表示获取列数，后面的1表示以行的形式输出，若缺失1则表示以列的形式输出
    if threshineq == 'lt':
        retarray[datamatrix[:,dimen]<=threshval]=-1.0#datamatrix中的第dimen列的所有样本取值，即第dimen个特征的每个样本的数据取值
    else:
        retarray[datamatrix[:,dimen]>threshval]=-1.0
    return retarray

"""
    找到数据集上最佳的单层决策树
    Parameters:
        dataArr - 数据矩阵
        classLabels - 数据标签
        D - 样本权重
    Returns:
        bestStump - 最佳单层决策树信息
        minError - 最小误差
        bestClasEst - 最佳的分类结果
        这里lt表示less than，表示分类方式，对于小于阈值的样本点赋值为-1，gt表示greater than，也是表示分类方式，对于大于阈值的样本点赋值为-1
"""       
def buildstump(dataarr,classlabels,D):
    datamatrix= np.mat(dataarr);
    labelmat=np.mat(classlabels).T
    m,n=np.shape(datamatrix)   #m为行数，即数据样本的个数；n为列数，即样本特征数
    numsteps=10.0
    beststump={}
    bestclassest=np.mat(np.zeros((m,1)))
    minerror=float(np.inf)
    for i in range(n):                                                            #遍历所有特征,range函数为左闭右开区间函数，即range（0，10）=[0,10)。此处的n为样本所包含的特征数
        rangemin = datamatrix[:,i].min(); rangemax = datamatrix[:,i].max()        #找到特征中最小的值和最大值
        stepsize = (rangemax - rangemin) / numsteps                                #将区间值分为numsteps段 ,计算步长
        for j in range(-1, int(numsteps) + 1):                                     
            for inequal in ['lt', 'gt']:                                          #大于和小于的情况，均遍历。lt:less than，gt:greater than
                threshval = (rangemin + float(j) * stepsize)                     #计算阈值
                predictedvals = stumpclassify(datamatrix, i, threshval, inequal)#计算分类结果
                errarr = np.mat(np.ones((m,1)))                                 #初始化误差矩阵
                errarr[predictedvals == labelmat] = 0                             #分类正确的,赋值为0
                weightederror = D.T * errarr                                      #计算误差
               # print("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshval, inequal, weightederror))
                if weightederror < minerror:                                     #找到误差最小的分类方式,如果获得的错误率比最小错误率都小，则替换当前的minerror，最好的bestclassest分类集，最好的树桩参数
                    minerror = weightederror
                    bestclassest = predictedvals.copy()
                    beststump['dim'] = i
                    beststump['thresh'] = threshval
                    beststump['ineq'] = inequal
    return beststump,minerror,bestclassest







def adaboosttrainds(dataarr,classlabels,numit=40):
    weakclassarr=[]
    m = np.shape(dataarr)[0]   #样本数量
    D=np.mat(np.ones((m,1))/m)   #初始化样本权重
    aggclassest=np.mat(np.zeros((m,1)))
    for i in range(numit):
        beststump,error,classest=buildstump(dataarr,classlabels,D)  #构建单层决策树
        #print('D:',D.T)
        alpha=float(0.5*np.log((1.0-error)/max(error,1e-16)))   #计算弱学习算法权重alpha,使error不等于0,因为分母不能为0,1e-16表示一个很小的数，当error为0时，取1e-16接近0
        beststump['alpha']=alpha     #存储当前最优树状的权重
        weakclassarr.append(beststump)   #存储当前的决策树
        #print("classest:",classest.T)   #输出当前的分类集
        expon=np.multiply(-1*alpha*np.mat(classlabels).T,classest) #计算e的指数项,     np.multiply(A,B)表示u数组对应元素位置相乘
        D=np.multiply(D,np.exp(expon))    #更新权值中的分子部分的计算方法
        D=D/D.sum()#更新新的样本权重矩阵
        #计算AdaBoost误差，当误差为0的时候，退出循环
        aggclassest +=alpha*classest   #生成强分类器的分类结果
        #print("aggclassest:",aggclassest)
        aggerrors=np.multiply(np.sign(aggclassest) !=np.mat(classlabels).T,np.ones((m,1)))  #计算当前强分类器的误差
        errorrate=aggerrors.sum()/m
        #print("total error:",errorrate,"\n")
        if errorrate == 0.0:break
    return weakclassarr,aggclassest



def adaclassfy(dattoclass,classifierarr):
    datamatrix=np.mat(dattoclass)
    m=np.shape(datamatrix)[0]         #shape(datamatrix)[0]表示获得datmat的行数，
    aggclassest=np.mat(np.zeros((m,1)))
    for i in range(len(aggclassest)):
        classest=stumpclassify(datamatrix,classifierarr[i]['dim'],classifierarr[i]['thresh'],classifierarr[i]['ineq'])
        aggclassest +=classifierarr[i]['alpha']*classest
        print(aggclassest)
    return np.sign(aggclassest)


# 自适应数据加载函数，该函数能够自动检测出特征的数目，假定最后一个特征是类别标签
def loaddataset(fileName) :
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():#直接一步到位，666
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat - 1) :
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)    #生成一个样本为一个矩阵的多个样本列表
        labelMat.append(float(curLine[-1]))  #生成所有样本的类别标签
    return dataMat,labelMat

    
def irisdata(filename):    #用于处理iris数据集来作为训练和测试数据集
    fr=open(filename)
    lists=fr.readlines()
    listdata=[]
    for list in lists:
        #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
         #注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。   split()表示分割标识符
        listdata.append(list.strip().split(','))
    classlabels1=[]
    datamat1=[]
    for i in range(len(listdata)):  #[0,len)的长度，故不需要加一
        classlabels1.append(listdata[i][-1])
        datamat1.append(listdata[i][0:-2])#选取[0,4)的元素
        datamat=np.mat(datamat1).astype(float)   #先将列表数据转换为矩阵，然后再将矩阵的元素转换为float型数据
        classlabels=np.mat(classlabels1).astype(float)
    return classlabels,datamat
    


#非均衡分类问题

def plotroc(predstrengths,classlabels):
    
    cur=(1.0,1.0)
    ysum=0.0
    numposclas=sum(np.array(classlabels)==1.0)#矩阵里面值为1时返回值为1，否则为0
    ystep=1/float(numposclas)#正例的倒数，y轴的步数
    xstep=1/float(len(classlabels)-numposclas)#反例的倒数，x轴的步数
    sortedindicies=predstrengths.argsort()#对可信度进行排序
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for index in sortedindicies.tolist()[0]:#tolist()作用是将列表sortedindicies从小到大的排列
        if classlabels[index]==1.0:
            delx=0;dely=ystep;
        else:
            delx=xstep;dely=0;
            ysum +=cur[1]
        ax.plot([cur[0],cur[0]-delx],[cur[1],cur[1]-dely],c='b')#分别从1.0开始减少x轴，y轴的值
        cur=(cur[0]-delx,cur[1]-dely)#循环一次降低一个步长
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('false positive rate');plt.ylabel('true positive rate')
    plt.title('roc curve for adaboost horse colic detection system')
    ax.axis([0,1,0,1])
    plt.show()
    print('the area under the curve is :',ysum*xstep)

    
                    
    

if __name__=='__main__':   
    #绘制roc曲线
    dataarr,labelarr=loaddataset('horseColicTraining2.txt')
    classifierarr,aggclassest=adaboosttrainds(dataarr,labelarr,10)
    plotroc(aggclassest.T,labelarr)
    
    
    
    
    
"""    
   #实现利用iris的部分数据作为训练数据集，部分作为测试数据集进行测试从而获得结果，发现没有错误正确率为100%，分类器比较好
    classlabels,datamat=irisdata('iris.txt')
    classifierarray=adaboosttrainds(datamat,classlabels,30)
    fr=open('iris-test.txt')
    lists=fr.readlines()
    datatest=[]
    for list in lists:    
        datatest.append(list.strip().split(','))#重写一编这部分代码的原因是上面函数irisdata（）输出的是包含多个数据样本的一个矩阵，而我们需要的是包含一个样本的数据矩阵
    for j in range(len(datatest)):
        a=np.mat(datatest[j][0:4]).astype(float)
        result=adaclassfy(a,classifierarray)
        print("the result is %d:",result,"the true result is %d:",datatest[j][-1])
"""
