import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials

# === Google Sheets Setup ===
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Load service account info from Streamlit secrets
credential_info = json.loads(st.secrets["google_sheets"]["credentials"])
creds = Credentials.from_service_account_info(credential_info, scopes=scopes)
client = gspread.authorize(creds)

# Replace with your actual Sheet ID
sheet_id = "17xj8_9JKI6-eLeqaqHS089Qq_GLOKCHQQk9dRRP37ss"
sheet = client.open_by_key(sheet_id)

# === Sheet Helper Functions ===
def append_data(worksheet, data: list) -> bool:
    """Append a row to the worksheet"""
    worksheet.append_row(data)
    return True

def grab_all_data(worksheet):
    """Return all data from the worksheet"""
    return worksheet.get_all_values()

def check_duplicate(worksheet, data: list) -> bool:
    """Check if the row already exists"""
    exist_data = worksheet.get_all_values()
    if len(exist_data) <= 1:  # Only header exists
        return False
    return data in exist_data
