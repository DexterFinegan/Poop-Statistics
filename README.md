The Big Poopathon Statistics Files

These sets of files hold the contents and programmes to using the stats on the poop data collected.
First be sure to collect the data via instagram messages download, medium quality is fine but a json file type is required.
This action may take 30mins to an hour.

DIRECTORY is a hard coded directory to the data, it should be fine to leave as is until the new year begins but should be present.
The Poop_Extractor_V2.py file is the most up-to-date file on what can be done.
For cleanliness import this into the Poop_Collection.py file and work from there.

Importing and Cleaning the data.

def extract_and_clean_all_data() uses many functions to extarct the data from the save file, clean it down per user and
provides a messages dataframe and a poop dataframe for each user.
The messages dataframe contains columns: Message ID, timestamp (date), content, reactions, share, photos, videos, audio_files, gifs, call_duration.
The poop dataframe contains columns: Poop, ID, user, timestamp (date), content, reactions, audio_files, gifs (for some reason)
This function only requires one parameter: directory pointing to the raw data (ie the DIRECTORY variable)

def get_users() is a function to extract a dataframe of all the users in the chat (even if they have left the groupchat)
it requires no parameters

Displaying Data on Graphs

def display_specific_poops() is a function to create a graph of the poops of users.
It has several parameters: users = a list of the users string names to have on the graph, if left empty all users will be included
                          time_period = a tuple of the start datetime and the end datetime for the graph to reach, if left blank will only do January
                          labels = a boolean whether username labels should be included - auto set to True
                          legend = a boolean whether a legend of usernames shoulc be included - auto set to False
                          save = a boolean for whether to save the plot to a file in the same directory
                          show = a boolean for whether to show to graph to the user

def like_sender() is a function that calculates how many likes each player has sent to others, returning a dictionary
It has 3 parameters: pie = a boolean of whether or not to display this on a pie chart - auto set to False
                      only_poops = a boolean of whether to just count likes on messages containing poop updates - auto set to False
                      save = a boolean for whether to save the plot to a file in the same directory

def dynamic_bar_chart() uses pygame to play a visual of the groups positions in a leaderboard over the course of the poopathon
This takes no parameters but may need hardcoding for the end time

def compare_year_poops() is a function to compare the poops of users over different years, they must have data spanning at least two years
This has 5 parameters: user = the name of the user to compare their data
                      directories = a list of directories that has all the data required for the multiple years
                      time_period = a list containing the start and end time of the data to show on the graph, if left empty the whole year will be included
                      save = a boolean for whether to save the plot to a file in the same directory
                      show = a boolean for whether to show the graph to the user

def smooth_display_specific_poops() uses techniques to show a smoother representation of the graph of users since people don't update timely
It's parameters are the exact same as for the display_specific_poops() function

def leaderboard() is a function to add users poops at the end of each month and their positions to a Json file called user_data.json
It takes no parameters.

def poops_per_day() uses everyones data to find how many poops everyone has done on each day of the month cumulated over every month of the year
This function takes one parameter: save = a boolean for whether to save the plot to a file in the same directory

def daily_poop_heatmap() is a function that shows a representation of a users poops over the course of the day displayed in hours
This function takes 4 parameters: user = the name of the user to see
                                  separate_days = a boolean of whether to split this data up by the day of the week it occured too
                                  save = a boolean for whether to save the plot to a file in the same directory
                                  show = a boolean for whether to show the heatmaps to the user

def shortest_time_between_poops() is a function to find the shortest time a user took between two updates, already fixing for backdated updates
it takes one parameter : user = the name of the user to find the shortest time between poops
This function prints the answer to terminal

def longest_time_between_poops() is a function to find the longest time a user took between two updates, already fixing for backdated updates
it takes one parameter : user = the name of the user to find the longest time between poops
This function prints the answer to terminal

def find_sd() is a function to find the standard deviation of the users updates to see their consistency with their schedule
This fucntion takes one parameter: user = the name of the user to find the information about
It prints the information to terminal

def interpersonal_relationships() is a functino to find all the likes sent and received for all messages and poops and other data including proportionality etc, returns a csv file of this data in the same directory
This functino takes one parameter : user = the string name of the user to find the data about

def content_sharer() is a function to find all the content information shared to the group chat, including pie charts that dispay who sent how many photos, videos, links and who received the most likes on these. On top of finding th emost well liked of each of these.
This function has 3 parameters: save = a boolean of whether to save the pie charts - auto set to False
                                pie = a boolean of whether to show the pie charts - auto set to False
                                biggest_content = a boolean that prints information and sends dicts of all content with keys of how many likes they received - auto set to False