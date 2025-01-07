import streamlit as st
import pandas as pd
from gs_client.gsClient import sheet, grab_all_data

worksheet = sheet.worksheet("Canada")

data = grab_all_data(worksheet)

df = pd.DataFrame(data[1:], columns=data[0])

def main():
    st.title("Canada Regional Stats")
    st.write("Note: These stats are based on scouting reports submitted to the GS")
    st.divider()
    unique_team_number = df["Team#"].unique()
    selected_team = st.selectbox("Select a Team", unique_team_number)
    if selected_team in unique_team_number:
        team_data = df[df["Team#"] == selected_team]
        with st.container():
            st.subheader(f"Team {selected_team} Data")
            
            col1, col2, col3 = st.columns(3)

            with col1:
                ...
            
            with col2:
                ...

            with col3:
                st.write("Raw Data")
                st.dataframe(df, hide_index=True)
    
    st.divider()
    st.dataframe(df, hide_index=True)



if __name__ == "__main__":
    main()