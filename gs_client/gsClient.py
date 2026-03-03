import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

st.write("GOOGLE SHEETS KEYS:")
st.write(st.secrets["google_sheets"].keys())
st.stop()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds_info = dict(st.secrets["google_sheets"])

creds = Credentials.from_service_account_info(
    creds_info,
    scopes=scopes
)

client = gspread.authorize(creds)

sheet_id = "1Sp-rPlrjyfu0UizkBmZKc__S3Sgy0g0Prl8s1wjFWHk"
sheet = client.open_by_key(sheet_id)

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