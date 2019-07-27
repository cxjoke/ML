# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:54:16 2018

@author: yewenbin
"""
import numpy as np 
fr = open('uci.txt')
array = fr.readlines()
number = len(array)
Mat = np.zeros((number, 4))
Labels = []
index = 0
for i in array:
    line = i.strip('\n').split(',')
    Mat[index,:] = line[0:4]
    Labels.append(int(line[-1]))
    index += 1
print(Mat)
print(Labels)
print(Mat[0][0])

