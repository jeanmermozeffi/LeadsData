import pandas as pd
from thefuzz import fuzz

from utils.configs import default_clients_list


def convert_employee_range(range_str: str) -> int:
    if not range_str.strip():
        return 0

    # Vérifier si la chaîne est mal formatée (ne contient pas de tiret ou a des espaces incorrects)
    if '-' not in range_str or range_str.strip().count('-') != 1:
        return 0

    try:
        parts = range_str.split('-')

        # Vérifier si la partie après le tiret est correcte
        if len(parts) != 2 or not parts[0].strip() or (not parts[1].strip() and not range_str.endswith(' ')):
            return 0

        start = int(parts[0].strip())

        # Si la partie après le tiret contient '+', ou si elle est vide mais que la chaîne se termine par '-'
        if '+' in parts[1] or range_str.endswith(' '):
            end = int(start)
        else:
            end = int(parts[1].strip())

        return int((start + end) // 2)

    except ValueError:
        # Gestion des erreurs de conversion
        return 0


def filter_no_email(dataframe, email_column):
    """
    Filtre les enregistrements qui n'ont pas d'adresse e-mail valide dans un DataFrame.

    Parameters:
    df (pandas.DataFrame): Le DataFrame à filtrer.
    email_column (str): Le nom de la colonne contenant les adresses e-mail.

    Returns:
    pandas.DataFrame: Un DataFrame filtré contenant uniquement les enregistrements avec des adresses e-mail valides.
    """
    # Filtrer les enregistrements où la colonne email_column n'est pas vide et n'est pas NaN
    filtered_df = dataframe[dataframe[email_column].notna() & dataframe[email_column].str.strip().astype(bool)]
    return filtered_df


def filter_valid_records(dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Filtre les enregistrements qui ont des valeurs valides (non nulles et non vides) dans toutes les colonnes
    spécifiées.

    Parameters:
    df (pandas.DataFrame): Le DataFrame à filtrer.
    columns (list of str): La liste des noms de colonnes à vérifier pour des valeurs valides.

    Returns:
    pandas.DataFrame: Un DataFrame filtré contenant uniquement les enregistrements avec des valeurs valides dans toutes
    les colonnes spécifiées.
    """

    for column in columns:
        dataframe = dataframe[dataframe[column].notna() & dataframe[column].str.strip().astype(bool)]

    return dataframe


def clean_strings_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les chaînes de caractères dans un DataFrame.
    Supprime les espaces en début et fin, remplace les espaces multiples par un seul espace,
    et met les chaînes en minuscules.
    """
    df_cleaned = df.copy()

    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].astype(str)
        df_cleaned[col] = df_cleaned[col].str.strip()
        df_cleaned[col] = df_cleaned[col].str.replace(r'\s+', ' ', regex=True)
        df_cleaned[col] = df_cleaned[col].str.lower()

    return df_cleaned


def remove_rows_with_specific_words(df: pd.DataFrame, columns: list, words: list) -> pd.DataFrame:
    """
    Supprime les lignes d'un DataFrame contenant des mots spécifiques dans une ou plusieurs colonnes.

    :param df: Le DataFrame à traiter.
    :param columns: Liste des colonnes à vérifier.
    :param words: Liste des mots à rechercher et supprimer.
    :return: Un DataFrame avec les lignes supprimées.
    """
    pattern = '|'.join(words)
    mask = df[columns].apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False)).any(axis=1)
    return df[~mask]


def filter_no_clients(dataframe: pd.DataFrame,
                      clients_list: list = default_clients_list,
                      threshold: int = 85
                      ) -> pd.DataFrame:
    def is_client(company_name: str) -> bool:
        for client in clients_list:
            if fuzz.token_set_ratio(company_name.lower(), client.lower()) >= threshold:
                return True
        return False

    return dataframe[~dataframe['current_company_name'].apply(is_client)]
