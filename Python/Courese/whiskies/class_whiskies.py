# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 01:59:45 2019

@author: z
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster.bicluster import SpectralCoclustering

workpath = os.getcwd()
whiskies = pd.read_csv(workpath + '\\' + 'whiskies.txt')
whiskies['Region'] = pd.read_csv(workpath + '\\' + 'regions.txt')
whiskies_data = whiskies.iloc[:,2:14]

#相关性矩阵
corr_whiskies = pd.DataFrame.corr(whiskies_data.transpose())

#聚类，重新排序
model = SpectralCoclustering(n_clusters=6,random_state=0)
model.fit(corr_whiskies)
np.sum(model.rows_,axis=1)

whiskies['Group'] = pd.Series(model.row_labels_,index=whiskies.index)
whiskies = whiskies.iloc[np.argsort(model.row_labels_)]
whiskies = whiskies.reset_index(drop=True)

#聚类排序后的相关性矩阵
correlations = pd.DataFrame.corr(whiskies.iloc[:,2:14].transpose())
correlations = np.array(correlations)

#绘图
plt.figure(figsize=(20,10))
plt.subplot(121)
plt.pcolor(corr_whiskies)
plt.title("Original")
plt.axis('tight')
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.axis('tight')
plt.savefig("correlations.pdf")
plt.show()
