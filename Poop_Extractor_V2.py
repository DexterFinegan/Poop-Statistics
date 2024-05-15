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
Dex_messages = change_mesasges_to_just_numbers(Dex_messages)

index = 0
start_num = 1
chain_num = 1
while index + 1 < len(Dex_messages):
    chain, index = find_chain(Dex_messages, start_num = start_num, start_index = index)
    if chain != []:
        start_num = chain[-1][0] + 1

        print(f"\nChain {chain_num}\n")
        for entry in chain:
            print(entry)
        chain_num += 1
    else:
        start_num += 1