def answer_question(question, df, results):

    question = question.lower().strip()

    # ==========================================
    # TOP PRODUCT
    # ==========================================

    if (
        "product" in question
        and (
            "highest" in question
            or "top" in question
            or "best" in question
            or "most revenue" in question
            or "best selling" in question
        )
    ):

        product_sales = (
            df.groupby("Product")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        product = product_sales.index[0]
        revenue = product_sales.iloc[0]

        return (
            f"🏆 {product} generated the highest "
            f"total revenue of ₹{revenue:,.0f}."
        )


    # ==========================================
    # TOP REGION
    # ==========================================

    if (
        "region" in question
        and (
            "highest" in question
            or "top" in question
            or "best" in question
            or "most revenue" in question
        )
    ):

        region_sales = (
            df.groupby("Region")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        region = region_sales.index[0]
        revenue = region_sales.iloc[0]

        return (
            f"🌍 {region} generated the highest "
            f"total revenue of ₹{revenue:,.0f}."
        )


    # ==========================================
    # TOTAL REVENUE
    # ==========================================

    if (
        "revenue" in question
        and (
            "total" in question
            or "overall" in question
            or "how much" in question
            or "generated" in question
        )
        and "product" not in question
        and "region" not in question
    ):

        return (
            f"💰 Total revenue is "
            f"₹{results['total_revenue']:,.0f}."
        )


    # ==========================================
    # AVERAGE REVENUE
    # ==========================================

    if (
        "revenue" in question
        and (
            "average" in question
            or "mean" in question
        )
    ):

        return (
            f"📊 Average revenue is "
            f"₹{results['average_revenue']:,.0f}."
        )


    # ==========================================
    # HIGHEST INDIVIDUAL REVENUE
    # ==========================================

    if (
        "highest individual" in question
        or "largest transaction" in question
        or "maximum transaction" in question
    ):

        highest = df["Revenue"].max()

        return (
            f"📈 The highest individual revenue is "
            f"₹{highest:,.0f}."
        )


    # ==========================================
    # LOWEST REVENUE
    # ==========================================

    if (
        "lowest revenue" in question
        or "minimum revenue" in question
    ):

        lowest = df["Revenue"].min()

        return (
            f"📉 The lowest individual revenue is "
            f"₹{lowest:,.0f}."
        )


    # ==========================================
    # TOTAL QUANTITY
    # ==========================================

    if (
        "quantity" in question
        and (
            "total" in question
            or "sold" in question
            or "how many" in question
            or "number" in question
        )
    ):

        total_quantity = df["Quantity"].sum()

        return (
            f"📦 Total quantity sold is "
            f"{total_quantity:,}."
        )


    # ==========================================
    # ROWS / RECORDS
    # ==========================================

    if (
        "how many rows" in question
        or "number of rows" in question
        or "how many records" in question
        or "number of records" in question
    ):

        return (
            f"📋 The dataset contains "
            f"{len(df):,} rows."
        )


    # ==========================================
    # COLUMNS
    # ==========================================

    if (
        "columns" in question
        or "fields" in question
        or "what data is available" in question
    ):

        return (
            "📋 The dataset contains these columns: "
            + ", ".join(df.columns)
        )


    # ==========================================
    # GENERAL INSIGHTS
    # ==========================================

    if (
        "insights" in question
        or "summary" in question
        or "analyze" in question
        or "analysis" in question
    ):

        return (
            f"📊 Key Insights:\n\n"
            f"💰 Total Revenue: "
            f"₹{results['total_revenue']:,.0f}\n\n"
            f"📦 Total Quantity: "
            f"{results['total_quantity']:,}\n\n"
            f"🏆 Top Product: "
            f"{results['top_product']}\n\n"
            f"🌍 Top Region: "
            f"{results['top_region']}"
        )


    # ==========================================
    # UNKNOWN QUESTION
    # ==========================================

    return (
        "🤖 I could not understand the question yet.\n\n"
        "Try asking about:\n"
        "• Revenue\n"
        "• Products\n"
        "• Regions\n"
        "• Quantity\n"
        "• Rows\n"
        "• Columns\n"
        "• Insights"
    )