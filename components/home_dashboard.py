from utils.capitalize_columns import capitalize_columns
import plotly.express as px
import pandas as pd

def home_dashboard(st, conn):
    st.title("1. Home Dashboard")
    st.write("---")

    # 1.1 Quetion Solution (All available teams and their conferences)
    query = """SELECT t.name AS team_name, t.alias, t.market, t.founded, t.mascot, t.fight_song, championships_won, c.name AS conference_name
        FROM teams AS t
        JOIN conferences AS c ON c.conference_id = t.conference_id;
    """
    teams_res = pd.read_sql(query, conn)
    capitalize_columns(teams_res)

    st.header("1. Available teams with their conference names")
    st.dataframe(teams_res, width='stretch')

    conf_counts = teams_res.groupby("Conference Name").size().reset_index(name="team_count")

    fig = px.bar(
        conf_counts,
        x="Conference Name",
        y="team_count",
        title="Teams per Conference",
        text="team_count"
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.header("Team count under each Conference")
    st.plotly_chart(fig, width='stretch')
    st.write("---")

    # 1.2 Quetion Solution (All active players)
    query = """SELECT p.first_name, p.last_name, p.abbr_name, p.birth_place, p.position, p.height, p.weight, p.status, p.eligibility, t.name AS team_name 
        FROM players as p 
        JOIN teams as t ON t.team_id = p.team_id;
    """
    players_res = pd.read_sql(query,conn)
    capitalize_columns(players_res)

    st.header("2. All the active players")
    st.dataframe(players_res[players_res["Status"] == "ACT"],width='stretch')
    
    team_counts = players_res['Team Name'].value_counts().reset_index()
    team_counts.columns = ['team_name', 'player_count']
    team_counts = team_counts.sort_values(by="player_count", ascending=False).head(25)

    fig = px.treemap(
    team_counts,
    path=["team_name"],
    values="player_count",
    )

    st.header("Players Treemap (Top 25)")
    st.plotly_chart(fig, width='stretch')
    st.write("---")

    # 1.3 Question Solutions (All current season years and their status)
    query = "SELECT year, status FROM seasons ORDER BY year DESC;"
    season_res = pd.read_sql(query,conn)
    capitalize_columns(season_res)

    st.header("3.All the current seasons years and their status")
    st.dataframe(season_res)
    st.write("---")


    # Overview of the dataset
    tables = ["coaches", "conferences", "divisions", "players", "player_statistics", "rankings", "seasons", "season_schedules", "teams", "venues"]
    results = []
    for table in tables:
        query = f"SELECT COUNT(*) AS row_count FROM {table}"
        df = pd.read_sql(query, conn)
        count_value = int(df.iloc[0]["row_count"])
        results.append({"Table": table, "Row Count": count_value})

    table_counts = pd.DataFrame(results)
    table_counts = table_counts.sort_values(by="Row Count", ascending=False).reset_index(drop=True)

    st.header("Quick Overview of the Dataset")
    st.markdown("""
        This dataset is built from the NCAAFB API and stores data of multiple seasons <br />
        Following is TLDR of the tables in the database: <br />
        <ol>
            <li><b>Teams</b> : Basic team information including conference, division, and venue.</li>
            <li><b>Players</b> : Roster data with profile info such as position, eligibility, height, weight, and status.</li>
            <li><b>Player Statistics</b> : Season-level performance metrics (games played, rushing, receiving, etc.).</li>
            <li><b>Rankings</b> : Weekly poll rankings showing rank, points, and first-place votes.</li>
            <li><b>Seasons</b> : Metadata for each season (year, dates, status).</li>
            <li><b>Conferences & Divisions</b> : Organizational grouping of teams.</li>
            <li><b>Venues</b> : Stadium details including capacity, location, and surface.</li>
            <li><b>Coaches</b> : Coaching staff linked to teams.</li>
        </ol>
    """, unsafe_allow_html=True)
    st.table(table_counts)