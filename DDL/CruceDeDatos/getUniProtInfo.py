import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from tqdm import tqdm


df_proteinas = pd.read_csv("datos/salida.csv", sep="~")
df_proteinas = df_proteinas.drop_duplicates(subset="UniProtID")
df_ProtParam = pd.DataFrame()

df_proteinas = df_proteinas.dropna(subset=["Secuencia"])

df_ProtParam["UniProtID"] = df_proteinas["UniProtID"]
df_ProtParam["Secuencia"] = df_proteinas["Secuencia"]


total_rows = len(df_ProtParam["Secuencia"])
progress_bar = tqdm(total=total_rows, desc='Progreso', position=0)

pesosMoleculares = []
pIs = []
fraccionesHelice = []
fraccionesGiro = []
fraccionesHoja = []

for _, row in df_ProtParam.iterrows():
    X = ProteinAnalysis(row["Secuencia"])
    pesosMoleculares.append("%0.2f" % X.molecular_weight())
    pIs.append("%0.2f" % X.isoelectric_point())
    fraccionesHelice.append("%0.2f" % X.secondary_structure_fraction()[0])
    fraccionesGiro.append("%0.2f" % X.secondary_structure_fraction()[1])
    fraccionesHoja.append("%0.2f" % X.secondary_structure_fraction()[2])

    progress_bar.update(1)
    
progress_bar.close()

df_ProtParam["pesoMol"] = pesosMoleculares
df_ProtParam["pI"] = pIs
df_ProtParam["fraccionHelice"] = fraccionesHelice
df_ProtParam["fraccionGiro"] = fraccionesGiro
df_ProtParam["fraccionHoja"] = fraccionesHoja

df_ProtParam.drop("Secuencia", axis=1)

df_ProtParam.to_csv("datos/protParam.csv", index=False)