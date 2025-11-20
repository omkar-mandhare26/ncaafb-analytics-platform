from utils.capitalize_columns import capitalize_columns
import plotly.express as px
import pandas as pd

def players_explorer(st,conn):
    st.title("3. Players Explorer")
    st.write("---")

    query = """ SELECT p.first_name, p.last_name, p.abbr_name, p.position, p.eligibility, p.height, p.weight, p.status, t.name AS team_name
        FROM players AS p
        JOIN teams AS t ON t.team_id = p.team_id;
    """
    players_res = pd.read_sql(query,conn)
    capitalize_columns(players_res)

    height_fig = px.histogram(players_res, x="Height", title="Player Height Distribution")
    height_fig.update_layout(xaxis_title="Height", yaxis_title="Player Count")

    # 1st Question Solution (Display all players with attributes like position, eligibility, height, and weight)
    st.header("1. Display all players with attributes like position, eligibility, height, and weight")
    st.dataframe(players_res)
    st.write("---")

    st.plotly_chart(height_fig, width="stretch")
    st.write("---")

    # 2nd Question Solution (Apply filters for position, status or eligibility)
    st.header("2. Apply filters for position, status or eligibility")
    filter_type = st.selectbox(
        "Filter by:", ["Position", "Status", "Eligibility"]
    )

    if filter_type == "Position":
        column_name = "Position"
        options = players_res[column_name].unique()
        selected_value = st.selectbox("Select a position", options)
    elif filter_type == "Status":
        column_name = "Status"
        options = players_res[column_name].unique()
        selected_value = st.selectbox("Select a status", options)
    elif filter_type == "Eligibility":
        column_name = "Eligibility"
        options =  players_res[column_name].unique()
        selected_value = st.selectbox("Select a eligibility", options)

    st.write("Selected:", selected_value)
    st.dataframe(players_res[players_res[column_name] == selected_value])
    st.write("---")

    # 3rd Question Solution (Search by player name or team name)
    st.header("3. Search by player name or team name")
    search_text = st.text_input("Search by player name or team name")

    if search_text.strip():
        players_res = players_res[
            players_res["First Name"].str.lower().eq(search_text.lower()) |
            players_res["Last Name"].str.lower().eq(search_text.lower()) |
            players_res["Abbr Name"].str.lower().eq(search_text.lower()) |
            players_res["Team Name"].str.contains(search_text, case=False, na=False)
        ]

        if players_res.empty: st.warning("No matching player found")
        else: st.dataframe(players_res)
    else: st.dataframe(players_res)