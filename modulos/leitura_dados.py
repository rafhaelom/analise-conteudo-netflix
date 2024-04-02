import numpy as np
import pandas as pd


def ler_dados(path_dados:None, sep:str):
    return pd.read_csv(path_dados, sep=sep)

# total = sum(df_base.type.value_counts().values)
# filmes = df_base.type.value_counts().values[0]
# series = df_base.type.value_counts().values[1]
# perc_total = (total/total)*100
# perc_filmes = (filmes/total)*100
# perc_series = (series/total)*100