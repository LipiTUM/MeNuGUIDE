import requests
import pandas as pd
import math
import io

url = "https://www.vmh.life/_api/microbegenes/"

payload = {}
headers = {}

page_1 = url + "?page=1"

response = requests.request("GET", page_1, headers=headers, data=payload)
response = response.json()

microbe_genes = pd.DataFrame(response["results"])

number_pages = math.ceil(response["count"] / len(response["results"]))  # => 12769

next_page = response["next"]
print(response["next"])

for i in range(2, number_pages + 1):
    response = requests.request("GET", next_page, headers=headers, data=payload)
    response = response.json()
    print(response["next"])
    microbe_genes_to_add = pd.DataFrame(response["results"])
    microbe_genes = microbe_genes.append(microbe_genes_to_add)
    next_page = response["next"]

microbe_genes = microbe_genes.reset_index()

buffer = io.StringIO()
microbe_genes.info(buf=buffer)
microbe_genes_info = buffer.getvalue()

print(microbe_genes.info())
with open('microbe_genes_info.txt', 'w') as file:
    file.write(microbe_genes_info)

microbe_genes.to_csv('/path/to/vmh/data/folder/vmh_microbe_genes_all.csv')
