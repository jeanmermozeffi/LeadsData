import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def load_google_sheet_to_df(credentials_path: str, spreadsheet_name: str) -> pd.DataFrame:
    # Définir la portée
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Ajouter les identifiants API depuis le fichier JSON
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

    # Autoriser les identifiants
    gc = gspread.authorize(credentials=credentials)

    try:
        spreadsheet = gc.open(spreadsheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Spreadsheet '{spreadsheet_name}' not found.")

    # Vérifier si la feuille de calcul est vide
    if not spreadsheet:
        raise ValueError(f"Spreadsheet '{spreadsheet_name}' is empty or not accessible.")

    sheet = spreadsheet.sheet1
    data = sheet.get_all_records()

    dataframe = pd.DataFrame(data)

    return dataframe


