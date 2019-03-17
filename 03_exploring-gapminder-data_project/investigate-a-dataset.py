#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:07:09 2017

@author: simon
"""

# =============================================================================
# Import Libraries
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# Defining Functions
# =============================================================================

def df_T_properly(df):
    """
    Transposes the dataframe, sets the column titles to the first row in the 
    transposed dataframe before removing the first row and returning the pro-
    perly transposed.
    
    Used in: calculate_nan_density_country(df_list)
    """
    
    # Transpose dataframe 
    df2 = df.transpose()
    
    # Rename columns
    df2.columns = df2.iloc[0]
    
    # Reset columns
    df3 = df2.reindex(df2.index.drop('Country'))
    
    return df3    


def plot_nan_density_year(df, df_name, x_label = "Year"):
    """
    Calculates the density of non-NaN values inside of a dataframe for each 
    row (i.e. year) and creates a plot with specified title showing this change.
    """
    
    # Calculate density per row
    year = []
    density = []
    for i in range(df.shape[1]):
        if i == 0: continue
        year.append(int(df.columns[i]))
        density.append(df.iloc[:, i].count()/len(df.iloc[:, i]))
    
    # Plot Results
    plt.plot(year, density)
    plt.xlabel(x_label)
    plt.ylabel("Non-NaN Density")
    plt.title("Non-NaN values for {}".format(df_name))
    axes = plt.gca()
    axes.set_ylim([0, 1])
    plt.show()
    
    
def basic_plot(x_series, y_series, x_label = "x", y_label="y", 
               y_ticks=False, plt_title = "plot"):
    """
    Creates a basic plot from two series, used for creating quick and dirty
    plots.
    
    For changing the xticks, input an integer for reduced_xticks. This only
    works if x_series can be converted to an integer
    
    You can also adjust the yticks by adding a tuple in the form of 
    (start, finish)
    """
    
    # Change years to int
    x_series = x_series.astype(int)
     
    # Create plot
    plt.plot(x_series, y_series, c='red')
    plt.xlabel(x_label)
    if y_ticks: plt.yticks(y_ticks)
    plt.ylabel(y_label)
    plt.title(plt_title)
    plt.show


def calculate_nan_density_country(df_list):
    """
    Looks at a list of dataframes and calculates the NaN density for each 
    country and returns that information inside of a datafame.
    
    Section of code will try to find the largest intersection of countries
    shared by all dataframes.
    
    This is so that the data can be grouped-by filtered and merged with other dfs
    later which will help gain into more insight into which columns that need to
    be dropped or transformed in some way.
    
    Dependencies: 
        country_check(check_country, df)
        common_countries(smallest_list)
        df_T_properly(df)
    """
    
    # Initialize values
    n_countries = {}
    smallest = 1e400
    
    # Find dataframes with lowest number of nonNaN rows
    for df in df_list:
        
        # Create relevant entry in dictionary
        if not eval(df).shape[0] in n_countries.keys(): n_countries[eval(df).shape[0]]=[df]
        else: n_countries[eval(df).shape[0]].append(df)
            
        # Keep track of smallest value
        if eval(df).shape[0] < smallest: 
            smallest = eval(df).shape[0]
    
    # Check smallest number of countries is unique
    if len(n_countries[smallest]) > 1:
        
        # Rename list
        smallest_list = n_countries[smallest]
        
        # Find unique columns
        check_country = common_countries(smallest_list)
    
    else: check_country =  list(eval(n_countries[smallest][0])['Country'])
    
    # Check that all check_country appear in ccode
    check_country2 = country_check(check_country, df_ccode)
    check_country3 = country_check(check_country2, df_GDP)
    check_country4 = country_check(check_country3, df_age)
    
    # Create dictionary which will be converted to dataframe
    dict_to_df = {}
    
    # Fill dictionary with relevant values
    for country in check_country4:

        # Init. row list
        row_list = [] 
        
        for df in df_list:
            # Calculate length
            
            df_row_length = eval(df)[eval(df)['Country']==country].iloc[0, 1:].notnull().count()
            
            # Calculate non-NaN values
            df_row_nonNaN = eval(df)[eval(df)['Country']==country].iloc[0, 1:].notnull().sum()
            
            # Append to List
            row_list.append(df_row_nonNaN/df_row_length)
        
        # Insert values into dictionary
        dict_to_df[country] = row_list
        
    # Convert dictionary to dataframe and transpose
    return_df = pd.DataFrame(dict_to_df)
    return_df.insert(loc = 0, column = 'Country', value = df_list)
    return_df = df_T_properly(return_df)
    
    return return_df
    

def common_countries(smallest_list):
    """
    Checks a list of strings that can be evaluated to dataframes and returns 
    countries which are not found in all dataframes.
    
    Used in: calculate_nan_density_country(df_list)
    """

    # Init. list
    ignore_country = []
    check_country= []

    # Check columns
    for i in range(len(smallest_list)):
        
        # Init j value to compare with later dfs
        j = i
        
        # Check larger dfs
        while j < len(smallest_list):
            
            # Find unique columns
            set_diff = set(eval(smallest_list[i])['Country']).difference(
                       set(eval(smallest_list[j])['Country']))
            
            # Add new unique columns to list
            for k in set_diff:
                if k not in ignore_country: ignore_country.append(k)
            
            # Increment j for next loop
            j+=1
        
    # find check_columns
    for df in smallest_list:
        good_columns = list(set(eval(df).Country).difference(set(ignore_country)))
        for col in good_columns:
            if col not in check_country: check_country.append(col)
    
    return check_country
  
    
def country_check(check_country, df):
    """
    Makes sure that each country can be found in df.
    
    Used in: calculate_nan_density_country(df_list)
    """
    
    # Init. list
    check_country2 = []
    
    # Check columns
    for country in check_country:
        try: 
            if country in list(df['name']): check_country2.append(country)
        except KeyError: 
            if country in list(df['Country']): check_country2.append(country)
    
    return check_country2    


def imputation_average(df):
    """
    Takes dataframe and imputes missing values for each column by using the
    mean of the column. Dataframe is then returned with all column names and
    indexesintact.
    """
    
    # Iterate over columns
    for i in range(df.shape[0]):
        
        # Calculate column mean
        row_mean = df.iloc[i, 1:].mean()
        
        # Fill NaN values
        df.iloc[i]=df.iloc[i].fillna(row_mean)
        
    return df

        
# =============================================================================
# Data Preprocessing
# =============================================================================

# Import data
df_GDP = pd.read_csv('data_csv/GDPpercapitaconstant2000US.csv')
df_agric = pd.read_csv('data_csv/indicator_t agriculture employ.csv')
df_indus = pd.read_csv('data_csv/indicator_t industry employ.csv')
df_servi = pd.read_csv('data_csv/indicator_t service employ.csv')
df_ccode = pd.read_csv('data_csv/country_codes.csv')
df_age = pd.read_csv('data_csv/indicator_median age.csv')

# Drop columns from df_ccode which will not be used
df_ccode.drop(['alpha-2', 'country-code', 'iso_3166-2', 'region-code',
               'sub-region-code'], axis=1, inplace=True)
    
# Rename bad label in df_age
df_age.rename(columns={'Median age': 'Country'}, inplace=True)

# Create dataframe list
df_list = ["df_GDP", "df_agric", "df_indus", "df_servi", "df_age"] 
for df in df_list:
    if df == 'df_age': continue # Skip df_age, complete data
    plot_nan_density_year(eval(df), df)

# Calculate Non-NaN density for each country
meta_df_NaN_Density = calculate_nan_density_country(df_list)

# Fix indexing issues
meta_df_NaN_Density.reset_index(inplace=True)
meta_df_NaN_Density.rename({'index': 'Country'}, axis=1, inplace=True)

# Find countries with Non-NaN densities higher than 0.7
threshold = 0.70
mdND_70 = meta_df_NaN_Density[(meta_df_NaN_Density['df_GDP'] > threshold) &\
                              (meta_df_NaN_Density['df_agric'] > threshold) &\
                              (meta_df_NaN_Density['df_indus'] > threshold) &\
                              (meta_df_NaN_Density['df_servi'] > threshold) &\
                              (meta_df_NaN_Density['df_age'] > threshold)]

# Join with df_ccode to determine general locations of countries
df_ccode.rename({'name': 'Country'}, axis=1, inplace=True)
mdND_70 = mdND_70.merge(right = df_ccode, how='inner', on='Country')

# Count rows by region
mdND_70.groupby('region')['Country'].count()

# Count rows by sub-region
mdND_70.groupby('sub-region')['Country'].count()

# Define countries to investigate
country_list = list(mdND_70['Country'])

# Update dataframes in df_T_List to contain the relevant countries
df_GDP = df_GDP[df_GDP['Country'].isin(country_list)]
df_agric = df_agric[df_agric['Country'].isin(country_list)]
df_indus = df_indus[df_indus['Country'].isin(country_list)]
df_servi = df_servi[df_servi['Country'].isin(country_list)]
df_age = df_age[df_age['Country'].isin(country_list)]


# Impute NaN values - Once again, no need to do anything with df_age
df_GDP = imputation_average(df_GDP)
df_agric = imputation_average(df_agric)
df_indus = imputation_average(df_indus)
df_servi = imputation_average(df_servi)

## check column values are appropriate
#df_GDP.info()
#df_agric.info()
#df_indus.info()
#df_servi.info()

# Change percentage range from 0-100 to 0-1
df_agric.iloc[:, 1:] = df_agric.iloc[:, 1:].divide(other=100)
df_indus.iloc[:, 1:] = df_indus.iloc[:, 1:].divide(other=100)
df_servi.iloc[:, 1:] = df_servi.iloc[:, 1:].divide(other=100)
#
# Merge region and sub-region into dataframes
df_GDP = df_ccode.merge(right = df_GDP, how='inner', on='Country')
df_agric = df_ccode.merge(right = df_agric, how='inner', on='Country')
df_indus = df_ccode.merge(right = df_indus, how='inner', on='Country')
df_servi = df_ccode.merge(right = df_servi, how='inner', on='Country')
df_age = df_ccode.merge(right = df_age, how='inner', on='Country')


# =============================================================================
# Data Analysis
# =============================================================================

"""
Directing questions:
    * As a country develops, how does the composition of its workforce change?
    * Which countries are progressing the fastest?
    * What can these countries expect as their GDP rises?
    * How does the average of each country in my sample operate?
    * How does median age change with GDP
    
You can also view these questions in terms of region/sub-region
"""

# Plot histogram
df_GDP.groupby('Country').mean().T.mean().plot(kind='hist', bins=15);

# Plot sample average GDP over time
basic_plot(x_series=df_GDP.columns[4:], 
           y_series=df_GDP.mean(), 
           x_label= "Year (C.E.)",
           y_label= 'GDP mean',
           plt_title='Global Mean GDP(USD in 2000, adj. for inf.)')
 
# Create plot
plt.plot(df_indus.columns[4:].astype(int), df_indus.mean(), 
         c='red', label='Industry')
plt.plot(df_agric.columns[4:].astype(int), df_agric.mean(), 
         c='blue', label='Agriculture')
plt.plot(df_servi.columns[4:].astype(int), df_servi.mean(),
          c='green', label='Service')
plt.xlabel('Year (C.E.)')
#plt.yticks((0, 0.25, 0.5, 0.75, 1))
plt.ylabel('Ratio Employed')
plt.title('Global Mean Employment(Ratio) by Sector over time')
plt.legend()
plt.show()

# Calculating correlation coefficients
corr_coeff_GDP_servi = np.corrcoef(x=df_GDP.mean()[20:-4], y=df_servi.mean())
corr_coeff_agric_indus = np.corrcoef(x=df_agric.mean(), y=df_indus.mean())

# Perform t-test on Service Employment ratio and GDP
from scipy.stats import ttest_ind
serv_ratio_series = df_GDP.mean()[20:-4]
GDP_series = df_servi.mean()
t_test_serv_GDP = ttest_ind(serv_ratio_series, GDP_series)
    
# Which region has progressed the fastest in terms of GDP?
ax = df_GDP.groupby('region').mean().T.plot(title='Region Mean Change in GDP (USD in 2000, adj. for inf.)')
ax.set_xlabel('Year (C.E.)')
ax.set_ylabel('GDP')

# How about Countries within a region?
for region in df_GDP['region'].unique():
    ax = df_GDP[df_GDP['region'] == region].groupby(
            'sub-region').mean().T.plot(title='Change in GDP (USD in 2000, adj. for inf.) over time in {}'.format(region))
    ax.set_xlabel('Year (C.E.)')
    ax.set_ylabel('GDP')
    
# Can we see the shift towards service employment in discreete coutnries or 
# if this just an aggregate effect?
    
MEDCs = ['Eastern Asia', 'Western Europe', 'Northern Europe', 
         'Australia and New Zealand', 'North America']

# Check countries
country_lookup = list(df_GDP[df_GDP['sub-region'].isin(MEDCs)]['Country'])

for country in country_lookup:
    plt.plot(df_indus.columns[4:].astype(int), 
             df_indus[df_indus['Country']==country].groupby('Country').mean().iloc[0], 
             c='red', 
             label='Industry')
    plt.plot(df_agric.columns[4:].astype(int), 
             df_agric[df_agric['Country']==country].groupby('Country').mean().iloc[0], 
             c='blue', 
             label='Agriculture')
    plt.plot(df_servi.columns[4:].astype(int), 
             df_servi[df_servi['Country']==country].groupby('Country').mean().iloc[0],
              c='green', 
              label='Service')
    plt.xlabel('Year (C.E.)')
    #plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.ylabel('Ratio Employed')
    plt.title('Employment(Ratio) by Sector over time in {}'.format(country))
    plt.legend()
    plt.show()

# Seaborn set style    
sns.set_style('whitegrid')

# Plot before and after world age distribution
sns.violinplot(data=df_age.iloc[:, 4:-8]);

# or
sns.boxplot(data=df_age[['1950', '2010']]);