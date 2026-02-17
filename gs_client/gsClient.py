import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# === Google Sheets Setup ===
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Load service account info directly from secrets (no json.loads)
creds_info = {
    "type": st.secrets["google_sheets"]["type"],
    "project_id": st.secrets["google_sheets"]["project_id"],
    "private_key_id": st.secrets["google_sheets"]["private_key_id"],
    "private_key": st.secrets["google_sheets"]["private_key"],
    "client_email": st.secrets["google_sheets"]["client_email"],
    "client_id": st.secrets["google_sheets"]["client_id"],
    "auth_uri": st.secrets["google_sheets"]["auth_uri"],
    "token_uri": st.secrets["google_sheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_sheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"],
    "universe_domain": st.secrets["google_sheets"]["universe_domain"],
}

creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "17xj8_9JKI6-eLeqaqHS089Qq_GLOKCHQQk9dRRP37ss"
sheet = client.open_by_key(sheet_id)

# === Sheet Helper Functions ===
def append_data(worksheet, data: list) -> bool:
    worksheet.append_row(data)
    return True

def grab_all_data(worksheet):
    return worksheet.get_all_values()

def check_duplicate(worksheet, data: list) -> bool:
    exist_data = worksheet.get_all_values()
    if len(exist_data) <= 1:
        return False
    return data in exist_data
