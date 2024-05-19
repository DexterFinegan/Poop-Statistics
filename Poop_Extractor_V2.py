# Instagram Poop Extractor 2024 Version 2
# Goal : Improve on Version 1 from 2023 and apply it to 2024
# See Goals.txt to read further

# Importing modules
from Extract import *
from Clean import *
from Display import *
from Reaction_Extractor import *

# Function to Extract, Clean and Save a new dataframe of poops
def new_clean_df():
    # Initialising project
    print("Creating Dataframe...")
    dataframe = extract_data(directory="DATA/messages/inbox/2023poopcounter")
    dataframe = data_drop(dataframe, drop_list=["share", "reactions", "photos", "audio_files", "videos", "call_duration"])
    dataframe = replace_names(dataframe)

    # Isolating one user
    Dex_messages = messages_sent_by(dataframe, user="Dex")

    # Cleaning Data
    Dex_messages = isolate_number_messages(Dex_messages)
    Dex_messages = change_mesasges_to_just_numbers(Dex_messages)
    Dex_messages = long_chain(Dex_messages)


    # Generalising to all users
    users = get_users(directory="DATA/messages/inbox/2023poopcounter", refactor=True)
    everyones_data = []
    for user in users["name"]:

        # Exclude Noel cuz he fucked his up sm
        if user != "Noel":

            print(f"Begining on {user}'s Data\n")
            # Cleaning Data
            user_messages = messages_sent_by(dataframe, user=user)
            user_messages = isolate_number_messages(user_messages)
            user_messages = change_mesasges_to_just_numbers(user_messages)
            user_numbers = long_chain(user_messages)

            print(f"{user}'s data has been cleaned\n")
            # Adding users name into their number chain
            for entry in user_numbers:
                everyones_data.append([user, entry[0], entry[1]])
            
            print(f"{user}'s data has been added\n")

    df = return_to_dataframe(everyones_data)
    df = clean_dataframe(df)
    save_csv(df)

    return df

# Function to Extract an uncleaned df
def new_unclean_df():
    df = extract_data(directory="DATA/messages/inbox/2023poopcounter")
    df = replace_names(df)
    df = df.reset_index(drop=True)

    return df

df = new_unclean_df()
names = get_users(directory="DATA/messages/inbox/2023poopcounter", refactor=True)
pie_of_messages(total_sent_messages(df=df, users=names))