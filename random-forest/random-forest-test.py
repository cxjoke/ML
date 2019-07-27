# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:32:58 2018

@author: chenxi
"""

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

iris = load_iris()  #加载iris数据

df = pd.DataFrame(iris.data, columns=iris.feature_names)#数据列表，表头为iris.feature_names

df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75  #左闭右开区间，len（df）输出样本数目，为int或元组(tuple)类型，
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
df.head()

train, test = df[df['is_train']==True], df[df['is_train']==False]

features = df.columns[:4]
clf = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(train['species'])
clf.fit(train[features], y)

preds = iris.target_names[clf.predict(test[features])]
pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])