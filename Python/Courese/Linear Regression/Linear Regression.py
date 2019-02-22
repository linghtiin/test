# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 19:00:16 2019

@author: z
"""

import numpy as np
import scipy.stats as ss
import statsmodels.api as sm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


#生成数据
n = 100
beta_0 = 5
beta_1 = 2
beta_2 = -1
np.random.seed(1)
x_1 = 10 * ss.uniform.rvs(size=n)
x_2 = 10 * ss.uniform.rvs(size=n)
X = np.stack([x_1,x_2], axis=1)
y_sci = beta_0 + beta_1 * x_1 + beta_2 * x_2 + ss.norm.rvs(loc=0, scale=1, size=n)

x = 10 * ss.uniform.rvs(size=n)
y = beta_0 + beta_1 * x + ss.norm.rvs(loc=0, scale=1, size=n)

plt.figure()
plt.plot(x,y,"o",ms=5)
xx = np.array([0,10])
plt.plot(xx,beta_0 + beta_1 * xx)
plt.xlabel("x")
plt.ylabel("y");

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y_sci, c=y_sci)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_zlabel("$y_sci$");

#计算方差
def compute_rss(y_estimate, y): 
  return sum(np.power(y-y_estimate, 2)) 
def estimate_y(x, b_0, b_1): 
  return b_0 + b_1 * x 
rss = compute_rss(estimate_y(x, beta_0, beta_1), y) 

#最小二乘估计
rss = []
slopes = np.arange(-10,15,0.01)
for slope in slopes:
    rss.append(np.sum((y - beta_0 - slope * x)**2))
ind_min = np.argmin(rss)

plt.figure()
plt.plot(slopes,rss)
plt.xlabel("Slope")
plt.ylabel("RSS")
print("Estimate for the slope: ", slopes[ind_min])

#使用Statsmodel模型库
X_sm = sm.add_constant(x)
mod = sm.OLS(y,X_sm)
est = mod.fit()
print(est.summary())

#使用Scikit_Learn机器学习库
lm = LinearRegression(fit_intercept=True)
lm.fit(X,y_sci)
print("beta 0: ",lm.intercept_)    #截距
print("beta 1&2: ",lm.coef_)         #变量数组
X_0 = np.array([2,4])
print("预测 [%d,%d]处y值: %.4f" % (X_0[0], X_0[1], lm.predict(X_0.reshape(1, -1))))
print("R2 :",lm.score(X, y_sci))


#测试数据
X_train, X_test, y_train, y_test = train_test_split(X, y_sci, train_size=0.5, random_state=1)
lm = LinearRegression(fit_intercept=True)
lm.fit(X_train, y_train)
lm.score(X_test, y_test)

