import requests
import pandas as pd

head = ["id",
        "annotId",
        "createDate",
        "updateDate",
        "geneName",
        "geneDesc",
        "species",
        "taxID",
        "domains",
        "flag",
        "flagNote",
        "aliases",
        "GSTpaper",
        "PDBIDs",
        "UniProtIDs"
        ]

df_rbp = pd.read_csv('datos/Proteinas.csv', header=None, names=head)

print(df_rbp.head())

df_largos = pd.DataFrame()

df_largos["PDBID"] = df_rbp["PDBIDs"]

url = "https://rest.uniprot.org/uniprotkb/P52756"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
