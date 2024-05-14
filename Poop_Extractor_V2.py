# Instagram Poop Extractor 2024 Version 2
# Goal : Improve on Version 1 from 2023 and apply it to 2024
# See Goals.txt to read further

# Importing modules
from Extract import extract_messages

print("Creating Dataframe...")
m = extract_messages(directory="DATA/messages/inbox/2023poopcounter")

print(m)
