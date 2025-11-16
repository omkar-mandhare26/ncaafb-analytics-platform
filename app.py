from pages.home_dashboard import home_dashboard
from pages.team_explorer import team_explorer
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
    "Check Analysis for", ("Home Dashboard", "Team Explorer", "Players Explorer", "Season & Schedule Viewer", "Rankings Table", "Venue Directory", "Coaches Table")
)

if option == "Home Dashboard": home_dashboard(st, conn)
elif option == "Team Explorer": team_explorer(st,conn)
else:
    st.header("Yet to build")