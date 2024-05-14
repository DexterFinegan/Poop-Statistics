# Contains all functions for extracting data from source

# Module Imports
import pandas as pd
import os
import json

# Function to Extract all messages from a json file in a specific directory within the folder
def extract_messages(directory):
    MEGAFRAME = pd.DataFrame()
    FILES = os.listdir(directory)
    for file in FILES:
        if file.endswith(".json"):
            with open(f"{directory}/{file}") as jf:
                JSON_DATA = json.load(jf)
                df = pd.DataFrame(JSON_DATA["messages"])
                MEGAFRAME = pd.concat([MEGAFRAME, df])

    MEGAFRAME['timestamp_ms'] = pd.to_datetime(MEGAFRAME['timestamp_ms'], unit='ms')
    MEGAFRAME.drop(["share", "reactions", "photos", "audio_files", "videos", "call_duration"], axis=1, inplace= True)
    MEGAFRAME["sender_name"].replace({'shauna\u00f0\u009f\u00a6\u0089': "Shauna",
                                    "\u00f0\u009d\u0093\u0094\u00f0\u009d\u0093\u00b8\u00f0\u009d\u0093\u00b2\u00f0\u009d\u0093\u00b7": "Eoin",
                                        "Neo O'Herlihy": "Neo",
                                        "Conor Mcmenamin": "Conor",
                                        "Noel Brassil": "Noel",
                                        "Ros Hanley": "Ros",
                                        "Jack McRann": "Jack" }, inplace=True)


    MEGAFRAME = MEGAFRAME[::-1]
    return MEGAFRAME