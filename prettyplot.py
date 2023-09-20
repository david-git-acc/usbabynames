import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolours

# This program is the same as alltime_plot, but specifically for creating pretty visualisations
# Differences: 
# -No x or y axes locators
# -No randomised bars

# Our dataset goes from 1880 to 2019 so we will use these numbers as our start and end points
start=1880
end = 2019
years = np.arange(start,end+1)

# Pixel to inch ratio
px=1/96

# So we can create a pandas dataframe for it
column_names = ["name","sex","quantity"]

# Male or female baby names
use_women = False
gender = "female" if use_women else "male"

# This dict will store the names as the key, and the list of percentages for this name at each year
# E.g from 1955-1960 { Lisa : [0, 12.1, 13.8, 14.9, 14.7, 14.6], Mark : [6.7, 6.3, 8.6, 9.1, 2.4, 8.6], ... }
gender_dict = {}

# We may only be interested in the top N most popular names - in this case it's 10
topN = 10

# Now we will collect the data from the csvs we have (1 for each year from 1880-2019)
for year in years:
    
    this_years_csv = pd.read_csv(f"baby_Names/yob{year}.txt", names=column_names)
    genderfilt = this_years_csv["sex"] == "F" if use_women else this_years_csv["sex"] == "M"
    
    # Get the top N most popular male/female baby names (and then remove sex obviously
    topNgender = this_years_csv[genderfilt].head(topN).drop("sex",axis=1).set_index("name")
    
    # Get the sum so we can convert the raw quantities into percentages
    topNgendersum = topNgender["quantity"].sum()
    
    # Convert to percentages
    topNgender["quantity"] = topNgender["quantity"].apply(lambda x : x * 100 / topNgendersum)
    
    # Get the top 50 names into a set
    top50sexlist = set( topNgender.index )
    
    # Now we will generate the popularity lists
    # For a new name that appears in a time after 1880, we will need to fill the time from 1880 to the time 
    # they first appeared with 0 percent
    for person in top50sexlist:
        # percentage for the person this year
        perc = topNgender.loc[person]["quantity"]
        
        # Check if the person has appeared in the gender dict before - if not, fill in the time from 1880 to now with 0
        if gender_dict.get(person) is None:
            uptonow = [0 for _ in range(start, year)] + [perc]
            gender_dict.update({person : uptonow})
        else:
            # If they appeared before then just update their current list
            gender_dict.update({ person : gender_dict[person] + [perc] } )
            
    # Now if someone who used to be in the top 50 has fallen from it, then we will still need to update their list
    # Since they're no longer in the top 50, give them 0% 
    for person in gender_dict.keys():
        if person not in top50sexlist:
            gender_dict.update({ person : gender_dict[person] + [0] } )
            
       
fig, ax = plt.subplots(figsize=(1920*px,1080*px))

# Defining the bounds of the plot
ax.set_xlim(start,end)
ax.set_ylim(0,100) # 0-100 percent

# We don't care about the names anymore, we only needed them at the start to collate all the data into lists
# Therefore .values() will give us the lists of percentages per name, which we can use for the stackplot
values = gender_dict.values()

# We'll use this array to generate our colour scheme for each stack - the numbers will be normalised to a colourmap
colours = np.linspace(1,10**6, len(values))

import random 

# Shuffle them about so that every single stack has differently coloured neighbours
random.shuffle(colours)


# Pretty and cyclic colour map
cmap = plt.get_cmap("hsv")
norm = mcolours.Normalize(vmin = colours.min(), vmax = colours.max())

the_plot = ax.stackplot(years, 
                        values,
                        colors = cmap(norm(colours)))


ax.set_xlabel("Year" , fontsize=15)
ax.set_ylabel("Percentage of total babies born with name", fontsize=15)
ax.set_title(f"US {gender} baby names on a stackplot", fontsize=22)

# plt.savefig(f"total{gender}.png")

plt.show()

