import json
from flatten_json import *
from numpy import NaN
from pandas.core.frame import DataFrame
import requests
import pandas as pd

hero_names = ["Anti-Mage","Axe","Bane","Bloodseeker","Crystal Maiden",\
    "Drow Ranger","Earthshaker","Juggernaut","Mirana","Morphling", \
        "Shadow Fiend","Phantom Lancer","Puck","Pudge","Razor", \
            "Sand King","Storm Spirit", "Sven", "Tiny" ,"Vengeful Spirit",\
            "Windranger", "Zeus", "Kunkka" , "Lina", "Lion", \
               "Shadow Shaman", "Slardar", "Tidehunter", "Witch Doctor", "Lich",\
                "Riki", "Enigma", "Tinker", "Sniper" , "Necrophos",\
                    "Warlock" , "Beastmaster" ,"Queen of Pain", "Venomancer" , "Faceless Void",\
                        "Wraith King", "Death Prophet", "Phantom Assassin", "Pugna" ,"Templar Assassin",\
                         "Viper", "Luna", "Dragon Knigh", "Dazzle", "Clockwerk",\
                          "Leshrac","Nature's Prophet","Lifestealer","Dark Seer", "Clinkz",\
                          "Omniknight","Enchantress","Huskar","Night Stalker","Broodmother","Bounty Hunter","Weaver","Jakiro","Batrider","Chen",\
                        "Spectre","Ancient Apparition","Doom","Ursa","Spirit Breaker","Gyrocopter","Alchemist","Invoker","Silencer",\
                            "Outworld Destroyer","Lycan","Brewmaster","Shadow Demon","Lone Druid","Chaos Knight","Meepo",\
                                "Treant Protector","Ogre Magi","Undying","Rubick","Disruptor","Nyx Assassin","Naga Siren",\
                                    "Keeper of the Light","Io","Visage","Slark","Medusa","Troll Warlord","Centaur Warrunner",\
                                        "Magnus","Timbersaw","Bristleback","Tusk","Skywrath Mage","Abaddon","Elder Titan",\
                                            "Legion Commander","Techies","Ember Spirit","Earth Spirit","Underlord","Terrorblade",\
                                                "Phoenix","Oracle","Winter Wyvern","Arc Warden","Monkey King","Dark Willow","Pangolier",\
                                                    "Grimstroke","Hoodwink","Void Spirit","Snapfire","Mars","Dawnbreaker","Marci"]

hero_metric_complete_df = pd.DataFrame()
# 1-137 even though only 122 heroes because of the weird unique ID coding system 
for element in range(1,140):
    url_name= "https://api.opendota.com/api/benchmarks"
    params = {'api_key':'352f2bed-ecf4-4c21-a0fa-959ce2df18d3',\
                'hero_id':element}
    hero_request = requests.get(url_name,timeout=10,params=params)
    print(element)
    print(hero_request,hero_request.url,hero_request.status_code)
    hero_json_data = hero_request.json()
    hero_json_data = flatten_json(hero_json_data)
    # hard code the index=[0] to be the first value(the key in the dict) to the columns of our dataframe
    df_hero = pd.DataFrame(pd.json_normalize(hero_json_data),index=[0])
    if df_hero.isnull().values.any():
        # continue vs break
        # continue: terminates the current iteration and proceeds to the next iteration
        # break: terminates current and overall iteration 
        continue
    else:
        hero_name = hero_names.pop(0)
        #finalized data_frame to output our .csv file
        df_heroes = df_hero.to_csv(f'{hero_name}_metric.csv')
        hero_metric_complete_df=hero_metric_complete_df.append(df_hero,ignore_index=True) 

hero_metric_complete_df.to_csv('total_heroes_metrics.csv')