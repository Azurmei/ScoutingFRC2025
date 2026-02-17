import streamlit as st
import requests
from gs_client.gsClient import client, sheet, append_data, check_duplicate
from data_validate.dataValidate import valid_data_count, check_empty, check_duplicate_alliance, check_pass_flag

# ===== Google Sheet =====
worksheet = sheet.worksheet("Hawaii")

# ===== Blue Alliance =====
TBA_KEY = st.secrets["tba"]["api_key"]
BASE_URL = "https://www.thebluealliance.com/api/v3"
HEADERS = {"X-TBA-Auth-Key": TBA_KEY}

# ===== Event info =====
YEAR = 2026
EVENT_CODE = f"{YEAR}hiho"  # Hawaii Regional key

# ===== Fetch team list =====
def get_comp_teams(event_code):
    url = f"{BASE_URL}/event/{event_code}/teams/simple"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return [team["team_number"] for team in response.json()]
    else:
        st.error(f"Failed to fetch teams: {response.status_code}")
        return []

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
        auto_CL1 = st.number_input("Auto CL1", value=0)
        auto_CL2 = st.number_input("Auto CL2", value=0)
        auto_CL3 = st.number_input("Auto CL3", value=0)
        auto_CL4 = st.number_input("Auto CL4", value=0)
        auto_Proc = st.number_input("Auto Processor", value=0)
        auto_Net = st.number_input("Auto Net", value=0)
        auto_desc = st.text_input("Auto Notes", value="N/A")
        auto_rp = st.toggle("Auto RP", value=False)
        st.divider()

        st.subheader("Teleop Period")
        teleop_CL1 = st.number_input("Teleop CL1", value=0)
        teleop_CL2 = st.number_input("Teleop CL2", value=0)
        teleop_CL3 = st.number_input("Teleop CL3", value=0)
        teleop_CL4 = st.number_input("Teleop CL4", value=0)
        teleop_Proc = st.number_input("Teleop Processor", value=0)
        teleop_Net = st.number_input("Teleop Net", value=0)
        tele_cycle_coral = st.selectbox("Teleop Cycle Time Coral", CYCLE_SPEED)
        tele_cycle_proc = st.selectbox("Teleop Cycle Time Processor", CYCLE_SPEED)
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
                auto_leave, auto_CL1, auto_CL2, auto_CL3, auto_CL4, auto_Proc, auto_Net, auto_desc, auto_rp,
                teleop_CL1, teleop_CL2, teleop_CL3, teleop_CL4, teleop_Proc, teleop_Net,
                tele_cycle_coral, tele_cycle_proc, tele_cycle_net, tele_priority,
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
