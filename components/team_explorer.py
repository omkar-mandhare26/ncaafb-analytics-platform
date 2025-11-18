import pandas as pd
import plotly.express as px

def team_explorer(st, conn):
    st.title("T2. eams Explorer")
    st.write("---")

    # 1st Question Solution (View all teams with details like team name, market, alias, conference, and venue)
    query = """SELECT t.name AS team_name, t.market, t.alias, c.name AS conference_name, v.name AS venue_name
        FROM teams AS t
        JOIN conferences AS c ON c.conference_id = t.conference_id
        JOIN venues AS v ON v.venue_id = t.venue_id;
    """

    teams_res = pd.read_sql(query,conn)
    teams_res.columns = [column.capitalize().replace("_", " ") for column in teams_res.columns]

    st.header("1. View all teams with details like team name, market, alias, conference, and venue")
    st.dataframe(teams_res)

    conf_counts = teams_res.groupby("Conference name").size().reset_index(name="team_count")

    fig = px.pie(
        conf_counts,
        values="team_count",
        names="Conference name",
        color_discrete_sequence=px.colors.sequential.RdBu
    ).update_layout(
        width=600,
        height=600,
    )

    st.header("Team count under each Conference")
    st.plotly_chart(fig, width='stretch')
    st.write("---")

    # 2nd Question Solutions (Apply filters for conference, division, or state)
    query = """SELECT t.name AS team_name, t.alias, t.market, t.founded, t.mascot, t.fight_song, t.championships_won, c.name AS conference_name, d.name AS division_name, v.state
        FROM teams AS t
        JOIN conferences AS c ON c.conference_id = t.conference_id
        JOIN divisions AS d ON d.division_id = t.division_id
        JOIN venues AS v ON v.venue_id = t.venue_id; 
    """
    teams_res = pd.read_sql(query,conn)
    teams_res.columns = [column.capitalize().replace("_", " ") for column in teams_res.columns]

    st.header("2. Apply filters for conference, division, or state")
    filter_type = st.selectbox(
        "Filter by:", ["Conference", "Division", "State"]
    )

    if filter_type == "Conference":
        column_name = "Conference name"
        options = teams_res["Conference name"].unique()
        selected_value = st.selectbox("Select a conference", options)

    elif filter_type == "Division":
        column_name = "Division name"
        options = teams_res["Division name"].unique()
        selected_value = st.selectbox("Select a division", options)

    elif filter_type == "State":
        column_name = "State"
        options = teams_res["State"].unique()
        selected_value = st.selectbox("Select a state", options)

    st.write("Selected:", selected_value)
    st.dataframe(teams_res[teams_res[column_name] == selected_value])
    st.write("---")

    # 3rd Question Solution (Search for a team by name or alias)
    query = "SELECT name, alias, market, founded, mascot, fight_song, championships_won FROM teams;"
    teams_res = pd.read_sql(query, conn)
    teams_res.columns = [column.capitalize().replace("_", " ") for column in teams_res.columns]

    st.header("3. Search for a team by name or alias")
    search_text = st.text_input("Search team by name or alias")

    if search_text.strip():
        teams_res = teams_res[
            teams_res["Name"].str.contains(search_text, case=False, na=False) |
            teams_res["Alias"].str.contains(search_text, case=False, na=False)
        ]

        if teams_res.empty: st.warning("No matching teams found")
        else: st.dataframe(teams_res)
    else: st.dataframe(teams_res)
    st.write("---")

    # 4th Question Solution (Option to view team roster by selecting a team)
    st.header("4. Option to view team roster by selecting a team")
    
    team_res = pd.read_sql("SELECT team_id, name, alias FROM teams;", conn)
    team_res["Label"] = team_res["name"] + "(" + team_res["alias"] + ")" 

    team_selected = st.selectbox(
        "Filter by:", team_res["Label"]
    )

    team_id = team_res[team_res["Label"] == team_selected].iloc[0].iloc[0]

    players_res = pd.read_sql(f"SELECT first_name, last_name, abbr_name, birth_place, position, height, weight, status FROM players WHERE team_id='{team_id}';", conn)
    players_res.columns = [column.capitalize().replace("_", " ") for column in players_res.columns]

    coaches_res = pd.read_sql(f"SELECT full_name, position FROM coaches WHERE team_id='{team_id}';", conn)
    coaches_res.columns = [column.capitalize().replace("_", " ") for column in coaches_res.columns]

    query = f"""SELECT t.name AS team_name, t.alias, t.market, t.founded, t.mascot, t.fight_song, t.championships_won, c.name AS conference_name, d.name AS division_name, v.name AS venue_name 
        FROM teams AS t
        JOIN conferences AS c ON c.conference_id = t.conference_id
        JOIN divisions AS d ON d.division_id = t.division_id
        JOIN venues AS v ON v.venue_id = t.venue_id
        WHERE t.team_id = '{team_id}';
    """
    team_res = pd.read_sql(query, conn)
    team_res.columns = [column.capitalize().replace("_", " ") for column in team_res.columns]


    st.write(f"Selected Team: {team_selected}")
    st.header("Team Roster")
    st.table(team_res)
    
    st.header("Players in the selected team")
    st.dataframe(players_res)

    st.header("Coaches in the selected team")
    st.table(coaches_res)