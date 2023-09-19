import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

start=1880
end = 2015
years = list(range(start,end+1))

column_names = ["name","sex","quantity"]

men_dict = {}
woman_dict = {}
topN = 10

for year in years:
    
    this_years_csv = pd.read_csv(f"baby_Names/yob{year}.txt", names=column_names)
    
    womanfilt = this_years_csv["sex"] == "F"
    
    top50women = this_years_csv[womanfilt].head(topN).drop("sex",axis=1).set_index("name")
    t50womensum = top50women["quantity"].sum()
    
    top50men = this_years_csv[~womanfilt].head(topN).drop("sex",axis=1).set_index("name")
    
    
    
    top50women["quantity"] = top50women["quantity"].apply(lambda x : np.round( x * 100 / t50womensum, decimals=2))
    
    top50womenlist = set( top50women.index )
    

    
    for woman in top50womenlist:
        perc = top50women.loc[woman]["quantity"]
        if woman_dict.get(woman) is None:
            uptonow = [0 for _ in range(start, year)] + [perc]
            woman_dict.update({woman : uptonow})
        else:
            woman_dict.update({ woman : woman_dict[woman] + [perc] } )
            
    for woman in woman_dict.keys():
        if woman not in top50womenlist:
            woman_dict.update({ woman : woman_dict[woman] + [0] } )
            
fig, ax = plt.subplots()

ax.set_ylim(0,100)

xintervalsize = 5

colours=["red","blue","green","yellow","purple"]


sorted_values_this_interval = [ (x[0],x[1][0:xintervalsize]) 
                                       for x in sorted(woman_dict.items(), 
                                        key=lambda dates:dates[1][0], reverse= True  )
                                       [0:topN]]

people_colours = list(zip([ x[0] for x in sorted(woman_dict.items(), 
                        key=lambda dates:dates[1][0], reverse= True  )
                        [0:topN]], colours))

def animate(i):
    
    global sorted_values_this_interval
    
    plt.cla()
    
    year = start + i
    
    sorted_values_this_interval = [ (x[0],x[1][i:i+xintervalsize]) 
                                       for x in sorted(woman_dict.items(), 
                                        key=lambda dates:dates[1][i], reverse= True  )
                                       [0:topN]]
    

            
    
    names_this_year = [x[0] for x in sorted_values_this_interval]
    values_this_year = [x[1] for x in sorted_values_this_interval]
    incoming_years = years[i:i+xintervalsize]
    
    # print(year, sorted_values_this_interval)
    # print(years[i:i+xintervalsize])
    
    ax.set_xticks(incoming_years)
    ax.set_xlim(year,year+xintervalsize-1)
    ax.set_ylim(0,100)
    
    the_plot = ax.stackplot(incoming_years, 
                            values_this_year, 
                            labels=names_this_year,
                            colors=colours)
    
    
    plt.legend(loc="upper left")

    


animation = FuncAnimation(fig, animate, interval=100, frames=100)


plt.show()

