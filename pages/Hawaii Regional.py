import streamlit as st
from gs_client.gsClient import client, sheet, append_data, check_duplicate
from data_validate.dataValidate import valid_data_count, check_empty, check_duplicate_alliance, check_pass_flag
from frc_api.frcApi import get_comp_teams
import time

worksheet = sheet.worksheet("HAWAII_MATCHES")

EVENT_CODE = "HIHO"

TEAM_LIST = get_comp_teams(EVENT_CODE)

CYCLE_SPEED = [x for x in range(0, 20)]

pass_flag = [False, False, False, False]


def main():
    st.title("Hawaii Regional Scouting")
    st.write("Please be sure all fields are filled in in order to submit data")
    st.divider()
    # Create a form with input fields
    with st.form("match data"):

        data = []

        # match data
        st.subheader("Match Data")
        match_number = st.number_input("Match Number", min_value=1, max_value=100, step=1, format="%d")
        team_number = st.number_input("Team Number", value=0)
        alliance1_number = st.number_input("Alliance Team 1 Number", value=0)
        alliance2_number = st.number_input("Alliance Team 2 Number", value=0)
        match_type = st.selectbox("Type of Match", ("Qualification", "Practice", "Elimination"))
        st.divider()

        # auto data
        st.subheader("Autonomous Period")
        auto_leave = st.toggle("Auto Leave Zone", value=False)
        auto_fuel_count = st.number_input("Auto Total Fuel", value=0)
        auto_desc = st.text_input("Auto desc/Pathing", value="N/A")
        auto_path = st.text_input("Auto Pathing", value="N/A")
        

        st.divider()

        # teleop data
        st.subheader("Teleop Period")
        teleop_fuel_count = st.number_input("Teleop Fuel Count", value=0)
        tele_cycle_option = st.toggle("Cycled in match?", value=False)
        tele_cycle_Count = st.number_input("Teleop Cycle Count", value=0)
        tele_priority = st.selectbox("Priority Cycles", ("Fuel", "Passing", "Defense"))
        
        st.divider()

        # endgame data
        st.subheader("End Game")
        end_hang = st.selectbox("End Hang Level", ("None", "HL1", "HL2", "HL3"))
        driver_perf = st.text_input("Driver/bot Performance", value="N/A")
        consistensy = st.selectbox("Consistency", ("Inconsistent", "Consistent", "Very Consistent"))
        st.divider()

        # end of match data
        st.subheader("End of Match")
        energized_rp = st.toggle("Energized RP", value=False)
        supercharged_rp = st.toggle("Supercharged RP", value=False)
        traversal_rp = st.toggle("Traversal RP", value=False)
        result = st.selectbox("Match Result", ("Win", "Loss","tied"))
        st.divider()
        
        # Other comments
        notes = st.text_input("Any other comments?", value="N/A")
        st.divider()
        submitted = st.form_submit_button("Submit")

        if submitted:
            data.extend([
                match_number, match_type,team_number, alliance1_number, alliance2_number,
                auto_leave, auto_desc, auto_fuel_count, auto_path,
                tele_priority, tele_cycle_option, tele_cycle_Count, teleop_fuel_count, 
                traversal_rp, energized_rp, supercharged_rp, end_hang, result, driver_perf, notes
            ])

            team = [team_number, alliance1_number, alliance2_number]

            if not valid_data_count(data):
                st.error(f"Missing Data: Data len is {len(data)}")
            else: pass_flag[0] = True
            
            if not check_empty(data):
                st.error("Some Data Maybe Empty / Null")
            else: pass_flag[1] = True
            
            if check_duplicate_alliance(team):
                st.error("Duplicate Alliance Number")
            else: pass_flag[2] = True
            

            if check_duplicate(worksheet, data):
                 st.error("Duplicate data was trying to be added")
            else: pass_flag[3] = True
            
            if check_pass_flag(pass_flag):
                if append_data(worksheet, data):
                    st.success("Data Added")
                

if __name__ == "__main__":
    main()