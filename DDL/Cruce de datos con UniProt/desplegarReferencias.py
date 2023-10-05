import pandas as pd
import ast

df_proteinas = pd.read_csv("datos/salida.csv", sep="~")

df_proteinas = df_proteinas.dropna()
rows = []
u = False
for _, row in df_proteinas.iterrows():
    anios = row["Anios"].split(sep="'")
    anios = [elemento.split(sep="-")[-1] for elemento in anios if any(char.isdigit() for char in elemento)]
    titulos = row["Titulos"][1:len(row["Titulos"])-1]
    titulos = titulos.split(sep="', ")
    
    autores = row["Autores"]
    autores = ast.literal_eval(autores)
    # autores = autores.strip("[]")
    # for i in autores:
    #     print(i)
    if not u:
        print(autores)
        u = True
    