# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 02:43:27 2019

@author: z
"""

import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

h = 1
sd = 1
n = 50
n_n = 1000
def gen_data(n, h, sd1, sd2):
    """ xxx """
    x1 = ss.norm.rvs(-h, sd1, n)
    y1 = ss.norm.rvs(0, sd1, n)
    
    x2 = ss.norm.rvs(h, sd2, n)
    y2 = ss.norm.rvs(0, sd2, n)
    return (x1, y1, x2, y2)

def plot_data(x1, y1, x2, y2):
    plt.figure()
    plt.plot(x1, y1, "o", ms=2)
    plt.plot(x2, y2, "o", ms=2)
    plt.xlabel("$X_1$")
    plt.ylabel("$X_2$")
    
def plot_probs(ax, clf, class_no):
    xx1, xx2 = np.meshgrid(np.arange(-5, 5, 0.1), np.arange(-5, 5, 0.1))
    probs = clf.predict_proba(np.stack((xx1.ravel(), xx2.ravel()), axis=1))
    Z = probs[:,class_no]
    Z = Z.reshape(xx1.shape)
    CS = ax.contourf(xx1, xx2, Z)
    cbar = plt.colorbar(CS)
    plt.xlabel("$X_1$")
    plt.ylabel("$X_2$")



(x1, y1, x2, y2) = gen_data(n_n, 1.5, 1, 1.5)
X = np.vstack((np.vstack((x1,y1)).T, np.vstack((x2,y2)).T))
y = np.hstack((np.repeat(1, n_n), np.repeat(2, n_n)))
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.5, random_state=1)

clf = LogisticRegression()
clf.fit(X_train, y_train)
print("测试数据：",clf.score(X_test, y_test))
print("单点分类概率：",clf.predict_proba(np.array([-2, 0]).reshape(1, -1)));
print("单点分类：",clf.predict(np.array([-2, 0]).reshape(1, -1)));

plt.figure(figsize=(5,8))
ax = plt.subplot(211)
plot_probs(ax, clf, 0)
plt.title("Pred. prob for class 1")
ax = plt.subplot(212)
plot_probs(ax, clf, 1)
plt.title("Pred. prob for class 2");
plot_data(x1, y1, x2, y2)


