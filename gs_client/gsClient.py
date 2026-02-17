import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# === Google Sheets Setup ===
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Load entire google_sheets block directly
creds_info = dict(st.secrets["google_sheets"])

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
