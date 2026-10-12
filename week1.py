import pandas as pd 
import os

jan = pd.read_csv("data/CRMLSListing202401.csv", low_memory=False)
print(jan.shape)
jan.head()
#.shape prints(row,columns), .head() shows the first 5 rows. When you scroll through the data set you can get a sense of the columns.

jan["PropertyType"].value_counts()
#this lists all the property types and how many rows each one has. 

feb = pd.read_csv("data/CRMLSListing202402.csv", low_memory=False)
test = pd.concat([jan, feb], ignore_index=True)

print("Jan rows:", len(jan))
print("Feb rows:", len(feb))
print("Jan + Feb:", len(jan) + len(feb))
print("Combined:", len(test))

#this is a practice combining the two months 

months = pd.date_range("2024-01", "2026-03", freq="MS").strftime("%Y%m").tolist()
print(len(months))
print(months)

#this builds a list of every month 

listing_frames = []
listing_total = 0

for month in months:
    df = pd.read_csv(f"data/CRMLSListing{month}.csv", low_memory=False)
    print(month, len(df))
    listing_total += len(df)
    listing_frames.append(df)

listings = pd.concat(listing_frames, ignore_index=True)

print("Sum of monthly rows:", listing_total)
print("Combined rows:", len(listings))

sold_frames = []
sold_total = 0
sold_missing = []

for month in months:
    path = f"data/CRMLSSold{month}.csv"
    if not os.path.exists(path):
        path = f"data/CRMLSSold{month}_filled.csv"
    if not os.path.exists(path):
        print(month, "MISSING")
        sold_missing.append(month)
        continue

    df = pd.read_csv(path, low_memory=False)
    print(month, len(df))
    sold_total += len(df)
    sold_frames.append(df)

sold = pd.concat(sold_frames, ignore_index=True)

print("Sum of monthly rows:", sold_total)
print("Combined rows:", len(sold))
print("Missing months:", sold_missing)

listings_res = listings[listings["PropertyType"] == "Residential"]
sold_res = sold[sold["PropertyType"] == "Residential"]

print("Listings before folter:", len(listings))
print("Listings after filter:", len(listings_res))
print("Sold before filter:", len(sold))
print("Sold after filter:", len(sold_res))

listings_res.to_csv("combined_listings_residential.csv", index=False)
sold_res.to_csv("combined_sold_residential.csv", index=False)
print("Saved.")