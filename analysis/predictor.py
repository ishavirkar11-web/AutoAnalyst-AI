import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_revenue(
    df,
    detected_columns=None,
    future_periods=3
):

    if detected_columns is None:
        detected_columns = {}

    # Detect columns
    date_column = detected_columns.get(
        "date",
        "Date"
    )

    revenue_column = detected_columns.get(
        "revenue",
        "Revenue"
    )

    # Check required columns
    if (
        date_column not in df.columns
        or revenue_column not in df.columns
    ):
        return None

    # Create working copy
    prediction_df = df[
        [date_column, revenue_column]
    ].copy()

    # Convert date
    prediction_df[date_column] = pd.to_datetime(
        prediction_df[date_column],
        errors="coerce"
    )

    # Remove invalid data
    prediction_df = prediction_df.dropna(
        subset=[
            date_column,
            revenue_column
        ]
    )

    if len(prediction_df) < 2:
        return None

    # Create monthly data
    prediction_df["Month"] = (
        prediction_df[date_column]
        .dt.to_period("M")
    )

    monthly_data = (
        prediction_df
        .groupby("Month")[revenue_column]
        .sum()
        .reset_index()
    )

    if len(monthly_data) < 2:
        return None

    # Convert month into numerical index
    monthly_data["Month_Number"] = range(
        len(monthly_data)
    )

    # Prepare ML data
    X = monthly_data[
        ["Month_Number"]
    ]

    y = monthly_data[
        revenue_column
    ]

    # Train Linear Regression model
    model = LinearRegression()

    model.fit(
        X,
        y
    )

    # Future month numbers
    last_month_number = (
        monthly_data["Month_Number"].iloc[-1]
    )

    future_numbers = range(
        last_month_number + 1,
        last_month_number + 1 + future_periods
    )

    future_X = pd.DataFrame({
        "Month_Number": list(
            future_numbers
        )
    })

    # Predict future revenue
    predictions = model.predict(
        future_X
    )

    # Generate future month labels
    last_period = monthly_data[
        "Month"
    ].iloc[-1]

    future_months = [
        last_period + i
        for i in range(
            1,
            future_periods + 1
        )
    ]

    # Create prediction table
    prediction_result = pd.DataFrame({
        "Month": [
            str(month)
            for month in future_months
        ],
        "Predicted Revenue": predictions
    })

    return prediction_result