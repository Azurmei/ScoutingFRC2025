import requests
import streamlit as st
import json

# == Base Defines ==
# API_KEY = st.secrets["frc_api"]
API_KEY = st.secrets["frcapi"]["api_key"]
BASE_URL = 'https://frc-api.firstinspires.org/v3.0'
SEASON = 2025


# Set up the headers with the Authorization token
headers = {
    'Authorization': f'Basic {API_KEY}',
    'Accept': 'application/json'  # Optional, depending on the API
}

def get_comp_teams(eventCode:str) -> list:

    team_list = []    

    # Get the competition teams
    url = f'{BASE_URL}/{SEASON}/teams?eventCode={eventCode}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        raw_data = response.json()

        for teams in raw_data['teams']:
            team_list.append(teams['teamNumber'])
        
        return team_list
    

if __name__ == "__main__":
    print(get_comp_teams("BCVI"))
