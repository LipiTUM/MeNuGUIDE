import traceback

import requests
import pandas as pd

with open('/path/to/vmh/data/folder/vmh_microbe_genes_all.csv', 'r') as file:
    microbe_genes = pd.read_csv(file)

url_microbe = "https://www.vmh.life/_api/microbegenereactions/"

payload = {}
headers = {}

microbe_gene_numbers = microbe_genes["gene_number"].dropna().unique().tolist()

outputfile = open("/path/to/vmh/data/folder/vmh_microbe_genereactions.csv", "a")
already_queried_file = open("/path/to/vmh/data/folder/genes_already_written.txt", "r+")

already_queried = set(already_queried_file.read().split('\n'))

try:
    for gene_number in microbe_gene_numbers:
        if gene_number in already_queried:
            continue
        else:
            reaction_url = url_microbe + str(gene_number) + "/"
            response = requests.request("GET", reaction_url, headers=headers, data=payload)
            response = response.json()
            if response["count"] != 0:
                for result in response["results"]:
                    reaction_genes = str(result['rxn_id']) + ',' + str(result['abbreviation']) + ',' + str(gene_number) + ',' + str(result['isHuman']) + ',' + str(result['isMicrobe']) + '\n'
                    outputfile.write(reaction_genes)
                already_queried_file.write(str(gene_number) + '\n')
except Exception as e:
    traceback.print_exc()

outputfile.close()
