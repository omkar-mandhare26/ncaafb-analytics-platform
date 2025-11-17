import pandas as pd

def players_explorer(st,conn):
    st.title("Players Explorer")
    st.write("---")

    query = """ SELECT p.first_name, p.last_name, p.abbr_name, p.position, p.eligibility, p.height, p.weight, p.status, t.name AS team_name
        FROM players AS p
        JOIN teams AS t ON t.team_id = p.team_id
    """
    players_res = pd.read_sql(query,conn)
    players_res.columns = [column.capitalize().replace("_", " ") for column in players_res.columns]
    players_res["Full name"] = players_res["First name"] + " " + players_res["Last name"]
    cols = list(players_res.columns)
    players_res = players_res[[cols[-1]] + cols[0:-1]]

    # 1st Question Solution (Display all players with attributes like position, eligibility, height, and weight)
    st.header("1. Display all players with attributes like position, eligibility, height, and weight")
    st.dataframe(players_res)
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
            players_res["Full name"].str.lower().eq(search_text.lower()) |
            players_res["First name"].str.lower().eq(search_text.lower()) |
            players_res["Last name"].str.lower().eq(search_text.lower()) |
            players_res["Abbr name"].str.lower().eq(search_text.lower()) |
            players_res["Team name"].str.lower().eq(search_text.lower())
        ]

        if players_res.empty: st.warning("No matching player found")
        else: st.dataframe(players_res)
    else: st.dataframe(players_res)