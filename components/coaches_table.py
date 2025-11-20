from utils.capitalize_columns import capitalize_columns
import pandas as pd

def coaches_table(st, conn): 
    st.title("7. Coaches Table")
    st.write("---")

    query = """ SELECT c.full_name, c.position, t.name AS team_name, t.alias
        FROM coaches AS c
        JOIN teams AS t ON t.team_id = c.team_id;
    """

    coaches_res = pd.read_sql(query, conn)
    capitalize_columns(coaches_res)

    st.header("Display all coaches with details like name, position, and associated team")
    search_text = st.text_input("Search by coach name or team")

    if search_text.strip():
        coaches_res = coaches_res[
            coaches_res["Full Name"].str.contains(search_text, case=False, na=False) |
            coaches_res["Team Name"].str.contains(search_text, case=False, na=False) | 
            coaches_res["Alias"].str.lower().eq(search_text.lower())
        ]

        if coaches_res.empty: st.warning("No matching teams found")
        else: st.dataframe(coaches_res)
    else: st.dataframe(coaches_res)