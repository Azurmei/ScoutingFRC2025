import streamlit as st
import pandas as pd
from gs_client.gsClient import sheet, grab_all_data
from stats_helper.statsHelper import *

worksheet = sheet.worksheet("Canada")

data = grab_all_data(worksheet)

df = pd.DataFrame(data[1:], columns=data[0])

headers = ['auto_leave', 'auto_CL1', 'auto_CL2',	
           'auto_CL3', 'auto_CL4', 'auto_Proc', 
           'auto_Net', 'auto_desc', 'auto_rp',	
           'tele_CL1', 'tele_CL2', 'tele_CL3', 
           'tele_CL4',	'tele_Proc', 'tele_Net',
           'tele_cycle_time_coral', 'tele_cycle_time_proc',
           'tele_cycle_time_net',	'end_Zone',	'end_SC', 
           'end_DC']

def main():
    st.title("Canada Regional Stats")
    st.write("Note: These stats are based on scouting reports submitted to the GS")
    st.divider()
    unique_team_number = df["Team#"].unique()
    st.write("Note: Team select is based on data input into the DB. No data will show if the DB is empty")
    selected_team = st.selectbox("Select a Team", unique_team_number)
    if selected_team in unique_team_number:
        team_data = df[df["Team#"] == selected_team]
        with st.container():
            st.subheader(f"Team {selected_team} Data")

            st.write("Raw Data")
            st.dataframe(team_data, hide_index=True)
            
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Priority", get_priority(team_data))
                st.metric("Average RP per Match", average_rp(team_data))
                st.metric("Average Auto Score", average_auto_points(team_data))
                st.metric("Average Teleop Score", average_teleop_points(team_data))
                st.metric("End Game Priority", endgame_priority(team_data))
                st.metric("Win %", win_percentage(team_data))
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
    st.subheader("All Teams Raw Data")
    st.dataframe(df, hide_index=True)



if __name__ == "__main__":
    main()