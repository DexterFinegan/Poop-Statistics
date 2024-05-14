# Instagram poop extractor 2023
# Goal: Use data science to extract groupchat messages of 2023 poop chat and make an accurate table of everyones poops thoughout the year
# Then make a visual representation of everyones poops over time using pygame
# Version 1 - 2023

import pandas as pd
import os
import json
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pygame
import time

print("Creating Dataframe...")
MEGAFRAME = pd.DataFrame()
FILES = os.listdir("DATA/messages/inbox/2023poopcounter")
for file in FILES:
    if file.endswith(".json"):
        with open(f"DATA/messages/inbox/2023poopcounter/{file}") as jf:
            JSON_DATA = json.load(jf)
            df = pd.DataFrame(JSON_DATA["messages"])
            MEGAFRAME = pd.concat([MEGAFRAME, df])

MEGAFRAME['timestamp_ms'] = pd.to_datetime(MEGAFRAME['timestamp_ms'], unit='ms')
MEGAFRAME.drop(["share", "reactions", "photos", "audio_files", "videos", "call_duration"], axis=1, inplace= True)
MEGAFRAME["sender_name"].replace({'shauna\u00f0\u009f\u00a6\u0089': "Shauna",
                                   "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                    "Neo O'Herlihy": "Neo",
                                     "Conor Mcmenamin": "Conor",
                                      "Noel Brassil": "Noel",
                                       "Ros Hanley": "Ros",
                                       "Jack McRann": "Jack" }, inplace=True)


MEGAFRAME = MEGAFRAME[::-1]

# Dictionary of users highest poops at time of downloading data
max_poops = {"Dex" : 319,
             "Shauna" : 255,
             "Eoin" : 437,
             "Conan" : 452,
             "Neo" : 406,
             "Ros" : 206,
             "Noel" : 161,
             "Jack" : 137, 
             "Conor" : 129}

# Pie Chart of user interaction
pie_chart = False
if pie_chart:
    plt.figure(figsize = (6,6))
    MEGAFRAME["sender_name"].value_counts().plot(kind='pie', autopct='%1.2f%%', shadow=True)
    plt.show()

print("Extarcting Data...")
# Extracting data from a user
def extract_data(user):
    all_nums = []
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i, row in MEGAFRAME.iterrows():
        if row["sender_name"] == user:
            message = row["content"]
            if not pd.isna(message):
                for index in range(len(message)):
                    if message[index] in numbers:
                        if message[index - 1] not in numbers or index == 0:
                            number = message[index]
                            j = 1
                            valid = True
                            while valid:
                                if index + j != len(message):
                                    if message[index + j] in numbers:
                                        number += message[index + j]
                                        j += 1
                                    else:
                                        valid = False
                                else:
                                    valid = False

                            all_nums.append([int(number), i])
    return all_nums

# Function to look at poop lists to decipher most appropriate poop instance
def check_appropriate_poop(key, poop_dict, last_poop):
    for entry in poop_dict[key]:
        if entry[0] > last_poop:
            appropriate = True
            if key < len(poop_dict) - 2:
                for entry2 in poop_dict[key + 1]:
                    if entry[0] > entry2[0] > last_poop:
                        appropriate = False
                if appropriate:
                    for entry3 in poop_dict[key + 2]:
                        if entry[0] > entry3[0] > last_poop:
                            appropriate = False
            
            if appropriate:
                return entry
    return None
    
# Function to find all instances of poop number
def find_poop_counts(num_list, max_poops, user):
    poop_counts = {}
    max_poop = max_poops[user]
    for poop in range(1, max_poop + 1):
        indexes = []
        for index in range(len(num_list)):
            if poop == num_list[index][0]:
                indexes.append([index, num_list[index][1]])
        poop_counts[poop] = indexes

    poop_counts_refined = {}
    lowest = 0
    for poop in poop_counts.keys():
        if poop != max_poop:
            good = check_appropriate_poop(poop, poop_counts, lowest)
            if good is not None:
                poop_counts_refined[poop] = good[1]
                lowest = good[0]

    return poop_counts_refined

def get_everyones_data(max_poops):
    everyones_data = {}
    for user in max_poops.keys():
        print(f"Extracting {user}'s Data")
        all_poops = find_poop_counts(extract_data(user), max_poops, user)
        everyones_data[user] = all_poops
    return everyones_data

all_data_refined = get_everyones_data(max_poops)

def change_chat_index_to_time(data):
    global MEGAFRAME
    new_data = {}

    for key in data:
        user_data = data[key]
        new_user_data = {}
        
        for poop in user_data:
            time = MEGAFRAME["timestamp_ms"][user_data[poop]]
            month = str(time)[5:7]
            if month[0] == "0":
                month = month[1]
            day = str(time)[8:10]
            if day[0] == "0":
                day = day[1]
            month, day = int(month), int(day)

            new_user_data[poop] = [month, day]
        
        new_data[key] = new_user_data
    return new_data

new_rep = change_chat_index_to_time(all_data_refined)
show = False
if show:
    for key in new_rep:
        print(f"{key} : {new_rep[key]} \n")

print("Preparing Presentation")   
pygame.init()
sc_w, sc_h = 800, 600
wn = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption("POOP COUNTER 2023")
clock = pygame.time.Clock()

# Participate classes
class Participant(object):
    def __init__(self, pos, data, user):
        self.pos = pos
        self.width = 1
        self.data = data
        self.user = user
        self.current_poop = list(self.data.keys())[0]
        self.found = True
        self.count = 5
        self.list_done = False
        self.y = 100 + 40 * self.pos
        self.picture = pygame.image.load("pictures/" + str(self.user.lower()) + ".png")


    def update(self, wn, date, highest_poop):
        # Calculate bar width 
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        months_dict = {"January" : 31,
              "February" : 28,
              "March" : 31,
              "April" : 30,
              "May" : 31,
              "June" : 30,
              "July" : 31,
              "August" : 31,
              "September" : 30,
              "October" : 31,
              "November" : 30,
              "December" : 31}
        m_num = months.index(date[0])
        d_num = date[1]/months_dict[date[0]]
        prop = m_num/12 + d_num/12
        self.width = self.current_poop*(80 + 550*prop)/highest_poop

        # Adjust y val
        goal_y = 100 + 40*self.pos
        dy = self.y - goal_y
        self.y -= 2*dy/3

        # Draw Bar
        pygame.draw.rect(wn, (255, 0, 0), (100, self.y + 3*self.current_poop/200, self.width, (3000 - self.current_poop*3)/100))

        # Name Bar
        font = pygame.font.SysFont("Arial", 20)
        name = font.render(self.user, 1, (0, 0, 0))
        wn.blit(name, (95 - name.get_width(), self.y + 15 - name.get_height()/2))

        # Print Count
        count = font.render(str(self.current_poop), 1, (0, 0, 0))
        wn.blit(count, (100 + self.width + 2, self.y + 15 - count.get_height()/2))

        # Draw image
        wn.blit(pygame.transform.scale_by(self.picture, 0.13), (100 + self.width - 25, self.y))

        # Find Poops on this date
        if not self.list_done:
            self.found = False
            while not self.found:
                self.find_poop(date)

    def find_poop(self, date):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        current_index = list(self.data.keys()).index(self.current_poop)
        if current_index + 1 < len(list(self.data.keys())):
            next_poop = list(self.data.keys())[current_index + 1]
            date_of_next_poop = self.data[next_poop]
            
            current_date = [months.index(date[0]) + 1, date[1]]


            if date_of_next_poop[0] < current_date[0]:
                self.current_poop = next_poop
            elif date_of_next_poop[0] == current_date[0] and date_of_next_poop[1] <= current_date[1]:
                self.current_poop = next_poop
            else:
                self.found = True
        else:
            self.found = True
            self.list_done = True
                

# Presentation
def run_window(wn, data):
    # Number of days in each month
    months = {"January" : 31,
              "February" : 28,
              "March" : 31,
              "April" : 30,
              "May" : 31,
              "June" : 30,
              "July" : 31,
              "August" : 31,
              "September" : 30,
              "October" : 31}
    date = ["January", 1]
    count = 0
    poop_dance = True

    names = ["Neo", "Jack", "Eoin", "Dex", "Shauna", "Conan", "Noel", "Conor", "Ros"]
    participants = []
    pos = 0
    highest_poop = 1
    for name in names:
        participants.append(Participant(pos, data[name], name))
        pos += 1

    bg = pygame.image.load("pictures/bg.png")
    poop1 = pygame.image.load("pictures/poop1.png")
    poop2 = pygame.image.load("pictures/poop2.png")

    while True:
        pygame.display.update()

        if count == 1:
            time.sleep(3)
        clock.tick(15)
        wn.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Updating players
        current_poops = []
        for player in participants:
            player.update(wn, date, highest_poop)
            current_poops.append(player.current_poop)
            if player.current_poop > highest_poop:
                highest_poop = player.current_poop

        # Rearranging players based on poop count
        ordered_poops = sorted(current_poops)[::-1]
        for poop in ordered_poops:
            for player in participants:
                if player.current_poop == poop:
                    player.pos = ordered_poops.index(poop)
        positions = []
        for player in participants:
            while player.pos in positions:
                player.pos += 1
            positions.append(player.pos)
        
        suffix = "th"
        if str(date[1])[-1] == "1":
            suffix = "st"
        elif str(date[1])[-1] == "2":
            suffix = "nd"
        elif str(date[1])[-1] == "3":
            suffix = "rd"

        font = pygame.font.SysFont("Arial", 45)
        date_title = font.render(f"{str(date[1])}{suffix} of {date[0]}", 1, (0, 0, 0))
        wn.blit(date_title, (sc_w - 10 - date_title.get_width(), sc_h - 10 - date_title.get_height()))

        font = pygame.font.SysFont("Arial", 65, bold=True)
        title = font.render("Poop Race 2023", 1, (0, 0, 0))
        wn.blit(title, (sc_w/2 - title.get_width()/2, 15))

        # Increase Data Increment
        count += 1
        if count % 2 == 0:
            date[1] += 1
            if date[1] > months[date[0]]:
                date[1] = 1
                new_index = list(months).index(date[0]) + 1
                if new_index < 11:
                    date[0] = list(months)[new_index]
        
        # Dancing poop
        if count % 7 == 0:
            if poop_dance:
                poop_dance = False
            else:
                poop_dance = True

        if poop_dance:
            for i in range(3):
                wn.blit(poop1, (20 + 150*i, sc_h - 80))
                wn.blit(poop2, (85 + 150*i, sc_h - 80))
        else:
            for i in range(3):
                wn.blit(poop2, (20 + 150*i, sc_h - 80))
                wn.blit(poop1, (85 + 150*i, sc_h - 80))

run_window(wn, new_rep)