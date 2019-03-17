# -*- coding: utf-8 -*-
"""
Spyder Editor

Creator: Simon Thornewill von Essen
"""

# Importing files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import datasets
df = pd.read_csv("YearlyAvgTemp.csv") 

"""
Next, we'll want to calculate the moving averages before doing the final plot

In my project submission I chose a moving average of 7 but this did not give a
smooth curve that was expected according to my feedback and I need to chose a
larger range. Given that the data spans around 200 years I'll want to
investigate 10 years and 100 years and maybe sharpen things from there
"""

# defining functions
"""
Simplifies calculation so that if I need to use this in creating multiple plots
then the command isn't as verbose and cumbersome.
"""
def simplifiedRollingMean(windowRolling, df_i):
    df_o = df_i.rolling(window = windowRolling, center=False, on = "year").mean().dropna()
    return df_o

# Calculation
rollingWindow = 150
df_movingAverage = simplifiedRollingMean(rollingWindow, df)


# Draw graph in matplotlib
plt.plot(df_movingAverage['year'], df_movingAverage['city_avg_temp'], label='Berlin')
plt.plot(df_movingAverage['year'], df_movingAverage['global_avg_temp'], label='Global')
plt.legend()
plt.xlabel("Year (C.E.)")
plt.ylabel("Temperature (°C)")
plt.title("Temperature in Berlin versus Global values ({} year moving avg)".format(rollingWindow))
plt.show()