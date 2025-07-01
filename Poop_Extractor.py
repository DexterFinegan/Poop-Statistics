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
from datetime import datetime, timedelta
import calendar

DIRECTORY = "DATA/messages/inbox/2025poopchat"
MAXPOOP = 400

# EXTRACTING AND CLEANING DATA
def extract_raw_data(directory):
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
    MEGAFRAME.to_csv("Save Files/All_Raw_Data.csv")
    print("Successfully Extracted and Saved Raw Data File")
    return  MEGAFRAME

def get_users():
    # INPUT #
    # refector  : Boolean - denoting whether names should be refactored

    # Accessing Refactor names config file
    file = open("DATA/refactor_names_config.txt", encoding="utf8")
    usernames = []
    for line in file.readlines():
        line = line.strip()
        line = line.split(": ")
        usernames.append(line[1])
    file.close()

    MEGAFRAME = pd.DataFrame({"user": usernames})

    # Saving to csv file
    MEGAFRAME.to_csv("Save Files/Users.csv")

    # Making a JSON File for users data
    data = {}
    for user in usernames:
        data[user] = {}
    with open("user_data.json", "w") as f:
        json.dump(data, f, indent=4)


    print("Successfully Extracted and Saved User Names")
    return MEGAFRAME["user"]

def separate_users():
    # Loading all relevant data to dataframes
    raw_data = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")["user"]
    
    for user in users:
        # Creating User's Messages
        filtered_df = raw_data[raw_data["user"] == user]
        filtered_df = filtered_df.drop(columns=["user"])
        filtered_df = filtered_df.rename(columns={"Unnamed: 0" : "Message ID"})
        filtered_df = filtered_df.reset_index(drop=True)
        
        # Saving File
        file_name = str(user) + "_Messages.csv"
        filtered_df.to_csv(f"Save Files/Messages/{file_name}")

def extracting_number_messages(user, provided_df=None):
    if provided_df is None:
        df = pd.read_csv(f"Save Files/Messages/{user}_Messages.csv", index_col=0)
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
    length = MAXPOOP
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
    full_df = pd.read_csv("Save Files/All_Raw_Data.csv")
    full_df = full_df.rename(columns={"Unnamed: 0" : "IDs"})
    recollected_df = pd.merge(df, full_df, on="IDs", how="inner")
    recollected_df = recollected_df.drop(columns=["share", "photos", "videos", "call_duration", "audio_files", "gifs"])

    file_name = str(recollected_df["user"][0]) + "_Poops.csv"
    recollected_df.to_csv(f"Save Files/Poops/{file_name}")
    return recollected_df

def extract_and_clean_all_data(directory):
    extract_raw_data(directory)
    users = get_users()
    separate_users()

    df_list = []
    
    for user in users:
        numbers = extracting_number_messages(user)
        possibilities = creating_possibility_poops(numbers)
        poop_numbers = refine_possibilities(possibilities)
        data = recollect_data(poop_numbers)

        # For the all poops file
        df_list.append(data)

        print(f"Cleaned {user}'s poops")
    
    # Creating the All_Poops file
    df = pd.concat(df_list, ignore_index=True)
    df = df.sort_values(by="IDs").reset_index(drop=True)
    df.to_csv("Save Files/Poops/All Poops.csv")
    print("Cleaned All Files Well")

def find_double_poops(user):
    # Smoothing out data
    df = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    for i in range(1, len(df) - 1):
        prev = df["timestamp"].iloc[i-1]
        curr = df["timestamp"].iloc[i]
        next = df["timestamp"].iloc[i+1]
        delta = next - curr
        if delta < pd.Timedelta(minutes=5):
            df.loc[i, "timestamp"] = prev + (curr - prev)/2
    
    return df

# DISPLAYING ON GRAPHS
def display_specific_poops(users=[], time_period=(), labels=True, legend=False, save=False, show=False):
    # INPUT 
    # users         : Array of users refactored names as strings, if [] it will use all users
    # time_period   : Tuple of two timestamps like (start_time, finish_time)

    # Acquiring users as a numpy array
    if not users:
        users = np.array(pd.read_csv("Save Files/Users.csv")["user"])
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

        MEGAFRAME = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
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

    if save:
        plt.savefig("Export Assets/Specific poop graph.png", bbox_inches="tight")
    if show:
        plt.show()

def like_sender(pie=False, only_poops=False, save=False):
    if only_poops:
        df = pd.read_csv("Save Files/Poops/All Poops.csv")
    else:
        df = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = list(pd.read_csv("Save Files/Users.csv")["user"])

    # Setting up the likes dataframe
    likes = {}
    for user in users:
        likes[user] = 0

    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        for user in reactors:
            likes[user] += 1

    if pie or save:
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
        if save:
            plt.savefig("Export Assets/Likes sender.png")
        if pie:
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
    ordered_dict = {}
    for value in ordered_list:
        keys = [key for key, val in dic.items() if val == value]
        count = 0
        if keys[count] not in ordered_dict.keys():
            ordered_dict[keys[count]] = int(value)
        else:
            count += 1
    return ordered_dict

def dynamic_bar_chart():
    pygame.init()
    sc_w, sc_h = 1200, 700
    wn = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("2025 POOP WAR")
    clock = pygame.time.Clock()

    users = pd.read_csv("Save Files/Users.csv")["user"]
    date_font = pygame.font.SysFont("Ariel", 40)
    df = pd.read_csv("Save Files/Poops/All Poops.csv")

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

def compare_year_poops(user, directories, time_period=None, save=False, show=False):
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
        poop_days = poop_days.apply(lambda x: x.replace(year=2024))
        plt.plot(poop_days, poops, label=key)
    
    plt.xlabel("Day")
    plt.ylabel("Poop Number")
    plt.xticks(rotation=45)
    plt.legend()
    plt.title(f"{user}'s Poop Comparison Graph")

    if save:
        plt.savefig(f"Export Assets/comp-{user}.png", bbox_inches="tight")
    if show:
        plt.show()

def leaderboard():
    # Function to update the json file of everyones position at the end of each month and the poops they were on
    print("Rejigging leaderboard data for users")
    users = list(pd.read_csv("Save Files/Users.csv")["user"])
    poop_dict = {}
    all_ends_to_months = get_end_of_current_month(all_months=True)
    # Finding the last poop of all users for each month and adding it to their Json file
    with open("user_data.json", "r") as f:
        data = json.load(f)
    f.close()
    
    for user in users:
        df = find_double_poops(user)
        poop_dict[user] = {}
        for month in all_ends_to_months:
            highest = 0
            for i in range(len(df)):
                if df["timestamp"][i] < month and df["Poop"][i] > highest:
                    highest = df["Poop"][i]
                else:
                    poop_dict[user][month.strftime("%B")] = int(highest)
                    break
                poop_dict[user][month.strftime("%B")] = int(highest)
        data[user]["monthly_scores"] = poop_dict[user]
        data[user]["position"] = {}
    
    # Finding the positions of each player in each month
    for month in all_ends_to_months:
        rankings = {}
        for user in poop_dict.keys():
            rankings[user] = poop_dict[user][month.strftime("%B")]
        ordered_rankings = order_dictionary(rankings)
        count = 1
        for user in ordered_rankings.keys():
            data[user]["position"][month.strftime("%B")] = count
            count += 1
    
    with open("user_data.json", "w") as f:
        json.dump(data, f, indent=4)
    f.close()

def poops_per_day(save=False):
    df = pd.read_csv("Save Files/Poops/All Poops.csv")

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
    if save:
        plt.savefig("Export Assets/poops per day.png", bbox_inches="tight")
    plt.show()

def daily_poop_heatmap(user, separate_days=False, save=False, show=False):
    # INPUT
    # user          : String of refactored user name to be plotted
    # separate_days : Bool saying whether it should be accumulated to one day or a week

    # OUTPUT
    # seaborns heatmap of the time of day the user updates

    # Loading and configuring data
    df = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
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
        name = ""
        if separate_days:
            name = str(user) + "'s weekly heatmap"
        else:
            name = str(user) + "'s daily heatmap"

        if save:
            print(f"Saving: h2-{name}.png")
            plt.savefig(f"Export Assets/h2-{name}.png", bbox_inches="tight")
        if show:
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
        name = ""
        if separate_days:
            name = str(user) + "'s weekly heatmap"
        else:
            name = str(user) + "'s daily heatmap"

        if save:
            print(f"Saving: h1-{name}.png")
            plt.savefig(f"Export Assets/h1-{name}.png", bbox_inches="tight")
        if show:
            plt.show()

def shortest_time_between_poops(user):
    # Finding the shortest time between poops
    df = find_double_poops(user)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    shortest = 90000000
    for i in range(1, len(df) - 1):
        curr = df["timestamp"].iloc[i]
        next = df["timestamp"].iloc[i+1]
        delta = (next - curr).total_seconds()
        if delta < shortest:
            shortest = delta
    
    # Converting the shortest time to hours minutes
    days = np.floor(((shortest/60)/60)/24)
    hours = np.floor(((shortest - days*24*60*60)/60)/60)
    minutes = np.floor((shortest - days*24*60*60 - hours*60*60)/60)
    seconds = shortest - days*24*60*60 - hours*60*60 - minutes*60
    print(f"{user}'s Shortest Time Between Poops is {days} Days, {hours} Hours, {minutes} Minutes and {seconds} Seconds")

def longest_time_between_poops(user):
    # Finding the longest time between poops
    df = find_double_poops(user)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    longest = 0
    for i in range(1, len(df) - 1):
        curr = df["timestamp"].iloc[i]
        next = df["timestamp"].iloc[i+1]
        delta = (next - curr).total_seconds()
        if delta > longest:
            longest = delta
    
    # Converting the longest time to hours minutes
    days = np.floor(((longest/60)/60)/24)
    hours = np.floor(((longest - days*24*60*60)/60)/60)
    minutes = np.floor((longest - days*24*60*60 - hours*60*60)/60)
    seconds = longest - days*24*60*60 - hours*60*60 - minutes*60
    print(f"{user}'s Longest Time Between Poops is {days} Days, {hours} Hours, {minutes} Minutes and {seconds} Seconds")

def find_sd(user):
    df = find_double_poops(user)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    total_time = df["timestamp"].iloc[-1] - pd.to_datetime("2025-01-01 00:00:01")
    avg = (total_time / df["Poop"].iloc[-1]).total_seconds()
    sum = 0
    for i in range(1, len(df) - 1):
        curr = df["timestamp"].iloc[i]
        next = df["timestamp"].iloc[i+1]
        delta = (next - curr).total_seconds()
        sum += (delta - avg)**2
    sd = timedelta(seconds=np.sqrt(sum/len(df)))
    print(f"{user}'s Standard Deviation is {sd}")
    avg = timedelta(seconds=avg)
    print(f"      68% of their shits happen within {avg - sd} and {avg + sd} of their last shit")

def interpersonal_relationships(user):
    # Function to find how much a user interacts with every other user and vice versa
    
    # Making a dictionary for each user
    users = list(pd.read_csv("Save Files/Users.csv")["user"])
    users.append("Total")
    user_df = pd.DataFrame(columns=["user", "likes_received", "poop_likes_received"])
    user_df["user"] = users
    user_df["likes_received"] = 0
    user_df["poop_likes_received"] = 0
    user_df["likes_sent"] = 0
    user_df["poop_likes_sent"] = 0
    user_df["likes_above_them"] = 0
    user_df["poop_likes_above_them"] = 0
    user_df["proportion_of_their_likes_received"] = 0
    user_df["proportion_of_your_likes_sent"] = 0

    # Finding how many likes received total
    df = pd.read_csv(f"Save Files/Messages/{user}_Messages.csv")
    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        for username in reactors:
            row = user_df.index[user_df["user"] == username][0]
            user_df.at[row, "likes_received"] += 1
            row = user_df.index[user_df["user"] == "Total"][0]
            user_df.at[row, "likes_received"] += 1
    
    # Finding just the poop likes received
    df = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        for username in reactors:
            row = user_df.index[user_df["user"] == username][0]
            user_df.at[row, "poop_likes_received"] += 1
            row = user_df.index[user_df["user"] == "Total"][0]
            user_df.at[row, "poop_likes_received"] += 1

    # Finding how many likes a user has sent to all other users
    df = pd.read_csv("Save Files/All_Raw_Data.csv")
    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        liked_user = df["user"][i]
        if user in reactors:
            row = user_df.index[user_df["user"] == liked_user][0]
            user_df.at[row, "likes_sent"] += 1
            row = user_df.index[user_df["user"] == "Total"][0]
            user_df.at[row, "likes_sent"] += 1

    # Finding how many likes sent to all other users poops
    df = pd.read_csv("Save Files/Poops/All Poops.csv")
    for i in range(len(df)):
        reactors = decode_reactions(df["reactions"][i])
        liked_user = df["user"][i]
        if user in reactors:
            row = user_df.index[user_df["user"] == liked_user][0]
            user_df.at[row, "poop_likes_sent"] += 1
            row = user_df.index[user_df["user"] == "Total"][0]
            user_df.at[row, "poop_likes_sent"] += 1
    
    # Adding the amount of likes youve sent more than received per person
    for i in range(len(user_df)):
        user_df["likes_above_them"][i] = user_df["likes_sent"][i] - user_df["likes_received"][i]
        user_df["poop_likes_above_them"][i] = user_df["poop_likes_sent"][i] - user_df["poop_likes_received"][i]

    # Working out proportions of likes sent
    row = user_df.index[user_df["user"] == "Total"][0]
    total_likes_sent = user_df["likes_sent"][row]
    for i in range(len(user_df)):
        user_df["proportion_of_your_likes_sent"][i] = str(round((user_df["likes_sent"][i]/total_likes_sent)*100, 2)) + "%"

    # Working out proportions of likes received
    likes = like_sender()
    for i in range(len(user_df) - 1):
        user_df["proportion_of_their_likes_received"][i] = str(round((user_df["likes_received"][i]/likes[user_df["user"][i]])*100,2)) + "%"

    user_df.to_csv(f"{user}_stats.csv", index=False)
    
def content_sharer(pie=False, save=False, biggest_content=False):
    # Finding a pie chart of everyone to see who shares the most links/photos/videos
    df = pd.read_csv("Save Files/All_Raw_Data.csv")

    num_links = {}
    num_link_likes = {}
    num_photos = {}
    num_photo_likes = {}
    num_videos = {}
    num_video_likes = {}
    total_shares = {}
    total_share_likes = {}
    users = list(pd.read_csv("Save Files/Users.csv")["user"])
    for user in users:
        num_links[user] = 0
        num_link_likes[user] = 0
        num_photos[user] = 0
        num_photo_likes[user] = 0
        num_videos[user]= 0 
        num_video_likes[user] = 0
        total_shares[user] = 0
        total_share_likes[user] = 0

    biggest_link = {}
    biggest_photo = {}
    for i in range(0, 21):
        biggest_link[i] = []
        biggest_photo[i] = []

    for i in range(len(df)):
        # Links
        if not pd.isna(df["share"][i]):
            link = df["share"][i].split("'")[3]
            likers = decode_reactions(df["reactions"][i])
            biggest_link[len(likers)].append(link)
            sender = df["user"][i]
            num_links[sender] += 1
            num_link_likes[sender] += len(likers)
            total_shares[sender] += 1
            total_share_likes[sender] += len(likers)
        

        # Photos
        if not pd.isna(df["photos"][i]):
            photo = df["photos"][i].split("'")[3]
            likers = decode_reactions(df["reactions"][i])
            biggest_photo[len(likers)].append(photo)
            sender = df["user"][i]
            num_photos[sender] += 1
            num_photo_likes[sender] += len(likers)
            total_shares[sender] += 1
            total_share_likes[sender] += len(likers)

        # Videos
        if not pd.isna(df["videos"][i]):
            video = df["videos"][i].split("'")[3]
            likers = decode_reactions(df["reactions"][i])
            biggest_photo[len(likers)].append(video)
            sender = df["user"][i]
            num_videos[sender] += 1
            num_video_likes[sender] += len(likers)
            total_shares[sender] += 1
            total_share_likes[sender] += len(likers) 
    
    if biggest_content:
        for i in range(0, 21):
            if len(biggest_link[i]) > 0:
                print(f"{len(biggest_link[i])} links have {i} likes")

        for i in range(0, 21):
            if len(biggest_photo[i]) > 0:
                print(f"{len(biggest_photo[i])} photos/videos have {i} likes")
        
        return biggest_link, biggest_photo


    total_content_ratio = {}
    for user in users:
        if total_shares[user] != 0:
            total_content_ratio[user] = round(total_share_likes[user]/total_shares[user], 2)
        else:
            total_content_ratio[user] = 0

   
    all_pie_data = {"Biggest Reels Sender": num_links, 
                    "Most Popular Reels Sender": num_link_likes,
                    "Biggest Photo Sender": num_photos,
                    "Most Popular Photo Sender": num_photo_likes,
                    "Biggest Video Sender": num_videos,
                    "Most Popular Video Sender": num_video_likes,
                    "Biggest Content Sharer" : total_shares,
                    "Funniest Content Sharer" : total_share_likes,
                    "Number of likes per share": total_content_ratio}

    if pie or save:
        for key in all_pie_data.keys():
            labels = []
            slices = []
            total = 0
            for name in all_pie_data[key].keys():
                labels.append(f"{name} {all_pie_data[key][name]}")
                slices.append(int(all_pie_data[key][name]))
                total += all_pie_data[key][name]

            plt.rcParams.update({'font.size': 7})
            plt.pie(slices, labels = labels)
            plt.title(f"{key} : {total}")
            if save:
                plt.savefig(f"Export Assets/{key}.png")
            if pie:
                plt.show()

def delete_all_export_files():
    # Function to clear all export files ready for new ones
    path = "Export Assets"
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("Old Export Assets Deleted")

def get_end_of_current_month(all_months=False):
    # Function to get the last day of the current month
    now = datetime.now()
    last_day = calendar.monthrange(now.year, now.month)[1]
    print(f"Last Day of this month is {datetime(year=now.year, month=now.month, day=last_day, hour=23, minute=59, second=59)}")
    if all_months:
        months = []
        for i in range(now.month):
            last_day = calendar.monthrange(now.year, i + 1)[1]
            months.append(datetime(year=now.year, month=i+1, day=last_day, hour=23, minute=59, second=59))
        return months
    else:
        return datetime(year=now.year, month=now.month, day=last_day, hour=23, minute=59, second=59)
