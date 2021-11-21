import json
from flatten_json import *
from numpy import NaN
from pandas.core.frame import DataFrame
import requests
import pandas as pd

url_name= "https://api.opendota.com/api/heroStats"
params = {'api_key':'352f2bed-ecf4-4c21-a0fa-959ce2df18d3'}
hero_request = requests.get(url_name,timeout=5,params=params)
all_hero_json_data = json.loads(hero_request.text)
# hard code the index=[0] to be the first value(the key in the dict) to the columns of our dataframe
df_all_heroes_metrics = pd.DataFrame(pd.json_normalize(all_hero_json_data))
df_all_heroes_metrics = df_all_heroes_metrics.to_csv('all_heroes_stats.csv')