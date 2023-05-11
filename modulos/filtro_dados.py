import streamlit as st

import numpy as np
import pandas as pd

def filtrar_dados(df:None, coluna:None, selecao_dados:None):
    return df[df[coluna].isin([selecao_dados])]

def calcular_estatisticas(df:None, filtro:None):
    if filtro == 'Filmes':
        st.write("Filmes")
        total = sum(df.type.value_counts().values)
        filmes = df.type.value_counts().values[0]
        series = 0
        perc_total = (total/total)*100
        perc_filmes = (filmes/total)*100
        perc_series = (series/total)*100
        return total, filmes, series, perc_total, perc_filmes, perc_series
    elif filtro == 'Séries':
        st.write("Séries")
        total = sum(df.type.value_counts().values)
        filmes = 0
        series = df.type.value_counts().values[1]
        perc_total = (total/total)*100
        perc_filmes = (filmes/total)*100
        perc_series = (series/total)*100
        return total, filmes, series, perc_total, perc_filmes, perc_series
    else:
        st.write("All")
        total = sum(df.type.value_counts().values)
        filmes = df.type.value_counts().values[0]
        series = df.type.value_counts().values[1]
        perc_total = (total/total)*100
        perc_filmes = (filmes/total)*100
        perc_series = (series/total)*100
        
        return total, filmes, series, perc_total, perc_filmes, perc_series
