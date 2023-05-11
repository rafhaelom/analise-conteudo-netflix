import streamlit as st

import numpy as np
import pandas as pd

import modulos.leitura_dados as leitura_dados
import modulos.filtro_dados as filtro_dados

df = leitura_dados.ler_dados(path_dados="./dados/tb_netflix.txt", sep=";")

##### Sidbar menu #####
st.sidebar.markdown("""<h1 align='center'>Análise Netflix<h1 align='justify'>""", unsafe_allow_html=True)
st.sidebar.markdown("""<p align='justify'>Os dados estão disponíveis <a href="https://www.kaggle.com/datasets/shivamb/netflix-shows">Kaggle</a>, e demonstra uma listagem de filmes e séries na Netflix.<p align='justify'>""", unsafe_allow_html=True)


##### INÍCIO APP.
# st.title('Visualização de Dados de filmes e séries da Netflix')
st.markdown("""<h1 align='center'>Visualização de Dados de filmes e séries da Netflix<h1 align='justify'>""", unsafe_allow_html=True)

st.markdown("""<p align='justify'>A <a href="https://www.netflix.com/br/">Netflix</a> é uma plataforma de serviço online de streaming norte-americano de mídia e vídeos sob demanda por assinatura (Over The Top - OTT) lançada em 2010 e disponível em mais de 190 países <cite><a href="https://pt.wikipedia.org/wiki/Netflix#cite_note-12">[Wikipedia]</a></cite>.
Como premissa para as análises e organização do projeto, é utilizada a metodologia <a href="https://www.datascience-pm.com/crisp-dm-2/">Cross Industry Standard Process for Data Mining (CRISP-DM)</a>.<p align='justify'>""", unsafe_allow_html=True)

st.markdown("""<h2 align='center'>Estatísticas Gerais<h2 align='justify'>""", unsafe_allow_html=True)

tipos = st.radio("Escolha o tipo:", ('All', 'Filmes', 'Séries'))

if tipos == 'Filmes':
    st.write("Filmes")
    df_base = filtro_dados.filtrar_dados(df, 'type', 'Movie')
    total, filmes, series, perc_total, perc_filmes, perc_series = filtro_dados.calcular_estatisticas(df_base, 'Filmes')
elif tipos == 'Séries':
    st.write("Séries")
    df_base = filtro_dados.filtrar_dados(df, 'type', 'TV Show')
    total, filmes, series, perc_total, perc_filmes, perc_series = filtro_dados.calcular_estatisticas(df_base, 'Séries')
else:
    st.write("All")
    df_base = df
    # total, filmes, series, perc_total, perc_filmes, perc_series = filtro_dados.calcular_estatisticas(df_base, None)
    total = sum(df_base.type.value_counts().values)
    filmes = df_base.type.value_counts().values[0]
    series = df_base.type.value_counts().values[1]
    perc_total = (total/total)*100
    perc_filmes = (filmes/total)*100
    perc_series = (series/total)*100


with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Qtd conteúdos", value=total, delta=f"{perc_total:1.0f}%")

    with col2:
        st.metric(label="Qtd filmes", value=filmes, delta=f"{perc_filmes:1.2f}%")

    with col3:
        st.metric(label="Qtd séries", value=series, delta=f"{perc_series:1.2f}%")

# with st.container():
#     st.markdown("""<h3 align='justify'>Qtd<h3 align='justify'>""", unsafe_allow_html=True)
