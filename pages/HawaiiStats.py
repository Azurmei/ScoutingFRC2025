import streamlit as st
import pandas as pd
from gs_client.gsClient import sheet, grab_all_data
from stats_helper.statsHelper import *
from frc_api.frcApi import comp_ranking
import matplotlib.pyplot as plt # type: ignore
import numpy as np

worksheet = sheet.worksheet("HAWAII_MATCHES")

data = grab_all_data(worksheet)

df = pd.DataFrame(data[1:], columns=data[0])

EVENT_CODE = 'HIHO'

headers = ['auto_leave', 'auto_hang', 'tele_fuel_count', 'end_hang']

def main():
    st.title("Hawaii Regional Stats")
    st.write("Note: These stats are based on scouting reports submitted to the GS")
    st.divider()
    unique_team_number = df["team_number"].unique()
    st.write("Note: Team select is based on data input into the DB. No data will show if the DB is empty")
    selected_team = st.selectbox("Select a Team", unique_team_number)
    if selected_team in unique_team_number:
        team_data = df[df["team_number"] == selected_team]
        with st.container():
            st.subheader(f"Team {selected_team} Data")

            st.write("Raw Data")
            st.dataframe(team_data, hide_index=True)
            
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Average Auto Score", round(average_auto_points(team_data), 2))
                st.metric("Average Teleop Score", round(average_teleop_points(team_data), 2))
                st.metric("Win %", round(win_percentage(team_data), 2))
                st.metric("Highest Score", highest_score(team_data))
                st.metric("Highest Score Alliance", highest_score_alliance(team_data))
                st.write("Highest wins based on alliance")
                st.table(best_alliance(team_data))
            
            with col2:
                st.subheader(f"Data Graphs of Team {selected_team}")
                st.write("Points per Match Data")
                st.bar_chart(match_point_graph_data(team_data))
                st.write("Win/Loss Data")
                st.bar_chart(match_win_loss_graph_data(team_data))
        
        st.divider()
        with st.container():

            st.subheader("Graphs based on user input")
            st.write("Select a metric to graph")
            
            selected_metric = st.selectbox("Select a metric", headers)
            if selected_metric in headers:
                st.write(f"Graph of {selected_metric} by match")
                st.bar_chart(select_graph_by_match(team_data, selected_metric))
            



    st.divider()
    st.subheader("Hawaii Ranking Data")
    st.write("Note: These stats are based on the FRC API for the regional")

    col1, col2 = st.columns(2)

    ranking_data = comp_ranking(EVENT_CODE)
    
    with col1:
        st.dataframe(ranking_data, hide_index=True)
    with col2:
        selected_data_graph = st.selectbox("Select data to graph", ("W/L/T", "Average Score"))

        
    st.divider()
    st.subheader("All Teams Raw Data")
    st.dataframe(df, hide_index=True)



if __name__ == "__main__":
    main()