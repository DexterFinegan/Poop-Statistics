# Similar to the poop extractor, this script will analyse messages to calculate popular messages and senders

# Modules to import
from Extract import *
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate total likes for each user
def total_likes(df, users):
    # INPUT #
    # df    :   pandas DataFrame - containing all messages sent into chat with refactored usernames
    # users :   pandas DataFrame - containing the refactored names of all users

    # OUTPUT #
    # num_likes_dict    :   Dictionary - with keys as users names, and data being the total number of reactions they received

    num_likes_dict = {}
    for user in users["name"]:
        num_likes = 0
        for index in range(len(df)):
            if df["sender_name"][index] == user:
                if isinstance(df["reactions"][index], list):
                    num_likes += len(df["reactions"][index])
        num_likes_dict[user] = num_likes

    return num_likes_dict

# Function to calculate the total likes given out 
def total_sent_likes(df, users):
    # Setting up Dictionary
    num_likes_dict = {}
    for index in range(len(users)):
        num_likes_dict[users["name"][index]] = 0

    # Counting Likes given by each person
    for index in range(len(df)):
        if isinstance(df["reactions"][index], list):
            for reaction in df["reactions"][index]:
                name = reaction["actor"]
                if name == "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7":
                    name = "Eoin"
                elif name == "lalala lucky to have me here":
                    name = "Soumia"
                elif name == "Conor Mcmenamin":
                    name = "Conor"
                elif name == "Stephen Allen":
                    name = "Stephen"
                elif name == "Dan Griffin":
                    name = "Dan"
                elif name == "Ros Hanley":
                    name = "Ros"
                elif name == "Katie Long":
                    name = "Katie"
                elif name == "Jack McRann":
                    name = "Jack"
                
                num_likes_dict[name] += 1
    return num_likes_dict

                

# Function to calculate the total number of messages sent by each user
def total_sent_messages(df, users):
    # INPUT #
    # df    :   pandas DataFrame - containing all messages sent into chat with refactored usernames
    # users :   pandas DataFrame - containing the refactored names of all users

    # OUTPUT #
    # total_messages_dict    :   Dictionary - with keys as users names, and data being the total number of messages sent

    num_messages_dict = {}
    for user in users["name"]:
        num_messages = 0
        for index in range(len(df)):
            if df["sender_name"][index] == user:
                num_messages += 1
        num_messages_dict[user] = num_messages
    
    return num_messages_dict

# Function to calculate the amount of reactions per message a user sends
def like_to_messsage_ratio(df, users):
    # INPUT #
    # df    :   pandas DataFrame - containing all messages sent into chat with refactored usernames
    # users :   pandas DataFrame - containing the refactored names of all users

    # OUTPUT #
    # ratio_dict    :   Dictionary - with keys as users names, and data being the ratio of likes per message sent

    ratio_dict = {}
    num_likes_dict = total_likes(df, users)
    num_messages_dict = total_sent_messages(df, users)

    for user in users["name"]:
        if num_messages_dict[user] != 0:
            ratio_dict[user] = num_likes_dict[user]/num_messages_dict[user]
        else:
            ratio_dict[user] = "Inconclusive"

    return ratio_dict

# Function to calculate top reacted to messages
def top_liked_messages(df):
    # INPUT #  
    # df    :   pandas DataFrame - containing all messages sent into chat with refactored usernames

    # OUTPUT #
    # liked_messages    :   pandas DataFrame - containing liked messages

    # Creating a list of dictionaries of each top rated message and their contents
    top_liked_list = []

    # Iterating through DataFrame
    for index in range(len(df)):
        if isinstance(df["reactions"][index], list):
            if len(df["reactions"][index]) >= 5:
                dictionary = {}
                dictionary["user"] = df["sender_name"][index]
                dictionary["num_likes"] = len(df["reactions"][index])
                dictionary["text"] = df["content"][index]
                dictionary["photo"] = df["photos"][index]
                dictionary["date"] = df["timestamp_ms"][index]
                top_liked_list.append(dictionary)

    liked_messages = pd.DataFrame(top_liked_list)
    liked_messages = liked_messages.sort_values(by="num_likes", ascending=False)
    return liked_messages

# Function to calculate the average time it takes for the next person to respond to your messages   UNFINISHED
def average_airtime(df, users, messages):
    # INPUT #
    # df    :   pandas DataFrame, cleaned
    # users :   pandas DataFrame - containing the refactored names of all users
    # messages : dictionary - containing keys of user names and data of total sent messages

    # OUTPUT #
    # airtimes  :   dictionary, keys are names, data is average air time

    airtimes = {}
    date_format = '%Y-%m-%d %H:%M:%S'

    for user in users["name"]:
        total_airtime = 0
        for index in range(len(df)):
            if df["user"][index] == user:
                stamp = df["timestamp"][index]
                print(f"As String : {type(stamp)}")
                time = datetime.strptime(stamp, date_format)

                print(f"Time = {time}, Type = {type(time)}")
                if index + 1 < len(df):
                    if total_airtime == 0:
                        total_airtime = datetime.strptime(df["timestamp"][index + 1], date_format) - datetime.strptime(df["timestamp"][index], date_format)
                    else:
                        total_airtime += datetime.strptime(df["timestamp"][index + 1], date_format) - datetime.strptime(df["timestamp"][index], date_format)
        print(f"{user} has {total_airtime} amount of airtime")

        avg_airtime = total_airtime / messages[user]
        airtimes[user] = avg_airtime
    
    print(airtimes)
    return airtimes