import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

# import modulos.leitura_dados as leitura_dados
# import modulos.filtro_dados as filtro_dados
# import modulos.graficos_dados as graficos_dados

############################## DADOS ##############################
df = pd.read_csv("./dados/tb_netflix.txt", sep=";")
# df_qtd_ano_mes_added = leitura_dados.ler_dados(path_dados="./dados/tb_netflix_ano_mes_add.txt", sep=";")
# df_qtd_diretor = leitura_dados.ler_dados(path_dados="./dados/tb_netflix_diretor.txt", sep=";")

############################## AJUSTES NOS DADOS ##############################
##### Segmentação entre filmes e séries #####
### Filmes
df_filmes = df.loc[df["type"] == "Movie"]
### Séries
df_series = df.loc[df["type"] != "Movie"]

##### Correção no formato da data adicionada na Netflix (date_added) #####
df["date_added_aux"] = pd.to_datetime(df['date_added'])

# Criar coluna mês adicionada na Netflix a partir de (date_added).
# mês numérico
df['month_added_num'] = df['date_added_aux'].dt.month.astype('Int64')
df['month_added_num'] = df['month_added_num'].fillna(np.nan)

# mês como carácter
df['month_added_char'] = df['date_added_aux'].dt.month.astype('Int64').astype(str)
df['month_added_char'].replace('<NA>', 'N/A', inplace  = True)

# nome do mês
df['month_name_added_char'] = df['date_added_aux'].dt.month_name().astype(str)
df['month_name_added_char'].replace('nan', 'N/A', inplace  = True)

# Criar coluna ano adicionada na Netflix a partir de (date_added).
# ano numérico
df['year_added_num'] = df['date_added_aux'].dt.year.astype('Int64')
df['year_added_num'] = df['year_added_num'].fillna(np.nan)

# ano como carácter
df['year_added_char'] = df['date_added_aux'].dt.year.astype('Int64').astype(str)
df['year_added_char'].replace('<NA>', 'N/A', inplace  = True)

# número do mês para número e sigla mês
num_nome_mes = {"1": "01-JAN",
                "2": "02-FEV",
                "3": "03-MAR", 
                "4": "04-ABR", 
                "5": "05-MAI", 
                "6": "06-JUN",
                "7": "07-JUL",
                "8": "08-AGO",
                "9": "09-SET",
                "10": "10-OUT",
                "11": "11-NOV",
                "12": "12-DEZ"}

df["nome_mes_extracao"] = df["month_added_char"].replace(num_nome_mes)

##### Correção do tipo para a duração (duration) #####
df['duration_char'] = df['duration'].apply(lambda x: str(x).split(" ")[0])
df['duration_char'].replace('nan', 'N/A',inplace  = True)
df['duration_num'] = df['duration_char'].replace('N/A', np.nan).astype('Int64')

##### Ajuste para o quantitativo de classificação indicativa (rating) #####
df['rating'] = df['rating'].astype(str)
df['rating'].replace('nan', 'N/A', inplace  = True)
df['rating'].replace('66 min', 'N/A', inplace  = True)
df['rating'].replace('74 min', 'N/A', inplace  = True)
df['rating'].replace('84 min', 'N/A', inplace  = True)

class_indicative_perfil = {'TV-MA':'Adults',
                           'TV-14':'Teens',
                           'TV-PG':'Kids',
                           'R':'Adults',
                           'PG-13':'Teens',
                           'TV-Y7':'Kids',
                           'TV-Y':'Kids',
                           'PG':'Kids',
                           'TV-G':'Kids',
                           'NR':'Adults',
                           'G':'Kids',
                           'N/A':'Sem Informação',
                           'TV-Y7-FV':'Kids',
                           'NC-17':'Adults',
                           'UR':'Não classificado'}

df["rating_profile"] = df["rating"].replace(class_indicative_perfil)

##### Ajuste para o quantitativo de diretores (director) #####
df['director'] = df['director'].astype(str)
df['director'].replace('nan', 'N/A', inplace  = True)

##### Ajuste para o quantitativo de atores (cast) #####
df['cast'] = df['cast'].astype(str)
df['cast'].replace('nan', 'N/A', inplace  = True)

##### Ajuste para o quantitativo da classificação do gênero (listed_in) #####
df['listed_in'] = df['listed_in'].astype(str)
df['listed_in'].replace('nan', 'N/A', inplace  = True)

##### Ajuste para o quantitativo por país (country) #####
df['country'] = df['country'].astype(str)
df['country'].replace('nan', 'N/A', inplace  = True)
df['country'] = df['country'].str.lstrip()
df['country'] = df['country'].str.strip()

##### Preparação do titulo (title) e da descrição (description) para representação em WordCloud #####
prep_title = str(list(df['title'])).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')
prep_description = str(list(df['description'])).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')

############################## INÍCIO APP ##############################
##### Sidbar menu #####
st.sidebar.title("Análise Netflix 🎬")
st.sidebar.write("Os dados estão disponíveis [Kaggle]('https://www.kaggle.com/datasets/shivamb/netflix-shows'), e demonstra uma listagem de filmes e séries na Netflix.")
st.sidebar.write("---")
##### Página app #####
st.title("Visualização de Dados de filmes e séries da Netflix 📺")
st.write("""A [Netflix]('https://www.netflix.com/br/') é uma plataforma de serviço online de streaming norte-americano de mídia e vídeos sob demanda por assinatura (Over The Top - OTT) lançada em 2010 e disponível em mais de 190 países [Wikipedia]('https://pt.wikipedia.org/wiki/Netflix#cite_note-12').
Como premissa para as análises e organização do projeto, é utilizada a metodologia [Cross Industry Standard Process for Data Mining (CRISP-DM)]('https://www.datascience-pm.com/crisp-dm-2/').""")

st.write("---")
############################## DADOS ##############################
st.header("Dados 🎲")
st.dataframe(df.head(), use_container_width=True)

st.write("---")
############################## ESTATÍSTICAS GERAIS ##############################
st.header("Estatísticas Gerais 🧮")

total = sum(df.type.value_counts().values)
filmes = df.type.value_counts().values[0]
series = df.type.value_counts().values[1]
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

st.write("---")
############################## VISUALIZAÇÃO ##############################
st.header("Visualização 📊")

df_base = df.copy()

with st.container():
    st.subheader("Proporção por tipo de conteúdo")

    ##### Proporção por tipo #####
    fig = plt.figure(figsize=(8,3))
    ax = sns.countplot(data=df_base, x=None, y='type', order=df['type'].value_counts(ascending=False).index, palette="mako")

    type_values = df_base['type'].value_counts(ascending=False).values
    # type_perc_values = df_base['type'].value_counts(ascending=False, normalize=True).values * 100
    type_labels = [f'{value[0]}' for value in zip(type_values)]
    ax.bar_label(container=ax.containers[0], labels=type_labels)

    plt.xlabel(None)
    plt.ylabel(None)
    ax.set(xticklabels=[])
    st.pyplot(fig)
    plt.clf()
    
    st.write("---")

with st.container():
    st.subheader("Proporção po Classificação Indicativa e tipo de conteúdo")

    ##### Proporção po Classificação Indicativa e tipo de conteúdo #####
    df_qtd_class_ind = df_base.groupby(by=['type', 'rating', 'rating_profile'], as_index=False)['show_id'].count()
    df_qtd_class_ind.rename(columns={'show_id':'qtd'}, inplace=True)
    df_qtd_class_ind2 = df_qtd_class_ind[["type", "rating_profile", "qtd"]].sort_values(by=['type', 'qtd'], ascending=False, ignore_index=True)
    
    fig = plt.figure(figsize=(12,4))
    sns.barplot(data=df_qtd_class_ind2, x="rating_profile", y="qtd", hue='type', palette="mako")
    st.pyplot(fig)
    plt.clf()

    st.write("---")

with st.container():
    st.subheader("Proporção por ano de lançamento e tipo")

    ##### Proporção por ano de lançamento e tipo #####
    # Quantitativo por ano de lançamento e tipo
    df_qtd_ano_mes_release_year = df_base.groupby(by=['type', 'release_year'], as_index=False)['show_id'].count()
    df_qtd_ano_mes_release_year.rename(columns={'show_id':'qtd'}, inplace=True)

    fig = plt.figure(figsize=(12,6))
    sns.lineplot(data=df_qtd_ano_mes_release_year, x='release_year', y='qtd', hue='type', palette="mako")
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(fig)
    plt.clf()

    st.write("---")

with st.container():
    st.subheader("Proporção por ano e mês adicionado na Netflix")

    ##### Proporção por ano, mês adicionado #####
    # Quantitativo por ano e mês adicionada na Netflix.
    df_qtd_ano_mes_added = df.groupby(by=['type', 'year_added_char', 'nome_mes_extracao'], as_index=False)['show_id'].count()
    df_qtd_ano_mes_added.rename(columns={'show_id':'qtd'}, inplace=True)

    df_qtd_ano_mes_added_filmes = df_qtd_ano_mes_added.loc[df_qtd_ano_mes_added["type"] == "Movie"]
    df_qtd_ano_mes_added_filmes = pd.pivot_table(data=df_qtd_ano_mes_added_filmes, values="qtd", index=["nome_mes_extracao"], columns=["year_added_char"], aggfunc=np.sum, fill_value=0)
    df_qtd_ano_mes_added_filmes = df_qtd_ano_mes_added_filmes.sort_index()

    df_qtd_ano_mes_added_series = df_qtd_ano_mes_added.loc[df_qtd_ano_mes_added["type"] != "Movie"]
    df_qtd_ano_mes_added_series = pd.pivot_table(data=df_qtd_ano_mes_added_series, values="qtd", index=["nome_mes_extracao"], columns=["year_added_char"], aggfunc=np.sum, fill_value=0)
    df_qtd_ano_mes_added_series = df_qtd_ano_mes_added_series.sort_index()

    st.markdown("### Filmes")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df_qtd_ano_mes_added_filmes, annot=True, fmt="d", linewidths=.5, ax=ax, cmap='mako')
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(fig)
    plt.clf()

    st.markdown("### Séries")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df_qtd_ano_mes_added_series, annot=True, fmt="d", linewidths=.5, ax=ax, cmap='mako')
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(fig)
    plt.clf()

    st.write("---")

with st.container():
    st.subheader("Proporção tempo de duração ou seções")

    filmes = df['duration_num'].loc[df['type'] == 'Movie'].fillna(0)
    series = df['duration_num'].loc[df['type'] == 'TV Show'].fillna(0)

    tab1, tab2 = st.tabs(["Filmes", "Séries"])
    
    with tab1:
        st.markdown("### Filmes")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(filmes, ax=ax)
        plt.xlabel("Minutos")
        st.pyplot(fig)
        plt.clf()

    with tab2:
        st.markdown("### Séries")
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.histplot(series, ax=ax)
        plt.xlabel("Seções")
        st.pyplot(fig)
        plt.clf()

    st.write("---")


with st.container():
    st.subheader("Top 10 diretores")

    # Quantitativo de diretores (director).
    # Filmes
    filmes_qtd_diretor = df_filmes['director'].str.get_dummies(', ').sum()
    df_filmes_qtd_diretor = pd.DataFrame({'diretor':filmes_qtd_diretor.index, 'qtd':filmes_qtd_diretor.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_filmes_qtd_diretor.insert(0, "type", "Movie")

    # Séries
    series_qtd_diretor = df_series['director'].str.get_dummies(', ').sum()
    df_series_qtd_diretor = pd.DataFrame({'diretor':series_qtd_diretor.index, 'qtd':series_qtd_diretor.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_series_qtd_diretor.insert(0, "type", "TV Show")

    df_qtd_diretor = pd.concat([df_filmes_qtd_diretor, df_series_qtd_diretor], ignore_index=True)

    tab1, tab2 = st.tabs(["Filmes", "Séries"])
    
    with tab1:
        st.markdown("### Filmes")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_diretor.loc[df_qtd_diretor.type == "Movie"][:10], x="qtd", y="diretor", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    with tab2:
        st.markdown("### Séries")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_diretor.loc[df_qtd_diretor.type != "Movie"][:10], x="qtd", y="diretor", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    st.write("---")



with st.container():
    st.subheader("Top 10 atores")

    st.write("---")


with st.container():
    st.subheader("Top 10 genero")

    ##### Quantitativo da classificação do gênero (listed_in) #####
    # Filmes
    filmes_qtd_genero = df_filmes['listed_in'].str.get_dummies(', ').sum()
    df_filmes_qtd_genero = pd.DataFrame({'genero':filmes_qtd_genero.index, 'qtd':filmes_qtd_genero.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_filmes_qtd_genero.insert(0, "type", "Movie")

    # Séries
    series_qtd_genero = df_series['listed_in'].str.get_dummies(', ').sum()
    df_series_qtd_genero = pd.DataFrame({'genero':series_qtd_genero.index, 'qtd':series_qtd_genero.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_series_qtd_genero.insert(0, "type", "TV Show")

    df_qtd_genero = pd.concat([df_filmes_qtd_genero, df_series_qtd_genero], ignore_index=True)

    # Top 10 genero
    tab1, tab2 = st.tabs(["Filmes", "Séries"])
    
    with tab1:
        st.markdown("### Filmes")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_genero.loc[df_qtd_genero.type == "Movie"][:10], x="qtd", y="genero", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    with tab2:
        st.markdown("### Séries")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_genero.loc[df_qtd_genero.type != "Movie"][:10], x="qtd", y="genero", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    st.write("---")


with st.container():
    st.subheader("Top 10 países")
    ##### Quantitativo por país (country) #####
    # Filmes
    filmes_qtd_pais = df_filmes['country'].str.get_dummies(', ').sum()
    df_filmes_qtd_pais = pd.DataFrame({'country':filmes_qtd_pais.index, 'qtd':filmes_qtd_pais.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_filmes_qtd_pais.insert(0, "type", "Movie")

    # Séries
    series_qtd_pais = df_series['country'].str.get_dummies(', ').sum()
    df_series_qtd_pais = pd.DataFrame({'country':series_qtd_pais.index, 'qtd':series_qtd_pais.values}).sort_values(by="qtd", ascending=False, ignore_index=True)
    df_series_qtd_pais.insert(0, "type", "TV Show")

    df_qtd_pais = pd.concat([df_filmes_qtd_pais, df_series_qtd_pais], ignore_index=True)

    # Top 10 país
    tab1, tab2 = st.tabs(["Filmes", "Séries"])
    
    with tab1:
        st.markdown("### Filmes")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_pais.loc[df_qtd_pais.type == "Movie"][:10], x="qtd", y="country", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    with tab2:
        st.markdown("### Séries")
        fig, ax = plt.subplots(figsize=(8,10))
        sns.barplot(data=df_qtd_pais.loc[df_qtd_pais.type != "Movie"][:10], x="qtd", y="country", palette="mako", ax=ax)
        st.pyplot(fig)
        plt.clf()

    st.write("---")


with st.container():
    st.subheader("Quais são as séries mais atuais e as mais antigas?")
    
    ##### Quais são as séries mais atuais e as mais antigas? #####
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Mais atuais")
        st.dataframe(df[["title", "release_year"]].sort_values(by="release_year", ascending=False, ignore_index=True)[:10])
    
    with col2:
        st.markdown("### Mais antigas")
        st.dataframe(df[["title", "release_year"]].sort_values(by="release_year", ascending=True, ignore_index=True)[:10])
    
    st.write("---")

with st.container():
    st.subheader("Nuvem de palavras do título dos conteúdos")
    with st.spinner('Carregando...'):
        wordcloud = WordCloud(background_color = 'white', width = 700,  height = 500, max_words = 150).generate(prep_title)

        fig = plt.figure(figsize=(12,6))
        plt.imshow(wordcloud, interpolation = 'bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        st.pyplot(fig)
        plt.clf()

    st.write("---")

with st.container():
    st.subheader("Nuvem de palavras da descrição dos conteúdos")
    with st.spinner('Carregando...'):
        wordcloud = WordCloud(background_color = 'white', width = 700,  height = 500, max_words = 150).generate(prep_description)

        fig = plt.figure(figsize=(12,6))
        plt.imshow(wordcloud, interpolation = 'bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        st.pyplot(fig)
        plt.clf()

    st.write("---")