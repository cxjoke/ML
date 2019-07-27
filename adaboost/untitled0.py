# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:19:03 2019

@author: chenxi
"""
import numpy as np


class person():
    empCount = 0

    def __init__(self,name,salary):
        self.name = name
        self.salary = salary
        person.empCount+=1
    def display(self):
        print("the person num is :%d"%person.empCount)
    def diplaypersoninfo(self):
        print("name:%d,Salary:%d"%self.name,%self.salary)
    
    


per1=person(6,5000)
per2=person(6,6000)
per1.diplaypersoninfo()
