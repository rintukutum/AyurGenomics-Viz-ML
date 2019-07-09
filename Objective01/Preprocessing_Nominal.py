
# coding: utf-8

# # Preprocessing Nominal Data

# ### Importing libraries

# In[1]:


import pandas as pd
import numpy as np


# ### Read file

# In[2]:


df = pd.read_csv("Nominal_Data.csv", header=None)


# ### Transpose DataFrame

# In[3]:


df = df.transpose()
df.columns = df.iloc[0]
df = df[1:]


# ### Lower Case

# In[4]:


# changing all columns to lower case
df.columns = [x.lower() for x in df.columns]

#converting dataset categries to lowercase.
for col in df:
    count = 1
    for ele in df[col]:
            df.loc[count, col] = str(ele).lower()
            count += 1


# ### Rename columns

# In[5]:


col_rename = {'hair_feel':'hair_feel_coarse',
             'hair_nature1': 'hair_graying',
             'hair_nature2': 'hair_falling',
             'hair_nature3': 'hair_breaking',
             'lips_nature2': 'lips_firm',
             'lips_nature5': 'lips_cracked',
             'lips_nature6': 'lips_wrinkled',
             'nails_nature2': 'nails_firm',
             'nails_nature5': 'nails_brittle',
             'palms_nature2': 'palms_firm',
             'palms_nature5': 'palms_cracked',
             'palms_nature6': 'palms_wrinkled',
             'soles_nature2': 'soles_firm',
             'soles_nature5': 'soles_cracked',
             'soles_nature6': 'soles_wrinkled',
             'teeth_appearance1': 'teeth_brittle',
             'teeth_appearance2': 'teeth_loose'}

df.rename(columns = col_rename, inplace = True)


# ### Handle null values

# In[6]:


# column names changed manually, changes to be recorded
# diff columns in the datasets 
for col in df:
    count = 1
    for ele in df[col]:
        if ele == 'nan':
            df.loc[count, col] = np.nan
        count += 1


# ### Rename categories

# In[7]:


# changing categories of features: like_**** & suit_**** to yes/no from like_/donotlike_
for col in df:
    count = 1
    if (col[:4] == 'like') | (col[:4] == 'suit'):
        for ele in df[col]:
            if (str(ele)[:4] == 'like') | (str(ele)[:4] == 'suit'):
                df.loc[count, col] = "yes"
            if (str(ele)[:4] == 'dono'):
                df.loc[count, col] = "no"
            count += 1

#cleaning column: suit_sweet
count = 1
for ele in df['suit_sweet']:
    if str(ele) == 'sweet':
        df.loc[count, 'suit_sweet'] = "yes"
    count+=1
    
# handling non_**** categories
for col in df:
    count = 1
    options = df[col].dropna().unique()
    if (options.size == 2) and ((options[0][:3] == 'non')  or (options[1][:3] == 'non')): 
        for ele in df[col]:
            if type(ele) == str:
                if str(ele)[:3] == 'non':
                    df.loc[count, col] = 'no'
                else:
                    df.loc[count, col] = 'yes'
            count+=1


# ### Save to csv

# In[8]:


df.transpose().to_csv("Preprocessed_Nominal.csv", header = None)

