# Contains all functions for extracting data from source

# Module Imports
import pandas as pd
import os
import json

# Function to Extract all messages from a json file in a specific directory within the folder
def extract_data(directory): 
    # INPUT #
    # directory : String - detailing path to groupchat folder

    # OUTPUT #
    # MEGAFRAME : pandas DataFrame with every message

    # Creating and extracting json file to dataframe of messages
    MEGAFRAME = pd.DataFrame()
    FILES = os.listdir(directory)
    for file in FILES:
        if file.endswith(".json"):
            with open(f"{directory}/{file}") as jf:
                JSON_DATA = json.load(jf)
                df = pd.DataFrame(JSON_DATA["messages"])
                MEGAFRAME = pd.concat([MEGAFRAME, df])

    # Changing timestamp in dataframe to date and time
    MEGAFRAME['timestamp_ms'] = pd.to_datetime(MEGAFRAME['timestamp_ms'], unit='ms')

    # Reversing order so indexes start at the beginning of the group chat
    MEGAFRAME = MEGAFRAME[::-1]

    return MEGAFRAME


# Function to remove columns in dataframe
def data_drop(MEGAFRAME, drop_list):
    # INPUT #
    # MEGAFRAME : pandas dataframe
    # drop_list : List of Strings of columns in MEGAFRAME to drop

    # OUTPUT #
    # MEGAFRAME : pandas dataframe with removed columns

    MEGAFRAME.drop(drop_list, axis=1, inplace= True)

    return MEGAFRAME

# Function to refactor names in dataframe - must alter for each set of users
def replace_names(MEGAFRAME):
    # INPUT #
    # MEGAFRAME : pandas dataframe

    # OUTPUT #
    # MEGAFRAME : pandas dataframe with refactored names, custom applied in function

    MEGAFRAME["sender_name"].replace({"Finn Blaumann": "Finn",
                                    "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                        "Stephen Allen": "Stephen",
                                        "Conor Mcmenamin": "Conor",
                                        "Dan Griffin": "Dan",
                                        "Ros Hanley": "Ros",
                                        "Jack McRann": "Jack",
                                        "lalala lucky to have me here": "Soumia",
                                        "Katie Long": "Katie" }, inplace=True)

    return MEGAFRAME

# Function to return all members of the group
def get_users(directory, refactor=False):
    # INPUT #
    # directory : String - detailing path to groupchat folder
    # refector  : Boolean - denoting whether names should be refactored

    # OUTPUT #
    # MEGAFRAME : pandas DataFrame with every user of the groupchat

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
        MEGAFRAME["name"].replace({"Finn Blaumann": "Finn",
                                    "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                        "Stephen Allen": "Stephen",
                                        "Conor Mcmenamin": "Conor",
                                        "Dan Griffin": "Dan",
                                        "Ros Hanley": "Ros",
                                        "Jack McRann": "Jack",
                                        "lalala lucky to have me here": "Soumia",
                                        "Katie Long": "Katie" }, inplace=True)

    return MEGAFRAME

# Function to return a dataframe of solely one users messages
def messages_sent_by(MEGAFRAME, user, sender_col_name="sender_name", content_col_name="content", time_col_name="timestamp_ms"):
    # INPUT #
    # MEGAFRAME     :   pandas DataFrame - containing all messages, preferably with refactored names
    # user          :   String - users name as shown in dataframe of messages to isolate
    # sender_col_name   :   String - In the case that the username in the dataframe is not "sender_name", this can be used to replace it
    # content_col_name  :   String - In the case that the content of the message in the dataframe is not "content", this cane be used to replace it
    # time_col_name :   String - In the case that the time in the dataframe is not "timestamp_ms", this can be used to replace it

    # OUTPUT #
    # User_messages :   pandas DataFrame - containing only the messages of the user selected
    
    # Creating Dictionary with keys being the timestamp and data being the message
    User_messages = {}                          

    # Iterating through all rows in MEGAFRAME
    for i,row in MEGAFRAME.iterrows():
        if row[sender_col_name] == user:
            if not pd.isna(row[content_col_name]):                                 # Not including NaN messages
                User_messages[str(row[time_col_name])] = row[content_col_name]
    
    return User_messages

# Function to quickly format the print of dictionary messages of a given user
def display_user_messages(User_messages):
    # INPUT #
    # User_messages :   Dictionary - of one users messages, keys being timestamps, data being the content of the message

    for key in User_messages.keys():
        print(f"{key} : {User_messages[key]}\n")

# Function to extract all gifs sent my a users (For Jack)
def gifs_sent_by(MEGAFRAME, user, sender_col_name="sender_name"):
    # INPUT #
    # MEGAFRAME     :   pandas DataFrame - containing all messages, preferably with refactored names
    # user          :   String - users name as shown in dataframe of messages to isolate
    # sender_col_name   :   String - In the case that the username in the dataframe is not "sender_name", this can be used to replace it

    # OUTPUT #
    # User_gifs     :   pandas DataFrame - containing only the gifs of the user selected
    
    # Creating Dictionary with keys being the timestamp and data being the gif link
    User_gifs = {}                          

    # Iterating through all rows in MEGAFRAME
    gif_num = 0
    for i,row in MEGAFRAME.iterrows():
        if row[sender_col_name] == user:
            if not pd.isna(row["share"]):                                # Not including NaN shares
                if not pd.isna(row["share"]["link"]):                    # Not including NaN links
                    if "giphy" in row["share"]["link"]:                  # Checking the link is a giphy link
                        User_gifs[str(row["timestamp_ms"])] = "g" + str(gif_num)
                        gif_num += 1
    
    return User_gifs

# Function to merge a users poops with the gifs they sent (if they were annoying enough to use gifs primarily)
def merge_messages_and_gifs(clean_df, unclean_df, user):
    # INPUT #
    # clean_df      :   pandas DataFrame - containing all poop messages, preferably with refactored names
    # unclean_df    :   pandas DataFrame - containing all messages sent by the user to the chat, with refactored names
    # user          :   String - users name as shown in dataframe of messages to isolate

    # OUTPUT #
    # df            :   pandas DataFrame - containg all poops of individual

    ## Not ready yet, isn't optimized ##
    
    # Collecting relevant messages into two dictionaries
    messages = messages_sent_by(clean_df, user, sender_col_name="user", content_col_name="poop", time_col_name="timestamp")
    gifs = gifs_sent_by(unclean_df, user)

    # Sorting through both dictionaries to create a DataFrame
    final = []
    for key in messages.keys():
        dictionary = {}
        dictionary["timestamp"] = key
        dictionary["poop"] = messages[key]
        final.append(dictionary)

    for key in gifs.keys():
        dictionary = {}
        dictionary["timestamp"] = key
        dictionary["poop"] = gifs[key]
        final.append(dictionary)

    df = pd.DataFrame(final)

    # Cleaning DataFrame
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed").dt.date
    df = df.sort_values(by="timestamp", ascending=True)

    return df