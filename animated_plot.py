import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# The goal of this program is to create a stackplot, animated over time, of the top 10 male/female baby names in the US from 1880 to 2019
# I chose a stackplot because it's a good way to visualise and analyse both the changes of names and the rate of change - the most 
# common observation is that female baby names change much more often than male ones.

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
            
# Given a number (integer presumably), return it as a string + the corresponding suffix for the number
# This is used for ranking the baby names in the plot animation
def number_suffix(num):
    strnum = str(num)
    
    # These are the "odd suffixes out" - since they all have the same use cases I just put them in a list to avoid repeating code
    one_two_three_suffixes = ["st","nd","rd"]
    
    # It's based on the last and second-to-last digits
    lastdigit = int( strnum[-1])
    # 1,2,3 are the odd numbers out
    if lastdigit in [1,2,3]:
        # The exception is 11/12/13, which all end in "th", while all others end in the special suffixes
        if len(strnum) >= 2 and strnum[-2] == "1":
            return strnum + "th"
        else:
            # If not the exception, give the corresponding special suffix
            return strnum + one_two_three_suffixes[lastdigit-1]
        
    # Otherwise, if not ending in 1,2,3, it's always going to end in "th"
    return strnum + "th"
        
# Interpolation extent - factor by which you want to increase the number of frames
# interpolation extent of 50 = 50 times more frames than before (actually not quite 50 due to endpoint not being extended)
# This also governs the fps - interpolation extent of 50 = the video produced will be 50 FPS
interpolation_extent = 50
            
# Function to perform linear interpolation on a list of numbers - used in interpolating the frames
# I could've used pandas but it's not time-series date so a resampling would've taken too much code
# easier to make a smaller function for it like this
def interpolate_list(arr, extent):
    
    # This array will store the result after interpolation
    new_arr = []
    
    # Now we will loop through each element in the array and generate the new values
    for i in range(0,len(arr)-1):
        
        # The new values inbetween the original ones - hence start with the first original number
        new_numbers = [arr[i]]
        
        # This loop will generate the interpolated values 
        for j in range(1,extent):
            # This is just the interpolation formula
            diff = (arr[i+1]-arr[i]) * (j/extent)
            new_numbers.append(arr[i] + diff)
        
        # Now send all of these numbers to the new array
        new_arr.extend(new_numbers)
    
    # Don't forget to add the last number at the end since this won't have been added in interpolation
    new_arr.append(arr[-1])        
    
    # new length = extent * len(original array) - (extent-1)
    return new_arr

# Interpolating all our data
for person in list( gender_dict.keys() ):
    gender_dict[person] = interpolate_list( gender_dict[person] , interpolation_extent )

years = interpolate_list(years,interpolation_extent)

# It's plotting time        
fig, ax = plt.subplots(figsize=(1920*px,1080*px))

# Will go from 0 to 100 percent
ax.set_ylim(0,100)

# I wanted to show the next 5 years since much shorter or longer would've have been relevant
xintervalsize = 5*interpolation_extent

# These are the 10 colours we will use for each name in the stackplot - I chose them at will
# These names will be given and then recycled whenever a new name becomes top 10
# I needed to have control over the colours to prevent the same colour from being given to adjacent stacks
colours=["red","blue","green","yellow","purple","brown","cyan","pink","magenta","orange"]

# Sort the names by their 1880 amounts and get the biggest 10 - we need to have an initial list for our animation 
# since the colours will be recycled - x[0] is the name, x[1] is the list of quantities, x[2] is the colour that represents that name
sorted_values_this_interval = [ [x[0],x[1][0:xintervalsize], colours[ind]] 
                                       for ind,x in enumerate(sorted(gender_dict.items(), 
                                        key=lambda dates:dates[1][0], reverse= True  )
                                       [0:topN])]

# The function that will trigger every frame
def animate(i):
    
    # We'll need to have access to both the old list and the new list so we can transfer important info over
    global sorted_values_this_interval
    
    # Don't want to accumulate plots or it'll become very slow very fast
    ax.cla()
    
    # Get the current year - the greater our interpolation, the more frames and the slower time will go
    year = start + i/interpolation_extent
    
    # Get the new list, finding the top 10 names for the given year - the indices mean the same as before
    # For reasons we will see shortly, we need to have both the old and the new values (then the new becomes the old at the end)
    new_sorted_values_this_interval = [ [x[0],x[1][i:i+xintervalsize],None] 
                                       for x in sorted(gender_dict.items(), 
                                        key=lambda dates:dates[1][i], reverse= True  )
                                       [0:topN]]
    
    # Get the colours that were used in the previous frame so we can carry them over to this frame
    # These are still implicitly linked to the names via their ordering 
    colourslist = [x[2] for x in sorted_values_this_interval]
    
    # Names for previous frame, and names for this frame - again, implicit ordering holds
    prevnames = [x[0] for x in sorted_values_this_interval]
    nextnames = [x[0] for x in new_sorted_values_this_interval]
    
    # If there was someone in the top 10 the last frame but no longer in the top 10, we need to remove their colour from the colourlist
    # This is done so that when removed, we can rededicate this colour to the next top10 person 
    for ind,personinfo in enumerate(sorted_values_this_interval):
        person = personinfo[0]

        if person not in nextnames:
            theircolour = personinfo[2]
            colourslist.remove(theircolour)
            

    # This loop will give people who were in the previous frame the same colours in the new frame (assuming they're still top 10)
    # and then provide colours to new top 10 people, recycled from the people who stopped being top 10 in the last frame
    for ind, personinfo in enumerate(new_sorted_values_this_interval):
        person = personinfo[0]

        if person in prevnames:
            # Give them back their old colour
            theircolour = sorted_values_this_interval[prevnames.index(person)][2]
            new_sorted_values_this_interval[ind][2] = theircolour    
        
        # New top 10 arrivals
        else:
            # Filter through the colour list and give them the first available colour 
            # Available colours will be in the list of colours (originally specified outside this function) but NOT in the colourslist
            for colour in colours:
                if colour not in colourslist:
                    # Once colour is found, add to the list of colours and break since we've found a colour we can use
                    new_sorted_values_this_interval[ind][2] = colour
                    colourslist.append(colour)
                    break
        
    # Once we've carried the colours over, we have no further use for the previous frame, so now set the new list to be the current one
    # which will then become the old one in the next frame and so on...
    sorted_values_this_interval = new_sorted_values_this_interval 
    
    # The problem with this new list is that it's sorted specifically by how popular they are, not by their original order in the gender_dict
    # This means that the biggest stack will always be on the bottom, then the next biggest, and so on until the smallest is at the top
    # And that means that every time a name becomes more popular than another, their stacks will instantly switch positions on the plot
    # This is very jerky and ugly to look at, so we need to always preserve the original order of the names as given in the dict to avoid this
    # This list will be the same as new_sorted_values_this_interval but preserve the original ordering of the names
    original_order = []    
    
    # To retrieve the original order, iterate through the dict until you find their name, then add them, doing this for the entire dict
    # Eventually all the names in sorted_values_this_interval will be found and placed into the list
    for person,_ in list(gender_dict.items()):
        if person in nextnames:
            # Remember that the nextnames list is order-linked to sorted_values_this_interval, allowing us to just use the index method 
            # to find its position in the original list without having to manually loop through to find it
            index_of_person = nextnames.index(person)
            original_order.append(sorted_values_this_interval[index_of_person])
        
        
        
            
            
        
    

            
    # Get all the relevant data to plot our stackplot
    names_this_year = [x[0] for x in original_order]
    values_this_year = [x[1] for x in original_order]
    colours_this_year = [x[2] for x in original_order]
    incoming_years = years[i:i+xintervalsize]
    
    # Don't want our x-axis to have decimal year values
    the_current_year = int(year)
    ax.set_xticks(list(range(the_current_year, the_current_year+xintervalsize//interpolation_extent)))
    
    # Define the bounds of the plot - this is made slightly more complicated by interpolation since it increases the density of the x-axis
    ax.set_xlim(year,year+(xintervalsize-1*interpolation_extent)/interpolation_extent)
    ax.set_ylim(0,100)
    
    # It's plotting time
    the_plot = ax.stackplot(incoming_years, 
                            values_this_year,  # Want to add the position of each name to make it clearer
                            labels=[ x + " (" + number_suffix(1 + nextnames.index(x)) + ")" for x in names_this_year ],
                            colors=colours_this_year)
    
    
    ax.set_xlabel("Year",fontsize=15)
    ax.set_ylabel(f"Percentage of top {topN} {gender} baby names",fontsize=15)
    ax.set_title(f"Top 10 most popular US {gender} baby names in {the_current_year}", fontsize=22)
    plt.legend(loc="upper left")

animation = FuncAnimation(fig, animate, interval=1000/interpolation_extent, frames = 131* interpolation_extent, repeat_delay = 10000)

animation.save(f"{gender}babynamesfps1.gif")

#plt.show()

