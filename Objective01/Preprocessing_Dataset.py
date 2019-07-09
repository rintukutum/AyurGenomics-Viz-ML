
# coding: utf-8

# # Preprocessing Dataset

# ### Import libraries

# In[28]:


import pandas as pd
import numpy as np


# ### Read Dataset

# In[29]:


df = pd.read_csv("Dataset_labelled_253.csv")


# ### Lower Case

# In[30]:


#converting dataset categries to lowercase.

# changing all columns to lower case
df.columns = [x.lower() for x in df.columns]

#to get all columns except study_id
df_1 = df.iloc[:,1:]

#changing dataset values
for col in df_1.columns:
    df[col] = df[col].str.lower()


# ### Rename columns

# In[31]:


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


# ### Rename categories

# In[32]:


# changing categories of features: like_**** & suit_**** to yes/no from like_/donotlike_
for col in df:
    count = 0
    if (col[:4] == 'like') | (col[:4] == 'suit'):
        for ele in df[col]:
            if (str(ele)[:4] == 'like') | (str(ele)[:4] == 'suit'):
                df.loc[count, col] = "yes"
            if (str(ele)[:4] == 'dono'):
                df.loc[count, col] = "no"
            count += 1


# In[33]:


#cleaning column: suit_sweet
count = 0
for ele in df['suit_sweet']:
    if str(ele) == 'sweet':
        df.loc[count, 'suit_sweet'] = "yes"
    count+=1


# In[34]:


# handling non_**** categories
for col in df:
    count = 0
    options = df[col].dropna().unique()
    if (options.size == 2) and ((options[0][:3] == 'non')  or (options[1][:3] == 'non')): 
        for ele in df[col]:
            if str(ele)[:3] == 'non':
                df.loc[count, col] = 'no'
            elif ele == np.nan:
                continue
            else:
                df.loc[count, col] = 'yes'
            count+=1


# ### Handle null values

# In[35]:


#filling nan values 
for col in df:
    count = 0
    for ele in df[col]:
        if ele == 'nan':
            df.loc[count, col] = np.nan
        count += 1


# ### Save to csv

# In[36]:


df.set_index('sampleid',inplace = True)
df.to_csv("Preprocessed_Dataset.csv")

