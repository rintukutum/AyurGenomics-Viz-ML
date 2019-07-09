
# coding: utf-8

# # Calculating Entropies/Distances

# ### Importing libraries

# In[29]:


import pandas as pd
import numpy as np
from pandas.api.types  import CategoricalDtype
from math import log
import math
import matplotlib.pyplot as plt


# ### Importing Nominal and Ordinal Categories

# In[30]:


ordinal_categories = pd.read_csv('Preprocessed_Ordinal.csv',header=None,index_col=0)
nominal_categories = pd.read_csv('Preprocessed_Nominal.csv',header=None,index_col=0)


# ### Making dictionary of Ordinal and Nominal Categories

# In[12]:


mapping_ordinal = {}  

for attr in ordinal_categories.index:
    nnull = ordinal_categories.loc[attr,ordinal_categories.loc[attr,:].notnull()].tolist()
    mapping_ordinal[attr]=CategoricalDtype(nnull,ordered=True)


# In[13]:


mapping_nominal = {}

for attr in nominal_categories.index:
    nnull = nominal_categories.loc[attr,nominal_categories.loc[attr,:].notnull()].tolist()
    mapping_nominal[attr]=CategoricalDtype(nnull,ordered=True)


# In[14]:


mapping = mapping_ordinal.copy()
mapping.update(mapping_nominal)


# ### Reading dataset

# In[15]:


data = pd.read_csv('Preprocessed_Dataset.csv', dtype=mapping, index_col=0)


# ### Select a particular Prakriti

# In[16]:


#If selecting particular column, uncomment the below line
#data = data.loc[data['prakriti'] == 'k']
data.drop("prakriti", axis = 1, inplace = True)


# ### Calculating probabilities

# In[17]:


prob_ordinal = []
for  attr in ordinal_categories.index:
    prob_ordinal.append(data[attr].value_counts(normalize=True,sort=False).tolist())
    
prob_nominal = []
for  attr in nominal_categories.index:
    prob_nominal.append(data[attr].value_counts(normalize=True,sort=False).tolist())


# ### Calculating Entropies

# In[31]:


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


# In[32]:


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


# ### Calculating Reliability

# In[21]:


RAr_ordinal = np.divide(EAr_ordinal,SAr_ordinal).tolist()
RAr_nominal = np.divide(EAr_nominal,SAr_nominal).tolist()


# ### Calculating Total Reliability and weights

# In[22]:


##  W = RAr / TR
##  where TR = sum(RAr) ie Total Reliability

TR = sum(RAr_ordinal) + sum(RAr_nominal)

weights_ordinal = np.divide(RAr_ordinal,TR).tolist()
weights_nominal = np.divide(RAr_nominal,TR).tolist()


# ### Precalculate distances between categories

# In[23]:


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


# ### Map from attribute to category distances

# In[33]:


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


# ### Map from attribute to entropies of categories

# In[36]:


# Uncomment the line below to map the attributes to their entropies as well
    
map_entropy = {}
for index,col in enumerate(ordinal_categories.index):
      map_entropy[col]=entropy_ordinal[index]
for index,col in enumerate(nominal_categories.index):
      map_entropy[col]=entropy_nominal[index]


# ### Calculating distance matrix between individuals

# In[37]:


# ''' SUBTASK 7 - Creating the Distance Matrix '''

# dist_matrix = []
# for index1 in data.index:
#     dist_temp =[]
#     for index2 in data.index:
#         dist = 0.0
#         for cols in data.columns: 
#             if type(data.loc[index1,cols]) == str and type(data.loc[index2,cols]) == str:
#                 #dist += (map_entropy[cols][mapping[cols].categories.tolist().index(data.loc[index1,cols])]- map_entropy[cols][mapping[cols].categories.tolist().index(data.loc[index2,cols])])**2
#                 dist += map_dist[cols][mapping[cols].categories.tolist().index(data.loc[index1,cols])][mapping[cols].categories.tolist().index(data.loc[index2,cols])]**2
#         dist_temp.append(math.sqrt(dist))
#     dist_matrix.append(dist_temp)


# ### Calculating Entropy matrix for all individuals

# In[27]:


tlist = []
for index1 in data.index:
    elist = []
    for col in data.columns:
        if type(data.loc[index1,col]) == str:
            elist.append(map_entropy[col][data[col].cat.categories.tolist().index(data.loc[index1,col])])
        else: 
            elist.append(None)
    tlist.append(elist)
df_entropy = pd.DataFrame(tlist)


# ### Saving Entropy matrix as csv

# In[ ]:


df_entropy.to_csv('Entropy_all.csv',header=False,index=False)

