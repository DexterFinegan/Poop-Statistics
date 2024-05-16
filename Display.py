# This script contains all functions relating to making graphs and representations of analytics

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# Function to create a plot of poops over time
def poops_over_time(df):
    # INPUT #
    # df    :   pandas DataFrame - as extracted and cleaned from other scripts

    # OUTPUT #
    # Display of a matplotlib graph to show combined poops over time

    # Creating an array of all dates poops occured 
    poop_days = df["timestamp"].to_numpy()
    poops = np.arange(2099)

    plt.plot(poop_days, poops)
    plt.show()

# Functoin to create a plot of individual poops over time
def poops_per_person(df, users):
    # INPUT #
    # df    :   pandas DataFrame - as extracted and cleaned from other scripts
    # users :   pandas DataFrame - names of all the users

    # OUTPUT #
    # Display of a matplotlib graph to show individual poops over time

    for user in users["name"]:
        poop_days = []
        poop = []
        if user == "Eoin" or user == "Conan":
            for index in range(len(df)):
                if df["user"][index] == user:
                    poop_days.append(df["timestamp"][index])
                    poop.append(df["poop"][index])
            plt.plot(poop_days, poop)
    
    plt.show()


    