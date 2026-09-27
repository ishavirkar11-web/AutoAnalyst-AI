def detect_columns(df):

    detected = {}

    for column in df.columns:

        name = str(column).lower().strip()

        if any(
            word in name
            for word in [
                "date",
                "time",
                "timestamp",
                "month",
                "year"
            ]
        ):

            detected["date"] = column

        elif any(
            word in name
            for word in [
                "revenue",
                "sales",
                "amount",
                "income",
                "turnover"
            ]
        ):

            detected["revenue"] = column

        elif any(
            word in name
            for word in [
                "quantity",
                "qty",
                "units",
                "count"
            ]
        ):

            detected["quantity"] = column

        elif any(
            word in name
            for word in [
                "product",
                "item",
                "product_name"
            ]
        ):

            detected["product"] = column

        elif any(
            word in name
            for word in [
                "region",
                "area",
                "location",
                "zone"
            ]
        ):

            detected["region"] = column

        elif any(
            word in name
            for word in [
                "category",
                "type",
                "segment"
            ]
        ):

            detected["category"] = column

    return detected