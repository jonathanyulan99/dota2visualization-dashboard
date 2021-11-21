import pandas as pd
import os, glob
import re

directory_path = os.path.dirname(__file__)
directory_path += "\players"
players_files = glob.glob(os.path.join(directory_path, "*.csv"))
player_key = None 
clean_player_key = ""

all_top_players_df = []
for player in players_files:
    top_players_df = pd.read_csv(player,sep=',')
    player_key = player.split('\\')[-1]
    for element in player_key:
        if element.isdigit()==True:
            clean_player_key += element
        else:
            print(clean_player_key)
            break 
    top_players_df['player_id'] = clean_player_key 
    all_top_players_df.append(top_players_df)
    clean_player_key = ""

merged_all_top_players_df = pd.concat(all_top_players_df,ignore_index=True,sort=True)
merged_all_top_players_df.to_csv( "top_player.csv")
