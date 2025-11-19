from components import (
    home_dashboard,
    team_explorer,
    players_explorer,
    seasons_schedule_viewer,
    ranking_table,
    venue_directory,
    coaches_table,
    analysis_questions
)
from utils.db import get_connection
import streamlit as st

try:
    conn = get_connection()
    print("Connection Successful")
except Exception as e:
    print("Connection Failed: ", e)

st.set_page_config(layout="wide")

st.sidebar.title("Sports Analysis")
option = st.sidebar.radio(
    "Check Analysis for", ("Home Dashboard", "Team Explorer", "Players Explorer", "Season & Schedule Viewer", "Rankings Table", "Venue Directory", "Coaches Table", "Analysis Questions")
)

if option == "Home Dashboard": home_dashboard(st, conn)
elif option == "Team Explorer": team_explorer(st,conn)
elif option == "Players Explorer": players_explorer(st,conn)
elif option == "Season & Schedule Viewer": seasons_schedule_viewer(st,conn)
elif option == "Rankings Table": ranking_table(st, conn)
elif option == "Venue Directory": venue_directory(st, conn)
elif option == "Coaches Table": coaches_table(st, conn)
elif option == "Analysis Questions": analysis_questions(st,conn)

conn.close()