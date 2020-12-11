#!/usr/bin/env python
# coding: utf-8

# In[32]:


#importing Libraries
import requests
import lxml.html as lh
import bs4 as bs
import urllib.request
import numpy as np 
import pandas as pd


# In[33]:


#Getting the data from url
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
res = requests.get(url)
soup = bs.BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
data = pd.read_json(df[0].to_json(orient='records'))


# In[34]:


#First 5 records
data.head()


# In[35]:


#Choosing only data where field Borough doesn't have not assigned value
raw_data_selected = data[data['Borough'] != 'Not assigned']


# In[36]:


#Grouping Data
raw_data_selected = raw_data_selected.groupby(['Borough', 'Postal Code'], as_index=False).agg(','.join)


# In[37]:


raw_data_selected.head()


# In[38]:


#Replacing values in Neighbourhood field with Borough where Neighbourhood is not assigned
raw_data_selected['Neighbourhood'] = np.where(raw_data_selected['Neighbourhood'] == 'Not assigned', raw_data_selected['Borough'], raw_data_selected['Neighbourhood'])


# In[39]:


#Shape of Data
raw_data_selected.shape


# In[ ]:





# In[ ]:





# In[40]:


geospatial_url = "https://cocl.us/Geospatial_data"
geospatial_data = pd.read_csv(geospatial_url)


# In[41]:


geospatial_data.head()


# In[42]:


# Renaming the columns
geospatial_data.columns = ['Postal Code', 'Latitude', 'Longitude']


# In[43]:


geospatial_data.columns


# In[44]:


#Merging dataframes
merged_data = pd.merge(raw_data_selected, geospatial_data, on='Postal Code')


# In[45]:


merged_data.head()


# In[ ]:




