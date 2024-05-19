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

    # Adjusting size of labels on axes
    plt.rc("xtick", labelsize=7)
    plt.rc("ytick", labelsize=15)

    # Changing the timestamp to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed").dt.date

    # Iterating through users to plot their graph
    for user in users["name"]:
        poop_days = []
        poop = []
        if user != "Noel":
            for index in range(len(df)):
                if df["user"][index] == user:
                    poop_days.append(df["timestamp"][index])
                    poop.append(df["poop"][index])
            plt.plot(poop_days, poop, label=user)
    
    # Plotting and displaying graph + legend
    plt.legend()
    plt.show()

# Function to display a pie chart of poops per person as a percentage of total poops
def pie_of_poops(df):
    # INPUT #
    # df    :   pandas DataFrame - as extracted and cleaned from other scripts

    # OUTPUT #
    # Pie chart displaying everyones poops as a percentage portion of the pie

    pass

# Function to display a pie chart of likes per person as a percentage of all likes/reactions in the chat
def pie_of_likes(df):
    # INPUT #
    # df    :   pandas DataFrame - as from total_likes()

    # OUTPUT #
    # Pie chart displaying everyones likes/reactions as a percentage portion of the pie

    # Constructing arrays for percentages and labels
    likes = []
    labels = []
    for key in df.keys():
        likes.append(df[key])
        labels.append(key)

    # Plotting pie chart
    plt.pie(likes, labels=labels, autopct="%1.1f%%")
    plt.title("Percentage Likes per Person")
    plt.show()    

# Function to display a pie chart of messages per person as a percentage of all messages sent into the chat
def pie_of_messages(df):
    # INPUT #
    # df    :   pandas DataFrame - as from total_sent_messages()

    # OUTPUT #
    # Pie chart displaying everyones messages as a percentage portion of the pie

    # Constructing arrays for percentages and labels
    messages = []
    labels = []
    for key in df.keys():
        messages.append(df[key])
        labels.append(key)

    # Plotting pie chart
    plt.pie(messages, labels=labels, autopct="%1.1f%%")
    plt.title("Percentage Messages Sent per Person")
    plt.show() 
        