import requests
import pandas as pd
import math
import io

url = "https://www.vmh.life/_api/reactiontomicrobegene/"

payload = {}
headers = {}

page_1 = url + "?page=1"

response = requests.request("GET", page_1, headers=headers, data=payload)
response = response.json()

reactions = pd.DataFrame()

number_pages = math.ceil(response["count"] / len(response["results"]))
next_page = page_1

count = 0

for i in range(1, number_pages + 1):
    response = requests.request("GET", next_page, headers=headers, data=payload)
    response = response.json()
    print(response["next"])
    for result in response['results']:
        information_dict = {}
        gene = result['gene']
        recon = result['recon']
        gene_number = gene['gene_number']
        model = recon['model']

        information_dict.update({'gene_number': gene_number, 'model_id': model['model_id'], 'model_name': model['name'], 'model_organism': model['organism'], 'model_organismtype': model['organismtype'], 'rxn': recon['rxn'], 'lb': recon['lb'], 'ub': recon['ub'], 'gpr': recon['gpr'], 'subsystem': recon['subsystem']})
        information_df = pd.DataFrame(information_dict, index=[count])
        reactions = reactions.append(information_df)
        count = count + 1

    next_page = response["next"]

print(reactions)

buffer = io.StringIO()
reactions.info(buf=buffer)
reactions_info = buffer.getvalue()

print(reactions.info())
with open('reactiontomicrobegene_info.txt', 'w') as file:
    file.write(reactions_info)

reactions.to_csv('/path/to/vmh/data/folder/vmh_reactiontomicrobegene.csv')
