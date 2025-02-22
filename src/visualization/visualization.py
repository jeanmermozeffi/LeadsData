import pandas as pd
import streamlit as st
import plotly.express as px


def plot_bar_chart(dataframe: pd.DataFrame):
    industry_counts = dataframe['industry'].value_counts()
    fig = px.bar(industry_counts, x=industry_counts.index, y=industry_counts.values,
                 labels={'x': 'Industry', 'y': 'Count'},
                 title='Distribution Nombre de personnes par secteur d\'industrie')
    st.plotly_chart(fig)


def plot_pie_chart(dataframe: pd.DataFrame):
    country_counts = dataframe['profile_country'].value_counts()
    fig = px.pie(country_counts, values=country_counts.values, names=country_counts.index,
                 title='Répartition des profils par pays')
    st.plotly_chart(fig)


def plot_scatter_plot(dataframe: pd.DataFrame):
    fig = px.scatter(dataframe, x='number_followers', y='industry',
                     size='number_followers', color='industry', hover_name='full_name',
                     title='Relation entre le nombre de followers et l\'industrie')
    st.plotly_chart(fig)


def plot_box_plot(dataframe: pd.DataFrame):
    fig = px.box(dataframe, x='industry', y='number_followers', points='all',
                 title='Répartition du nombre de followers par secteur d\'industrie')
    st.plotly_chart(fig)


def plot_histogram(dataframe: pd.DataFrame):
    fig = px.histogram(dataframe, x='company_employees_range', color='company_employees_range',
                       title='Distribution des employés par entreprise')
    st.plotly_chart(fig)


def plot_profiles_by_language(dataframe: pd.DataFrame):
    language_counts = dataframe['profile_language'].value_counts()
    total_profiles = language_counts.sum()

    fig = px.bar(language_counts, x=language_counts.index, y=language_counts.values,
                 labels={'x': 'Langue', 'y': 'Nombre de profils'},
                 title='Nombre de profils par langue de profil')

    # Ajout des annotations pour afficher les pourcentages
    fig.update_traces(texttemplate='%{y:.0f} (%{text:.1f}%)', text=language_counts / total_profiles * 100)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    st.plotly_chart(fig)
