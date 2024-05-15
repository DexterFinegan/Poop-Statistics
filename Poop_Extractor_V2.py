# Instagram Poop Extractor 2024 Version 2
# Goal : Improve on Version 1 from 2023 and apply it to 2024
# See Goals.txt to read further

# Importing modules
from Extract import *
from Clean import *

# Initialising project
print("Creating Dataframe...")
dataframe = extract_data(directory="DATA/messages/inbox/2023poopcounter")
dataframe = data_drop(dataframe, drop_list=["share", "reactions", "photos", "audio_files", "videos", "call_duration"])
dataframe = replace_names(dataframe)

# Isolating one user
Dex_messages = messages_sent_by(dataframe, user="Dex")

# Cleaning Data
Dex_messages = isolate_number_messages(Dex_messages)
display_user_messages(Dex_messages)