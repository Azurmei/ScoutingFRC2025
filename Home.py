import streamlit as st
version = "0.2.28.25.2"


def main():
    st.title("Team2438 2025 Scouting App")
    st.write("Created by Shane Matsushima")
    st.write(f"V{version}")
    st.warning("This application is specific for Team 2438.")
    st.warning("Internet connection is required.")
    st.success("Analytics and Form implemented for CanPac Regional")
    st.divider()
    st.write("This app is designed to help teams collect and analyze data from the 2025 FRC season.")
    st.write("Scouting reports can be added by selecting the tournament being scouted on the side bar.")
    st.divider()
    st.write("For any issues or suggestions, please contact Shane. Thanks!")



if __name__ == "__main__":
    main()