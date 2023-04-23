#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:42:13 2023

@author: anano
"""

#%% IMPORTING MODULES AS NEEDED

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% CLEANING THE DATASET

#I first read the dataset as csv file. Because I will be working on several vizualizations, I need to make some minor changes in the data.
#The code capitalizes the first letter of each country name in the 'countryname' column using the str.capitalize() method. 
#Next the code creates a dictionary  called replacement_dict that maps some specific country names to their corrected
#names. For example, it replaces 'Czechrep' with 'Czech Rep', 'Fyrom' with 'North Macedonia', 'Slovakia' with 'Slovak Rep', and 'Bosnia' with 'Bosnia and Herz.'.
#Finally, it replaces all the country names in the 'countryname' column of the DataFrame with their corrected names 
#using the replace() method. This method takes the replacement_dict dictionary as an argument, which maps the incorrect country names to their corrected versions.

df = pd.read_csv('cleaned_dataset2006.csv')
df['countryname'] = df['countryname'].str.capitalize()
replacement_dict = {'Czechrep': "Czech Rep", 'Fyrom': 'North Macedonia', "Slovakia": "Slovak Rep", 'Bosnia':"Bosnia and Herz."}
df['countryname'] = df['countryname'].replace(replacement_dict)
x = 0.85 #defining the weight assigned by EBRD

#%%Calculating Share of State Employment per Country

#This code first groups the dataframe by the 'countryname' column using the groupby(). 
#It then calculates the mean of the 'state_emp_now' column for each country using the mean() 
#method on the groupby object, and stores the result in a new object called state_employment_prop.
grouped_df = df.groupby('countryname')
state_employment_prop = grouped_df['state_emp_now'].mean()

#Next, it multiplies state_employment_prop by 100 and rounds the result to 2 decimal places 
#using the round() function, which creates a new object called state_employment_perc. 
#This step is converting the state employment mean from a proportion to a percentage.
state_employment_perc = round(state_employment_prop * 100, 2)
print(state_employment_perc)

#Finally, we save it as a CSV file called 'state_employment_perc.csv' using the to_csv() 
#method with index=True argument. We will use the csv file to create employment map
state_employment_perc.to_csv('state_employment_perc.csv', index=True)

#%% Comparing Democracies and Non-democracies by Share of State Employment 

#This code creates two lists of country names - non_democracies and democracies
# - which represent non-democratic and democratic countries, respectively.
#Next, we filter the state_employment_perc object by selecting only the rows corresponding
#to the non-democratic countries using .loc[non_democracies]. The resulting object is stored in 
#a new variable called non_democracies_perc. Then, we calculate the mean of the state employment 
#percentages for the non-democratic countries using .mean(), and round the result to two decimal places using round(). T
#the resulting mean percentage is stored in a variable called mean_perc_n.

non_democracies = ['Belarus', 'Russia', 'Bosnia and Herz.', 'Armenia', 'Azerbaijan', 'Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan']
non_democracies_perc = state_employment_perc.loc[non_democracies] # filtering the state employment percentages for the non-democratic countries
mean_perc_n = non_democracies_perc.mean() # calculating the mean percentage
mean_perc_n = round(mean_perc_n, 2)
print(mean_perc_n)

#I perfrom the above-described method on democratic countries

democracies = ['Albania', 'Bulgaria', 'Croatia', 'Czech Rep', 'Estonia', 'Georgia','Hungary', 'Latvia', 'Lithuania', 'North Macedonia', 'Moldova' ,'Montenegro', 'Poland', 'Romania', 'Serbia', 'Slovak Rep', 'Slovenia', 'Ukraine']
democracies_perc = state_employment_perc.loc[democracies] # filtering the state employment percentages for the non-democratic countries
mean_perc_d = democracies_perc.mean() # calculating the mean percentage
mean_perc_d = round(mean_perc_d, 2)
print(mean_perc_d)

#%% Share of State Benefits 
#After calculating the share of public employment per country, we move on to calculate the percentage
#of sample that depends on state-provided assistance.

state_assistance_prop = grouped_df['state_assistance'].mean()
state_assistance_perc = round(state_assistance_prop * 100, 2)
print(state_assistance_perc)

#%% **State Employment Comparison by Country Type**

plt.rcParams['font.family'] = 'Times New Roman'
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=['Non-Democratic Countries', 'Democratic Countries'], y=[mean_perc_n, mean_perc_d], ax=ax, palette=['orange', 'red'], alpha=0.7)
ax.set(title='Average Percentage of State-Employed People by Country Type', xlabel='Country Type', ylabel='Percent Employed in Public Sector ')
plt.ylim(0, max(mean_perc_n, mean_perc_d) + 5)

# add values to the bars
for i, v in enumerate([mean_perc_n, mean_perc_d]):
    ax.text(i, v + 1, str(v), ha='center', fontweight='bold', fontsize=12)

# save the figure
plt.savefig('state_employment_comparison.png', dpi=300, bbox_inches='tight') 
plt.show()

#%%  "State Employment Share vs. State Assistance Share in Post-Communist Europe and Central Asia"

#This scatter plot shows the relationship between the average percentage of people receiving 
#state assistance and the average percentage of state employment for each country in Post-Communist
#Europe and Central Asia.

plt.rcParams['font.family'] = 'Times New Roman' #I choose a font for our scatterplot
plt.scatter(state_assistance_perc, state_employment_perc) #I use the scatter() function from the matplotlib library 
#to plot a set of (x, y) points. In this case, the x-axis values are the average percentage of people 
#receiving state assistance and the y-axis values are the average percentage of state employment for each country in the dataset
plt.xlabel('Average Percent of People Receiving State Assistance', fontsize = 10)
plt.ylabel('Avrage Percent of State Employment', fontsize = 10)
plt.title('State Employment Share vs. State Assistance Share\nin Post-Communist Europe and Central Asia', fontsize=12)

#I use the enumerate() function to loop through the keys of the grouped_df.groups dictionary, 
#which contains the unique country names in the countryname column of the df dataframe. For each country, 
#the loop variable i stores its index in the state_assistance_perc and state_employment_perc arrays, 
#which were created by grouping and aggregating the data in the df.
for i, country in enumerate(grouped_df.groups.keys()):
    plt.text(state_assistance_perc[i], state_employment_perc[i], country, fontsize=4)

plt.grid(False)# I remove gridlines
plt.savefig('state_employment_vs_assistance.png', dpi=300)
plt.show()

#%%  Calculating Share of State-Employment in Middle Class in whole sample

grouped_df = df.groupby('countryname')[['MiddleClass', 'state_emp_middleclass']].sum()
state_emp_mc_share = grouped_df['state_emp_middleclass'] / grouped_df['MiddleClass']*x
print(state_emp_mc_share)

#%% Calculating Mean Share of State-Employment in Middle Class for Non Democracies
nondemocracies_emp_mc_share = state_emp_mc_share.loc[non_democracies]
mean_share_nondems= nondemocracies_emp_mc_share.mean() # calculating the mean percentage
mean_share_nondems = round(mean_share_nondems, 2)
print(mean_share_nondems)

#%% Calculating Mean Share of State-Employment in Middle Class for Democracies
democracies_emp_mc_share = state_emp_mc_share.loc[democracies]
mean_share_dems= democracies_emp_mc_share.mean() # calculating the mean percentage
mean_share_dems = round(mean_share_dems, 2)
print(mean_share_dems)



