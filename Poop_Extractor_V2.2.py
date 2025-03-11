# New Algorithm based poop extractor
# 12/1/25

import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pygame
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

DIRECTORY = "DATA/messages/inbox/2025poopchat"

# EXTRACTING AND CLEANING DATA
def extract_raw_data(directory, save=True):
    # INPUTS
    # directory     :   String - describes the directory from programme file to the location of the instagram json file
    
    # Creating and extracting json file to dataframe of messages
    MEGAFRAME = pd.DataFrame()
    FILES = os.listdir(directory)
    for file in FILES:
        if file.endswith(".json"):
            with open(f"{directory}/{file}") as jf:
                JSON_DATA = json.load(jf)
                df = pd.DataFrame(JSON_DATA["messages"])
                MEGAFRAME = pd.concat([MEGAFRAME, df])

    # Changing timestamp in dataframe to date and time, rounded to the nearest seocnd
    MEGAFRAME['timestamp_ms'] = pd.to_datetime(MEGAFRAME['timestamp_ms'], unit='ms')
    MEGAFRAME.rename(columns={"timestamp_ms" : "timestamp"}, inplace=True)
    MEGAFRAME["timestamp"] = MEGAFRAME["timestamp"].dt.round("1s")

    # Reversing order so indexes start at the beginning of the group chat
    MEGAFRAME = MEGAFRAME[::-1]

    # Accessing Refactor names config file
    file = open("DATA/refactor_names_config.txt", encoding="utf8")
    refactor_dict = {}
    for line in file.readlines():
        line = line.strip()
        line = line.split(": ")
        refactor_dict[line[0]] = line[1]
    file.close()

    # Replacing user's names to more readable ones
    MEGAFRAME["sender_name"] = MEGAFRAME["sender_name"].replace(refactor_dict)
    
    # Reversing indexes to be in chronological order 
    MEGAFRAME = MEGAFRAME.reset_index(drop=True)
    MEGAFRAME = MEGAFRAME.rename(columns={"sender_name": "user"})

    # Removing the "is_geoblocked_for_viewer" key because idek what that is
    MEGAFRAME.drop(["is_geoblocked_for_viewer", "is_unsent_image_by_messenger_kid_parent"], axis=1, inplace= True)

    # Saving to csv file
    if save:
        MEGAFRAME.to_csv("Save Files 2/All_Raw_Data.csv")
    return  MEGAFRAME

    print("Successfully Extracted and Saved Raw Data File")

def get_users(directory):
    # INPUT #
    # directory : String - detailing path to groupchat folder
    # refector  : Boolean - denoting whether names should be refactored

    # Creating and extracting json file to dataframe
    MEGAFRAME = pd.DataFrame()
    FILES = os.listdir(directory)
    for file in FILES:
        if file.endswith(".json"):
            with open(f"{directory}/{file}") as jf:
                JSON_DATA = json.load(jf)
                df = pd.DataFrame(JSON_DATA["participants"])
                MEGAFRAME = pd.concat([MEGAFRAME, df])

    # Accessing Refactor names config file
    file = open("DATA/refactor_names_config.txt", encoding="utf8")
    refactor_dict = {}
    for line in file.readlines():
        line = line.strip()
        line = line.split(": ")
        refactor_dict[line[0]] = line[1]
    file.close()
    
    # Refactoring names to be more legible, custom in code and assumed works
    MEGAFRAME["name"] = MEGAFRAME["name"].replace(refactor_dict)
    MEGAFRAME = MEGAFRAME.rename(columns={"name": "user"})

    # Saving to csv file
    MEGAFRAME.to_csv("Save Files 2/Users.csv")

    print("Successfully Extracted and Saved User Names")
    return MEGAFRAME["user"]

def separate_users():
    # Loading all relevant data to dataframes
    raw_data = pd.read_csv("Save Files 2/All_Raw_Data.csv")
    users = pd.read_csv("Save Files 2/Users.csv")["user"]
    
    for user in users:
        # Creating User's Messages
        filtered_df = raw_data[raw_data["user"] == user]
        filtered_df = filtered_df.drop(columns=["user"])
        filtered_df = filtered_df.rename(columns={"Unnamed: 0" : "Message ID"})
        filtered_df = filtered_df.reset_index(drop=True)
        
        # Saving File
        file_name = str(user) + "_Messages.csv"
        filtered_df.to_csv(f"Save Files 2/Messages/{file_name}")

def extracting_number_messages(user, provided_df=None):
    if provided_df is None:
        df = pd.read_csv(f"Save Files 2/Messages/{user}_Messages.csv", index_col=0)
    else:
        df = provided_df

    refined_data = {"Message ID" : [], "content" : []}
    new_df = pd.DataFrame(refined_data)

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for index in range(len(df["content"])):
        number = ""
        if not pd.isna(df["content"][index]):
            for char in df["content"][index]:
                if char in numbers:
                    number += char
                else:
                    if number != "":
                        new_df.loc[len(new_df)] = [df["Message ID"][index], number]
                        number = ""
            if number != "":
                new_df.loc[len(new_df)] = [df["Message ID"][index], number]

    return new_df 
    
def creating_possibility_poops(df):
    data = {}
    length = 110
    for index in range(len(df["content"])):
        poop = int(df["content"][index])
        if 0 < poop <= length:
            if poop in data.keys():
                data[poop].append(int(df["Message ID"][index]))
            else:
                data[poop] = [int(df["Message ID"][index])]
    refactored_data = {"Poop" : data.keys(), "Possible Message IDs" : data.values()}
    new_df = pd.DataFrame(refactored_data)
    new_df = new_df.sort_values(by="Poop")
    new_df = new_df.reset_index(drop=True)
    return new_df

def refine_possibilities(df):
    data = {"Poop" : [], "IDs" : []}
    for index in range(len(df["Possible Message IDs"])):
        if data["IDs"]:
            for entry in df["Possible Message IDs"][index]:
                if int(entry) >= data["IDs"][-1] and int(entry) - data["IDs"][-1] < 1000:
                    data["IDs"].append(int(entry))
                    data["Poop"].append(int(df["Poop"][index]))
                    break
        else:
            if int(df["Possible Message IDs"][index][0]) < 700:
                data["IDs"].append(int(df["Possible Message IDs"][index][0]))
                data["Poop"].append(int(df["Poop"][index]))
    new_df = pd.DataFrame(data)
    return new_df

def recollect_data(df):
    full_df = pd.read_csv("Save Files 2/All_Raw_Data.csv")
    full_df = full_df.rename(columns={"Unnamed: 0" : "IDs"})
    recollected_df = pd.merge(df, full_df, on="IDs", how="inner")
    recollected_df = recollected_df.drop(columns=["share", "photos", "videos", "call_duration"])

    file_name = str(recollected_df["user"][0]) + "_Poops.csv"
    recollected_df.to_csv(f"Save Files 2/Poops/{file_name}")
    return recollected_df

def extract_and_clean_all_data(directory):
    extract_raw_data(directory)
    users = get_users(directory)
    separate_users()

    df_list = []
    
    for user in users:
        numbers = extracting_number_messages(user)
        possibilities = creating_possibility_poops(numbers)
        poop_numbers = refine_possibilities(possibilities)
        data = recollect_data(poop_numbers)

        # For the all poops file
        df_list.append(data)

        print(f"Cleaned {user}'s poops\n")
    
    # Creating the All_Poops file
    df = pd.concat(df_list, ignore_index=True)
    df = df.sort_values(by="IDs").reset_index(drop=True)
    df.to_csv("Save Files 2/Poops/All Poops.csv")
    
def test_cleaning(user):
    numbers = extracting_number_messages(user)
    possibilities = creating_possibility_poops(numbers)
    poop_numbers = refine_possibilities(possibilities)
    recollect_data(poop_numbers)

# DISPLAYING ON GRAPHS
def display_specific_poops(users=[], time_period=(), labels=True, legend=False):
    # INPUT 
    # users         : Array of users refactored names as strings, if [] it will use all users
    # time_period   : Tuple of two timestamps like (start_time, finish_time)

    # Acquiring users as a numpy array
    if not users:
        users = np.array(pd.read_csv("Save Files 2/Users.csv")["user"])
    else:
        users = np.array(users)

    # Fixing Ticking
    plt.rc("xtick", labelsize=7)
    plt.rc("ytick", labelsize=15)

    for user in users:
        # Acquiring correct time period
        if time_period:
            start_time, end_time = time_period[0], time_period[1]
        else:
            start_time, end_time = pd.to_datetime("2025-01-01 00:00:01"), pd.to_datetime("2025-12-31 23:59:59")

        MEGAFRAME = pd.read_csv(f"Save Files 2/Poops/{user}_Poops.csv")
        MEGAFRAME["timestamp"] = pd.to_datetime(MEGAFRAME["timestamp"])
        filtered_MEGAFRAME = MEGAFRAME[(MEGAFRAME['timestamp'] >= start_time) & (MEGAFRAME['timestamp'] <= end_time)]
        poops = filtered_MEGAFRAME['Poop']
        poop_days = filtered_MEGAFRAME['timestamp']
        plt.plot(poop_days, poops, label=user)

        if labels:
            plt.text(list(poop_days)[-1], list(poops)[-1], user, fontsize=5, in_layout=False, fontweight='bold', backgroundcolor='white', verticalalignment='top', horizontalalignment='right')

    plt.xlabel("Day")
    plt.ylabel("Poop Number")
    if legend:
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.subplots_adjust(right=0.8)

    plt.title("Specific Poop Graph")

    plt.show()

def like_sender(pie=False, only_poops=False):
    if only_poops:
        df = pd.read_csv("Save Files 2/Poops/All Poops.csv")
    else:
        df = pd.read_csv("Save Files 2/All_Raw_Data.csv")
    users = list(pd.read_csv("Save Files 2/Users.csv")["user"])

    # Setting up the likes dataframe
    likes = {}
    for user in users:
        likes[user] = 0

    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        for user in reactors:
            likes[user] += 1

    if pie:
        labels = []
        slices = []
        total = 0
        for name in likes.keys():
            labels.append(f"{name} {likes[name]}")
            slices.append(int(likes[name]))
            total += likes[name]

        plt.rcParams.update({'font.size': 7})
        plt.pie(slices, labels = labels)
        plt.title(f"Total Likes Sent : {total}")
        plt.show()

    return likes

def decode_reactions(reaction_list):
    # INPUT 
    # reaction_list        : A string of the reactions to a particular message, as shown in the All_Raw_Data.csv reactions column

    # OUTPUT
    # new_reactors      : List of strings of the refactored names of the users that reacted to the message

    # reaction_list is a string of what is in the reactions column, a string of a list of dictionaries
    if pd.isna(reaction_list):
        return []
    reaction_list = reaction_list.split("'")

    # Extracting original names
    names = []
    file = open("DATA/refactor_names_config.txt", encoding="utf8")
    for line in file.readlines():
        line = line.strip().split(": ")
        names.append(line[0])
        names.append(line[1])
        if len(line) == 3:
            names.append(line[2])
    file.close()

    # Extracting reactors
    reactors = []
    for entry in reaction_list:
        if entry in names:
            reactors.append(entry)
        elif entry == ': "Niamh O':
            reactors.append("Niamh O'Neill")

    # Getting refactored names of reactors
    file = open("DATA/refactor_names_config.txt", encoding="utf8")
    new_reactors = []
    for line in file.readlines():
        line = line.strip().split(": ")
        for reactor in reactors:
            if reactor in line:
                new_reactors.append(line[1])
    file.close()

    return new_reactors
    
def order_dictionary(dic):
    # INPUT
    # dic       : Dictionary with keys, and numbers for values

    ordered_list = sorted(list(dic.values()), reverse=True)
    for value in ordered_list:
        keys = [key for key, val in dic.items() if val == value]
        print(f"{keys[0]} : {value}")

def dynamic_bar_chart():
    pygame.init()
    sc_w, sc_h = 1200, 700
    wn = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("2025 POOP WAR")
    clock = pygame.time.Clock()

    users = pd.read_csv("Save Files 2/Users.csv")["user"]
    date_font = pygame.font.SysFont("Ariel", 40)
    df = pd.read_csv("Save Files 2/Poops/All Poops.csv")

    # Creating user bar charts
    colours = [
    (255, 0, 0),      # Bright Red
    (0, 255, 0),      # Bright Green
    (0, 0, 255),      # Bright Blue
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (255, 20, 147),   # Deep Pink
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (75, 0, 130),     # Indigo
    (0, 255, 127),    # Spring Green
    (255, 105, 180),  # Hot Pink
    (127, 255, 0),    # Chartreuse
    (255, 69, 0),     # Red-Orange
    (0, 191, 255),    # Deep Sky Blue
    (148, 0, 211),    # Dark Violet
    (0, 128, 255),    # Vivid Blue
    (255, 0, 127),    # Bright Pink
    (46, 139, 87),    # Sea Green
    (255, 223, 0),    # Golden Yellow
    (186, 85, 211),   # Medium Orchid
    (255, 140, 0),    # Dark Orange
    (144, 238, 144),  # Light Green
    (30, 144, 255),   # Dodger Blue
    (220, 20, 60),    # Crimson
    (238, 130, 238)   # Violet
    ]
    bars = []
    place = 0
    for user in users:
        colour = colours[place]
        bars.append(Bar(user, place, colour))
        place += 1

    poop_dict = {}
    for user in users:
        poop_dict[user] = 0

    bg = pygame.image.load("pictures/bar_chart_bg.jpg")
    image_size = (sc_w, sc_h)
    bg = pygame.transform.scale(bg, image_size)

    wait_time = 30

    index = 0
    while True:
        clock.tick(12)
        wn.fill((0, 0, 0))
        wn.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        title_font = pygame.font.SysFont("Ariel", 60)
        title_text = title_font.render("POOP WAR 2025", 1, (0, 0, 0))
        wn.blit(title_text, (sc_w/2 - title_text.get_width()/2, 10))
        
        # Update Poop Dict
        if wait_time < 0 or wait_time == 30:
            if index < len(df["Poop"]) - 1:
                poop_dict[df["user"][index]] = int(df["Poop"][index])
                index += 1
                sorted_data = dict(sorted(poop_dict.items(), key=lambda item: item[1], reverse=True))
                for bar in bars:
                    bar.update(sorted_data)

            # Display Text
            for bar in bars:
                bar.draw(wn)

            # Display Date
            date = datetime.strptime(df["timestamp"][index], "%Y-%m-%d %H:%M:%S")
            day, month = date.day, date.strftime("%B")
            date_text = date_font.render(f"{day} of {month}", 1, (0, 0, 0))
            wn.blit(date_text, (sc_w - date_text.get_width() - 20, sc_h - date_text.get_height() - 10))

        wait_time -= 1
        pygame.display.update()

class Bar(object):
    def __init__(self, user, place, colour):
        self.user = user
        self.place = place
        self.colour = colour
        self.length = 0
        self.poop = 0
        self.y = self.place*27
        self.x = 0

    def draw(self, wn):
        # User Name Text
        font = pygame.font.SysFont("Ariel", 26)
        text = font.render(self.user, 1, (0, 0, 0))
        wn.blit(text, (30, 85 + self.y))

        # Bar
        pygame.draw.rect(wn, self.colour, (150, 85 + self.y, self.x, 20))

        # Write the poop count
        text = font.render(str(int(self.poop)), 1, (0, 0, 0))
        wn.blit(text, (160 + self.x, 85 + self.y))

    def update(self, data):
        # Finding place
        sorted_keys = list(data.keys())
        self.place = sorted_keys.index(self.user)
        self.poop = data[self.user]

        # Finding bar Length
        highest = list(data.items())[0]
        user, poop = highest
        self.length = 1000*(self.poop/poop)

        # Moving the bar
        dy = self.place*27 - self.y
        if dy != 0:
            if -15 < dy < 15:
                self.y = self.place * 27
            else:
                self.y += dy/5

        # Moving the length of the bar
        dx = self.length - self.x
        if dx != 0:
            if -13 < dx < 13:
                self.x = self.length
            else:
                self.x += dx/5

def compare_year_poops(user, directories, time_period=None):
    # INPUT
    # user              :   String of the refactored user name
    # directories       :   A list of strings of the directories of multpile json data files
    # time_period       :   A tuple of two timestamps, the start time and the end time

    # Recleaning each year fo the user
    dfs = {}
    for directory in directories:
        whole_df = extract_raw_data(directory, save=False)
        whole_df["Unnamed: 0"] = whole_df.index
        filtered_df = whole_df[whole_df["user"] == user]
        filtered_df = filtered_df.drop(columns=["user"])
        filtered_df = filtered_df.rename(columns={"Unnamed: 0" : "Message ID"})
        filtered_df = filtered_df.reset_index(drop=True)
        df = extracting_number_messages(user, filtered_df)
        df = creating_possibility_poops(df)
        df = refine_possibilities(df)
        whole_df = whole_df.rename(columns={"Unnamed: 0" : "IDs"})
        recollected_df = pd.merge(df, whole_df, on="IDs", how="inner")
        df = recollected_df.drop(columns=["share", "photos", "videos", "call_duration"])

        # Adjusting to the time period
        year = str(pd.to_datetime(df["timestamp"][0]).year)
        if time_period:
            start_time, end_time = time_period[0], time_period[1]
            start_time = start_time.replace(year=int(year))
            end_time = end_time.replace(year=int(year))
        else:
            start_time, end_time = pd.to_datetime(f"{year}-01-01 00:00:01"), pd.to_datetime(f"{year}-12-31 23:59:59")

        df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]


        dfs[year] = df

    # Plotting each on a graph
    plt.rc("xtick", labelsize=7)
    plt.rc("ytick", labelsize=15)
    for key in dfs.keys():
        dfs[key]["timestamp"] = pd.to_datetime(dfs[key]["timestamp"])
        poops = dfs[key]['Poop']
        poop_days = dfs[key]['timestamp']
        poop_days = pd.to_datetime(poop_days)
        poop_days = poop_days.apply(lambda x: x.replace(year=1969))
        plt.plot(poop_days, poops, label=key)
    
    plt.xlabel("Day")
    plt.ylabel("Poop Number")
    plt.xticks(rotation=45)
    plt.legend()
    plt.title(f"{user}'s Poop Comparison Graph")

    plt.show()

def smooth_display_specific_poops(users=[], time_period=(), labels=True, scatter=False):
    # INPUT 
    # users         : Array of users refactored names as strings, if [] it will use all users
    # time_period   : Tuple of two timestamps like (start_time, finish_time)

    # Acquiring users as a numpy array
    if not users:
        users = np.array(pd.read_csv("Save Files 2/Users.csv")["user"])
    else:
        users = np.array(users)

    # Fixing Ticking
    plt.rc("xtick", labelsize=7)
    plt.rc("ytick", labelsize=15)

    for user in users:
        # Acquiring correct time period
        if time_period:
            start_time, end_time = time_period[0], time_period[1]
        else:
            start_time, end_time = pd.to_datetime("2025-01-01 00:00:01"), pd.to_datetime("2025-12-31 23:59:59")

        MEGAFRAME = pd.read_csv(f"Save Files 2/Poops/{user}_Poops.csv")
        MEGAFRAME["timestamp"] = pd.to_datetime(MEGAFRAME["timestamp"])
        filtered_MEGAFRAME = MEGAFRAME[(MEGAFRAME['timestamp'] >= start_time) & (MEGAFRAME['timestamp'] <= end_time)]

        start = pd.to_datetime("2025-01-01 00:00:01")
        filtered_MEGAFRAME['hours_since_year_start'] = (filtered_MEGAFRAME['timestamp'] - start).dt.total_seconds() / 3600
        x = list(filtered_MEGAFRAME['hours_since_year_start'])
        y = list(filtered_MEGAFRAME['Poop'])
        x = np.array(x).reshape(-1, 1)
        y = np.array(y).reshape(-1, 1)

        x_grid = np.arange(min(x), max(x), 0.1)
        x_grid = x_grid.reshape((len(x_grid), 1))

        poly_reg = PolynomialFeatures(degree=5)
        poop_poly = poly_reg.fit_transform(x)
        lin_reg = LinearRegression()
        lin_reg.fit(poop_poly, y)

        if scatter:
            plt.scatter(x, y, label=user)
        plt.plot(x_grid, lin_reg.predict(poly_reg.fit_transform(x_grid)))

        if labels:
            plt.text(x[-1], y[-1], user, fontsize=6, fontweight='bold', backgroundcolor='white', verticalalignment='top', horizontalalignment='right')

    plt.xlabel("Day")
    plt.ylabel("Poop Number")

    plt.title("Specific Poop Graph")

    plt.show()

def leaderboard():
    # Setting up screen
    pygame.init()
    sc_w, sc_h = 800, 600
    wn = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("2025 POOP LEADERBOARD")
    clock = pygame.time.Clock()

    # Collecting Leaderboard
    users = np.array(pd.read_csv("Save Files 2/Users.csv")["user"])
    leaders = {}
    total = 0
    for name in users:
        poops = list(pd.read_csv(f"Save Files 2/Poops/{name}_Poops.csv")["Poop"])[-1]
        leaders[name] = poops
        total += poops
    print(f"Average Poops = {total/21}")

    ordered_list = sorted(list(leaders.values()), reverse=True)
    leader = []
    
    for value in ordered_list:
        keys = [key for key, val in leaders.items() if val == value and [key, val] not in leader]
        leader.append([keys[0], value])
   
    bg = pygame.image.load("pictures/Leaderboard_bg.jpg")
    image_size = (sc_w, sc_h)
    bg = pygame.transform.scale(bg, image_size)
    running = True
    while running:
        pygame.display.update()
        wn.fill((255, 255, 255))
        wn.blit(bg, (0,0))
        clock.tick(24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Title
        title_font = pygame.font.SysFont("Ariel", 60)
        title = title_font.render("January Leaderboard!!!", 1, (0, 0, 0))
        wn.blit(title, (sc_w/2 - title.get_width()/2, 25))

        # Users
        place = 1
        for index in range(len(leader)):
            user_font = pygame.font.SysFont("Ariel", 30)
            position = user_font.render(f"{place} - {leader[index][0]} with {leader[index][1]}", 1, (0, 0, 0))
            wn.blit(position, (110 + (index//11)*400, 80 + (index%11)*45))
            place += 1

        # Total Poops
        total_font = pygame.font.SysFont("Ariel", 45)
        total_text = total_font.render(f"Total Poops : {total}", 1, (0, 0, 0))
        wn.blit(total_text, (sc_w/2 - total_text.get_width()/2, sc_h - 10 - total_text.get_height()))

def poops_per_day():
    df = pd.read_csv("Save Files 2/Poops/All Poops.csv")

    timestamps = [1]
    poops = []
    current_timestamp = 1
    poop_count = 0

    for i in range(len(df["Poop"])):
        date = datetime.strptime(df["timestamp"][i], "%Y-%m-%d %H:%M:%S").day
        if current_timestamp != date:
            timestamps.append(date)
            current_timestamp = datetime.strptime(df["timestamp"][i], "%Y-%m-%d %H:%M:%S").day
            poops.append(poop_count)
            poop_count = 0
        else:
            poop_count += 1
    poops.append(poop_count)

    plt.bar(timestamps, poops, color='skyblue')
    plt.title("Group Poops Each Day")
    plt.xlabel("Day of the Month")
    plt.ylabel("Num Poops")
    plt.show()

# Function to create a heatmap of time of day for each poop of a user
def daily_poop_heatmap(user, separate_days=False):
    # INPUT
    # user          : String of refactored user name to be plotted
    # separate_days : Bool saying whether it should be accumulated to one day or a week

    # OUTPUT
    # seaborns heatmap of the time of day the user updates

    # Loading and configuring data
    df = pd.read_csv(f"Save Files 2/Poops/{user}_Poops.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if not separate_days:
        df["hour"] = df["timestamp"].dt.hour

        # Count the number of entries for each hour
        hour_counts = df["hour"].value_counts().sort_index()

        # Convert to a dataframe and reshape for heatmap
        heatmap_data = hour_counts.reindex(range(24), fill_value=0).to_frame()
        heatmap_data.columns = ["Counts"]

        # Create the heatmap
        plt.figure(figsize=(4, 8))  # Adjust figure size for vertical orientation
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=True,
            xticklabels=False,  
            yticklabels=range(24), 
            annot_kws={"size": 7}
        )
        plt.ylabel("Hour of Day")
        plt.title(f"{user}'s Daily Poop Heatmap")
        plt.show()
    else:
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.day_name()
        
        hours = range(24)  
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Create a complete index of days and hours
        heatmap_data = (
            df.groupby(["day_of_week", "hour"])
            .size()
            .unstack(fill_value=0)  
            .reindex(index=days, columns=hours, fill_value=0)  
        )
        
        vmin, vmax = heatmap_data.values.min(), heatmap_data.values.max()

        # Create the heatmaps
        fig, axes = plt.subplots(1, 7, figsize=(20, 8), sharey=True)
        cmap = sns.color_palette("Blues", as_cmap=True)

        for ax, (day, data) in zip(axes, heatmap_data.iterrows()):
            sns.heatmap(
                data.to_frame(), 
                annot=True,
                fmt="g",
                cmap="Blues",
                cbar=False,  
                vmin = vmin,
                vmax = vmax,
                ax=ax,
                xticklabels=True, 
                yticklabels=range(24),
                annot_kws={"size": 6}
            )
            ax.set_title(day)
            if ax == axes[0]:
                ax.set_ylabel("Hour of Day")
            else:
                ax.set_ylabel("")

        # Add a single global color bar
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  
        norm = plt.Normalize(vmin=vmin, vmax=vmax) 
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  
        fig.colorbar(sm, cax=cbar_ax, label="Entry Counts")

        plt.subplots_adjust(wspace=0.4)
        fig.suptitle(f"{user}'s Weekly Poop Heatmap", fontsize=16)
        plt.show()





#extract_and_clean_all_data(DIRECTORY)
#leaderboard()
#display_specific_poops(labels=True, legend=True)
#dynamic_bar_chart()
#like_sender(pie=True, only_poops=True)
#poops_per_day()
compare_year_poops("Eoin", [DIRECTORY, "DATA/messages/inbox/poopooheads"], time_period=[pd.to_datetime("1969-01-01 00:00:01"), pd.to_datetime(f"1969-02-28 00:00:01")])

#users = get_users(DIRECTORY)
#for user in users:
#    daily_poop_heatmap(user=user)