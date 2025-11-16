import pandas as pd
import plotly.express as px

def home_dashboard(st, conn):
    st.title("Home Dashboard")
    st.write("---")

    # 1.1 Quetion Solution (All available teams and their conferences)
    query = """SELECT t.name, t.alias, t.market, t.founded, t.mascot, t.fight_song, championships_won, c.name
    FROM teams as t
    JOIN conferences as c ON c.conference_id = t.conference_id;
    """
    teams_data = pd.read_sql(query, conn)
    teams_data.columns = ["Team Name", "Alias", "Market", "Founded", "Mascot", "Fight Song", "Championships Won", "Conference Name"]

    st.header("1. Available teams with their conference names")
    st.dataframe(teams_data.reset_index(drop=True), use_container_width=True)

    query = """SELECT c.name AS conference_name, COUNT(t.team_id) AS team_count
    FROM conferences c
    LEFT JOIN teams t ON t.conference_id = c.conference_id
    GROUP BY c.conference_id, c.name
    HAVING COUNT(t.team_id) > 0
    ORDER BY team_count DESC;
    """

    teams_res = pd.read_sql(query, conn)
    fig = px.bar(
        teams_res,
        x="conference_name",
        y="team_count",
        title="Teams per Conference",
        text="team_count"
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.header("Team count under each Conference")
    st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # 1.2 Quetion Solution (All active players)
    query = "SELECT p.first_name, p.last_name, p.abbr_name, p.birth_place, p.position, p.height, p.weight, p.status, p.eligibility, t.name AS team_name FROM players as p JOIN teams as t ON t.team_id = p.team_id;"
    players_res = pd.read_sql(query,conn)

    st.header("2. All the active players")
    st.dataframe(players_res[players_res["status"] == "ACT"],use_container_width=True)
    
    team_counts = players_res['team_name'].value_counts().reset_index()
    team_counts.columns = ['team_name', 'player_count']

    fig = px.treemap(
    team_counts,
    path=["team_name"],
    values="player_count",
    )

    st.header("Players Treemap")
    st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # 1.3 Question Solutions (All current season years and their status)
    # | season_id                            | year | start_date | end_date   | status | type_code |
    query = "SELECT year, status FROM seasons ORDER BY year DESC;"
    season_res = pd.read_sql(query,conn)

    st.header("3.All the current seasons years and their status")
    st.dataframe(season_res)

    st.write("---")

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