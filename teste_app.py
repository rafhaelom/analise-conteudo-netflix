import streamlit as st
import pandas as pd

df = pd.read_csv("dados/netflix_titles.csv")

st.title("Análise Netflix")
st.dataframe(df)
st.bar_chart(data=df[["show_id", "type"]].groupby(by="type")["show_id"].count())

st.bar_chart(data=df[["show_id", "type", "release_year"]].groupby(by="release_year")["show_id"].count())

st.metric(label="Qtd conteudo", value=len(df))

# st.area_chart(data=df[["show_id", "type", "release_year"]].groupby(by=["type", "release_year"])["show_id"].count(), y=df[["show_id", "type", "release_year"]].groupby(by=["type", "release_year"])["show_id"].count().index)