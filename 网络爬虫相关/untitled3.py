# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:00:13 2018

@author: chenxi
"""
import csv
# 文件头，一般就是数据名
fileHeader = ["name", "score"]
# 假设我们要写入的是以下两行数据
d1 = ["Wang", "100"]
d2 = ["Li", "80"]
# 写入数据
csvFile = open("instance.csv", "w")
writer = csv.writer(csvFile)
# 写入的内容都是以列表的形式传入函数
writer.writerow(fileHeader)
writer.writerow(d1)
writer.writerow(d1)
csvFile.close()