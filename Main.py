#!/usr/bin/env python
# coding: utf-8

# In[146]:


import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import random as rnd
from scipy.stats import zscore


# In[147]:


data = pd.read_csv("data.csv")


# In[148]:


data.info()


# In[149]:


data.head(35)


# In[150]:


data.describe()


# In[151]:


data=data.fillna(0)


# In[152]:


countries_stats= data.drop_duplicates(ignore_index=True, subset=['Entity', 'Average temperature per year', 'Hospital beds per 1000 people',
       'Medical doctors per 1000 people', 'GDP/Capita', 'Population',
       'Median age', 'Population aged 65 and over (%)'])

countries_stats=countries_stats.drop(['Date', 'Daily tests','Cases', 'Deaths'],axis=1)
countries_stats=countries_stats.rename(columns={"Entity":"Country"})
countries_stats=countries_stats.set_index("Country")


# In[153]:


print(countries_stats.shape)
for country in countries_stats.index:
    print(country)


# In[154]:


data_days_stats={}
for country in countries_stats.index:
    single_country=data.loc[data['Entity']==country]
    single_country=single_country[['Date','Daily tests','Cases','Deaths']]
    single_country=single_country.set_index("Date")
    data_days_stats[country]=  single_country


# In[155]:


data_days_stats['France'].info()


# In[156]:


for country in data_days_stats.values():
    country["Daily cases"]=country['Cases'].diff(1)
    country["Daily deaths"]=country['Deaths'].diff(1)



# In[157]:


for country,dataframes in data_days_stats.items():
    data_days_stats[country]=dataframes.fillna(0)
    print(country,data_days_stats[country].describe())


# In[158]:


for country,dataframes in data_days_stats.items():

    print(country,data_days_stats[country].median())


# In[159]:


country,dataframes = rnd.choice(list(data_days_stats.items()))
sns.lineplot(data=dataframes,x=dataframes.index,y='Daily cases').set(title=country)



# In[160]:


print(data_days_stats['Malta'].head(40))
print(data_days_stats['Malta'].tail(40))


# In[170]:


print(data_days_stats['France'].head(50))
print(data_days_stats['France'].tail(50))


# In[171]:


mean_daily_tests=[]
mean_daily_cases=[]
mean_daily_deaths=[]
for dataframes in data_days_stats.values():
    mean_daily_tests.append(dataframes["Daily tests"].mean())
    mean_daily_cases.append(dataframes['Daily cases'].loc[dataframes["Cases"]>10].mean())
    mean_daily_deaths.append(dataframes['Daily deaths'].loc[dataframes["Cases"]>10].mean())


# In[175]:


countries_stats['Mean daily tests']=mean_daily_tests
countries_stats['Mean daily cases']=mean_daily_cases
countries_stats['Mean daily deaths']=mean_daily_deaths



# In[177]:


countries_stats.head(10)


# In[179]:


countries_stats[['Mean daily tests','Mean daily cases','Mean daily deaths']]=countries_stats[['Mean daily tests','Mean daily cases','Mean daily deaths']].apply(lambda  x:round(x))


# In[180]:


countries_stats.head(10)


# In[185]:


pd.options.display.max_rows=105
countries_stats.sort_values(by=['Mean daily deaths'],ascending=False)


# In[188]:


countries_stats["Daily tests per thousand people"]=countries_stats['Mean daily tests']/(countries_stats['Population']/1000)
countries_stats["Daily cases per thousand people"]=countries_stats['Mean daily cases']/(countries_stats['Population']/1000)
countries_stats["Daily deaths per thousand people"]=countries_stats['Mean daily deaths']/(countries_stats['Population']/1000)


# In[189]:


pd.options.display.max_rows=105
countries_stats.sort_values(by=['Daily deaths per thousand people'],ascending=False)


# In[200]:


total_cases=[]
total_deaths=[]
for dataframe in data_days_stats.values():
    total_cases.append(dataframe.loc['2021-02-28','Cases'])
    total_deaths.append(dataframe.loc['2021-02-28','Deaths'])
countries_stats['Total cases']= total_cases
countries_stats['Total deaths']= total_deaths


# In[204]:


countries_stats['Total cases percentage']=countries_stats['Total cases']/countries_stats['Population']*100
countries_stats['Total deaths percentage']=countries_stats['Total deaths']/countries_stats['Population']*100


# In[211]:


countries_stats.sort_values(by='Total deaths percentage',ascending=False)


# In[212]:
