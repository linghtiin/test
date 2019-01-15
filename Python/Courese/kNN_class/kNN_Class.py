# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:33:23 2019

@author: z
"""
import math
import random
import numpy as np
import scipy.stats as ss
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

def distance(p1,p2):
    """ Return the distance of point. """
    return np.sqrt(np.sum(np.power(p2 - p1,2)))

def majority_vote(votes):
    """Pick the winner of vote."""
    vote_count = Counter(votes)
    winners = []
    max_count = max(vote_count.values())
    for vote,count in vote_count.items():
        if count == max_count:
            winners.append(vote)
    return random.choice(winners)

def majority_vote_by_mode(votes):
    """ Pick the winner of vote by mode. """
    mode,count = ss.mstats.mode(votes)
    return mode

def find_nearest_neighbors(p,points,k=5):
    """ Find the k nearest neighbors of point p and return their indices. """
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p,points[i])
    ind = np.argsort(distances)
    return ind[:k]

def knn_predict(p,points,outcomes,k=5):
    ind =find_nearest_neighbors(p,points,k)
    return majority_vote(outcomes[ind])
    
def generate_synth_data(n=50):
    """ generate data. """
    class1 = ss.norm(0,1).pdf()
    class2 = ss.norm(1,1).pdf(size=n)
    predictors = np.compress(class1,class2,axis=0)
    outcomes = np.compress(np.zeros(len(class1)),np.ones(len(class2)))
    return (predictors,outcomes)
    
    
def make_prediction_grid(predictors,outcomes,limits,h=1,k=5):
    (x_min,x_max,y_min,y_max) = limits
    xs = np.arange(x_min,x_max,h)
    ys = np.arange(y_min,y_max,h)
    xx,yy = np.meshgrid(xs,ys)
    
    prediction_grid = np.zeros(xx.shape,dtype = int)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            p = np.array([x,y])
            prediction_grid[j,i] = knn_predict(p,predictors,outcomes,k)
            
    return xx,yy,prediction_grid
            
def plot_prediction_grid (xx, yy, predictors,outcomes, prediction_grid, filename):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)
    
iris = load_iris()
xx,yy,prediction_grid = make_prediction_grid(iris.data[:,0:2],iris.target,(3,8,2,4),0.1,5)
plot_prediction_grid(xx,yy,iris.data[:,0:2],iris.target,prediction_grid,'iris.pdf')