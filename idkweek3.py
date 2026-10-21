#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

sold = pd.read_csv("combined_sold_residential.csv", low_memory=False)
listings = pd.read_csv("combined_listings_residential.csv", low_memory=False)

print("Sold:", sold.shape)
print("Listings:", listings.shape)


# In[3]:


url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])

print(mortgage.shape)
print(mortgage.head())
print(mortgage.tail())


# In[4]:


mortgage.columns = ["date", "rate_30yr_fixed"]
print(mortgage.head())


# In[7]:


mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

print(mortgage_monthly.tail(12))


# In[8]:


sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")
listings["year_month"] = pd.to_datetime(listings["ListingContractDate"]).dt.to_period("M")

print(sold[["CloseDate", "year_month"]].head())
print(listings[["ListingContractDate", "year_month"]].head())


# In[10]:


sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(mortgage_monthly, on="year_month", how="left")

print("Sold rows before/after:", len(sold), len(sold_with_rates))
print("Listings rows before/after:", len(listings), len(listings_with_rates))


# In[11]:


sold_nulls = sold_with_rates["rate_30yr_fixed"].isnull().sum()
listing_nulls = listings_with_rates["rate_30yr_fixed"].isnull().sum()

print("Sold rows with no rate:", sold_nulls)
print("Listings rows with no rate:", listing_nulls)


# In[12]:


missing = sold_with_rates[sold_with_rates["rate_30yr_fixed"].isnull()]
print(missing[["CloseDate", "year_month"]].head(20))


# In[13]:


print(sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head())
print(listings_with_rates[["ListingContractDate", "year_month", "ListPrice", "rate_30yr_fixed"]].head())


# In[14]:


sold_with_rates.to_csv("sold_with_rates.csv", index=False)
listings_with_rates.to_csv("listings_with_rates.csv", index=False)
print("Saved.")


# In[ ]:





# In[ ]:





# In[ ]:




