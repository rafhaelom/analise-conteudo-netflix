import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

sns.set_style("darkgrid")

def grafico_contagem(df:pd.DataFrame, x:None, y:None, titulo:str, paleta_cores:None):
    fig = plt.figure(figsize=(8,3))
    ax = sns.countplot(data=df, y=x,
                       order=df[x].value_counts(ascending=False).index,
                       palette=paleta_cores)

    type_values = df[x].value_counts(ascending=False).values
    type_perc_values = df[x].value_counts(ascending=False, normalize=True).values * 100
    type_labels = [f'{value[0]} ({value[1]:1.2f}%)' for value in zip(type_values, type_perc_values)]
    ax.bar_label(container=ax.containers[0], labels=type_labels)

    plt.title(titulo)
    plt.xlabel(None)
    plt.ylabel(None)
    ax.set(xticklabels=[])
    # plt.show()
    st.pyplot(fig)
    plt.clf()


def grafico_linha(df:pd.DataFrame, x:None, y:None, legenda:None, titulo:str, paleta_cores:None):
    fig = plt.figure(figsize=(12,4))
    sns.lineplot(data=df, x=x, y=y, hue=legenda, palette=paleta_cores)
    plt.title(titulo)
    plt.xlabel(None)
    plt.ylabel(None)
    # plt.show()
    st.pyplot(fig)
    plt.clf()

def grafico_mapacalor(df:pd.DataFrame, x:None, y:None, legenda:None, titulo:str, paleta_cores:None):
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df, annot=True, fmt="d", linewidths=.5, ax=ax, cmap=paleta_cores)
    plt.title(titulo)
    plt.xlabel(None)
    plt.ylabel(None)
    # plt.show()
    st.pyplot(fig)
    plt.clf()

def grafico_barras(df:pd.DataFrame, x:None, y:None, legenda:None, titulo:str, paleta_cores:None):
    fig = plt.figure(figsize=(20,10))
    sns.barplot(data=df, x=x, y=y, hue=legenda, palette=paleta_cores)
    plt.title(titulo)
    plt.xlabel(None)
    plt.ylabel(None)
    # plt.show()
    st.pyplot(fig)
    plt.clf()