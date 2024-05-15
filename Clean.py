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

