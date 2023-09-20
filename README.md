# usbabynames

The goal of this repos is to visualise using a stackplot the change over time of the most popular US baby names from 1880 to 2019 to see what insights we can find. 
These are segregated between male baby names and female baby names. I wanted to use a stackplot since I haven't used these in any prior visualisations and 
I thought it'd be the most visually insightful graphic, if a little plain.
The source of the data can be found here: https://www.kaggle.com/datasets/kaggle/us-baby-names

I've made 2 main programs for this purpose:

**alltime_plot.py** 
This program creates a stackplot from 1880 to 2019 of the most popular US baby names. Due to the sheer number of names, more so with females than males, it's impossible to give labels,
but here the focus is less on the exact most popular names (the animated plot does this) and more on the _distribution_ of names over time - the more densely packed the lines are 
together, the more variation in baby names over that region of time and vice versa. The y-axis is the percentage of total US male/female baby names - e.g if a bar goes from 20 to 50
on the y-axis, then it means that 30% of baby names of that gender would be that name.

I noticed here that female baby names have much greater variation than their male counterparts - this can be seen both in the density of lines and colours in the female plot compared
to the male one, and also in the significantly greater filesize of the female plot animation compared to the male one (approx. 9KB vs 7KB respectively). As to why, I speculate that 
there's more acceptance of differences in female names compared to male ones. To support this theory, look at the animated plot; most of the most popular female names in the 1880s-1960s 
have completely vanished from selection in the 2010s, but the equivalent most popular male ones are still in common use today (albeit at a reduced rate of selection).

**animated_plot.py**
This program creates an animation of the top 10 most popular male/female baby names in the US. The x-axis, but it only shows an interval of 5 years, and the year increases
with time instead of showing it all at once. This makes it much easier to see names and their growth/decline rates, and labels for the top 10 names have been added, along with their
positions from 1st to 10th. The y-axis has a key difference - instead of showing the percentage of *all* US baby names for that gender for a given stack, it instead shows the percentage
of all *top 10* US baby names, instead of all baby names altogether. This is a key difference, meaning that the sum of all stack plots for a given year should sum to 100%. 

I chose this axis type because if I had selected the percentage of all US baby names as I had done in *alltime_plot*, then the entire stack plot would be very small and hard to read, since
even the accumulated top 10 names are usually only a small fraction of the total US names, reflecting much greater diversity in name selection. I also made the choice to recycle colours
for names - e.g when a name drops out of the top 10, its colour may then be used for the *next* new top 10 name in its place. 

In the videos, it can be seen that sometimes the sum of the stacks in parts of the plot does not add up to 100%, leaving a white space at the top of the plot. This is **NOT a bug**. The
reason this happens is because my program considers the top 10 baby names on the first point of the x-axis, which is the given year. For the 5 years after this point, new baby names will 
have entered the top 10, but are not shown because they aren't in the top 10 *yet* since the plot hasn't reached that year yet. The result is white space where these new baby names will be
once they reach that year. This is good because it shows the decline in baby names and only shows names once they actually reach the top 10.

Since the data only covers every year, animating it by itself would create a very jagged animation. Hence, I used 50x linear interpolation to increase the frame rate to 50FPS so the videos
would look smooth and pleasant to look at. I could've used Pandas to do this but it was easier to make my own minifunction since I didn't want to play around with datetimes where it was not 
necessary and such datetimes were not present in the original dataset (since there's one dataset per year, they didn't include any time column).

I also made another program, **prettyplot.py**. This is just to use the data to create visually appealing images out of the data, which was made in babymale.png and babyfemale.png. 
Finally, I had to delete the gifs that I made (I converted them into mp4s) in previous git versions since they were too large to upload to Github in one go. 

