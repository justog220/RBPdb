import requests
import pandas as pd
import time
import numpy as np
from tqdm import tqdm

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
df_rbp = df_rbp.drop_duplicates(subset="UniProtIDs")
print(df_rbp.info())

df_largos = pd.DataFrame()

df_largos["UniProtID"] = df_rbp["UniProtIDs"]
df_largos.replace('\\N', np.nan, inplace=True)
df_largos = df_largos.dropna(subset=["UniProtID"])


N = len(df_largos["UniProtID"])
cont = 0

salida = open("datos/salida.csv", "w")

salida.write("UniProtID~Largo~Secuencia~Anios~Titulos~Autores\n")

total_rows = len(df_largos["UniProtID"])
progress_bar = tqdm(total=total_rows, desc='Progreso', position=0)

for _, row in df_largos.iterrows():
    pbid = row["UniProtID"].split(sep=";")[0]

    url = f"https://rest.uniprot.org/uniprotkb/{pbid}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200 and "sequence" in response.json():
            largo = response.json()["sequence"]["length"]
            sec = response.json()["sequence"]["value"]
            if "references" in response.json():
                 referencias = response.json()["references"]
                 stop = 0
                 anios = []
                 titulos = []
                 autores = []
                 for referencia in referencias:
                    ref = referencia["citation"]
                    if "publicationDate" in ref:
                        anios.append(ref["publicationDate"])
                    else:
                        anios.append(" ")

                    if "title" in ref:
                        titulos.append(ref["title"])
                    else:
                        titulos.append(" ")

                    if "authors" in ref:
                        autores.append(ref["authors"])
                    else:
                        autores.append(" ")
                    stop+=1
                    if(stop==4):
                         break

    else:
        largo = np.nan
        sec = np.nan
        anio = np.nan
        titulo = np.nan
        autores = np.nan

    cont += 1

    #print(f"{round(cont/N*100, 2)}% | UniProtID = {pbid} ; Largo = {largo}")

    salida.write(f"{pbid}~{largo}~{sec}~{anios}~{titulos}~{autores}\n")
    progress_bar.update(1)
    # time.sleep(1)
progress_bar.close()
# TODO: cruzar con informacion de estructuras y referencias



