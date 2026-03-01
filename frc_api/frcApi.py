import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

def _get_first_config():
    """Helper to fetch FIRST API credentials from secrets at runtime."""
    secrets = st.secrets["first"]
    return secrets["username"], secrets["auth_key"], secrets["base_url"], secrets["season"]

def get_comp_teams(event_code: str) -> list:
    """
    Returns a list of team numbers attending an event.
    Example event_code: 'HIHO'
    """
    username, auth_key, base_url, season = _get_first_config()
    team_list = []

    url = f"{base_url}/{season}/teams?eventCode={event_code}"
    response = requests.get(url, auth=HTTPBasicAuth(username, auth_key))

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
    username, auth_key, base_url, season = _get_first_config()
    ranking_list = []

    url = f"{base_url}/{season}/rankings/{event_code}"
    response = requests.get(url, auth=HTTPBasicAuth(username, auth_key))

    if response.status_code == 200:
        raw_data = response.json()
        rankings = raw_data.get("Rankings", [])
        for rank in rankings:
            ranking_list.append({
                "team#": rank.get("teamNumber"),
                "rank": rank.get("rank"),
                "wins": rank.get("wins"),
                "losses": rank.get("losses"),
                "ties": rank.get("ties"),
                "matches": rank.get("matchesPlayed"),
                "avg_score": rank.get("sortOrder1")
            })

    return ranking_list