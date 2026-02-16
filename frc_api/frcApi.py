import streamlit as st
import requests

TBA_API_KEY = st.secrets["tba"]["api_key"]

BASE_URL = "https://www.thebluealliance.com/api/v3"

HEADERS = {
    "X-TBA-Auth-Key": TBA_API_KEY
}

def get_comp_teams(event_code, season=2025):
    """
    event_code example: "bcvi"
    season example: 2025
    """

    event_key = f"{season}{event_code.lower()}"
    url = f"{BASE_URL}/event/{event_key}/teams"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"TBA Error {response.status_code}: {response.text}")

    teams = response.json()

    # Return sorted team numbers only
    return sorted([team["team_number"] for team in teams])
