def capitalize_columns(df):
    df.columns = [cols.replace("_" , " ").title() for cols in df.columns]