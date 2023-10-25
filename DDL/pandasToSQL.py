import pandas as pd
import numpy as np
import ast

colsProt = [
    "id_proteina", 
    "uniProtID",
    "descripcion",
    "id_especie"
]

colsSecuencia = [
    "id_secuencia",
    "secuencia",
    "id_proteina",
    "largo"
]

colsEspecie = [
    "id_especie",
    "taxId",
    "nombre"
]

colsGen = [
    "id_gen",
    "nombre"
]

colsReferencia = [
    "id_referencia",
    "titulo",
    "anio"
]

colsAutor = [
    "id_autor",
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

dfProteina["id_proteina"] = range(1, len(dfProteina)+1)

# print("~"*20, "\nTabla proteina")
# print(dfProteina.info())
# print("~"*20)

# Se crea DataFrame para insertar en secuencia
dfSecuenciaCsv = pd.read_csv("CruceDeDatos/datos/salida.csv", sep="~")
dfSecuenciaCsv = dfSecuenciaCsv.drop_duplicates(subset="UniProtID")
dfSecuencia[["secuencia", "largo", "UniProtTemp"]]= dfSecuenciaCsv[["Secuencia", "Largo", "UniProtID"]]
dfSecuencia["id_secuencia"] = range(1, len(dfSecuencia)+1)
dfSecuencia = dfSecuencia.merge(dfProteina[["uniProtID", "id_proteina"]], left_on="UniProtTemp", right_on="uniProtID", how="inner", copy=True)
dfSecuencia.drop(labels=["id_proteina_x", "UniProtTemp", "uniProtID"], axis=1, inplace=True)
dfSecuencia.rename(columns={"id_proteina_y":"id_proteina"}, inplace=True)

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
dfEspecie["id_especie"] = range(1, len(dfEspecie)+1)
print("~"*20, "\nTabla especie")
print(dfEspecie.info())
print("~"*20)

dfProteina.drop("id_especie", axis=1, inplace=True)
dfProteina = dfProteina.merge(dfEspecie[["taxId", "id_especie"]], left_on="taxID", right_on="taxId")
dfProteina.drop("taxID", axis=1, inplace=True)
dfProteina.drop("taxId", axis=1, inplace=True)
print("~"*20, "\nTabla proteina")
print(dfProteina.info())
print("~"*20)

# Se crea DataFrame para insertar en gen
dfGen["nombre"] = dfTemp["geneName"]
dfGen = dfGen.merge(dfProteina[["id_proteina", "geneName"]], left_on="nombre", right_on="geneName")
dfGen = dfGen.drop_duplicates()
dfGen["id_gen"] = range(1, len(dfGen)+1)
dfGen.drop("geneName", axis=1, inplace=True)
print("~"*20, "\nTabla gen")
print(dfGen.info())
print("~"*20)

# Se crea DataFrame para insertar en autores
dfTemp = pd.read_csv("CruceDeDatos/datos/autores.csv", sep="~")
dfAutor["nombre"] = dfTemp["Autor"].unique().copy()
dfAutor["id_autor"] = range(1, len(dfAutor)+1)
print("~"*20, "\nTabla autores")
print(dfAutor.info())
print("~"*20)

# Se crea DataFrame para insertar en referencia
dfTemp = pd.read_csv("CruceDeDatos/datos/referencias.csv", sep="~")
dfTemp.replace(" ", np.nan, inplace=True)
dfReferencia["titulo"] = dfTemp["Titulo"]
dfReferencia["anio"] = dfTemp["Anio"]
dfReferencia["uniProtID"] = dfTemp["UniProtID"]
dfReferencia["autores"] = dfTemp["Autores"]
dfReferencia = dfReferencia.merge(dfProteina[["uniProtID", "id_proteina"]], on="uniProtID", how="inner")
dfReferencia.drop("uniProtID", axis=1, inplace=True)
#dfReferencia.drop("autores", axis=1, inplace=True)
dfReferencia["id_referencia"] = range(1, len(dfReferencia)+1)
print("~"*20, "\nTabla referencias")
print(dfReferencia.info())
print("~"*20)


#Se crea DataFrame para insertar en ref_autor

idsRef = []
idsAutor = []
from tqdm import tqdm

total_rows = len(dfReferencia)
progress_bar = tqdm(total=total_rows, desc='Progreso', position=0)

for _, row in dfReferencia.iterrows():
    autores = row["autores"]
    if not pd.isna(row["autores"]):
        autores = ast.literal_eval(autores)
        for autor in autores:
            # print(autor)
            fila = dfAutor.loc[dfAutor["nombre"] == autor, "id_autor"]
            # print(fila["id_autor"])
            # dfRelacion = dfRelacion.append({
            #     "id_referencia" : row["id_referencia"],
            #     "id_autor" : fila["id_autor"]
            # }, ignore_index=True)
            idsRef.append(row["id_referencia"])
            idsAutor.append(fila.values[0])

    progress_bar.update(1)

progress_bar.close()
dfRelacion = pd.DataFrame({
    "id_referencia" : idsRef,
    "id_autor" : idsAutor
})

dfRelacion.to_csv("relacion.csv", index=False)
dfReferencia.drop("autores", axis=1, inplace=True)
dfProteina.drop("geneName", axis=1, inplace=True)
dfProteina["descripcion"] = dfProteina["descripcion"].str[:99]
dfProteina["dominios"] = dfProteina["dominios"].str[:99]
dfReferencia["titulo"] = dfReferencia["titulo"].str[:199]
# dfSecuencia.rename("id_proteina_y", axis=1, inplace=True)
print("~"*20, "\nTabla relacion")
print(dfRelacion.info())
print(dfRelacion.head())
print("~"*20)

print("~"*20, "\nTabla referencias")
print(dfReferencia.info())
print("~"*20)

print("~"*20, "\nTabla secuencia")
print(dfSecuencia.info())
print("~"*20)
dataFrames = [
    [dfEspecie, "especie"],
    [dfProteina, "proteina"],
    [dfSecuencia, "secuencia"],
    [dfGen, "gen"],
    [dfReferencia, "referencia"],
    [dfAutor, "autor"],
    [dfRelacion, "ref_tiene_autor"]
]

from sqlalchemy import URL, create_engine

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/RBPDB")

for dataframe in dataFrames:
    df = dataframe[0]
    for columna in df.columns:
        df.rename(columns={columna : columna.lower()}, inplace=True)
    df.to_sql(name=dataframe[1], con=engine, if_exists="append", index=False)