# Contains all functions for cleaning data

# Modules to import
import pandas as pd
from Extract import data_drop

# Function to remove messages with no numbers in them
def isolate_number_messages(User_messages):
    # INPUT #
    # User_messages :   Dictionary - containg all messages from a user, keys are timestamps, data is the content of the message

    # OUTPUT #
    # Number_messages :   Dictionary - containing only messages that contain at least on number in them, keys are timestamps, data is the content of the message

    # Creating a new Dictionary to store valid messages
    Number_messages = {}

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Iterating through Dictionary containing all messages
    for key in User_messages.keys():
        contains_number = False
        message = User_messages[key]

        # Fixing for dan_griffin6 error
        if "dan_griffin6" not in message:
            # Iterating through all characters in the message to check if it has a number in it
            for letter in message:
                if letter in numbers:
                    contains_number = True
            
            # Adding messages with numbers in them to new dictionary
            if contains_number:
                Number_messages[key] = message

    return Number_messages

# Function to examine a message and return all numbers in it
def numbers_in_message(message):
    # INPUT #
    # message   :   String - message from a user

    # OUTPUT #
    # message_numbers   :   List - containg all numbers in the message as integers

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    message_numbers = []

    # Iterating through characters in a message
    number = ""
    for letter in message:
        if letter in numbers:
            number += letter
        elif number != "":
            message_numbers.append(int(number))
            number = ""
    
    # Check for number being the last bit of the message
    if number != "":
        message_numbers.append(int(number))

    return message_numbers

# Function to extract just the numbers within a message a remove the useless text associated
def change_mesasges_to_just_numbers(User_messages):
    # INPUT #
    # User_messages :   Dictionary - containg only messages with numbers in the of a user, keys are timestamps, data is the content of the message

    # OUTPUT #
    # User_numbers  :   Dictionary - containing only the numbers sent by a user, keys are timestamps, data is a list of numbers in the message sent
    
    User_numbers = {}
    for key in User_messages.keys():
        User_numbers[key] = numbers_in_message(User_messages[key])

    return User_numbers

# Function to find chains of consecutive numbers in consecutive messages
def find_chain(User_messages, start_num = 1, start_index = 0):
    # INPUT #
    # User_messages :   Dictionary - numbers sent by a user, keys are timestamps, data is a list of numbers in message sent at that time
    # start_num     :   Integer - Designated as the starting number of the chain
    # start_index   :   Integer - Index of the message list at which the chain should start after

    # OUTPUT #
    # chain         :   List - containing messages with consecutive numbers as lists with index 0 as the number and index 1 as the timestamp
    # current_index :   Integer - messages index where the chain failed to continue, to allow for next chain beginning
    
    # Converting messages dictionary to a list of lists as [numbers, timestamp]    (Because I find it easier to use)
    messages = []
    chain = []
    for key in User_messages.keys():
        messages.append([User_messages[key], key])
    
    # Iterating over list to find index of start number (start)
    start = 0
    for index in range(start_index, len(messages)):
        if start_num in messages[index][0]:
            start = index
            break
    
    # Fail Scenario 1 : Number never posted in chat
    if start == 0 and start_index != 0:
        return chain, start_index
    
    # Fail Scenario 2 : Number posted in chat but unreasonably long after previous number, hence must be irrelevant
    if start - start_index > 20:                                    # Assuming consecutive numbers should be within 20 messages of each other, unsure tho
        return chain, start_index
    
    # Examine consecutive messages from start point for consecutive numbers
    chain.append([start_num, messages[start][1]])    
    current_number = start_num + 1
    current_index = start
    searching = True
    while searching:
        # Checking did not exceed messages list
        if current_index + 1 == len(messages):
            searching = False

        # Check same message as previous number was found
        elif current_number in messages[current_index][0]:
            chain.append([current_number, messages[current_index][1]])
            current_number += 1
        
        # Check Consecutive message
        elif current_number in messages[current_index + 1][0]:
            current_index += 1
            chain.append([current_number, messages[current_index][1]]) 
            current_number += 1
        
        # Not found scenario
        else:
            searching = False
    
    return chain, current_index

# Function to display all chains of a users poops, including missed poops
def display_chains(User_messages):
    # INPUT #
    # User_messages :   List - list of lists conatining all numbers in each message in index 0 and the timestamp of the message in index 1

    index = 0
    start_num = 1
    chain_num = 1
    while index + 1 < len(User_messages):
        chain, index = find_chain(User_messages, start_num = start_num, start_index = index)
        if chain != []:
            start_num = chain[-1][0] + 1

            print(f"\nChain {chain_num}\n")
            for entry in chain:
                print(entry)
            chain_num += 1
        else:
            print(f"\nCould not find {start_num} in list of messages")
            start_num += 1

# Function to create one long chain of all numbers of a particular user
def long_chain(User_messages):
    # INPUT #
    # User_messages :   List - list of lists conatining all numbers in each message in index 0 and the timestamp of the message in index 1

    # OUTPUT #
    # User_numbers  :   List - list of lists containing each consecutive number (excluding missed numbers) in index 0 and the message timestamp in index 1

    User_numbers = []

    index = 0
    start_num = 1
    chain_num = 1
    give = 0            # Give variable breaks major flaws

    # Creating all chains
    while index + 1 < len(User_messages):
        chain, index = find_chain(User_messages, start_num = start_num, start_index = index)
        if chain != []:
            start_num = chain[-1][0] + 1

            for entry in chain:
                # Appending chain to big chain
                User_numbers.append(entry)
            chain_num += 1
            give = 0
        else:
            start_num += 1
            give += 1
            if give > 7:
                return User_numbers
    
    return User_numbers

# Function to convert a list of messages into a pandas dataframe
def return_to_dataframe(data):
    # INPUT #
    # data  :   List - list of lists of all messages with index 0 being the user name, index 1, being the number, index 2 being the timestamp of the message

    # OUTPUT #
    # DataFrame : pandas DataFrame - containing all messages appropriately stored

    # First changing it to a list of dictionaries akin to original json file
    messages = []
    for entry in data:
        dictionary = {}
        dictionary["user"] = entry[0]
        dictionary["poop"] = entry[1]
        dictionary["timestamp"] = entry[2]
        messages.append(dictionary)
    
    # Making it into a dataframe like in the extract section
    DataFrame = pd.DataFrame(messages)

    return DataFrame

# Function to clean up appearance of DataFrame; change timestamp to date format, put in chronological order
def clean_dataframe(DataFrame):
    # INPUT #
    # DataFrame :   pandas DataFrame - used for after all data has been cleaned

    # OUTPUT #
    # DataFrame :   pandas DataFrame - organised dataframe

    DataFrame = DataFrame.sort_values(by="timestamp", ascending=True)
    DataFrame["timestamp"] = pd.to_datetime(DataFrame["timestamp"], format="mixed").dt.date
    DataFrame = DataFrame.reset_index(drop=True)

    return DataFrame

# Function to save dataframe to csv file
def save_csv(df):
    # INPUT #
    # df    :   pandas DataFrame - as wished to be saved

    df.to_csv("save_file.csv")

# Function to load dataframe from csv file
def load_csv(directory):
    # INPUT #
    # directory :   String - path to csv file

    # OUTPUT #
    # df    :   pandas DataFrame - as shown in csv file

    df = pd.read_csv(directory)
    df = data_drop(df, ["Unnamed: 0"])
    return df
