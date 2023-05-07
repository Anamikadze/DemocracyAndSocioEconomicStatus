#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:36:40 2023

@author: anano
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 09:01:12 2023

@author: anano
"""
#%% IMPORTING NECESSARY MODULES

import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

#%%
#In this code, I load a shapefile of world countries using GeoPandas, selects only certain columns of interest,
# and defines a list of countries in Eurasia that were formerly part of the USSR or had post-communist governments.

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[['name', 'continent', 'geometry', 'pop_est', 'gdp_md_est']]
replacement_dict = {'Czechia': "Czech Rep",  "Slovakia": "Slovak Rep"}
world['name'] = world['name'].replace(replacement_dict)


#defining ex communist countries in Europe and Central Asia. The list unites 15 ex USSR republics
#and post-communist countries in Europe and Central Asia
ex_communist_eurasia = ['Albania', 'Bulgaria', 'Croatia', 'Czech Rep', 'Estonia', 'Georgia','Hungary', 
                        'Latvia', 'Lithuania', 'North Macedonia', 'Moldova' ,'Montenegro', 'Poland', 'Romania', 
                        'Serbia', 'Slovak Rep', 'Slovenia', 'Ukraine', 'Belarus', 'Russia', 'Bosnia and Herz.', 
                        'Armenia', 'Azerbaijan', 'Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan']


#%%manipulate russia's geometry

#%% In this part of the code, I create variable 'eurasia' that contains geometry and necassary variables
#of the countries of interest. After that, manipulate projections to fit all selected countries on the map in the right position.
#To do that, I define proj_lcc. Thus is a string that defines the Lambert Conformal Conic projection with specific parameters, 
#which will be used to project the map to a different coordinate reference system.

eurasia = world[world['name'].isin(ex_communist_eurasia)]

proj_lcc = '+proj=lcc +lat_1=30 +lat_2=60 +lat_0=55 +lon_0=90'
eurasia_proj = eurasia.to_crs(proj_lcc)

colors = plt.cm.Set1(range(len(eurasia)))

# Plot the initial map

ax = eurasia_proj.plot(figsize=(10, 10), column='name', cmap='Set1', edgecolor='black', linewidth=0.5)
ax.set_title('Post-Communist Countries in Europe and Central Asia')
ax.set_facecolor('white')  # setting the background color to white
ax.set_axis_off()  # hidding the axis lines and labels

#%%Merging state employment percentages into shapefile

state_employment_perc = pd.read_csv('state_employment_perc.csv')
state_employment_perc = state_employment_perc.rename(columns={'countryname': 'name'})
merged_data = eurasia_proj.merge(state_employment_perc, on='name', how='left', indicator=True)
print(merged_data["_merge"].value_counts())

#%% Creating heatmap

fig, ax = plt.subplots(figsize=(10, 10))
merged_data.plot(column='stateemployment', legend=True, ax=ax, cmap='Reds')
ax.set_title('Share of Public Employment in\n27 Post-Communist Countries in Europe and Central Asia', fontsize=16)
ax.set_axis_off()  # Hide the axis lines and labels
# Add country names as annotations
for i, country in enumerate(merged_data['name']):
    centroid = merged_data[merged_data['name'] == country]['geometry'].centroid
    ax.annotate(i+1, xy=(centroid.x, centroid.y), ha='center', fontsize=8)

# Add legend with numbers and corresponding country names
legend_elements = []
for i, country in enumerate(merged_data['name']):
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', label=f"{i+1}. {country}", markerfacecolor='orange', markersize=8))
ax.legend(handles=legend_elements, title='Countries', fontsize=9, bbox_to_anchor=(0.54, 0.37), ncol=4, loc='upper center', borderaxespad=15, frameon=False)  
plt.savefig('Heatmap_Emp.png', dpi=300)  # Save plot with 300 dpi resolution

