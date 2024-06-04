# Instagram Poop Extractor 2024 Version 2
# Goal : Improve on Version 1 from 2023 and apply it to 2024
# See Goals.txt to read further

# Importing modules
from Extract import *
from Clean import *
from Display import *
from Reaction_Extractor import *

location = "DATA/messages/inbox/weaponsofassdestruction"

# Function to Extract, Clean and Save a new dataframe of poops
def new_clean_df(dir):
    # Initialising project
    print("Creating Dataframe...")
    dataframe = extract_data(directory=dir)
    dataframe = replace_names(dataframe)
    dataframe = dataframe.reset_index(drop=True)
    dataframe = data_drop(dataframe, drop_list=["share", "is_geoblocked_for_viewer", "reactions", "photos", "audio_files", "videos", "call_duration"])

    # Generalising to all users
    users = get_users(directory=dir, refactor=True)
    everyones_data = []
    for user in users["name"]:
        # Cleaning Data
        user_messages = messages_sent_by(dataframe, user=user)
        user_messages = isolate_number_messages(user_messages)
        user_messages = change_mesasges_to_just_numbers(user_messages)
        user_numbers = long_chain(user_messages)

        # Adding users name into their number chain
        for entry in user_numbers:
            everyones_data.append([user, entry[0], entry[1]])
        
        print(f"{user}'s data has been added\n")

    df = return_to_dataframe(everyones_data)
    df = clean_dataframe(df)
    save_csv(df)

    return df

# Function to Extract an uncleaned df
def new_unclean_df(dir):
    df = extract_data(directory=dir)
    df = replace_names(df)
    df = df.reset_index(drop=True)

    return df

# Testing for Jack
df = new_unclean_df(location)
players = get_users(location, refactor=True)
print(f"Total Likes : {total_likes(df, players)}\n")
print(f"Total Messages : {total_sent_messages(df, players)}\n")
print(f"L/M Ratio : {like_to_messsage_ratio(df, players)}\n")
