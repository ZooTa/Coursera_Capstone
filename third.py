#!/usr/bin/env python
# coding: utf-8

# In[108]:


#importing Libraries
import requests
import lxml.html as lh
import bs4 as bs
import urllib.request
import numpy as np 
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns


# In[109]:


#Getting the data from url
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
res = requests.get(url)
soup = bs.BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
data = pd.read_json(df[0].to_json(orient='records'))


# In[110]:


#First 5 records
data.head()


# In[111]:


#Choosing only data where field Borough doesn't have not assigned value
raw_data_selected = data[data['Borough'] != 'Not assigned']


# In[112]:


#Grouping Data
raw_data_selected = raw_data_selected.groupby(['Borough', 'Postal Code'], as_index=False).agg(','.join)


# In[113]:


raw_data_selected.head()


# In[114]:


#Replacing values in Neighbourhood field with Borough where Neighbourhood is not assigned
raw_data_selected['Neighbourhood'] = np.where(raw_data_selected['Neighbourhood'] == 'Not assigned', raw_data_selected['Borough'], raw_data_selected['Neighbourhood'])


# In[115]:


#Shape of Data
raw_data_selected.shape


# In[ ]:





# In[ ]:





# In[116]:


geospatial_url = "https://cocl.us/Geospatial_data"
geospatial_data = pd.read_csv(geospatial_url)


# In[117]:


geospatial_data.head()


# In[118]:


# Renaming the columns
geospatial_data.columns = ['Postal Code', 'Latitude', 'Longitude']


# In[119]:


geospatial_data.columns


# In[120]:


#Merging dataframes
merged_data = pd.merge(raw_data_selected, geospatial_data, on='Postal Code')


# In[121]:


merged_data.head()


# In[ ]:





# In[ ]:





# In[122]:


merged_data['Coordinates'] = list(zip(merged_data['Latitude'], merged_data['Longitude']))


# In[123]:


merged_data.head()


# In[124]:


merged_data['Coordinates'] = merged_data['Coordinates'].apply(Point)


# In[125]:


gdf = gpd.GeoDataFrame(merged_data, geometry='Coordinates')


# In[126]:


gdf.head()


# In[129]:


# set up map
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
ax = cities[cities.name == "Toronto"].plot(
    color='green', edgecolor='black')
 plot and show
gdf.plot(ax=ax, color='red')

plt.show()


# In[ ]:




