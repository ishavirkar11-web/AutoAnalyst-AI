def clean_data(df):
    """
    Automatically cleans the uploaded dataset.
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing numerical values with median
    numerical_columns = df.select_dtypes(include="number").columns

    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].median())

    # Fill missing text values with Unknown
    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].fillna("Unknown")

    return df