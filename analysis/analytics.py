def analyze_data(df, detected_columns=None):

    results = {}

    # Use detected columns if available
    if detected_columns is None:
        detected_columns = {}


    # ========================================================
    # REVENUE
    # ========================================================

    revenue_column = detected_columns.get("revenue", "Revenue")

    if revenue_column in df.columns:

        results["total_revenue"] = df[revenue_column].sum()

        results["average_revenue"] = df[revenue_column].mean()


    # ========================================================
    # QUANTITY
    # ========================================================

    quantity_column = detected_columns.get("quantity", "Quantity")

    if quantity_column in df.columns:

        results["total_quantity"] = df[quantity_column].sum()


    # ========================================================
    # TOP PRODUCT
    # ========================================================

    product_column = detected_columns.get("product", "Product")

    if (
        product_column in df.columns
        and revenue_column in df.columns
    ):

        product_revenue = (
            df.groupby(product_column)[revenue_column]
            .sum()
            .sort_values(ascending=False)
        )

        if not product_revenue.empty:

            results["top_product"] = product_revenue.index[0]

            results["top_product_revenue"] = (
                product_revenue.iloc[0]
            )


    # ========================================================
    # TOP REGION
    # ========================================================

    region_column = detected_columns.get("region", "Region")

    if (
        region_column in df.columns
        and revenue_column in df.columns
    ):

        region_revenue = (
            df.groupby(region_column)[revenue_column]
            .sum()
            .sort_values(ascending=False)
        )

        if not region_revenue.empty:

            results["top_region"] = region_revenue.index[0]

            results["top_region_revenue"] = (
                region_revenue.iloc[0]
            )


    return results