#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:58:12 2023

@author: anano
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 12:04:46 2023

@author: anano
"""
#Importing necassary modules

import numpy as np
import pandas as pd 

#%% Merging original CSV files and pre-processing the data

#The data comes in several seperate csv files. This code reads four CSV files 
#named "LITS2006_1.csv", "LITS2006_2.csv", "LITS2006_3.csv", and "LITS2006_5.csv" 
#using Pandas read_csv function, and stores each of them as a DataFrame object named 
#"df1", "df2", "df3", and "df4", respectively. #Then, the code merges the DataFrames 
#using the merge() function, joining them on their common index column using the 
#left_index and right_index arguments. The merge() function is called four times, 
#merging the DataFrames in pairs, and finally creating a merged DataFrame named 
#"merged_df" that contains all the columns from the original DataFrames

df1 = pd.read_csv("LITS2006_1.csv") #Opening csv file 
df3 = pd.read_csv("LITS2006_3.csv") #Opening csv file 
df2 = pd.read_csv("LITS2006_2.csv") #Opening csv file 
df4 = pd.read_csv("LITS2006_5.csv") #Opening csv file 

merged1_df = df1.merge(df2, left_index=True, right_index=True)
merged2_df = merged1_df.merge(df3, left_index=True, right_index=True)
merged_df = merged2_df.merge(df4, left_index=True, right_index=True)

print(len(merged_df)) #Checking the length of the dataframe

#The first line of this code sets the index of the DataFrame "merged_df" to 
#the column "countryname" using the set_index() method. 
#For future convenience, "countryname" column will become the new index of the
#DataFrame, and the original index will be discarded
filtered_df = merged_df.set_index('countryname')
 
# I remove Turkey and Mongolia from the sample 
filtered_df = filtered_df.drop(index=['turkey', 'mongolia'])

#%% Exploring Data

#This part of the code is not necassary for cleaning the data. However, it gives
#a good sense of what we are working with

print(len(filtered_df))
value_counts = filtered_df['q602b2a'].value_counts() #types of employments
print(value_counts)
val_statemp = filtered_df['q602b3a1'].value_counts(dropna=False) #state owned versus not state owned job

#georgia_df = filtered_df.loc[filtered_df.index == 'georgia']
#al_statemp_geo = georgia_df['q602b3a1'].value_counts(dropna=False) #shows number of state employed, private employed and NAs
#for Georgia only
val_statemp_education = filtered_df['q501'].value_counts(dropna=False) 
val_statemp_occupation = filtered_df['q405a'].value_counts(dropna=False)
filtered_df['q501'].value_counts(dropna=False)
counts = filtered_df['q602b1a'].value_counts(dropna=False)



#%% BUILDING NEW DATASET - The purpose of this script is to create dependent, independent 
#and control variables for the future analysis. Detailed information about
#nature, structure and type of those variables can be found in README file

clean_df = pd.DataFrame(index=filtered_df.index) #creating new dataframe that has the same index as filtered dataframe

#Creating dependent variable for state employment. State employment variable that I use in the analysis 
#takes a value of one if an individual has been employed in the state sector and 0 otherwise

clean_df['state_emp_now'] = filtered_df['q602b3a1'].apply(lambda x: 1 if x == 1 else 0) 
clean_df['state_emp_now'].value_counts(dropna=True) #counting values in state employment

#'state_emp_now' variable only gives general information about employment type. Below, I am creating seperate 
#variables for state employed educators, health professionals and persons directly involved in public administartion.
clean_df['occupation'] = filtered_df['q602b2a']

#Adding state educators column
clean_df['public_educators'] = clean_df.apply(lambda row: 1 if row['state_emp_now'] == 1 and row['occupation'] 
                                              == 'education' else 0 if not pd.isna(row['state_emp_now']) and not
                                              pd.isna(row['occupation']) else np.nan, axis=1)
#Adding state health professionals column
clean_df['public_health_professionals'] = clean_df.apply(lambda row: 1 if row['state_emp_now'] == 1 and row['occupation'] 
                                              == 'health and health work' else 0 if not pd.isna(row['state_emp_now']) and not
                                              pd.isna(row['occupation']) else np.nan, axis=1)
#Adding state career as column
clean_df['state_career'] = clean_df['occupation'].apply(lambda x: 1 if x == 'public administration, military, social security' else 0 if not pd.isna(x) else np.nan)

#%% Building Dependent Variable - Democracy

#Adding column called 'DemocracySupport' which equals 1 if value of q311 of filtered_df = democracy preferable and 0 otehrwise
clean_df['DemocracySupport'] = filtered_df['q311'].apply(lambda x: 1 if x == 'democracy preferable' else (np.nan if pd.isna(x) else 0))
cols = ['q312_1', 'q312_3', 'q312_6', 'q312_7', 'q312_5', 'q312_2', 'q312_9'] #colums of dataframe about institutions
#InstitutionalSupport is binary variable that equals to 1 if if values of q312_1, q312_3, q312_6, q312_7, q312_5, q312_2, q312_9 of filtered_df equal to 'strongly agree' and 0 otherwise
clean_df['InstitutionSupport'] = (filtered_df[cols].isin(['strongly agree', 'agree'])).all(axis=1).astype(int)
clean_df['Democracy'] = np.where((clean_df['DemocracySupport'] == 1) & (clean_df['InstitutionSupport'] == 1), 1, 0)
clean_df['Democracy'] = clean_df['Democracy'].where((~clean_df['Democracy'].isna()), np.nan)
clean_df['Democracy'].value_counts(dropna=False)

#%% Building Independent Variable - Middle Class

#This code creates binary variable called Education that equals 1 if 
#filtered_df['q501'] has value of professional education, higher or post grad and 0 otherwise
conditions = [filtered_df['q501'].isin(['higher professional degree (university, college)', 'post graduate degree']),
    filtered_df['q501'].isna()]
choices = [1, np.nan]
clean_df['Education'] = np.select(conditions, choices, default=0)
clean_df['Education'].value_counts(dropna=False)


#This code creates binary variable called Occupation that equals to 1 if value of
#q405 of dataframe filtered_df equals to 'professionals' or 'technicians and 
#associated professionals' (any of those) and 0 otherwise. 
clean_df['Occupation'] = filtered_df['q602b1a'].apply(lambda x: 1 if x in 
                                                    ['professionals', 'technicians and associated professionals', 'legislator, senior official, manager']
                                                    else 0 if pd.notna(x) else np.nan)
clean_df['Occupation'].value_counts(dropna=False)


#This code creates binary variable called MiddleClass that equals 1 if both 
#Education and Occupation equals , ) if either Education or Occupation = 0 and keeps missing values as Nans
conditions = [(clean_df['Occupation'] == 1) & (clean_df['Education'] == 1), (clean_df['Occupation'] == 0) | (clean_df['Education'] == 0),]
choices = [1, 0]
clean_df['MiddleClass'] = np.select(conditions, choices, default=np.nan)
clean_df['MiddleClass'].value_counts(dropna=False)

#%% CONTROL VARIABLES

clean_df["Age"] = filtered_df["age1"]
clean_df['age2'] = clean_df['Age'].apply(lambda x: x**2) #quadratic of age
clean_df["Gender"] = filtered_df["q102_1"].apply(lambda x: 1 if x == "male" else 0 if x == "female" else np.nan)
clean_df["Expenditures"] = filtered_df["exp_ae"]
#IncDist shows perceptions of where a household stands in income distribution of 
#the country; 1-poorest and 10-richest
clean_df["IncDist"] = filtered_df["q211"] 
clean_df["IncDist"].replace(66, np.nan, inplace=True) # In that particular case, answer 'don't know'
clean_df["IncDist"].value_counts(dropna=False)
# is coded as 66, so I replace 66 with missing values
clean_df['FreeMarket_Support'] = filtered_df["q310"].apply(lambda x: 1 if x == "market economy preferable"
                                                                      else 0 if pd.notna(x) else np.nan)
clean_df['stateemployment'] = filtered_df["q408a1"] #alternative stateemployment that takes into consideration
#previous jobs

#%% BUILDING VARIABLE SOCIAL ASSISTANCE

clean_df['state_assistance'] = np.nan
clean_df.loc[(filtered_df['q210a8'] == "yes") | (filtered_df['q210a6'] == "yes"), 'state_assistance'] = 1
clean_df.loc[(filtered_df['q210a8'] == "no") & (filtered_df['q210a6'] == "no"), 'state_assistance'] = 0

#%% IINTERACTION TERM

#for regression purposes, we will need interaction term between middle class and
#state employement. Interaction term is built as a product of those two variables
clean_df['state_emp_middleclass'] = clean_df['state_emp_now'] * clean_df['MiddleClass']

#%% SAVING DATA TO CSV

clean_df.to_csv('cleaned_dataset2006_alt.csv', index_label='countryname')








