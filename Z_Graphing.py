
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import pandas as pd

# a=1; b=-8; c=26; d=50
# tc<- function(q) a*q^3 +b*q^2 + c*q + d
# MC<- function(q) 3*a*q^2 + 2*b*q +c
# AVC<- function(q) a*q^2 +b*q +c
# AC<-  function(q) a*q^2 +b*q+ c +d/q
# Step 1: Define the function


def my_function_mc(x):
    return 3*x**2 - 16*x + 26


def my_function_avc(x):
    return x**2 - 8*x + 26


def my_function_atc(x):
    return x**2 - 8*x + 26 + 50/x


# Generate a dense grid of x values
x_values = np.linspace(.5, 6, 400)

# Compute the y values for each function
y_values_mc = my_function_mc(x_values)
y_values_avc = my_function_avc(x_values)
y_values_atc = my_function_atc(x_values)

# Use Seaborn to plot all three functions
sns.lineplot(x=x_values, y=y_values_mc, label='MC')
sns.lineplot(x=x_values, y=y_values_avc, label='AVC')
sns.lineplot(x=x_values, y=y_values_atc, label='ATC')

# Customize the plot
plt.title('Cost Curves')
plt.xlabel('Quantity, Q')
plt.ylabel('MC, ATC, AVC')
