from utils.capitalize_columns import capitalize_columns
import pandas as pd

def ranking_table(st, conn): 
    st.title("5. Rankings Table")
    st.write("---")

    # 1st & 2nd Question Solution (Display the weekly rankings from the AP(Associated Press Top 25) Poll, Columns include: week, team name, rank, points, first-place votes, wins, and losses.)
    query = """ SELECT t.name AS team_name, r.week, r.current_rank, r.points, r.fp_votes, r.wins, r.losses, s.year AS season
        FROM rankings AS r
        JOIN teams AS t ON t.team_id = r.team_id
        JOIN seasons AS s ON s.season_id = r.season_id
        WHERE poll_name = 'Associated Press Top 25';
    """
    rankings_res = pd.read_sql(query, conn)
    capitalize_columns(rankings_res)

    st.header("Display the weekly rankings from the AP(Associated Press Top 25) Poll with filter")
    
    # 3rd Question solution (Filters available for season, week, and rank range)
    filter_type = st.selectbox(
        "Filter by:", ["Show all", "Season", "Week", "Rank (Range)"]
    )

    if filter_type == "Show all": st.dataframe(rankings_res)
    elif filter_type == "Rank (Range)": 
        min_val, max_val = st.slider(
            "Select range",
            min_value=1,
            max_value=rankings_res["Current Rank"].max(),
            value=(1, 5)
        )

        st.dataframe(rankings_res[
            (rankings_res["Current Rank"] >= min_val) &
            (rankings_res["Current Rank"] <= max_val)
        ])
    else:
        if filter_type == "Season":
            column_name = "Season"
            options = rankings_res[column_name].unique()
            selected_value = st.selectbox("Select a season", options)
        elif filter_type == "Week":
            column_name = "Week"
            options = rankings_res[column_name].unique()
            selected_value = st.selectbox("Select a week", options)
        st.dataframe(rankings_res[rankings_res[column_name] == selected_value])
    st.write("---")

    # 4th Question Solution (Supports searching for a specific team’s ranking history)
    query = """SELECT t.name AS team_name, t.alias, s.year, r.current_rank, r.prev_rank, r.week, r.points, r.fp_votes, r.wins, r.losses, r.ties
    FROM rankings AS r
    JOIN teams AS t ON t.team_id = r.team_id
    JOIN seasons AS s ON s.season_id = r.season_id;
    """
    teams_ranking_res = pd.read_sql(query, conn)
    capitalize_columns(teams_ranking_res)

    st.header("Supports searching for a specific team's ranking history")
    search_text = st.text_input("Search ranking history by team")

    if search_text.strip(): 
        teams_ranking_res = teams_ranking_res[
            teams_ranking_res["Team Name"].str.contains(search_text, case=False, na=False) |
            teams_ranking_res["Alias"].str.lower().eq(search_text.lower()) ]

        if teams_ranking_res.empty: st.warning("No matching player found")
        else: st.dataframe(teams_ranking_res)
    else: st.dataframe(teams_ranking_res)