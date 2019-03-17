
/*
This file will display the commands used to download the CSV files
from the online database using SQL.

It should be noted that because my city could not be found in the
city_list, I have downloaded the information for "Berlin" instead.
*/

-- Proof that Bonn is not in city_list
SELECT *
FROM city_list
WHERE country like 'Germany';
-- Returns three cities, Berlin, Hamburg and Munch but not Bonn or Cologne.

-- Rename columns for joining
ALTER TABLE global_data RENAME COLUMN avg_temp to global_avg_temp;

ALTER TABLE city_data RENAME COLUMN avg_temp to city_avg_temp;

-- Download the joined tables
SELECT global_data.year, global_data.global_avg_temp, city_avg_temp
FROM global_data INNER JOIN city_data
ON global_data.year=city_data.year
WHERE city like 'Berlin';
-- Saved as YearlyAvgTemp.csv

/* An inner join was chosen because I have enough data to process
even if I drop a couple of rows. Doing this in SQL means I don't
need to do this in python later.*/
