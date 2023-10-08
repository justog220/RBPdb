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
    "nombre"
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

# Se crea DataFrame para insertar en proteina
dfTemp = pd.read_csv("CruceDeDatos/datos/Proteinas.csv", header=None, names=head)
dfTemp.replace('\\N', np.nan, inplace=True)
dfTemp = dfTemp.dropna(subset=["UniProtID"])
dfTemp = dfTemp.drop_duplicates(subset="UniProtID")

dfProteina["uniProtID"] = dfTemp["UniProtID"].copy()

dfProteina = dfProteina.merge(dfTemp[["UniProtID", "domains", "geneDesc", "taxID", "geneName"]], left_on="uniProtID", right_on="UniProtID", how="inner", copy=True)
dfProteina.drop("UniProtID", axis=1, inplace=True)
dfProteina.drop("descripcion", axis=1, inplace=True)
dfProteina.rename(columns={"geneDesc" : "descripcion"}, inplace=True)
dfProteina.rename(columns={"domains" : "dominios"}, inplace=True)

dfProtParam = pd.read_csv("CruceDeDatos/datos/protParam.csv")
dfProteina = dfProteina.merge(dfProtParam[["UniProtID", "pesoMol", "pI", "fraccionHelice", "fraccionGiro", "fraccionHoja"]], left_on="uniProtID", right_on="UniProtID", how="inner", copy=True)
dfProteina.drop(["UniProtID"], axis=1, inplace=True)

dfProteina["idProteina"] = range(1, len(dfProteina)+1)

print("~"*20, "\nTabla proteina")
print(dfProteina.info())
print("~"*20)

# Se crea DataFrame para insertar en secuencia
dfSecuenciaCsv = pd.read_csv("CruceDeDatos/datos/salida.csv", sep="~")
dfSecuenciaCsv = dfSecuenciaCsv.drop_duplicates(subset="UniProtID")
dfSecuencia[["secuencia", "largo", "UniProtTemp"]]= dfSecuenciaCsv[["Secuencia", "Largo", "UniProtID"]]
dfSecuencia["idSecuencia"] = range(1, len(dfSecuencia)+1)
dfSecuencia = dfSecuencia.merge(dfProteina[["uniProtID", "idProteina"]], left_on="UniProtTemp", right_on="uniProtID", how="inner", copy=True)
dfSecuencia.drop(labels=["idProteina_x", "UniProtTemp", "uniProtID"], axis=1, inplace=True)
dfSecuencia.rename(columns={"idProteina_y":"idProteina"}, inplace=True)

#duplicados = dfSecuenciaCsv[dfSecuenciaCsv.duplicated(subset=["Secuencia"], keep=False)]
#print(duplicados[["UniProtID", "Secuencia"]].sort_values(by="Secuencia"))
print("~"*20, "\nTabla secuencia")
print(dfSecuencia.info())
print("~"*20)

# Se crea DataFrame para insertar en especie
tuplas = dfTemp[["taxID", "species"]].drop_duplicates()
nombresEspecies = []
taxIDs = []
dfEspecie[["taxId", "nombre"]] = tuplas[["taxID", "species"]].copy()
dfEspecie["idEspecie"] = range(1, len(dfEspecie)+1)
print("~"*20, "\nTabla especie")
print(dfEspecie.info())
print("~"*20)

dfProteina.drop("idEspecie", axis=1, inplace=True)
dfProteina = dfProteina.merge(dfEspecie[["taxId", "idEspecie"]], left_on="taxID", right_on="taxId")
dfProteina.drop("taxID", axis=1, inplace=True)
print("~"*20, "\nTabla proteina")
print(dfProteina.info())
print("~"*20)

# Se crea DataFrame para insertar en gen
dfGen["nombre"] = dfTemp["geneName"]
dfGen = dfGen.merge(dfProteina[["idProteina", "geneName"]], left_on="nombre", right_on="geneName")
dfGen = dfGen.drop_duplicates()
dfGen["idGen"] = range(1, len(dfGen)+1)
dfGen.drop("geneName", axis=1, inplace=True)
print("~"*20, "\nTabla gen")
print(dfGen.info())
print("~"*20)