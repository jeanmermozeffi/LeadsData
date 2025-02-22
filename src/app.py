
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st


# from utils.data_cleaning import preprocessing
from loads import loads
from utils import configs
from visualization.visualization import plot_bar_chart, plot_pie_chart, plot_scatter_plot, plot_box_plot, \
    plot_histogram, plot_profiles_by_language


st.set_page_config(
    page_title="Rapporting Data Storage",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.sidebar.title("Statistique Data Mailing")

pages = ["Contexte du projet", "Exploration des données", "Analyse de données", "Modélisation"]

page = st.sidebar.radio("Aller vers la page :", pages)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# Fonction pour charger les données depuis Google Sheets
@st.cache_data
def load_data(credentials, spreadsheet_name):
    dataframe = loads.load_google_sheet_to_df(credentials, spreadsheet_name)
    return dataframe


if page == pages[0]:
    original_title = '<h1 style="font-family: serif; color:white; font-size: 20px;">✨ </h1>'
    st.markdown(original_title, unsafe_allow_html=True)

    # Utilisation de la fonction cache pour charger les données
    df_raw = load_data(GOOGLE_APPLICATION_CREDENTIALS, configs.search_keys[0])
    df = df_raw.copy()

    st.write("### Exploration des données")
    st.dataframe(df.head(50))
    st.write("Dimensions :")
    st.write("Total Observations", df.shape[0])
    st.write("Total Colonnes", df.shape[1])

    cols = ['first_name',
            'last_name',
            'full_name',
            'job_title',
            'email',
            'phone',
            'current_company_name',
            'industry',
            'profile_country',
            'number_followers',
            'languages',
            'company_employees_range',
            'profile_url',
            'linkedin_company_url',
            'company_industry',
            'profile_language',
            'profile_id'
            ]

    df = df[cols]
    st.dataframe(df)

    plot_bar_chart(df)
    plot_pie_chart(df)
    plot_scatter_plot(df)
    plot_box_plot(df)
    plot_histogram(df)

    plot_profiles_by_language(df)