import json
import requests
from pprint import pprint
import pandas as pd

url_name = "https://api.opendota.com/api/playersByRank"
r = requests.get(url_name)
answer =r.text
json_data = json.loads(answer)
pprint(json_data)
df = pd.DataFrame(json_data)
df.to_csv('test.csv')
df2 = pd.DataFrame.from_dict(json_data)
df3 = pd.DataFrame.from_records(json_data)

df2.to_csv('test1.csv')
df3.to_csv('test2.csv')