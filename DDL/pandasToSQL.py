import pandas as pd
import numpy as np

colsProt = [
    "idProteina", 
    "uniProtID",
    "descripcion",
    "idEspecie"
]

colsSecuencia = [
    "idSecuencia",
    "secuencia",
    "idProteina",
    "largo"
]

colsEspecie = [
    "idEspecie",
    "taxId",
    "nombre"
]

colsGen = [
    "idGen",
    "nombre",
    "idProteina"
]

colsReferencia = [
    "idReferencia",
    "titulo",
    "anio"
]

colsAutor = [
    "idAutor",
    "nombre"
]

dfProteina = pd.DataFrame(columns=colsProt)
dfSecuencia = pd.DataFrame(columns=colsSecuencia)
dfEspecie = pd.DataFrame(columns=colsEspecie)
dfGen = pd.DataFrame(columns=colsGen)
dfReferencia = pd.DataFrame(columns=colsReferencia)
dfAutor = pd.DataFrame(columns=colsAutor)

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
        "UniProtID"
        ]


dfTemp = pd.read_csv("CruceDeDatos/datos/Proteinas.csv", header=None, names=head)
dfTemp.replace('\\N', np.nan, inplace=True)
dfTemp = dfTemp.dropna(subset=["UniProtID"])

dfProteina["uniProtID"] = dfTemp["UniProtID"].copy()

dfProteina = dfProteina.merge(dfTemp[["UniProtID", "domains", "geneDesc"]], left_on="uniProtID", right_on="UniProtID", how="inner")
dfProteina.drop("UniProtID", axis=1, inplace=True)
dfProteina.drop("descripcion", axis=1, inplace=True)
dfProteina.rename(columns={"geneDesc" : "descripcion"}, inplace=True)
dfProteina.rename(columns={"domains" : "dominios"}, inplace=True)

dfProtParam = pd.read_csv("CruceDeDatos/datos/protParam.csv")
dfProteina = dfProteina.merge(dfProtParam[["UniProtID", "pesoMol", "pI", "fraccionHelice", "fraccionGiro", "fraccionHoja"]], left_on="uniProtID", right_on="UniProtID", how="inner")
dfProteina.drop(["UniProtID"], axis=1, inplace=True)

dfProteina["idProteina"] = range(1, len(dfProteina)+1)

print(dfProteina.info())

