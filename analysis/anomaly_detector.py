import pandas as pd


def detect_anomalies(df):

    anomalies = []

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numerical_columns:

        # Calculate Q1 and Q3
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        # Calculate IQR
        iqr = q3 - q1

        # Define boundaries
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Find unusual values
        unusual_rows = df[
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        ]

        for index, row in unusual_rows.iterrows():

            anomalies.append({
                "row": index,
                "column": column,
                "value": row[column],
                "reason": "Unusual numerical value"
            })

    return anomalies