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

# Function to refactor names in dataframe
def replace_names(MEGAFRAME):
    # INPUT #
    # MEGAFRAME : pandas dataframe

    # OUTPUT #
    # MEGAFRAME : pandas dataframe with refactored names, custom applied in function

    MEGAFRAME["sender_name"].replace({'shauna\u00f0\u009f\u00a6\u0089': "Shauna",
                                    "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                        "Neo O'Herlihy": "Neo",
                                        "Conor Mcmenamin": "Conor",
                                        "Noel Brassil": "Noel",
                                        "Ros Hanley": "Ros",
                                        "Jack McRann": "Jack" }, inplace=True)

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
        MEGAFRAME["name"].replace({'shauna\u00f0\u009f\u00a6\u0089': "Shauna",
                                        "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                            "Neo O'Herlihy": "Neo",
                                            "Conor Mcmenamin": "Conor",
                                            "Noel Brassil": "Noel",
                                            "Ros Hanley": "Ros",
                                            "Jack McRann": "Jack" }, inplace=True)

    return MEGAFRAME

# Function to return a dataframe of solely one users messages
def messages_sent_by(MEGAFRAME, user):
    # INPUT #
    # MEGAFRAME     :   pandas DataFrame - containing all messages, preferably with refactored names
    # user          :   String - users name as shown in dataframe of messages to isolate

    # OUTPUT #
    # MEGAFRAME     :   pandas DataFrame - containing only the messages of the user selected
    
    # Creating Dictionary with keys being the timestamp and data being the message
    User_messages = {}                          

    # Iterating through all rows in MEGAFRAME
    for i,row in MEGAFRAME.iterrows():
        if row["sender_name"] == user:
            if not pd.isna(row["content"]):                                 # Not including NaN messages
                User_messages[str(row["timestamp_ms"])] = row["content"]
    
    return User_messages

# Function to quickly format the print of dictionary messages of a given user
def display_user_messages(User_messages):
    # INPUT #
    # User_messages :   Dictionary - of one users messages, keys being timestamps, data being the content of the message

    for key in User_messages.keys():
        print(f"{key} : {User_messages[key]}\n")