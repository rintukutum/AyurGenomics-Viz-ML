
# coding: utf-8

# # Preprocessing Nominal Data

# ### Importing libraries

# In[1]:


import pandas as pd
import numpy as np


# ### Read file

# In[2]:


df = pd.read_csv("Testing/Ordinal_Data.csv", header=None)


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


# ### Handle null values

# In[5]:


# column names changed manually, changes to be recorded
# diff columns in the datasets 
for col in df:
    count = 1
    for ele in df[col]:
        if ele == 'nan':
            df.loc[count, col] = np.nan
        count += 1


# ### Save to csv

# In[6]:


df.transpose().to_csv("Preprocessed_Ordinal.csv", header = None)

