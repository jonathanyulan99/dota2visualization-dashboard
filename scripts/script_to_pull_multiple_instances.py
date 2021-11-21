import json
import requests
from pprint import pprint
import pandas as pd

element_id = [86860683,180076810,163913761,348367120,83003505]
 
for element in element_id: 
    url_name= "https://api.opendota.com/api/players/" + str(element) 
    print(url_name)
    r = requests.get(url_name)
    answer =r.text
    json_data = json.loads(answer)
    json_data = pd.json_normalize(json_data)
    df = pd.DataFrame(json_data)
    df = df.to_csv(str('player'+str(element)+'.csv'))

