import requests
import pandas as pd
import math
import io

url = "https://www.vmh.life/_api/genes/"

payload = {}
headers = {}

page_1 = url + "?page=1"

response = requests.request("GET", page_1, headers=headers, data=payload)
response = response.json()

human_genes = pd.DataFrame(response["results"])

number_pages = math.ceil(response["count"] / len(response["results"]))
next_page = response["next"]
print(response["next"])

for i in range(2, number_pages + 1):
    response = requests.request("GET", next_page, headers=headers, data=payload)
    response = response.json()
    print(response["next"])
    human_genes_to_add = pd.DataFrame(response["results"])
    human_genes = human_genes.append(human_genes_to_add)
    next_page = response["next"]

human_genes = human_genes.reset_index()

buffer = io.StringIO()
human_genes.info(buf=buffer)
human_genes_info = buffer.getvalue()

print(human_genes.info())
with open('human_genes_info.txt', 'w') as file:
    file.write(human_genes_info)

human_genes.drop(columns=['index', 'createdDate', 'updatedDate', 'wikipedia', 'mimAccession',
                          'mimDescription', 'ucsc', 'wikigene', 'goTermAccession', 'goTermName', 'goTermDefinition',
                          'gstart', 'gend', 'tstart', 'tend', 'genecards', 'diseaseMeth', 'gwasCatalog', 'geno2MP',
                          'lovd', 'ghr', 'clinGene', 'gwasCentral', 'decipher', 'humanProteomeAtlasAB', 'strand',
                          'band', 'ensembl_trans', 'ensembl_protein', 'entrez_id'], inplace=True)

human_genes.to_csv('/path/to/vmh/data/folder/vmh_human_genes.csv')
