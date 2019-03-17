# Investigation notes

--------------------------------------------------------------------------------

## Dataset Introduction

### Definitions for each indicator

- Gross Domestic Product per capita in constant 2000 US$

  - Adjusted for inflation

  - Not adjusted for differences in cost of living between countries

- Agriculture workers (% total labor force)

- Industry workers (% total labor force)

- Service workers (% total labor force)

### Questions

I want to investigate the relationship between different countries regarding their GDP per capita and the proportions of different workers in various sectors.

- As a country develops, how does the composition of its workforce change?
- Which countries are progressing the fastest?
- What can these countries expect as their GDP rises?

### Parameters

- independent variable:

  - Years

- dependent variables:

  - GDP

  - % Agriculture workers

  - % Industry workers

  - % Service workers

### Challenges w/ the data

- Contains many missing values: will likely need to select only series with mostly complete rows and impute missing values

  - Adds a bias

  - Probably too many rows for good analysis anyway, aggregating the data in different ways might help

- Would be more convienient to transpose dataset so that rows are years and columns are countries

- Would be interesting to find a way to group by continent

--------------------------------------------------------------------------------

## Preprocessing notes

- Each of the employment sector dataframes have the same plots for Non-Nan value density. This suggests that NaN values will be in the same places because otherwise the probability that all plots would look the same is very low.

- The Max value for the employment sector dataframes is 2007 which means that we cannot see how the credit crunch effected these countries.

- Each column within the employment sector dataframes was found within the GDP dataframe. Unfortunately, 28 columns were not found within the country code dataframe which means that only 147 countries will be available for processing.

- Of these countries, only 38 have a non-NaN density higher than 0.7 for each value. When grouped by region, the majority of these countries are from Western Countries followed by the Americas and Asia. This can be seen in the table below

region     | count
---------- | -----
_Africa_   | 1
_Americas_ | 10
_Asia_     | 10
_Europe_   | 16
_Oceania_  | 1

- When grouped by sub regions it seems that the regions are taken from a diverse area after all. Obviously, when selecting data in this way you have a bias towards countries that developed quickly within the later part of the 20th century. In return for this bias the data becomes cleaner to work with

sub-region                | count
------------------------- | -----
Australia and New Zealand | 1
Caribbean                 | 3
Central America           | 3
Eastern Asia              | 1
Eastern Europe            | 1
Northern Africa           | 1
Northern America          | 1
Northern Europe           | 5
South America             | 3
South-Eastern Asia        | 5
Southern Asia             | 1
Southern Europe           | 5
Western Asia              | 3
Western Europe            | 5

- Hence, I will take this approach since I have found a nice sample of countries with reasonably complete data where I can impute the rest of the values

- I will also want to change the values within the sector employment dataframes from floats between 0 and 100 (percentages) to numbers between 0 and 1.

- It seems that in their current form, I cant merge relevant dataframes by country and so I'll need to undo the trasposition function and change everything that follows on from it

--------------------------------------------------------------------------------

## Data Analysis notes

- There is a lot of data for The Americas, Asia and Europe so it might be interesting to take an average of the data and plot it against df_agric, df_ccode and

- Note that these dates are after the industrial revolution, so the impact that this had is not easily seen within the data without prior knowledge

- Mean correlation coefficient between industry and agriculture is 0.87 which isn't as strong as the correlation between industry employment and GDP (0.98) but is still relatively strong regardless.

- When t-test is used to compare the two values it is found that it is unlikely that this correlation is a coincidence (p=5.7e-33)

- When discussing the GDP (USD, y2000), inflation but not the differences in the cost of living between countries has been taken into account.

- Check countries which have improved in GDP over the recent timescale

  - Eastern Asia
  - Western/Northern Europe
  - Australia
  - North America

- Luxembourg has improved the most so the change here should be most noticable

--------------------------------------------------------------------------------

## Visualisation notes

- It seems that mean GDP and Employment in the Service Sector are very strongly correlated

  - Correlation coefficient of 0.98

  - If GDP continues to grow then service will max out, so there is a limit

- GDP growth is negatively correlated with industry and agriculture. This could be because GDP growth is correlated with technological development which reduces jobs in these sectors

- Doing plots by country ends up being too noisy so filtering by region and plotting by subregion works far better

--------------------------------------------------------------------------------

## Update notes

- Seems that I need more varied plots which is difficult with the data that I have now so I'm adding an extra variable to my analysis (median age)

- Updated data Preprocessing

- 
