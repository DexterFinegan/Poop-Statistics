# Similar to the poop extractor, this script will analyse messages to calculate popular messages and senders

# Modules to import
from Extract import *
import pandas as pd

# Creating the DataFrame and list of users
df = extract_data(directory="DATA/messages/inbox/2023poopcounter")
df = replace_names(df)
df = df.reset_index(drop=True)
users = get_users(directory="DATA/messages/inbox/2023poopcounter", refactor=True)

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
        ratio_dict[user] = num_likes_dict[user]/num_messages_dict[user]

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
