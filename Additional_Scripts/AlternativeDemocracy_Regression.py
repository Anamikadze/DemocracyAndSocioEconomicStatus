#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:01:19 2023

@author: anano
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:45:08 2023
"""

#%% This script uses the cleaned dataset 'cleaned_dataset2006.csv' generated from an earlier script and applies 
#logistic regression analysis to investigate the regime preferences of three socio-economic groups: state-employed 
#middle class, privately employed middle class, and recipients of state assistance. The analysis aims to explore 
#the factors that influence the regime preferences of these groups, which could provide insights into their 
#political attitudes and behaviors.

#%% IMPORTING MODULES

import pandas as pd
import numpy as np
import statsmodels.api as sm # statsmodels.api provides tools for statistical modeling and inference

#%% PREPARING DATA FOR LOGISTIC REGRESSION

#When using StatsModels to run logistic regression in Python, it is important to ensure that the input dataset 
#only includes variables that are relevant to the analysis, such as independent and dependent variables 
#(including control variables). Any extraneous columns can prevent the regression from running correctly. 
#To address this issue, I cleaned the dataset to remove any variables that are not necessary for the regression analysis.

df = pd.read_csv('cleaned_dataset2006_alt.csv')
cols_to_keep = ['state_emp_now', 'Democracy', 'MiddleClass', 'state_assistance', 'Age', 'age2', 'Gender']
df_filtered = df[cols_to_keep].copy() #I use copy() to create a copy of the subset of data frame created by 
#df[cols_to_keep]. This is done to avoid accidentally modifying the original data frame df while working with the filtered data.

#Creating an interaction term between two variables, in this case 'state_emp_now' and 'MiddleClass', 
#allows us to examine the combined effect of these variables on the outcome variable.

df_filtered['state_emp_middleclass'] = df_filtered['state_emp_now'] * df_filtered['MiddleClass']
df_filtered.dropna(inplace=True) #I drop all missing values from the regression dataset


#%% Running Logistic Regression on Full Sample (Democratic and Non-Democratic Countries)

#StatsModels package has two different ways to run logistic regression. 1) sm.logit: the function fits a logistic regression model using maximum likelihood estimation (MLE).
# sm.GLM: This function can also be used to fit logistic regression models using MLE, but it is a more 
#general function that can be used to fit other types of generalized linear models as well. I use sm.GLM that assumes
#binomial distribution with a logit link function. In this case, GLM and Logit do the same thing. The reason is that
#GLM has get_prediction method with standard errors and confidence interval for predicted mean, which I use later to get 
#predicted probabilities for democracy support. However sm.GLM does not support margins method. I use Logit function
#at the end of the script to show marginal effects of independet variables

Y = df_filtered["Democracy"] #Democracy" is the dependent variable in this logistic regression.
X = df_filtered.drop(["Democracy"], 1) #This line creates a new dataframe X that contains all the independent variables.
X = sm.add_constant(X.astype(float)) #This line adds a constant term to the independent variables matrix X
X = X.dropna() #removing missing values from explanatory variables
Y = Y[X.index] #removing corresponding values from dependent variable

model = sm.GLM(Y, X, family=sm.families.Binomial()) #This line creates a GLM model object using the sm.GLM() method. 
#In this case, the GLM model in statsmodels is assuming a binomial 
#distribution for the dependent variable Y with a logit link function.
logit_model = model.fit() #This line fits the logistic regression model to the data using the fit() method of the 
#GLM model object created in the previous line. It estimates the coefficients of the model using maximum likelihood estimation
print(logit_model.summary())

#%% Calculating Predicted Probability for Middle Class, Not State Employed

#This code creates a dictionary private_mc_dict containing the values of independent variables for the hypothetical 
#individual of interest, in this case, a privately employed middle-class with the average age of the sample.
#The dictionary is then converted to a DataFrame new_observation with a single row using the pd.DataFrame.from_dict() method, 
#where the orient parameter is set to 'index' to swap rows and columns. #The next step is to add a constant to the DataFrame using 
#the sm.add_constant() method so that it can be used with the fitted logistic regression model. Then, the reindex() method is used to 
#ensure that the columns of the new observation DataFrame match the columns of the original dataset.
#The predicted probability and the standard error for the hypothetical individual are calculated using the get_prediction() 
#method of the fitted logistic regression model object logit_model


private_mc_dict = {
    "MiddleClass": 1,
    "state_emp_now": 0,
    "state_assistance": 0,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": df_filtered["Age"].mean(),
    "age2": df_filtered["age2"].mean(),
}

#%%
# convert the dictionary to a dataframe with a single row
new_observation = pd.DataFrame.from_dict(private_mc_dict, orient='index').T #swaps the rows and columns of a DataFrame.

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
new_observation = sm.add_constant(new_observation)
new_observation = new_observation.reindex(columns=X.columns, fill_value=1)

private_mc_prob_pred = logit_model.get_prediction(new_observation)
private_mc_prob = private_mc_prob_pred.predicted_mean[0]
private_mc_prob_se = private_mc_prob_pred.se_mean[0]
print("P for private middle class: ", private_mc_prob)
print("Standard error for the predicted probability: ", private_mc_prob_se)

#%% Creating new observation for Middle Class, State Employed

state_mc_dict = {
    "MiddleClass": 1,
    "state_emp_now": 1,
    "state_assistance": 0,
    "state_emp_middleclass" : 1,
    "Gender" : 1,
    "Age": df_filtered["Age"].mean(),
    "age2": df_filtered["age2"].mean(),
}

new_observation_1 = pd.DataFrame.from_dict(state_mc_dict, orient='index').T #swaps the rows and columns of a DataFrame.
new_observation_1 = sm.add_constant(new_observation_1)
new_observation_1 = new_observation_1.reindex(columns=X.columns, fill_value=1)
state_mc_prob_pred = logit_model.get_prediction(new_observation_1)
state_mc_prob = state_mc_prob_pred.predicted_mean[0]
state_mc_prob_se = state_mc_prob_pred.se_mean[0]
print("P for state middle class: ", state_mc_prob)
print("Standard error for the predicted probability: ", state_mc_prob_se)

#%%
#Calculating probabilty fo being 'democrat' for people who are on state-assistance

state_assistance_dict = {
    "MiddleClass": 0,
    "state_emp_now": 0,
    "state_assistance": 1,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": df_filtered["Age"].mean(),
    "age2": df_filtered["age2"].mean(),
}

new_observation_2 = pd.DataFrame.from_dict(state_assistance_dict, orient='index').T #swaps the rows and columns of a DataFrame.
new_observation_2 = sm.add_constant(new_observation_2)
new_observation_2 = new_observation_2.reindex(columns=X.columns, fill_value=1)

state_assistance_prob_1 = logit_model.get_prediction(new_observation_2)
state_assistance_prob = state_assistance_prob_1.predicted_mean[0]
stata_assistance_se = state_assistance_prob_1.se_mean[0]
print("P for stata assistance: ", state_assistance_prob)
print("SE for state assistance:", stata_assistance_se )

#%%This code creates a new empty pandas DataFrame called "probs_full" with columns 'scenario' and 'Full Sample'. 
#Then, it appends the predicted probabilities for each of the three scenarios: "Middle Class, Private Employed", 
#"Middle Class, State Employed", and "Recipients of State Assistance". Finally, it prints the entire "probs_full" 
#DataFrame which shows the predicted probabilities for each scenario in a tabular format

probs_full = pd.DataFrame(columns=['scenario', 'Full Sample'])

# append the probabilities for each scenario
probs_full.loc[0] = ['Middle Class, Private Employed', private_mc_prob]
probs_full.loc[1] = ['Middle Class, State Employed', state_mc_prob]
probs_full.loc[2] = ['Recepients of State Assistance', state_assistance_prob]

# display the probabilities DataFrame
print(probs_full)


#%%  **RUNNING LOGISTIC REGRESSION FOR NON-DEMOCRACIES ONLY** 

#Please not that all the steps performed above follow the same logic as steps above. Therefore, if you need any explanation
#of what each line of code does, refer to my earlier comments

countries = ['belarus', 'russia', 'bosnia', 'armenia', 'azerbaijan', 'kazakhstan', 'kyrgyzstan', 'tajikistan', 'uzbekistan']
nondems_df = df[df['countryname'].isin(countries)]
cols_to_keep = ['state_emp_now', 'Democracy', 'MiddleClass', 'state_assistance', 'Age', 'age2', 'Gender']
nondems_df = nondems_df[cols_to_keep].copy()
nondems_df['state_emp_middleclass'] = nondems_df['state_emp_now'] * nondems_df['MiddleClass']
print(len(nondems_df))

#%% Running regression

import statsmodels.api as sm

Y = nondems_df["Democracy"] #setting dependent variable
X = nondems_df.drop(["Democracy"], 1) #setting independent variables
X = sm.add_constant(X.astype(float))
X = X.dropna() #removing missing values from explanatory variables
Y = Y[X.index] #removing corresponding values from dependent variable

model = sm.GLM(Y, X, family=sm.families.Binomial())
logit_model = model.fit()
print(logit_model.summary())

#%% Predictions for non-democracies

# Calculating Predicted Probability for middleclass, not state employed person 
n_privatemc_dict = {
    "MiddleClass": 1,
    "state_emp_now": 0,
    "state_assistance": 0,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
n_non_emp_observation = pd.DataFrame.from_dict(n_privatemc_dict, orient='index').T

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
n_non_emp_observation = sm.add_constant(n_non_emp_observation)
n_non_emp_observation = n_non_emp_observation.reindex(columns=X.columns, fill_value=1)

# calculate the predicted probability for a non-state employed person
n_non_emp_prob_pred = logit_model.get_prediction(n_non_emp_observation)
n_non_emp_prob = n_non_emp_prob_pred.predicted_mean[0]
n_non_emp_prob_se = n_non_emp_prob_pred.se_mean[0]
print("P for private middle class, not state employed: ", n_non_emp_prob)
print("Standard error for the predicted probability: ", n_non_emp_prob_se)

#%%
# Calculating Predicted Probability for middle class stata employed

non_statemiddle_dict = {
    "MiddleClass": 1,
    "state_emp_now": 1,
    "state_assistance": 0,
    "state_emp_middleclass" : 1,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
n_state_middle_1 = pd.DataFrame.from_dict(non_statemiddle_dict, orient='index').T

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
n_state_middle_1 = sm.add_constant(n_state_middle_1)
n_state_middle_1 = n_state_middle_1.reindex(columns=X.columns, fill_value=1)

# calculate the predicted probability for a non-state employed person
non_statemiddle_prob_pred = logit_model.get_prediction(n_state_middle_1)
non_statemiddle_prob = non_statemiddle_prob_pred.predicted_mean[0]
non_statemiddle_prob_se = non_statemiddle_prob_pred.se_mean[0]
print("P for state middle class: ", non_statemiddle_prob)
print("Standard error for the predicted probability: ", non_statemiddle_prob_se)

#%%

# Calculating Predicted Probability for people on state assistance

n_assistance_dict = {
    "MiddleClass": 0,
    "state_emp_now": 0,
    "state_assistance": 1,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
new_observation = pd.DataFrame.from_dict(n_assistance_dict, orient='index').T #swaps the rows and columns of a DataFrame.

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
new_observation = sm.add_constant(new_observation)
new_observation = new_observation.reindex(columns=X.columns, fill_value=1)

state_assistance_prob_nondems_1 = logit_model.get_prediction(new_observation)
state_assistance_prob_nondems = state_assistance_prob_nondems_1.predicted_mean[0]
print("P for state assistance: ", state_assistance_prob_nondems)
state_assistance_sterror_nondems = state_assistance_prob_nondems_1.se_mean[0]
print(state_assistance_sterror_nondems)

#%%
prob_nondems = pd.DataFrame(columns=['scenario', 'Non-Democratic Countries'])

prob_nondems.loc[0] = ['Middle Class, Private Employed', n_non_emp_prob]
prob_nondems.loc[1] = ['Middle Class, State Employed', non_statemiddle_prob]
prob_nondems.loc[2] = ['Recepients of State Assistance', state_assistance_prob_nondems]

# print the dataframe
print(prob_nondems)

#%%  **RUNNING LOGISTIC REGRESSION FOR DEMOCRACIES ONLY** 

# Preparing data for regression

democracies = ['albania', 'bulgaria', 'croatia', 'czechrep ', 'estonia', 'georgia','hungary', 'latvia', 'lithuania' ,'montenegro', 'poland', 'romania', 'slovakia', 'slovenia', 'ukraine']
dems_df = df[df['countryname'].isin(democracies)]
cols_to_keep = ['state_emp_now', 'Democracy', 'MiddleClass', 'state_assistance', 'Age', 'age2', 'Gender']
dems_df = dems_df[cols_to_keep].copy()
dems_df['state_emp_middleclass'] = dems_df['state_emp_now'] * dems_df['MiddleClass']


#%%
# Runnign logistic regression

Y = dems_df["Democracy"] #setting dependent variable
X = dems_df.drop(["Democracy"], 1) #setting independent variables
X = sm.add_constant(X.astype(float))
X = X.dropna() #removing missing values from explanatory variables
Y = Y[X.index] #removing corresponding values from dependent variable

model = sm.GLM(Y, X, family=sm.families.Binomial())
logit_model = model.fit()
print(logit_model.summary())


#%%

dem_middleclass_dict = {  #n_privatemc_dict
    "MiddleClass": 1,
    "state_emp_now": 0,
    "state_assistance": 0,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
dem_middle_obs = pd.DataFrame.from_dict(dem_middleclass_dict, orient='index').T

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
dem_middle_obs= sm.add_constant(dem_middle_obs)
dem_middle_obs = dem_middle_obs.reindex(columns=X.columns, fill_value=1)

# calculate the predicted probability for a non-state employed person
dem_middle_prob_pred = logit_model.get_prediction(dem_middle_obs)
dem_middle_prob = dem_middle_prob_pred.predicted_mean[0]
dem_middle_prob_se = dem_middle_prob_pred.se_mean[0]
print("P for private middle class, not state employed: ", dem_middle_prob) 
print("Standard error for the predicted probability: ", dem_middle_prob_se)

#%%

dem_statemiddleclass_dict = {  #n_privatemc_dict
    "MiddleClass": 1,
    "state_emp_now": 1,
    "state_assistance": 0,
    "state_emp_middleclass" : 1,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
dem_statemiddle_obs = pd.DataFrame.from_dict(dem_statemiddleclass_dict, orient='index').T

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
dem_statemiddle_obs= sm.add_constant(dem_statemiddle_obs)
dem_statemiddle_obs = dem_statemiddle_obs.reindex(columns=X.columns, fill_value=1)

# calculate the predicted probability for a non-state employed person
dem_statemiddle_pred = logit_model.get_prediction(dem_statemiddle_obs)

# extract the predicted probability and its standard error
dem_statemiddle_prob = dem_statemiddle_pred.predicted_mean[0]
dem_statemiddle_prob_se = dem_statemiddle_pred.se_mean[0]

print("P for private middle class, state employed: ", dem_statemiddle_prob)
print("Standard error for the predicted probability: ", dem_statemiddle_prob_se)

#%%
dem_assistance_dict = {  #n_privatemc_dict
    "MiddleClass": 0,
    "state_emp_now": 0,
    "state_assistance": 1,
    "state_emp_middleclass" : 0,
    "Gender" : 1,
    "Age": nondems_df["Age"].mean(),
    "age2": nondems_df["age2"].mean(),
}

# convert the dictionary to a dataframe with a single row
dem_assistance_obs = pd.DataFrame.from_dict(dem_assistance_dict, orient='index').T

# add a constant to the dataframe, so it can be used with the fitted logistic regression model
dem_assistance_obs= sm.add_constant(dem_assistance_obs)
dem_assistance_obs = dem_assistance_obs.reindex(columns=X.columns, fill_value=1)

# calculate the predicted probability for a non-state employed person
dem_assistance_prob_1 = logit_model.get_prediction(dem_assistance_obs)
dem_assistance_prob = dem_assistance_prob_1.predicted_mean[0]
print("P for poeple on state assistance: ", dem_assistance_prob)
assistance_dems_stderror = dem_assistance_prob_1.se_mean[0]


#%%


prob_dems = pd.DataFrame(columns=['scenario', 'Democratic Countries'])

prob_dems.loc[0] = ['Middle Class, Private Employed', dem_middle_prob]
prob_dems.loc[1] = ['Middle Class, State Employed', dem_statemiddle_prob]
prob_dems.loc[2] = ['Recepients of State Assistance', dem_assistance_prob]



#%%Reshaping dataframe for plot

#This code first creates a new dataframe merged by merging the probs_full DataFrame with prob_nondems DataFrame based on the 'scenario' 
#column. It then merges the resulting DataFrame with the prob_dems DataFrame based on the 'scenario' column to create a new DataFrame 
#probability. After that, the code reshapes the DataFrame probability using pd.melt() function by setting 'scenario' as the id variable 
#and the remaining column names as variable names ('category') and their corresponding values as the value names ('probability').
#Finally, the code creates a new column 'SE' in the probability_melt DataFrame by creating a list se_values that contains the 
#standard error values for each scenario and assigns it as a Series to the 'SE' column. This probability_melt DataFrame can be 
#used for further analysis and visualization of the logistic regression results.

merged = probs_full.merge(prob_nondems, on='scenario') 
probability = merged.merge(prob_dems, on='scenario')
probability_melt = pd.melt(probability, id_vars=['scenario'], var_name='category', value_name='probability')
se_values = [private_mc_prob_se, state_mc_prob_se, stata_assistance_se,n_non_emp_prob_se, non_statemiddle_prob_se, state_assistance_sterror_nondems, dem_middle_prob_se, dem_statemiddle_prob_se, assistance_dems_stderror]
probability_melt['SE'] = pd.Series(se_values)

#%%This code generates a scatter plot with error bars using Seaborn and Matplotlib. It takes the probability data from the 
#probability_melt DataFrame, which includes the scenario, category (Democracy or MiddleClass), probability, and standard error values.

probability_melt['category'] = probability_melt['category'].astype('category')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Times New Roman'

# Create a copy of the dataframe with a new column for the x-coordinate
probability_melt['x'] = probability_melt.groupby('category').ngroup()
sns.set_style('white')

# Create the scatterplot with error bars using catplot()
sns.catplot(x='x', y='probability', hue='scenario', data=probability_melt, jitter=False, dodge=False, palette='dark', kind='strip')

# Add error bars to the plot
for i, group_data in probability_melt.groupby(['category', 'scenario']):
    x = group_data['x'].values[0]
    y = group_data['probability'].values[0]
    se = group_data['SE'].values[0]
    plt.errorbar(x, y, yerr=se, fmt='none', ecolor='k', capsize=6)

# Set the axis labels and tick labels
plt.xlabel(' ')
plt.ylabel('Probability')
plt.xticks(ticks=probability_melt['x'].unique(), labels=probability_melt['category'].unique())
# Adding title
plt.title("Exploring the Relationship Between Socio-Economic Factors \nand Democracy Support: Predicted Probabilities Analysis", loc='center')

plt.savefig('probability_plot_alt.png', dpi=300)
# Show the plot
plt.show()


#%% Displaying Marginal Effects

Y = df_filtered["Democracy"] #setting dependent variable
X = df_filtered.drop(["Democracy"], 1) #setting independent variables
X = sm.add_constant(X.astype(float))
X = X.dropna() #removing missing values from explanatory variables
Y = Y[X.index] #removing corresponding values from dependent variable

model = sm.Logit(Y, X)
logit_model = model.fit()
print(logit_model.summary())

marginal_effects = logit_model.get_margeff(method="dydx", at="mean", dummy=True)
# Print the summary of marginal effects
print(marginal_effects.summary())









