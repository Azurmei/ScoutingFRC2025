import streamlit as st
from gs_client.gsClient import client, sheet, append_data, check_duplicate
from data_validate.dataValidate import valid_data_count, check_empty, check_duplicate_alliance, check_pass_flag
from frc_api.frcApi import get_comp_teams

# ===== Google Sheet =====
worksheet = sheet.worksheet("HAWAII_MATCHES")

# ===== Event info =====
YEAR = 2026
EVENT_CODE = f"{YEAR}hiho"  # Hawaii Regional key

TEAM_LIST = get_comp_teams(EVENT_CODE)
if not TEAM_LIST:
    st.warning("Team list could not be loaded. Check your TBA key or event code.")

# ===== Cycle speed options =====
CYCLE_SPEED = [x for x in range(0, 20)]

# ===== Pass flags =====
pass_flag = [False, False, False, False]

# ===== Main =====
def main():
    st.title("Hawaii Regional Scouting [Input]")
    st.write("Please ensure all fields are filled in before submitting.")
    st.divider()

    # --- Match form ---
    with st.form("match data"):
        data = []

        st.subheader("Match Data")
        match_number = st.number_input("Match Number", min_value=1, max_value=100, step=1)
        team_number = st.selectbox("Team Number", TEAM_LIST)
        alliance1_number = st.selectbox("Alliance 1 Number", TEAM_LIST)
        alliance2_number = st.selectbox("Alliance 2 Number", TEAM_LIST)
        match_type = st.selectbox("Type of Match", ("Qualification", "Practice", "Elimination"))
        st.divider()

        st.subheader("Autonomous Period")
        auto_leave = st.toggle("Auto Leave Zone", value=False)
        auto_Net = st.number_input("Auto Net", value=0)
        auto_desc = st.text_input("Auto Notes", value="N/A")

        st.divider()

        st.subheader("Teleop Period")
        teleop_CL1 = st.number_input("Teleop CL1", value=0)
        tele_cycle_net = st.selectbox("Teleop Cycle Time Net", CYCLE_SPEED)
        tele_priority = st.selectbox("Priority Cycles", ("Coral", "Algae", "Defense"))
        
        tele_cycle_option = st.toggle("Cycled in match?", value=False)
        st.divider()

        st.subheader("End Game")
        end_zone = st.toggle("Zone Park", value=False)
        end_SC = st.toggle("Shallow Carriage Hang", value=False)
        end_DC = st.toggle("Deep Carriage Hang", value=False)
        driver_perf = st.text_input("Driver Performance", value="N/A")
        st.divider()

        st.subheader("End of Match")
        coral_rp = st.toggle("Coral RP", value=False)
        hang_rp = st.toggle("Hang RP", value=False)
        win = st.toggle("Win", value=False)
        loss = st.toggle("Loss", value=False)
        coop_bonus = st.toggle("Coop Bonus", value=False)
        tied = st.toggle("Tied", value=False)
        notes = st.text_input("Other Comments", value="N/A")
        st.divider()

        submitted = st.form_submit_button("Submit")
        if submitted:
            data.extend([
                match_number, team_number, alliance1_number, alliance2_number,
                auto_leave, auto_Net, auto_desc,
                teleop_CL1, tele_cycle_net, tele_priority,
                end_zone, end_SC, end_DC, coral_rp, hang_rp, win, loss, coop_bonus,
                match_type, driver_perf, tied, tele_cycle_option, notes
            ])

            team = [team_number, alliance1_number, alliance2_number]

            if not valid_data_count(data):
                st.error("Missing data")
            else:
                pass_flag[0] = True

            if not check_empty(data):
                st.error("Empty data found")
            else:
                pass_flag[1] = True

            if check_duplicate_alliance(team):
                st.error("Duplicate alliance number")
            else:
                pass_flag[2] = True

            if check_duplicate(worksheet, data):
                st.error("Duplicate row in sheet")
            else:
                pass_flag[3] = True

            if check_pass_flag(pass_flag):
                if append_data(worksheet, data):
                    st.success("Data Added")

if __name__ == "__main__":
    main()
