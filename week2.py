#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt


# In[13]:


sold = pd.read_csv("combined_sold_all.csv", low_memory=False) 
print("Rows, columns:", sold.shape)
sold.head()


# In[14]:


print(sold.dtypes.to_string())


# In[15]:


print(sold["PropertyType"].unique())
print(sold["PropertyType"].value_counts())
print(sold["PropertyType"].value_counts(normalize=True) * 100)


# In[16]:


rows_before = len(sold)
sold = sold[sold["PropertyType"] == "Residential"]
rows_after = len(sold)

print("Before filter:", rows_before)
print("After filter:", rows_after)
print("Removed:", rows_before - rows_after)


# In[17]:


null_counts = sold.isnull().sum()
null_pct = (null_counts / len(sold)) * 100

null_summary = pd.DataFrame({
    "null_count" : null_counts,
    "null_pct" : null_pct.round(2)
}).sort_values("null_pct", ascending=False)

null_summary


# In[18]:


high_missing = null_summary[null_summary["null_pct"] > 90]
print("Columns over 90% missing:", len(high_missing))
high_missing


# In[19]:


pd.set_option("display.float_format", "{:,.2f}".format)


# In[20]:


key_fields = ["ClosePrice", "LivingArea", "DaysOnMarket"]

summary = sold[key_fields].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
summary


# In[21]:


cols = ["ClosePrice", "ListPrice", "LivingArea", "DaysOnMarket", "City", "PropertySubType"]

print("Highest close prices:")
print(sold.nlargest(10, "ClosePrice")[cols])

print("\nLargest living areas:")
print(sold.nlargest(10, "LivingArea")[cols])

print("\nNegative days on market:", (sold["DaysOnMarket"] < 0).sum())


# In[22]:


for field in key_fields:
    low = sold[field].quantile(0.01)
    high = sold[field].quantile(0.99)
    trimmed = sold[field][(sold[field] >= low) & (sold[field] <= high)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    trimmed.plot(kind="hist", bins=50, ax=axes[0], title=f"{field} – Histogram (1st–99th pct)")
    trimmed.plot(kind="box", ax=axes[1], title=f"{field} – Boxplot (1st–99th pct)")
    plt.show()


# In[ ]:





# In[ ]:




