import requests
import pandas as pd
import math
import io

url = "https://www.vmh.life/_api/reactions/"

payload = {}
headers = {}

page_1 = url + "?page=1"

response = requests.request("GET", page_1, headers=headers, data=payload)
response = response.json()

reactions = pd.DataFrame(response["results"])

number_pages = math.ceil(response["count"] / len(response["results"]))
next_page = response["next"]
print(response["next"])

for i in range(2, number_pages + 1):
    response = requests.request("GET", next_page, headers=headers, data=payload)
    response = response.json()
    print(response["next"])
    reactions_to_add = pd.DataFrame(response["results"])
    reactions = reactions.append(reactions_to_add)
    next_page = response["next"]

reactions = reactions.reset_index()

buffer = io.StringIO()
reactions.info(buf=buffer)
reactions_info = buffer.getvalue()

print(reactions.info())
with open('reactions_info.txt', 'w') as file:
    file.write(reactions_info)

reactions.drop(columns=['index', 'createdDate', 'updatedDate', 'mcs', 'csecoida', 'cog', 'reconMap',
                        'wikipedia', 'seed', 'miriam', 'keggorthology', 'metanetx', 'massbalance'], inplace=True)

reactions.to_csv('/path/to/vmh/data/folder/vmh_reactions.csv')
