# This script contains all functions relating to making graphs and representations of analytics

import pandas as pd 
import numpy as np
import pygame
import matplotlib.pyplot as plt
import datetime
from Extract import get_users
import random

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
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")

    # Iterating through users to plot their graph
    for user in users["name"]:
        poop_days = []
        poop = []
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

# Function to display a moving bar chart over time, akin to that of last years using pygame
### This Function is set up poorly, unoptimized and honestly should just restart another time ###
def display_bar_chart(df, users, size=[800, 500]):
    # INPUT #
    # df        :   pandas DataFrame - of all poops, cleaned and refined for every user
    # size      :   List - of form [sc_w, sc_h]

    # OUTPUT # 
    # pygame display of moving data

    # Initialising system
    pygame.init()
    sc_w, sc_h = size[0], size[1]
    wn = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("Poop Statistics")
    clock = pygame.time.Clock()
    tick = 0

    # Local Variables pre run
    running = True
    stop = False
    date_font = pygame.font.SysFont("Ariel", 35)
    bg = pygame.image.load("bg.png")
    user_dict = {}
    bars = []
    place = 0
    for user in users["name"]:
        if user != "Finn":
            user_dict[user] = 0
            bars.append(Bar(user, place))
            place += 1

    # Game Loop
    while running:
        # Event Polling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Temp display of tick
        user_dict[df["user"][tick]] = df["poop"][tick]

        # Ticking
        if not stop:
            tick += 1

        # Updating Window
        wn.blit(bg, (0, 0))
        clock.tick(60)

        # Updating all bars positions
        for bar in bars:
            bar.calculate_position(user_dict)
        
        # Checking for bars in the same place
        positions = []
        for bar in bars:
            while bar.place in positions:
                bar.place += 1
            positions.append(bar.place)
        
        # Drawing Bars
        for bar in bars:
            bar.update(wn, user_dict)

        # Date
        date = pd.to_datetime(df["timestamp"][tick], format="mixed")
        format = "%B %d"
        string = date.strftime(format)
        string_text = date_font.render(string, 1, (255, 255, 255))
        wn.blit(string_text, (sc_w - 10 - string_text.get_width(), sc_h - 10 - string_text.get_height()))

        # Correcting for KeyError
        if tick + 2 == len(df):
            stop = True

        pygame.display.update()

# Class to help with bar chart organising
class Bar(object):
    def __init__(self, user, place):
        self.user = user
        self.place = place
        self.name_font = pygame.font.SysFont("Ariel", 30)
        self.goal_y = 450 - self.place*40
        self.y = self.goal_y
        self.width = 0
        self.col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, wn, dict):
        self.calculate_y()
        poop = str(dict[self.user])
        name = self.name_font.render(self.user, 1, (255, 255, 255))
        poop_num = self.name_font.render(str(poop), 1, (255, 255, 255))
        pygame.draw.rect(wn, self.col, (105, self.y - 10, self.width, 20))
        wn.blit(name, (100 - name.get_width(), self.y - name.get_height()/2))
        wn.blit(poop_num, (110 + self.width, self.y - poop_num.get_height()/2))

    def calculate_position(self, dict):
        # Calculating Place in Leaderboards
        current_poop = dict[self.user]
        poops = []
        for key in dict.keys():
            poops.append(dict[key])
        poops = sorted(poops)
        self.place = poops.index(current_poop)
        self.goal_y = 435 - self.place*40

        # Calculating width of bar
        highest_poop = poops[-1]
        if highest_poop != 0:
            width_rate = current_poop/highest_poop
        else:
            width_rate = 0
        self.width = 600*width_rate
        


    def calculate_y(self):
        dy = self.goal_y - self.y
        if dy != 0:
            rate = 0.13
            move = rate*dy

            if dy**2 <= 2:
                self.y = self.goal_y
            else:
                self.y += move

        