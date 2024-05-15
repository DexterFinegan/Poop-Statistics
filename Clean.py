# Contains all functions for cleaning data

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
    
    # Fail Scenario : Number never posted in chat
    if start == 0 and start_index != 0:
        print(f"\nCould not find {start_num} in list of messages")
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

        

