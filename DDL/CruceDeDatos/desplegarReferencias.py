import pandas as pd
import ast

salidaRef = open("datos/referencias.csv", "w")
salidaRef.write("idReferencia~UniProtID~Titulo~Anio~Autores\n")

df_proteinas = pd.read_csv("datos/salida.csv", sep="~")

df_proteinas = df_proteinas.dropna()
rows = []

dfAutores = pd.DataFrame(columns=["Autor", "idReferencia"])

dictAutores = {}

u = False
cont = 1
sum = 0
for _, row in df_proteinas.iterrows():
    anios = row["Anios"].split(sep="'")
    anios = [elemento.split(sep="-")[-1] for elemento in anios if any(char.isdigit() for char in elemento)]
    # titulos = row["Titulos"][1:len(row["Titulos"])-1]
    # titulos = titulos.split(sep="', ")
    
    autores = row["Autores"]
    autores = ast.literal_eval(autores)

    titulos = row["Titulos"]
    titulos = ast.literal_eval(titulos)
    sum += len(titulos)
    anios = row["Anios"]
    anios = ast.literal_eval(anios)

    uniprotid = row["UniProtID"]

    for i in range(len(titulos)):
        linea = ""
        linea += (str(cont) + "~" + uniprotid + "~" + titulos[i] + "~" + anios[i].split(sep="-")[-1] + "~" + str(autores[i])+ "\n")
        salidaRef.write(linea)
        sum += len(autores[i])
        for j in autores[i]:
            if j in dictAutores.keys():
                dictAutores[j].append(cont)
            else:
                dictAutores[j] = [cont]
                # print(j)
                # dfAutores.append({"Autor" : j, "idReferencia":cont}, ignore_index=True)
        cont += 1

salidaRef.close()

# df = pd.read_csv("datos/referencias.csv", sep="~")
# print(df.info())
# #df["idReferencia"] = range(1, len(df)+1)
# df.to_csv("datos/referencias.csv", sep="~", index=False)

salidaAutores = open("datos/autores.csv", "w")
salidaAutores.write("idReferencia~Autor\n")

for autor in dictAutores.keys():
    print(autor, dictAutores[autor])
    for ref in dictAutores[autor]:
        salidaAutores.write(f"{ref}~{autor}\n")
