import requests
import pandas as pd
import io

with open('vmh_reactions_all.csv', 'r') as file:
    reactions = pd.read_csv(file)

url_human = "https://www.vmh.life/_api/reactiongenes/"

payload = {}
headers = {}

reaction_ids_human = reactions[reactions["isHuman"] == True]
reaction_ids_human = reaction_ids_human["reconMap"].dropna().tolist()

human_reaction_genes = pd.DataFrame()

for human_reaction_id in reaction_ids_human:
    reaction_url = url_human + human_reaction_id + "/"
    response = requests.request("GET", reaction_url, headers=headers, data=payload)
    response = response.json()
    if response["count"] != 0:
        reaction_genes = pd.DataFrame(response["results"])
        reaction_genes["reaction"] = human_reaction_id
        human_reaction_genes = human_reaction_genes.append(reaction_genes)

print(human_reaction_genes)

# Save all reactiongenes to csv
buffer = io.StringIO()
human_reaction_genes.info(buf=buffer)
human_reaction_genes_info = buffer.getvalue()

with open('reactiongenes_info.txt', 'w') as file:
    file.write(human_reaction_genes_info)

human_reaction_genes.to_csv('/path/to/vmh/data/folder/vmh_reactiongenes_all.csv')
