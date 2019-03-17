# Udacity-Project---Exploring-Weather-Trends
Udacity Data Analytics Nanodegree Project 01 - Exploring Weather Trends using Python and SQL

## Description

Analyze local and global temperature data and compare the temperature trends where you live to overall global temperature trends.

- create a visualization
- prepare a write up describing the similarities and differences between global temperature trends and temperature trends in the closest big city to where you live

### Steps:

1. Extract the data from the database
    * Using SQL
2. Extract CSV file for use in line chart
    * Drawn with Matplotlib in Python
3. Use said chart to make observations

### Submission:

The final analysis will take the form of a PDF document which contains a plot of the data, analysis of said plot and outlines the steps taken:

* What tools were used for each step
* How calculations were perfomed
* Key considerations when analyzing the trends

All code used will be placed in this repository for inspection.

## Important files

* "SQL-queries.sql" contains the SQL query used for this project with step by
step explanations of what I did.
* "YearlyAvgTemp.csv" is the resultant CSV from running the SQL query above
* "CSV-Analysis.py" is the python script used to analyze "YearlyAvgTemp.csv"
and creates the plots containted in "/Report/Plots/".
* "Report" contains the .tex file used for creating "paper.pdf" which is the name
of the final report. It also contains the folder "Plots" which is where the figures
produced by "CSV-Analysis.py" are saved.

## References and Citations

1. The Report was compiled using LaTeX. The Template used can be found in the url below:

https://www.overleaf.com/latex/templates/template-for-lnt-seminar-report/ngyxxzrpkgbs#
