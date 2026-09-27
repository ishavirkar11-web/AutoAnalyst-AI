import plotly.express as px


def revenue_by_product(df, detected_columns=None):

    if detected_columns is None:
        detected_columns = {}

    product_column = detected_columns.get("product", "Product")
    revenue_column = detected_columns.get("revenue", "Revenue")

    if (
        product_column not in df.columns
        or revenue_column not in df.columns
    ):
        return None

    result = (
        df.groupby(product_column)[revenue_column]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        result,
        x=product_column,
        y=revenue_column,
        title="💰 Revenue by Product",
        text_auto=True
    )

    return fig


def revenue_by_region(df, detected_columns=None):

    if detected_columns is None:
        detected_columns = {}

    region_column = detected_columns.get("region", "Region")
    revenue_column = detected_columns.get("revenue", "Revenue")

    if (
        region_column not in df.columns
        or revenue_column not in df.columns
    ):
        return None

    result = (
        df.groupby(region_column)[revenue_column]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        result,
        x=region_column,
        y=revenue_column,
        title="🌍 Revenue by Region",
        text_auto=True
    )

    return fig


def quantity_by_category(df, detected_columns=None):

    if detected_columns is None:
        detected_columns = {}

    category_column = detected_columns.get("category", "Category")
    quantity_column = detected_columns.get("quantity", "Quantity")

    if (
        category_column not in df.columns
        or quantity_column not in df.columns
    ):
        return None

    result = (
        df.groupby(category_column)[quantity_column]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        result,
        names=category_column,
        values=quantity_column,
        title="📦 Quantity by Category"
    )

    return fig