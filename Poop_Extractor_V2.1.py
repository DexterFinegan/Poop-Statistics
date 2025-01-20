# 4/8/24
# Newest Renewed and refined version of the instagram poop data analysis programme
# Will reuse a lot of code from Version 2
# See Goals.txt to see previous goals and new goals for this programme

import pandas as pd
import os
import json
import ast
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime, date
import pygame
import numpy as np

DIRECTORY = "DATA/messages/inbox/poopooheads"

# Function to Extract raw data from the instagram json file to a dataframe
# This will include replacing the names of users to more readable ones, and resetting index order
# Saves to All_Raw_Data.csv file
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

    # Replacing user's names to more readable ones
    MEGAFRAME["sender_name"].replace({"\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                        "Stephen Allen": "Stephen",
                                        "Conor Mcmenamin": "Conor",
                                        "Dan Griffin": "Dan",
                                        "Ros Hanley": "Ros",
                                        "Jack McRann": "Jack",
                                        "lalala lucky to have me here": "Soumia",
                                        "Katie Long": "Katie",
                                        "Conan Davis": "Conan" }, inplace=True)
    
    # Reversing indexes to be in chronological order 
    MEGAFRAME = MEGAFRAME.reset_index(drop=True)

    # Removing the "is_geoblocked_for_viewer" key because idek what that is
    MEGAFRAME.drop(["is_geoblocked_for_viewer"], axis=1, inplace= True)

    # Saving to csv file
    MEGAFRAME.to_csv("Save Files/All_Raw_Data.csv")

    print("Successfully Extracted and Saved Raw Data File")

# Function to get a list of all the users of the groupchat
# Saves to Users.csv file
def get_users(directory, refactor=True):
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
    
    # Refactoring names to be more legible, custom in code and assumed works
    if refactor:
        MEGAFRAME["name"].replace({"\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                    "Stephen Allen": "Stephen",
                                    "Conor Mcmenamin": "Conor",
                                    "Dan Griffin": "Dan",
                                    "Ros Hanley": "Ros",
                                    "Jack McRann": "Jack",
                                    "lalala lucky to have me here": "Soumia",
                                    "Katie Long": "Katie" }, inplace=True)

    # Saving to csv file
    MEGAFRAME.to_csv("Save Files/Users.csv")

    print("Successfully Extracted and Saved User Names")

# Function to seperate all the raw data messages into individual user csv files from files in Save Files Folder
def separate_users():
    # Loading all relevant data to dataframes
    raw_data = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")

    # Iterating through each user
    for i in range(len(users)):
        user = users["name"][i]
        print(f"\nExtracting {user}'s Messages Now\n")

        # Creating a dictionary of a particular users messages
        messages = {"content" : [],
                    "timestamp" : [],
                    "reactions" : [],
                    "share" : [],
                    "audio_files" : [],
                    "photos" : [],
                    "videos" : [],
                    "call_duration" : []}
        
        # Iterating over every message to dissect which is a particular users
        for j in range(len(raw_data)):
            if raw_data["sender_name"][j] == user:
                messages["content"].append(raw_data["content"][j])
                messages["timestamp"].append(raw_data["timestamp"][j])
                messages["share"].append(raw_data["share"][j])
                messages["audio_files"].append(raw_data["audio_files"][j])
                messages["photos"].append(raw_data["photos"][j])
                messages["videos"].append(raw_data["videos"][j])
                messages["call_duration"].append(raw_data["call_duration"][j])

                # Must do reactions more intensely
                reactions = []
                if not pd.isna(raw_data["reactions"][j]):
                    if "x9d" in raw_data["reactions"][j]:
                        reactions.append("Eoin")
                    if "Stephen Allen" in raw_data["reactions"][j]:
                        reactions.append("Stephen")
                    if "Conor Mcmenamin" in raw_data["reactions"][j]:
                        reactions.append("Conor")
                    if "Dan Griffin" in raw_data["reactions"][j]:
                        reactions.append("Dan")
                    if "Ros Hanley" in raw_data["reactions"][j]:
                        reactions.append("Ros")
                    if "Jack McRann" in raw_data["reactions"][j]:
                        reactions.append("Jack")
                    if "lalala lucky to have me here" in raw_data["reactions"][j]:
                        reactions.append("Soumia")
                    if "Katie Long" in raw_data["reactions"][j]:
                        reactions.append("Katie")
                    if "Conan" in raw_data["reactions"][j]:
                        reactions.append("Conan")
                    if "Dex" in raw_data["reactions"][j]:
                        reactions.append("Dex")
                messages["reactions"].append(reactions)
        
        # Converting the dictionary into a pandas DataFrame
        MEGAFRAME = pd.DataFrame(data=messages)

        # Saving to a csv file in the Save Files Messages Folder
        file_name = str(user) + "_Messages.csv"
        MEGAFRAME.to_csv(f"Save Files/Messages/{file_name}")

        print(f"\n{user}'s Messages have been Successfully Extracted and Saved\n")

# Function to clean a user's raw message data to a dataframe of just their poops
# Saves to a poop file in Save Files Poops
def clean_users_poop_data(user):
    # INPUTS
    # user      :   String - the users refactored name to be cleaned

    # Loading relevant file
    MEGAFRAME = pd.read_csv(f"Save Files/Messages/{user}_Messages.csv")
    print(f"Beginning to clean {user}'s Poop Data\n")

    # Dropping Irrelevant headers (keeping reactions for further use but to be dormant for now)
    drop_list = ["share", "audio_files", "photos", "videos", "call_duration"]
    MEGAFRAME.drop(drop_list, axis=1, inplace= True)

        #### Removing messages that don't have ANY numbers in them and isolating the numbers ####
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    messages = {"content" : [], "timestamp" : [], "reactions" : []}

    # Iterating over every message from this user
    for i in range(len(MEGAFRAME)):
        message = MEGAFRAME["content"][i]
        new_message = ""
        # Iterating through each character and comparing it to numbers
        if not pd.isna(message):
            for char in message:
                if char in numbers:
                    new_message += char
                elif char == " " and new_message != "":
                    messages["content"].append(int(new_message))
                    messages["timestamp"].append(MEGAFRAME["timestamp"][i])
                    messages["reactions"].append(MEGAFRAME["reactions"][i])    # Left for later 
                    new_message = ""
            if new_message != "":
                messages["content"].append(int(new_message))
                messages["timestamp"].append(MEGAFRAME["timestamp"][i])
                messages["reactions"].append(MEGAFRAME["reactions"][i])    # Left for later 
                new_message = ""

    MEGAFRAME = pd.DataFrame(data=messages)

        #### Refining to more likely numbers by comparing to the numberth message ####
    messages = {"content" : [], "timestamp" : [], "reactions" : []}
    count = 1
    for i in range(len(MEGAFRAME)):
        number = int(MEGAFRAME["content"][i])
        if count*0.4 < number <= count*2:
            count += 1
            messages["content"].append(number)
            messages["timestamp"].append(MEGAFRAME["timestamp"][i])
            messages["reactions"].append(MEGAFRAME["reactions"][i])    # Left for later 
    
    MEGAFRAME = pd.DataFrame(data=messages)

        #### Making a list of chains of consecutive numbers ####
    chains = []
    chain = []
    for i in range(len(MEGAFRAME)):
        if len(chain) == 0:
            chain.append([MEGAFRAME["content"][i], MEGAFRAME["timestamp"][i], MEGAFRAME["reactions"][i]])
        else:
            if MEGAFRAME["content"][i] == chain[-1][0] + 1:
                chain.append([MEGAFRAME["content"][i], MEGAFRAME["timestamp"][i], MEGAFRAME["reactions"][i]])
            else:
                chains.append(chain)
                chain = [[MEGAFRAME["content"][i], MEGAFRAME["timestamp"][i], MEGAFRAME["reactions"][i]]]
    if len(chain) > 0:
        chains.append(chain)

        #### Making a list of long chains ####
    long_chains = [] 
    for chain in chains:
        if len(chain) > 1:
            long_chains.append(chain)
    
        #### Joining consecutive long chains ####
    refined_long_chains = []
    new_chain = []
    for i in range(len(long_chains)):
        if len(new_chain) == 0:
            new_chain = long_chains[i]
        else:
            if long_chains[i][0][0] == new_chain[-1][0] + 1:
                for j in range(len(long_chains[i])):
                    new_chain.append(long_chains[i][j])
            elif long_chains[i][0][0] == new_chain[-1][0]:
                for j in range(len(long_chains[i]) - 1):
                    new_chain.append(long_chains[i][j+1])
            else:
                refined_long_chains.append(new_chain)
                new_chain = long_chains[i]
    refined_long_chains.append(new_chain)

        #### Checking if chains over lap ####
    final_count = []
    for chain in refined_long_chains:
        final_count += chain

        #### Converting back to messages dictionary ####
    messages = {"content" : [], "timestamp" : [], "reactions" : []}
    for update in final_count:
        messages["content"].append(update[0])
        messages["timestamp"].append(update[1])
        messages["reactions"].append(update[2])
    
    MEGAFRAME = pd.DataFrame(data=messages)

    # Saving DataFrame to csv file
    file_name = str(user) + "_Poops.csv"
    MEGAFRAME.to_csv(f"Save Files/Poops/{file_name}")

    print(f"{user}'s Poops have been Successfully Cleaned and Saved\n")

def combine_poops():

    users = pd.read_csv("Save Files/Users.csv")
    dataframes = []
    for user in users["name"]:
        df = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
        df["user"] = user
        df = df.drop(columns=["Unnamed: 0"])

        print(df)
        dataframes.append(df)

    combined_df = pd.concat(dataframes)
    combined_df = combined_df.sort_values(by='timestamp')
    combined_df = combined_df.reset_index(drop=True)

    combined_df.to_csv(f"Save Files/Poops/All_Poops.csv")

# Function to display poops on a graph, used to verify if clean poops function works
def display_poops(user):
    # INPUTS
    # user      :   String - the users refactored name to be plotted on a graph

    # Loading relevant file
    MEGAFRAME = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
    poops = MEGAFRAME["content"]

    plt.plot(poops, "o")

    plt.xlabel("Entry")
    plt.ylabel("Poop Number")
    plt.title(f"{user}'s Poop Cleaning Consistency")

    plt.show()

# Function to re-do all functions to reset the data when downloading the data again
def remake_files(directory):
    # Extraction
    extract_raw_data(directory)
    get_users(directory)
    separate_users()

    # Cleaning
    users = pd.read_csv("Save Files/Users.csv")
    for user in users["name"]:
        clean_users_poop_data(user)

    combine_poops()

# Function to create a heatmap of time of day for each poop of a user
def daily_poop_heatmap(user, separate_days=False):
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

# Function to find the number of messages each user has sent to the chat
def total_messages():
    # Creating workspace
    data = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")["name"]

    messages = {}
    for name in users:
        messages[name] = 0

    # Counting messages
    for i in range(len(data["content"])):
        messages[data["sender_name"][i]] += 1
    
    return messages

# Function to collect data of all likes received by a selected user
def likes_received(selected_user, total=False, just_poops=False, display=False):
    # INPUTS
    # selected_user     : String of a refactored users name
    # total             : Bool of whether to display the total accumulated likes received
    # just_poops        : Bool of whether this search should be on just poop messages
    # display           : Bool of whether display this information on a pie chart

    # OUTPUTS
    # data              : dictionary of every users name as a key a number of likes given to the selected user as the data
    # total_likes       : Integer of the total likes received by this user

    # Setting up the list and dictionary
    users = pd.read_csv("Save Files/Users.csv")
    users = users["name"]
    data = {}
    for user in users:
        data[user] = 0

    # Creating Dictionary
    if just_poops:
        raw_data = pd.read_csv(f"Save Files/Poops/{selected_user}_Poops.csv")
    else:
        raw_data = pd.read_csv(f"Save Files/Messages/{selected_user}_Messages.csv")
    for i in raw_data["reactions"]:
        i = ast.literal_eval(i)
        for name in i:
            data[name] += 1
    
    # Counting Total Likes
    if total:
        total_likes = 0
        for name in data.keys():
            total_likes += data[name]

    # Creating Pie Chart
    if display:
        labels = []
        slices = []
        for name in data.keys():
            label = name + " " + str(data[name])
            labels.append(label)
            slices.append(data[name])

        plt.pie(slices, labels=labels)
        plt.title(f"Likes Received by {selected_user}")
        plt.show()
    
    if total:
        return data, total_likes
    else:
        return data

# Function to acquire an compare the total likes of each user
def total_likes_received(just_poops=False, display=False):
    # INPUTS
    # just_poops        : Bool whether to investigate just poop messages
    # display           : Bool whether to display information into a pie chart

    # OUTPUTS
    # total_likes       : Dictionary of each user and their total received likes

    # Creating workspace
    users = pd.read_csv("Save Files/Users.csv")["name"]
    total_likes = {}
    for name in users:
        data, likes = likes_received(name, total=True, just_poops=just_poops)
        total_likes[name] = likes
    
    # Creating Pie Chart
    if display:
        labels = []
        slices = []
        for name in total_likes.keys():
            label = name + " " + str(total_likes[name])
            labels.append(label)
            slices.append(total_likes[name])

        plt.pie(slices, labels=labels)
        plt.title(f"Likes Received Comaprison")
        plt.show()
    
# Function to generate how many likes a selected user has given
def total_likes_given(just_poops=False, display=False, self_provided=False):
    # INPUTS
    # just_poops    : Bool whether to investigate just the poop messages
    # display       : Bool whether to display total information
    # self_provided  : Bool whether to create a new dictionary of total likes given to ones' self

    # OUTPUTS
    # given_likes   : Dictionary of all users and the amount of likes they've given
    # self_provided_likes   : Dictionary of all users number of likes given to themselves

    # Setting up workspace
    users = pd.read_csv("Save Files/Users.csv")["name"]
    given_likes = {}
    self_provided_likes = {}
    for name in users:
        given_likes[name] = 0
        self_provided_likes[name] = 0
    
    for name in users:
        data = likes_received(selected_user=name, just_poops=just_poops)
        for name2 in data.keys():
            if name2 != name:
                given_likes[name2] += data[name2]
            else:
                if self_provided:
                    self_provided_likes[name] += data[name]

    
    # Creating Pie Chart
    if display:
        labels = []
        slices = []
        for name in given_likes.keys():
            label = name + " " + str(given_likes[name])
            labels.append(label)
            slices.append(given_likes[name])

        plt.pie(slices, labels=labels)
        plt.title(f"Likes Given Comaprison")
        plt.show()
    
    if self_provided:
        return given_likes, self_provided_likes
    else:
        return given_likes

# Function to find the biggest content sharer (links, gifs & photos)
def biggest_content_sharer(display=False):
    # INPUTS
    # display       : Bool whether to display data on a pie chart

    # OUTPUTS
    # sharers       : dictionary of all users and how much they've shared to the chat

    all_data = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")["name"]

    sharers = {}
    for name in users:
        sharers[name] = 0

    for i in range(len(all_data["share"])):
        if not pd.isna(all_data["share"][i]):
            sharers[all_data["sender_name"][i]] += 1

    for i in range(len(all_data["photos"])):
        if not pd.isna(all_data["photos"][i]):
            sharers[all_data["sender_name"][i]] += 1
    
    # Creating Pie Chart
    if display:
        labels = []
        slices = []
        for name in sharers.keys():
            label = name + " " + str(sharers[name])
            labels.append(label)
            slices.append(sharers[name])

        plt.pie(slices, labels=labels)
        plt.title(f"Content Sharers")
        plt.show()

    return sharers

# Function to calculate approximate lifetime poops of each user
def lifetime_approximation(month=12):
    # INPUTS
    # month         : Integer of the month of latest data intake

    # STATICS
    avg_lifetime = 82.66 # years
    days_alive = avg_lifetime*365

    # Calculate total number of days spent
    numdays = (date(2024, month, 28) - date(2024, 1, 1)).days

    # Find highest poop of each user
    users = pd.read_csv("Save Files/Users.csv")["name"]
    lifetime_poops = {}
    for user in users:
        data = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
        lifetime_poops[user] = int((data["content"].iloc[-1]/numdays)*days_alive)
    
    return lifetime_poops

# Function to find the longest airtime of all users
def airtime_per_user():
    # OUTPUTS
    # longest_airtime       : Dictionary of all users with the longest time they've been aired for
    # total_airtime         : Dictionary of all users with the total time they've been aired for
    # avg_airtime           : Dictionary of the average amount of airtime a user receives

    # Setting up workspace
    data = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")["name"]
    date_format = '%Y-%m-%d %H:%M:%S'

    longest_airtime = {}
    total_airtime = {}
    for name in users:
        longest_airtime[name] = 0
        total_airtime[name] = 0

    # Iterating through all messages to find the longest airtime
    for i in range(len(data["timestamp"]) - 1):
        date_str1 = data["timestamp"][i]
        date_str2 = data["timestamp"][i + 1]

        date_obj1 = datetime.strptime(date_str1, date_format)
        date_obj2 = datetime.strptime(date_str2, date_format)
        timediff = date_obj2 - date_obj1

        name = data["sender_name"][i]
        if longest_airtime[name] == 0 or timediff > longest_airtime[name]:
            longest_airtime[name] = timediff
        if total_airtime[name] == 0:
            total_airtime[name] = timediff
        else:
            total_airtime[name] += timediff

    # Average Airtime
    messages = total_messages()
    avg_airtime = {}
    for name in users:
        avg_airtime[name] = total_airtime[name] / messages[name]
        
    # Converting teimdeltas to strings
    for name in users:
        longest_airtime[name] = str(longest_airtime[name])
        total_airtime[name] = str(total_airtime[name])
        avg_airtime[name] = str(avg_airtime[name])
    
    return longest_airtime, total_airtime, avg_airtime

# Function to count the number of times a word was sent to chat
def count_word(word, display=False, per_user=False):
    # INPUT
    # word      : String of the word to count
    # display   : Bool whether to print each message containing the counted word
    # per_user  : Bool whether to make a dictionary containing the number of times each user said the counted word

    # OUTPUT
    # count     : Integer of the count of how many times the word has found

    messages = pd.read_csv("Save Files/All_Raw_Data.csv")
    users = pd.read_csv("Save Files/Users.csv")["name"]
    count = 0

    if per_user:
        counters = {}
        for name in users:
            counters[name] = 0

    for i in range(len(messages)):
        if not pd.isna(messages["content"][i]):
            if word in messages["content"][i]:
                count += messages["content"][i].count(word)

                if display:
                    string = str(messages["content"][i])
                    print(f"{string} : {count}")

                if per_user:
                    counters[messages["sender_name"][i]] += messages["content"][i].count(word)

    if per_user:
        return count, counters

    return count

def display_dynamic_barchart():
    pygame.init()
    w, h = 800, 600
    wn = pygame.display.set_mode((w, h))
    pygame.display.set_caption("2024 Poop Graph")
    clock = pygame.time.Clock()

    users = pd.read_csv("Save Files/Users.csv")
    poop_dict = {}
    for user in users:
        poop_dict[user] = 0

    date = date(2024, 1, 1)

    while True:
        print(date)
        date = date + pd.Timedelta(days=1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        pygame.display.update()

def display_all_poops():
    df = pd.read_csv("Save Files/Poops/All_Poops.csv")
    users = pd.read_csv("Save Files/Users.csv")
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
                poop.append(df["content"][index])
        plt.plot(poop_days, poop, label=user)
    
    # Plotting and displaying graph + legend
    plt.title("ALL OUR POOPS")
    plt.legend()
    plt.show()

# Function to display poops from a user (or more), over a specific time period
def display_specific_poops(users=[], time_period=()):
    # INPUT 
    # users         : Array of users refactored names as strings, if [] it will use all users
    # time_period   : Tuple of two timestamps like (start_time, finish_time)

    # Acquiring users as a numpy array
    if not users:
        users = np.array(pd.read_csv("Save Files/Users.csv")["name"])
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
            start_time, end_time = pd.to_datetime("2024-01-01 00:00:01"), pd.to_datetime("2024-12-31 23:59:59")

        MEGAFRAME = pd.read_csv(f"Save Files/Poops/{user}_Poops.csv")
        MEGAFRAME["timestamp"] = pd.to_datetime(MEGAFRAME["timestamp"])
        filtered_MEGAFRAME = MEGAFRAME[(MEGAFRAME['timestamp'] >= start_time) & (MEGAFRAME['timestamp'] <= end_time)]
        poops = filtered_MEGAFRAME['content']
        poop_days = filtered_MEGAFRAME['timestamp']

        plt.plot(poop_days, poops, label=user)

    plt.xlabel("Day")
    plt.ylabel("Poop Number")
    plt.legend()
    plt.title("Specific Poop Graph")

    plt.show()


# Call Space to work out kinks and represent data
using = True
if using:
    time = (pd.to_datetime("2024-01-01 01:00:00"), pd.to_datetime("2024-02-01 01:00:00"))
    display_specific_poops(time_period=time)