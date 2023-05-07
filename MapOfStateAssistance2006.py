#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

#%%Read the CSV file into a Pandas dataframe

#In this code, I am importing 'state_assistance_perc.csv' created in earlier script. Than, I make change column and value country names to match 
#with names of shape file I will use later in the script

state_assistance_perc = pd.read_csv('state_assistance_perc.csv')
state_assistance_perc["countryname"] = state_assistance_perc["countryname"].str.capitalize()
replacement_dict = {'Czech rep': "Czech Rep", 'North macedonia': 'North Macedonia', "Slovak rep": "Slovak Rep", 'Bosnia and herz.':"Bosnia and Herz."}
state_assistance_perc['countryname'] = state_assistance_perc['countryname'].replace(replacement_dict)
state_assistance_perc = state_assistance_perc.rename(columns={'countryname': 'name'})


#%%CREATING A MAP

#In this code, I load a shapefile of world countries using GeoPandas, selects only certain columns of interest,
# and defines a list of countries in Eurasia that were formerly part of the USSR or had post-communist governments.

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
replacement_dict = {'Czechia': "Czech Rep",  "Slovakia": "Slovak Rep"}
world['name'] = world['name'].replace(replacement_dict)
world = world[['name', 'continent', 'geometry', 'pop_est', 'gdp_md_est']]
ex_communist_eurasia = ['Albania', 'Bulgaria', 'Croatia', 'Czech Rep', 'Estonia', 'Georgia','Hungary', 
                        'Latvia', 'Lithuania', 'North Macedonia', 'Moldova' ,'Montenegro', 'Poland', 'Romania', 
                        'Serbia', 'Slovak Rep', 'Slovenia', 'Ukraine', 'Belarus', 'Russia', 'Bosnia and Herz.', 
                        'Armenia', 'Azerbaijan', 'Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan']
    
#%% In this part of the code, I create variable 'eurasia' that contains geometry and necassary variables
#of the countries of interest. After that, manipulate projections to fit all selected countries on the map in the right position.
#To do that, I define proj_lcc. Thus is a string that defines the Lambert Conformal Conic projection with specific parameters, 
#which will be used to project the map to a different coordinate reference system.

eurasia = world[world['name'].isin(ex_communist_eurasia)]
proj_lcc = '+proj=lcc +lat_1=30 +lat_2=60 +lat_0=55 +lon_0=90'
eurasia_proj = eurasia.to_crs(proj_lcc)



# I plot the map to check if all went well 

colors = plt.cm.Set1(range(len(eurasia)))
ax = eurasia_proj.plot(figsize=(10, 10), column='name', cmap='Greys', edgecolor='black', linewidth=0.5)
ax.set_title('Post-Communist Countries in Europe and Central Asia')
ax.set_facecolor('white')  # setting the background color to white
ax.set_axis_off()  # hidding the axis lines and labels


#%% Next, I merge stata_assistance_perc dataframe to the shapefile

merged_data = eurasia_proj.merge(state_assistance_perc, on='name', how='left', indicator=True)
print(merged_data["_merge"].value_counts())

#%% Creating heatmap

fig, ax = plt.subplots(figsize=(10, 10))
merged_data.plot(column='state_assistance', legend=True, ax=ax, cmap='Blues')
ax.set_title('Share of State Provided Assistance in\n26 Post-Communist Countries in Eurasia', fontsize=16)
ax.set_axis_off()  # Hide the axis lines and labels
# Add country names as annotations
for i, country in enumerate(merged_data['name']):
    centroid = merged_data[merged_data['name'] == country]['geometry'].centroid
    ax.annotate(i+1, xy=(centroid.x, centroid.y), ha='center', fontsize=8)

# Add legend with numbers and corresponding country names
legend_elements = []
for i, country in enumerate(merged_data['name']):
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', label=f"{i+1}. {country}", markerfacecolor='blue', markersize=8))
ax.legend(handles=legend_elements, title='Countries', fontsize=9, bbox_to_anchor=(0.54, 0.37), ncol=4, loc='upper center', borderaxespad=15, frameon=False)  
plt.savefig('Heatmap_map_assistance.png', dpi=300)  # Save plot with 300 dpi resolution
