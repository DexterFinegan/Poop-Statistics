# This script contains all functions relating to making graphs and representations of analytics

import pandas as pd 
import numpy as np
import pygame
import matplotlib.pyplot as plt
import datetime
from Extract import get_users

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
        for index in range(len(df)):
            if df["user"][index] == user:
                poop_days.append(df["timestamp"][index])
                poop.append(df["poop"][index])
        print(f"{user} : {poop}\n")
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

# Function to display a moving bar chart over time, akin to that of last years using pygame
### This Function is set up poorly, unoptimized and honestly should just restart another time ###
def display_bar_chart(df, size=[800, 500]):
    # INPUT #
    # df        :   pandas DataFrame - of all poops, cleaned and refined for every user
    # size      :   List - of form [sc_w, sc_h]

    # OUTPUT # 
    # pygame display of moving data

    # Initialising system
    pygame.init()
    sc_w, sc_h = size[0], size[1]
    wn = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("Poop Statisitics")
    clock = pygame.time.Clock()

    # Local Variables pre run
    running = True
    start = datetime.datetime(2023, 1, 1)
    end = df["timestamp"].iloc[-1]
    delta = datetime.timedelta(days=1)

    # Setting up Log dictionary, to locate each users count at a given date
    logs = {}
    users = get_users(directory="DATA/messages/inbox/2023poopcounter", refactor=True)
    for user in users["name"]:
        logs[user] = 0
    
    # Setting fonts
    date_font = pygame.font.SysFont("Ariel", 50)
    title_font = pygame.font.SysFont("Ariel", 75)
    title = title_font.render("Poop Marathon 2023", 1, (0, 0, 0))
    user_font = pygame.font.SysFont("Ariel", 40)

    while running:
        # Updating Window
        pygame.display.update()
        wn.fill((255, 255, 255))
        clock.tick(24)

        # Updating date n title
        month = date_font.render(start.strftime("%B"), 1, (0, 0, 0))
        day = date_font.render(start.strftime("%d"), 1, (0, 0, 0))
        wn.blit(month, (sc_w - 10 - month.get_width(), sc_h - 10 - month.get_height()))
        wn.blit(day, (sc_w - 25 - month.get_width() - day.get_width(), sc_h - 10 - month.get_height()))
        wn.blit(title, (sc_w/2 - title.get_width()/2, 15))

        # Updating User titles
        for i in range(len(logs.keys())):
            name = list(logs.keys())[i]
            text = user_font.render(name, 1, (0, 0, 0))
            wn.blit(text, (15, 35 + title.get_height() + i*(text.get_height() + 10)))
            number = user_font.render(str(logs[name]), 1, (0, 0, 0))
            wn.blit(number, (sc_w - number.get_width() - 20, 35 + title.get_height() + i*(text.get_height() + 10)))


        # Checking User Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # Iterating over days
        for i,row in df.iterrows():
            # Converting df timestamp from string to datetime class
            date = row["timestamp"].split("-")
            date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

            # Checking if any dates match and affecting change in the dictionary
            if date == start:
                logs[row["user"]] += 1
        #print(logs, end="\n")

        # Incrementing date
        start += delta


        