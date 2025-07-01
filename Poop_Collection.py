from Poop_Extractor import *

DIRECTORY = "DATA/messages/inbox/2025poopchat"

users = get_users(DIRECTORY).to_list()
extract_and_clean_all_data(directory=DIRECTORY)

# Getting the bigger graphs
display_specific_poops(users=users, 
                       time_period = (pd.to_datetime("2025-01-01 00:00:01"), pd.to_datetime("2025-6-30 23:59:59")),
                       labels=True,
                       legend=True,
                       save=True,
                       show=False)
display_specific_poops(users=users, 
                       time_period = (pd.to_datetime("2025-04-15 00:00:01"), pd.to_datetime("2025-6-30 23:59:59")),
                       labels=False,
                       legend=False,
                       save=True,
                       show=False)

# Getting Heatmaps
for user in users:
    daily_poop_heatmap(user=user, separate_days=False, save=True, show=False)
    daily_poop_heatmap(user=user, separate_days=True, save=True, show=False)

# Getting Interpersonal Relationship CSVs
#for user in users:
#    interpersonal_relationships(user=user)

# Getting the content
content_sharer(save=True)
content, photo = content_sharer(biggest_content=True)
print(content[9], content[8], content[7])
print(photo[9], photo[8], photo[7])