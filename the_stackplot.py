import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy

start=1880
end = 2019
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
    
    
    
    top50women["quantity"] = top50women["quantity"].apply(lambda x : x * 100 / t50womensum)
    
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

colours=["red","blue","green","yellow","purple","brown","cyan","pink","magenta","orange"]


sorted_values_this_interval = [ [x[0],x[1][0:xintervalsize], colours[ind]] 
                                       for ind,x in enumerate(sorted(woman_dict.items(), 
                                        key=lambda dates:dates[1][0], reverse= True  )
                                       [0:topN])]


def animate(i):
    
    global sorted_values_this_interval
    
    plt.cla()
    
    year = start + i
    
    new_sorted_values_this_interval = [ [x[0],x[1][i:i+xintervalsize],None] 
                                       for x in sorted(woman_dict.items(), 
                                        key=lambda dates:dates[1][i], reverse= True  )
                                       [0:topN]]
    
    colourslist = [x[2] for x in sorted_values_this_interval]
    
    prevnames = [ x[0] for x in sorted_values_this_interval]
    nextnames = [x[0] for x in new_sorted_values_this_interval]
    
    for ind,personinfo in enumerate(sorted_values_this_interval):
        person = personinfo[0]

        if person not in nextnames:
            theircolour = personinfo[2]
            colourslist.remove(theircolour)
            

    
    for ind, personinfo in enumerate(new_sorted_values_this_interval):
        person = personinfo[0]

        if person in prevnames:
            theircolour = sorted_values_this_interval[prevnames.index(person)][2]
            
            new_sorted_values_this_interval[ind][2] = theircolour    
        
        else:
            for colour in colours:
                if colour not in colourslist:
                    new_sorted_values_this_interval[ind][2] = colour
                    colourslist.append(colour)
                    break
        

    sorted_values_this_interval = new_sorted_values_this_interval
    
    original_order = []
    

    
    for person,_ in list(woman_dict.items()):
        
        if person in nextnames:
            original_order.append(sorted_values_this_interval[nextnames.index(person)])
        
        
        
            
            
        
    

            
    
    names_this_year = [x[0] for x in original_order]
    values_this_year = [x[1] for x in original_order]
    colours_this_year = [x[2] for x in original_order]
    incoming_years = years[i:i+xintervalsize]
    
    # print(year, sorted_values_this_interval)
    # print(years[i:i+xintervalsize])
    
    ax.set_xticks(incoming_years)
    ax.set_xlim(year,year+xintervalsize-1)
    ax.set_ylim(0,100)
    
    the_plot = ax.stackplot(incoming_years, 
                            values_this_year, 
                            labels=names_this_year,
                            colors=colours_this_year)
    
    
    plt.legend(loc="upper left")

    


animation = FuncAnimation(fig, animate, interval=1000, frames = 135, repeat_delay = 10000)


plt.show()

