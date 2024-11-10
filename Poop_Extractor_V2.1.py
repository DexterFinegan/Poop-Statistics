# 4/8/24
# Newest Renewed and refined version of the instagram poop data analysis programme
# Will reuse a lot of code from Version 2
# See Goals.txt to see previous goals and new goals for this programme

import pandas as pd
import os
import json
import ast
from Clean import *

DIRECTORY = "DATA/messages/inbox/weaponsofassdestruction"

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
                messages["reactions"].append(raw_data["reactions"][j])
                messages["share"].append(raw_data["share"][j])
                messages["audio_files"].append(raw_data["audio_files"][j])
                messages["photos"].append(raw_data["photos"][j])
                messages["videos"].append(raw_data["videos"][j])
                messages["call_duration"].append(raw_data["call_duration"][j])
        
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
    print(f"Beginning to clean {user}'s Poop Data\n\n")

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
                    messages["reactions"].append("")    # Left for later 
                    new_message = ""
            if new_message != "":
                messages["content"].append(int(new_message))
                messages["timestamp"].append(MEGAFRAME["timestamp"][i])
                messages["reactions"].append("")    # Left for later 
                new_message = ""

    MEGAFRAME = pd.DataFrame(data=messages)

        #### Refining to more likely numbers by comparing to the numberth message ####
    messages = {"content" : [], "timestamp" : [], "reactions" : []}
    for i in range(len(MEGAFRAME)):
        number = int(MEGAFRAME["content"][i])
        if i*0.3 < number < i*2:
            messages["content"].append(number)
            messages["timestamp"].append(MEGAFRAME["timestamp"][i])
            messages["reactions"].append("")    # Left for later 
    
    MEGAFRAME = pd.DataFrame(data=messages)

        #### Creating Chains of consecutive updates ####
    chain = [MEGAFRAME["content"][0]]
    messages = {"content" : [], "timestamp" : [], "reactions" : []}
    for i in range(1, len(MEGAFRAME)):
        if int(MEGAFRAME["content"][i]) == int(chain[-1]) + 1:
            chain.append(MEGAFRAME["content"][i]) 
        else:
            if len(chain) > 1:
                for j in range(len(chain)):
                    backtracking = len(chain) - j
                    messages["content"].append(chain[j])
                    messages["timestamp"].append(MEGAFRAME["timestamp"][i - backtracking])
                    messages["reactions"].append("")    # Left for later 
            chain = [MEGAFRAME["content"][i]]
    MEGAFRAME = pd.DataFrame(data=messages)

        #### Checking for and removing duplicate updates ####
    all_updates = list(MEGAFRAME["content"])
    if len(all_updates) != len(set(all_updates)):
        messages = {"content" : [], "timestamp" : [], "reactions" : []}
        for i in range(len(all_updates)):
            if all_updates[i] not in messages["content"]:
                messages["content"].append(MEGAFRAME["content"][i])
                messages["timestamp"].append(MEGAFRAME["timestamp"][i])
                messages["reactions"].append("")    # Left for later
    MEGAFRAME = pd.DataFrame(data=messages)

        #### Filling in missing data by evenly spacing missed updates in their correct places ####
    messages = {"content" : [MEGAFRAME["content"][0]], "timestamp" : [MEGAFRAME["timestamp"][0]], "reactions" : [""]}
    correct_datetime_objects(MEGAFRAME)

    # The rest of the updates
    for i in range(1, len(MEGAFRAME)):
        print(i)
        print(MEGAFRAME["content"][i])
        print(messages["content"][i - 1])
        if MEGAFRAME["content"][i] == messages["content"][i - 1] + 1:
            print("True")
            messages["content"].append(MEGAFRAME["content"][i])
            messages["timestamp"].append(MEGAFRAME["timestamp"][i])
            messages["reactions"].append("")    # Left for later
        else: 
            missing_updates = MEGAFRAME["content"][i] - MEGAFRAME["content"][i-1]
            time_period = abs(MEGAFRAME["timestamp"][i - 1] - MEGAFRAME["timestamp"][i])
            for j in range(missing_updates):
                messages["content"].append(MEGAFRAME["content"][i - 1] + j + 1)
                messages["timestamp"].append(MEGAFRAME["timestamp"][i - 1] + time_period*(j+1)/missing_updates)
                messages["reactions"].append("")    # Left for later
            
        MEGAFRAME = pd.DataFrame(data=messages)

    # Saving DataFrame to csv file
    file_name = str(user) + "_Poops.csv"
    MEGAFRAME.to_csv(f"Save Files/Poops/{file_name}")

    print(f"\n{user}'s Poops have been Successfully Cleaned and Saved\n")

# Function to correct loaded dataframe to have string timestamps to datetime.datetime objects
def correct_datetime_objects(df):
    # INPUT #
    # df    :   pandas Dataframe with a "timestamp" column

    # OUTPUT #
    # df  :   pandas DataFrame with "timestamp" colum filled with corresponding pandas datetime objects

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    df["timestamp"] = df["timestamp"].dt.round("1s")

    return df


# Function to calculate number of likes sent to a particular person from all other users as a dictionary
def likes_roster(users, selected_user):
    # INPUT #
    # users :   pandas Dataframe of all users
    # selected_user  :   string of the selected user

    # OUTPUT #
    # roster :  list of every other user's likes to you

    # Loading users messages and creating other users dictionary
    if selected_user != "all":
        all_messages = pd.read_csv(f"Save Files/Messages/{selected_user}_Messages.csv")
    else:
        all_messages = pd.read_csv("Save Files/All_Raw_Data.csv")
    roster = {}
    for user in users["name"]:
        roster[user] = 0

    # Iterating through messages and counting likes
    for reaction in all_messages["reactions"]:
        if not pd.isna(reaction):
            if "x93¸ð" in reaction:
                roster["Eoin"] += 1
            if "Stephen Allen" in reaction:
                roster["Stephen"] += 1
            if "Conor Mcmenamin" in reaction:
                roster["Conor"] += 1
            if "Dan Griffin" in reaction:
                roster["Dan"] += 1
            if "Ros Hanley" in reaction:
                roster["Ros"] += 1
            if "Jack McRann" in reaction:
                roster["Jack"] += 1
            if "Conan" in reaction:
                roster["Conan"] += 1
            if "lalala lucky to have me here" in reaction:
                roster["Soumia"] += 1
            if "Katie Long" in reaction:
                roster["Katie"] += 1
            if "Dex" in reaction:
                roster["Dex"] += 1

    # Note : Could not change reactions list/dictionary from dtring back to list/dictionary so had to find thru string, must fix
    return roster


# Call Space to work out kinks and represent data
using = True
if using:
    users = pd.read_csv("Save Files/Users.csv")
    user = "Stephen"
    roster = likes_roster(users, user)

    print(f"{user}'s Roster : {roster}")

    all_likes = likes_roster(users, "all")
    percentages = {}
    for user in roster.keys():
        percentages[user] = roster[user]/all_likes[user] * 100

    print(f"Percentages : {percentages}")




