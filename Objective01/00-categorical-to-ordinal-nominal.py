#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:34:13 2019

@author: Rohit Jain, Ishita Mediratta, Kartik Bhatia, Anmol Agarwal, Syed Ahsan Abbas, Nischit Soni

This code is meant to calculate the entropy-based distances using both, 
ordinal & nominal attributes.

Source: Y. Zhang, Y. Cheung and K. C. Tan, "A Unified Entropy-Based 
Distance Metric for Ordinal-and-Nominal-Attribute Data Clustering," in IEEE 
Transactions on Neural Networks and Learning Systems.
doi: 10.1109/TNNLS.2019.2899381


    * Data: 
        1. We are given a dataset(as .csv file) that contains 
        the phenotype attribute and the order of the choices that were given 
        on the questionnaire - Separate into 2 datasets - Ordinal & Nominal
        2. CSV of the responses filled

"""

###############################################################################
#                               SOURCE CODE                                   #
###############################################################################

''' IMPORTING THE DEPENDENCIES '''

import pandas as pd
import numpy as np
from pandas.api.types  import CategoricalDtype
from math import log
import math
import matplotlib.pyplot as plt


''' READING THE FILES '''

ordinal_categories = pd.read_csv('Ordinal Data.csv',header=None,index_col=0)
nominal_categories = pd.read_csv('Nominal Data.csv',header=None,index_col=0)
 
##  1. Read this file and create a dictionary of the form {phenotype: [category1, category2 .....]}
##  2. Use this dictionary to store the data from the responses as the categorical data 


mapping_ordinal = {}  

for attr in ordinal_categories.index:
    nnull = ordinal_categories.loc[attr,ordinal_categories.loc[attr,:].notnull()].tolist()
    mapping_ordinal[attr]=CategoricalDtype(nnull,ordered=True)

mapping_nominal = {}

for attr in nominal_categories.index:
    nnull = nominal_categories.loc[attr,nominal_categories.loc[attr,:].notnull()].tolist()
    mapping_nominal[attr]=CategoricalDtype(nnull,ordered=True)

mapping = mapping_ordinal.copy()
mapping.update(mapping_nominal)

''' READING THE DATASET '''

## We have created a dictionary from the phenotype attribute to the values that it can assume. 
## We will read the responses data as categorical data.

data = pd.read_csv('dataset.csv', dtype=mapping, index_col=0)


## Uncomment the lines below to see the attricutes with their respective responses
# for col in data.columns:
#   print(data[col].value_counts(dropna=False))


''' SUBTASK 1 - Find the occurence probability for all the categories for all the atrributes '''

##  p = number of occurences / number of people

prob_ordinal = []
for  attr in ordinal_categories.index:
    prob_ordinal.append(data[attr].value_counts(normalize=True,sort=False).tolist())
    
prob_nominal = []
for  attr in nominal_categories.index:
    prob_nominal.append(data[attr].value_counts(normalize=True,sort=False).tolist())

''' SUBTASK 2 - Find the entropy E for all the categories, entropy of an attribute EAr and the standard entropy of an attribute SAr for all the attributes '''

##  Entropy = -p * log(p)
##  EAr = sum(Entropy)
##  SAr = log(no of categories)

# Stores entropy of ordinal categories
entropy_ordinal = []    
EAr_ordinal = []
SAr_ordinal = []
for ele in prob_ordinal:
    entropy_attr = []
    for p in ele:
        if p:
            entropy_attr.append(-1*p*log(p,2))
        else:
            entropy_attr.append(0)
    entropy_ordinal.append(entropy_attr)
    EAr_ordinal.append(sum(entropy_attr))
    SAr_ordinal.append(log(len(entropy_attr),2))

# Stores entropy of nominal categories    
entropy_nominal = []
EAr_nominal = []
SAr_nominal = []
for ele in prob_nominal:
    entropy_attr = []
    for p in ele:
        if p:
            entropy_attr.append(-1*p*log(p,2))
        else:
            entropy_attr.append(0)
    entropy_nominal.append(entropy_attr)
    EAr_nominal.append(sum(entropy_attr))
    SAr_nominal.append(log(len(entropy_attr),2))
    
''' SUBTASK 3 - Calculate Reliability RAr for each attribute '''

##  RAr = EAr / SAr

RAr_ordinal = np.divide(EAr_ordinal,SAr_ordinal).tolist()
RAr_nominal = np.divide(EAr_nominal,SAr_nominal).tolist()

''' SUBTASK 4 - Calculate the weights for the attributes '''

##  W = RAr / TR
##  where TR = sum(RAr) ie Total Reliability

TR = sum(RAr_ordinal) + sum(RAr_nominal)

weights_ordinal = np.divide(RAr_ordinal,TR).tolist()
weights_nominal = np.divide(RAr_nominal,TR).tolist()

''' SUBTASK 5 - Storing the distances of all categories '''

##  Ordinal distances also considers the sum of all categories in [i,j]
##  Nominal distances only consider the sum o {i,j}

dist_ordinal = []
for index,ele in enumerate(entropy_ordinal):
    dist_cat_attr =[]
    for i in range(len(ele)):
        for j in range(len(ele)):
            if i == j:
                dist_cat_attr.append(0)
            else:
                dist_cat_attr.append(weights_ordinal[index]*sum(ele[min(i,j):(max(i,j)+1)]))
    dist_cat_attr = np.array(dist_cat_attr).reshape(len(ele),len(ele)).tolist()
    dist_ordinal.append(dist_cat_attr)

dist_nominal = []
for index,ele in enumerate(entropy_nominal):
    dist_cat_attr =[]
    for i in range(len(ele)):
        for j in range(len(ele)):
            if i == j:
                dist_cat_attr.append(0)
            else:
                dist_cat_attr.append(weights_nominal[index]*(ele[i]+ele[j]))
    dist_cat_attr = np.array(dist_cat_attr).reshape(len(ele),len(ele)).tolist()
    dist_nominal.append(dist_cat_attr)
    
''' SUBTASK 6 - Mapping attributes with their respective distances '''

map_dist = {}
for index,col in enumerate(ordinal_categories.index):
    map_dist[col]=dist_ordinal[index]

for index,col in enumerate(nominal_categories.index):
    map_dist[col]=dist_nominal[index]
    
## Uncomment the line below to map the attributes to their entropies as well
    
#   map_entropy = {}
#   for index,col in enumerate(ordinal_categories.index):
#       map_entropy[col]=entropy_ordinal[index]
#   for index,col in enumerate(nominal_categories.index):
#       map_entropy[col]=entropy_nominal[index]
    
''' SUBTASK 7 - Creating the Distance Matrix '''

dist_matrix = []
for index1 in data.index:
    dist_temp =[]
    for index2 in data.index:
        dist = 0.0
        for cols in data.columns: 
            if type(data.loc[index1,cols]) == str and type(data.loc[index2,cols]) == str:
                #dist += (map_entropy[cols][mapping[cols].categories.tolist().index(data.loc[index1,cols])]- map_entropy[cols][mapping[cols].categories.tolist().index(data.loc[index2,cols])])**2
                dist += map_dist[cols][mapping[cols].categories.tolist().index(data.loc[index1,cols])][mapping[cols].categories.tolist().index(data.loc[index2,cols])]**2
        dist_temp.append(math.sqrt(dist))
    dist_matrix.append(dist_temp)
    
    
    
###############################################################################
#                             VISUALISATION                                   #
###############################################################################

## Storing the distance matrix
pd.DataFrame(dist_matrix).to_csv('distance_matrix.csv')

## Reading the csv
result = pd.read_csv('distance_matrix.csv',index_col=0)

## Converting into a Numpy Matrix
mat = np.matrix(result)
#print(mat.shape)

''' Visualizing the Matrix '''

plt.imshow(result,interpolation='nearest',cmap='jet')

''' Applying Agglomerative Clustering '''

import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))  
plt.title("Dendogram")  
dend = shc.dendrogram(shc.linkage(mat, method='ward'))  



## Using the Dendogram to approximate the number of clusters that we can use

from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')  
cluster.fit_predict(mat) 
print(cluster.labels_)

''' Applying MDS to see if there are any clusters formed when all attributes are considered '''

from sklearn import manifold

embedding = manifold.MDS(n_components=2)
X_r = embedding.fit_transform(mat)
print(plt.scatter(X_r[:,0],X_r[:,1]))

## We are able to see roughly 3 clusters are formed
