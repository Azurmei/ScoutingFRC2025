import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = st.secrets["first"]["base_url"]
SEASON = st.secrets["first"]["season"]
USERNAME = st.secrets["first"]["username"]
AUTH_KEY = st.secrets["first"]["auth_key"]


def get_comp_teams(event_code: str) -> list:
    """
    Returns a list of team numbers attending an event.
    Example event_code: 'HIHO' or 'Hawaii'
    """

    team_list = []

    url = f"{BASE_URL}/{SEASON}/teams?eventCode={event_code}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, AUTH_KEY)
    )

    if response.status_code == 200:
        raw_data = response.json()
        teams = raw_data.get("teams", [])

        for team in teams:
            team_list.append(team.get("teamNumber"))

    return team_list


def get_comp_ranking(event_code: str) -> list:
    """
    Returns ranking data for an event.
    Example event_code: 'HIHO'
    """

    ranking_list = []

    url = f"{BASE_URL}/{SEASON}/rankings/{event_code}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, AUTH_KEY)
    )

    if response.status_code == 200:
        raw_data = response.json()
        rankings = raw_data.get("Rankings", [])

        for rank in rankings:
            team_data = {
                "team#": rank.get("teamNumber"),
                "rank": rank.get("rank"),
                "wins": rank.get("wins"),
                "losses": rank.get("losses"),
                "ties": rank.get("ties"),
                "matches": rank.get("matchesPlayed"),
                "avg_score": rank.get("sortOrder1")  # depends on season game metrics
            }

            ranking_list.append(team_data)

    return ranking_list