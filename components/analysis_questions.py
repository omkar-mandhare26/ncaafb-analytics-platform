from utils.capitalize_columns import capitalize_columns
import pandas as pd

def analysis_questions(st, conn): 
    st.title("8. Analysis Question")
    st.write("---")

    # 1. Which teams have maintained Top 5 rankings across multiple seasons?
    query = """SELECT ANY_VALUE(t.name) AS team_name, t.alias, COUNT(DISTINCT r.season_id) AS top_5_count 
        FROM rankings r 
        JOIN teams t ON r.team_id = t.team_id 
        WHERE r.current_rank <= 5 
        GROUP BY t.alias
        HAVING COUNT(DISTINCT r.season_id) > 1
        ORDER BY COUNT(DISTINCT r.season_id) DESC;
    """
    rankings_res = pd.read_sql(query, conn)
    capitalize_columns(rankings_res)

    st.header("1. Which teams have maintained Top 5 rankings across multiple seasons?")
    st.dataframe(rankings_res)
    st.write("---")
    
    # 2. What are the average ranking points per team by season?
    query = """SELECT s.year, ANY_VALUE(t.name) AS team_name, t.alias, AVG(r.points) AS average_points 
        FROM rankings r
        JOIN seasons s ON r.season_id = s.season_id 
        JOIN teams t ON r.team_id = t.team_id 
        GROUP BY s.year, t.alias 
        ORDER BY s.year DESC, ANY_VALUE(t.name);
    """
    rankings_res = pd.read_sql(query, conn)
    capitalize_columns(rankings_res)

    st.header("2. What are the average ranking points per team by season?")
    st.dataframe(rankings_res)
    st.write("---")

    # 3. How many first-place votes did each team receive across weeks?
    query = """SELECT ANY_VALUE(t.name) AS team_name, t.alias, SUM(r.fp_votes) AS total_first_place_votes 
        FROM rankings r 
        JOIN teams t ON r.team_id = t.team_id 
        GROUP BY t.alias 
        ORDER BY SUM(r.fp_votes) DESC;
    """
    rankings_res = pd.read_sql(query, conn)
    capitalize_columns(rankings_res)

    st.header("3. How many first-place votes did each team receive across weeks?")
    st.dataframe(rankings_res)
    st.write("---")
    
    # 4. Which players have appeared in multiple seasons for the same team?
    query = """SELECT p.first_name, p.last_name, p.abbr_name, t.name AS team_name, COUNT(DISTINCT ps.season_id) AS season_count
        FROM player_statistics ps
        JOIN players p ON p.player_id = ps.player_id
        JOIN teams t ON t.team_id = ps.team_id
        GROUP BY ps.player_id, ps.team_id
        HAVING COUNT(DISTINCT ps.season_id) > 1;
    """
    player_res = pd.read_sql(query,conn)
    capitalize_columns(player_res)

    st.header("4. Which players have appeared in multiple seasons for the same team?")
    st.dataframe(player_res)
    st.write("---")
    
    # 5. What are the most common player positions and their distribution across teams?
    query = """SELECT p.position, t.name AS team_name, COUNT(*) AS player_count
        FROM players p
        JOIN teams AS t ON p.team_id = t.team_id
        GROUP BY p.position, t.name
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC, t.name;
    """
    position_res = pd.read_sql(query,conn)
    capitalize_columns(position_res)


    st.header("5. What are the most common player positions and their distribution across teams?")
    st.dataframe(position_res)
    st.write("---")
    
    # 6. Which players contributed the highest total yards (rushing + receiving) in a season?
    query = """SELECT p.first_name, p.last_name, p.abbr_name, t.name AS team_name, t.alias, (ps.rushing_yards + ps.receiving_yards) AS total_yards, ps.games_played, ps.games_started
        FROM player_statistics AS ps
        JOIN players AS p ON p.player_id = ps.player_id
        JOIN teams AS t ON t.team_id = ps.team_id
        ORDER BY (ps.rushing_yards + ps.receiving_yards) DESC
        LIMIT 10;
    """
    stats_res = pd.read_sql(query,conn)
    capitalize_columns(stats_res)

    st.header("6. Which players contributed the highest total yards (rushing + receiving) in a season?")
    st.dataframe(stats_res)
    st.write("---")

    # 7. Which venues hosted the most games across all seasons?
    query = """SELECT v.name, COUNT(ss.venue_id) AS game_count
        FROM season_schedules AS ss
        JOIN venues AS v ON v.venue_id = ss.venue_id
        GROUP BY v.name
        ORDER BY COUNT(ss.venue_id) DESC;
    """
    venue_res = pd.read_sql(query, conn)
    capitalize_columns(venue_res)

    st.header("7. Which venues hosted the most games across all seasons?")
    st.dataframe(venue_res)
    st.write("---")

    # 8. How does ranking improvement correlate with game performance (points scored)?
    query = """SELECT t.name AS team_name, t.alias, r.current_rank, r.prev_rank, r.points
        FROM rankings AS r
        JOIN teams AS t ON t.team_id = r.team_id
        WHERE r.current_rank < r.prev_rank OR r.prev_rank = 0;
    """
    rankings_res = pd.read_sql(query, conn)
    capitalize_columns(rankings_res)

    st.header("8. How does ranking improvement correlate with game performance (points scored)?")
    st.dataframe(rankings_res)
    st.write("---")