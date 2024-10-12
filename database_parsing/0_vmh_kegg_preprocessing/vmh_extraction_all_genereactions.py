import requests
import pandas as pd
import io

with open('/path/to/vmh/data/folder/vmh_human_genes_all.csv', 'r') as file:
    human_genes = pd.read_csv(file)

url_human = "https://www.vmh.life/_api/genereactions/"

payload = {}
headers = {}

human_gene_numbers = human_genes["gene_number"].dropna().tolist()

human_genereactions = pd.DataFrame()

for gene_number in human_gene_numbers:
    reaction_url = url_human + str(gene_number) + "/"
    response = requests.request("GET", reaction_url, headers=headers, data=payload)
    response = response.json()
    if response["count"] != 0:
        reaction_genes = pd.DataFrame(response["results"])
        reaction_genes["searched_gene_number"] = gene_number
        human_genereactions = human_genereactions.append(reaction_genes)

print(human_genereactions)

# Save all reactiongenes to csv
buffer = io.StringIO()
human_genereactions.info(buf=buffer)
human_genereactions_info = buffer.getvalue()

with open('genereactions_info.txt', 'w') as file:
    file.write(human_genereactions_info)

human_genereactions.to_csv('/path/to/vmh/data/folder/vmh_genereactions_all.csv')
