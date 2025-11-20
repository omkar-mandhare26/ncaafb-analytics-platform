from utils.capitalize_columns import capitalize_columns
import pandas as pd

def venue_directory(st, conn): 
    st.title("6. Venue Directory")
    st.write("---")

    query = "SELECT name, city, state, country, capacity, surface, roof_type FROM venues;"
    venue_res = pd.read_sql(query,conn)
    capitalize_columns(venue_res)

    st.header("View list of venues and details such as city, state, capacity, and roof type.")
    st.subheader("Filter by state or roof type")
    filter_type = st.selectbox(
        "Filter by:", ["Show all", "State", "Roof Type"]
    )

    if filter_type == "Show all": st.dataframe(venue_res)
    else:
        if filter_type == "State":
            column_name = "State"
            options = venue_res[column_name].unique()
            selected_value = st.selectbox("Select a state", options)
        elif filter_type == "Roof Type":
            column_name = "Roof Type"
            options = venue_res[column_name].unique()
            selected_value = st.selectbox("Select a roof type", options)
        st.write("Selected:", selected_value)
        st.dataframe(venue_res[venue_res[column_name] == selected_value])