import base64
import requests
import streamlit as st

BASE_URL = "https://frc-api.firstinspires.org/v3.0"
SEASON = 2025

USERNAME = st.secrets["frcapi"]["username"]
AUTH = st.secrets["frcapi"]["auth"]

# Combine and encode
token_raw = f"{USERNAME}:{AUTH}"
token_bytes = token_raw.encode("ascii")
auth_token = base64.b64encode(token_bytes).decode("ascii")

headers = {
    "Authorization": f"Basic {auth_token}",
    "Accept": "application/json"
}


def get_comp_teams(eventCode: str) -> list:
    team_list = []
    url = f"{BASE_URL}/{SEASON}/teams?eventCode={eventCode}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for t in data["teams"]:
            team_list.append(t["teamNumber"])
    else:
        st.error(f"API Error: {response.status_code} — {response.text}")

    return team_list
