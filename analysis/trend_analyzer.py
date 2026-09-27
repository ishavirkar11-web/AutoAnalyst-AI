import pandas as pd


def analyze_trends(
    df,
    detected_columns=None
):

    if detected_columns is None:
        detected_columns = {}

    # Detect date and revenue columns
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

    # Create a copy
    trend_df = df.copy()

    # Convert date column
    trend_df[date_column] = pd.to_datetime(
        trend_df[date_column],
        errors="coerce"
    )

    # Remove invalid dates
    trend_df = trend_df.dropna(
        subset=[date_column]
    )

    if trend_df.empty:
        return None

    # Create month
    trend_df["Month"] = (
        trend_df[date_column]
        .dt.to_period("M")
        .astype(str)
    )

    # Calculate monthly revenue
    monthly_revenue = (
        trend_df
        .groupby("Month")[revenue_column]
        .sum()
        .reset_index()
    )

    # Sort chronologically
    monthly_revenue = monthly_revenue.sort_values(
        "Month"
    )

    # Highest revenue month
    highest_month = monthly_revenue.loc[
        monthly_revenue[revenue_column].idxmax()
    ]

    # Lowest revenue month
    lowest_month = monthly_revenue.loc[
        monthly_revenue[revenue_column].idxmin()
    ]

    # Determine overall trend
    if len(monthly_revenue) >= 2:

        first_value = monthly_revenue[
            revenue_column
        ].iloc[0]

        last_value = monthly_revenue[
            revenue_column
        ].iloc[-1]

        if last_value > first_value:
            trend = "Increasing"

        elif last_value < first_value:
            trend = "Decreasing"

        else:
            trend = "Stable"

    else:
        trend = "Insufficient data"

    return {
        "monthly_revenue": monthly_revenue,
        "highest_month": highest_month["Month"],
        "highest_month_revenue": highest_month[
            revenue_column
        ],
        "lowest_month": lowest_month["Month"],
        "lowest_month_revenue": lowest_month[
            revenue_column
        ],
        "overall_trend": trend
    }