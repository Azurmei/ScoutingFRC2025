import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

credential_info = json.loads(st.secrets["google_sheets"]["credentials"])
creds = Credentials.from_service_account_info(credential_info, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "17xj8_9JKI6-eLeqaqHS089Qq_GLOKCHQQk9dRRP37ss"
sheet = client.open_by_key(sheet_id)

def append_data(worksheet, data:list) -> bool:
    worksheet.append_row(data)
    return True