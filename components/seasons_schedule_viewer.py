import pandas as pd

def seasons_schedule_viewer(st, conn): 
    st.title("4. Season & Schedule Viewer")
    st.write("---")

    # 1st & 2nd Question Solution (List of available seasons with start and end dates. Filter by year or status)
    seasons_res = pd.read_sql("SELECT * FROM seasons ORDER BY year DESC;", conn)
    seasons_res.columns = [column.capitalize().replace("_", " ") for column in seasons_res.columns]

    st.header("List of available seasons with start and end dates. Filter by year or status")
    filter_type = st.selectbox(
        "Filter by:", ["Show all", "Year", "Status"]
    )

    if filter_type == "Show all": st.dataframe(seasons_res.drop(columns=["Season id"]))
    else:
        if filter_type == "Year":
            column_name = "Year"
            options = seasons_res[column_name].unique()
            selected_value = st.selectbox("Select a year", options)
        elif filter_type == "Status":
            column_name = "Status"
            options = seasons_res[column_name].unique()
            selected_value = st.selectbox("Select a status", options)
        st.dataframe(seasons_res[seasons_res[column_name] == selected_value])
    st.write("---")
    

    # 3rd Question Solution (Joinable with rankings_weekly for season-specific rankings data)
    query = """SELECT s.year, t.name, r.current_rank, r.prev_rank, r.week, r.wins, r.losses, r.ties, r.poll_name,  r.points
    FROM rankings AS r
    JOIN seasons AS s ON s.season_id = r.season_id
    JOIN teams AS t ON t.team_id = r.team_id
    """
    seasons_res = pd.read_sql(query,conn)
    seasons_res.columns = [column.capitalize().replace("_", " ") for column in seasons_res.columns]


    st.header("Joinable with rankings_weekly for season-specific rankings data")
    filter_type = st.selectbox(
        "Filter by:", ["Show all", "Season Year", "Current Rank"]
    )

    if filter_type == "Show all": st.dataframe(seasons_res)
    else:
        if filter_type == "Season Year":
            column_name = "Year"
            options = seasons_res[column_name].unique()
            selected_value = st.selectbox("Select a year", options)
        elif filter_type == "Current Rank":
            column_name = "Current rank"
            options = seasons_res[column_name].unique()
            selected_value = st.selectbox("Select current rank", options)
        st.dataframe(seasons_res[seasons_res[column_name] == selected_value])