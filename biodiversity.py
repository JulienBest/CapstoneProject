
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[4]:


from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[5]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[6]:


species.head(10)


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[7]:


print(species.scientific_name.nunique())


# What are the different values of `category` in `species`?

# In[8]:


for animal in species.category.unique():
    print(animal)


# What are the different values of `conservation_status`?

# In[9]:


for val in species.conservation_status.unique():
    print(val)


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[10]:


species.groupby('conservation_status').scientific_name.nunique().reset_index()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[11]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[12]:


species.groupby('conservation_status').scientific_name.nunique().reset_index()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[13]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[14]:


plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),
        protection_counts.scientific_name)

ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status)
plt.title('Conservation Status by Species')
plt.ylabel('Number of Species')
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[15]:


species['is_protected'] = species.conservation_status.values != 'No Intervention'


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[16]:


category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[17]:


category_counts.head(14)


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[27]:


category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[28]:


category_pivot.head(10)


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[30]:


category_pivot.columns =['category', 'not_protected', 'protected']


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[34]:


category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)


# Examine `category_pivot`.

# In[35]:


category_pivot.head(10)

#own analysis:

percent_protected_list = [8.8608,15.3689,8.7302,17.0455,1.5015,6.4103,1.0793]
names = ['Amphibian', 'Bird', 'Fish', 'Mammal', 'Nonvascular Plant', 'Reptile', 'Vascular Plant']
plt.pie(percent_protected_list, labels=names, autopct = '%0.001f')
plt.show()


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[36]:


contingency = [[30, 146],[75, 413]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[37]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[38]:


chi2_contingency(contingency)


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[42]:


contingency = [[30, 146], [5, 73]]
chi2_contingency(contingency)


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[47]:


observations = pd.read_csv('observations.csv')
observations.head(10)


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[1]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[2]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[53]:


species['is_sheep'] = species.common_names.apply(lambda x:'Sheep' in x)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[54]:


species[species.is_sheep]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[55]:


sheep_species = species[(species.is_sheep == True)&(species.category == 'Mammal')]


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[57]:


sheep_observations = pd.merge(observations, sheep_observations)
sheep_observations.head()


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[66]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[78]:


plt.figure(figsize=(16,4))
ax= plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name)
plt.title('Observations of Sheep per Week')
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[81]:


minimum_detectable_effect =(0.05 / 0.15)*100
print(minimum_detectable_effect)

sample_size = 870 #I used the calculator of codecademy


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[82]:


bryce = 870 / 250.
yellowstone = 870 / 507.

# Roughly 3 weeks at Bryce and 1 + 1/2 week at Yellowstone.


# In[192]:


# Own analysis
import numpy as np
Mammals_no_intervention = species[(species.category=='Fish')&(species.conservation_status == 'In Recovery')].count().reset_index()
print(Mammals_no_intervention)


# In[217]:



conservation = species.conservation_status.unique()
print(conservation)
no_intervention = [176, 442, 74, 73, 116, 4424, 328]
species_of_concern = [28,72,5,4,4,43,5]
endangered = [7,4,0,1,3,1,0]
threatened = [2,0,0,2,4,2,0]
in_recovery = [1,3,0,0,0,0,0]
plt.figure(figsize=(20,15))
ax= plt.subplot()
x = range(len(no_intervention))
plt.bar(x,no_intervention)
plt.bar(x, species_of_concern, bottom=no_intervention, color = 'orange', label = 'Species Of Concern')
plt.bar(x, endangered, bottom = np.add(no_intervention, species_of_concern),color = 'green', label = 'Endangered')
plt.bar(x, threatened, bottom = np.add(np.add(no_intervention, species_of_concern), endangered),color = 'red', label = 'Threatened')
plt.bar(x, in_recovery, bottom = np.add(np.add(np.add(no_intervention, species_of_concern), endangered), threatened), color = 'yellow', label = 'In Recovery')
x_labels = ['Error','Mammal','Bird','Reptile','Amphibian','Fish','Vascular Plant','Nonvascular Plant']
ax.set_xticklabels(x_labels)
plt.legend()
plt.ylabel('Number of Animals')
plt.show()



# In[216]:


plt.figure(figsize=(20,15))
ax2 = plt.subplot()
plt.bar(x, species_of_concern, color = 'orange', label = 'Species Of Concern')
plt.bar(x, endangered, bottom= species_of_concern, color = 'green', label = 'Endangered')
plt.bar(x, threatened, bottom = np.add(species_of_concern,endangered),color='red', label = 'Threatened')
plt.bar(x, in_recovery, bottom = np.add(np.add(species_of_concern,endangered), threatened),color = 'yellow', label = 'In Recovery')
ax2.set_xticklabels(x_labels)
plt.legend()
plt.ylabel('Number of Animals')

