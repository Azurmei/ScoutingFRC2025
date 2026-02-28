import streamlit as st
import requests

TBA_API_KEY = st.secrets["tba"]["api_key"]
BASE_URL = "https://www.thebluealliance.com/api/v3"

headers = {
    "X-TBA-Auth-Key": TBA_API_KEY
}

def get_comp_teams(event_key: str) -> list:
    """
    Returns a list of team numbers attending an event.
    Example event_key: '2026hiho'
    """
    team_list = []

    url = f"{BASE_URL}/event/{event_key}/teams"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()

        for team in raw_data:
            # team_key format: 'frc3005'
            team_number = int(team["team_key"].replace("frc", ""))
            team_list.append(team_number)

    return team_list


def get_comp_ranking(event_key: str) -> list:
    """
    Returns ranking data for an event.
    Example event_key: '2026hiho'
    """
    team_list = []

    url = f"{BASE_URL}/event/{event_key}/rankings"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()

        rank_data = raw_data.get("rankings", [])

        for rank in rank_data:
            team_number = int(rank["team_key"].replace("frc", ""))

            team_data = {
                "team#": team_number,
                "rank": rank.get("rank"),
                "wins": rank.get("record", {}).get("wins"),
                "losses": rank.get("record", {}).get("losses"),
                "ties": rank.get("record", {}).get("ties"),
                "matches": rank.get("matches_played"),
                "avg_score": rank.get("sort_orders", [None])[0]
            }

            team_list.append(team_data)

    return team_list