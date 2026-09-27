from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf_report(
    file_path,
    df,
    results,
    trend_results=None,
    prediction_results=None,
    anomalies=None,
    business_insights=""
):

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    content = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    content.append(
        Paragraph(
            "AutoAnalyst AI",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Automated Data Analysis Report",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # DATASET OVERVIEW
    # -------------------------------------------------

    content.append(
        Paragraph(
            "1. Dataset Overview",
            styles["Heading2"]
        )
    )

    overview_data = [
        ["Metric", "Value"],
        ["Rows", str(df.shape[0])],
        ["Columns", str(df.shape[1])],
        [
            "Missing Values",
            str(int(df.isnull().sum().sum()))
        ],
        [
            "Duplicate Rows",
            str(int(df.duplicated().sum()))
        ]
    ]

    overview_table = Table(
        overview_data,
        colWidths=[3 * inch, 2 * inch]
    )

    overview_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    content.append(
        overview_table
    )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # KEY BUSINESS METRICS
    # -------------------------------------------------

    content.append(
        Paragraph(
            "2. Key Business Metrics",
            styles["Heading2"]
        )
    )

    metrics = [
        ["Metric", "Value"]
    ]

    if "total_revenue" in results:

        metrics.append([
            "Total Revenue",
            f"Rs. {results['total_revenue']:,.0f}"
        ])

    if "average_revenue" in results:

        metrics.append([
            "Average Revenue",
            f"Rs. {results['average_revenue']:,.0f}"
        ])

    if "total_quantity" in results:

        metrics.append([
            "Total Quantity",
            f"{results['total_quantity']:,}"
        ])

    if "top_product" in results:

        metrics.append([
            "Top Product",
            str(results["top_product"])
        ])

    if "top_region" in results:

        metrics.append([
            "Top Region",
            str(results["top_region"])
        ])

    metrics_table = Table(
        metrics,
        colWidths=[3 * inch, 2 * inch]
    )

    metrics_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    content.append(
        metrics_table
    )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # TREND ANALYSIS
    # -------------------------------------------------

    content.append(
        Paragraph(
            "3. Trend Analysis",
            styles["Heading2"]
        )
    )

    if trend_results is not None:

        content.append(
            Paragraph(
                f"Overall Trend: "
                f"{trend_results['overall_trend']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Highest Revenue Month: "
                f"{trend_results['highest_month']} "
                f"(Rs. "
                f"{trend_results['highest_month_revenue']:,.0f})",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Lowest Revenue Month: "
                f"{trend_results['lowest_month']} "
                f"(Rs. "
                f"{trend_results['lowest_month_revenue']:,.0f})",
                styles["BodyText"]
            )
        )

    else:

        content.append(
            Paragraph(
                "Trend analysis was not available.",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # REVENUE PREDICTION
    # -------------------------------------------------

    content.append(
        Paragraph(
            "4. Revenue Prediction",
            styles["Heading2"]
        )
    )

    if prediction_results is not None:

        prediction_data = [
            ["Month", "Predicted Revenue"]
        ]

        for _, row in prediction_results.iterrows():

            prediction_data.append([
                str(row["Month"]),
                f"Rs. {row['Predicted Revenue']:,.0f}"
            ])

        prediction_table = Table(
            prediction_data,
            colWidths=[3 * inch, 2 * inch]
        )

        prediction_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        content.append(
            prediction_table
        )

    else:

        content.append(
            Paragraph(
                "Revenue prediction was not available.",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # ANOMALIES
    # -------------------------------------------------

    content.append(
        Paragraph(
            "5. Anomaly Detection",
            styles["Heading2"]
        )
    )

    if anomalies:

        content.append(
            Paragraph(
                f"{len(anomalies)} unusual value(s) "
                f"were detected.",
                styles["BodyText"]
            )
        )

        anomaly_data = [
            ["Row", "Column", "Value"]
        ]

        for anomaly in anomalies:

            anomaly_data.append([
                str(anomaly["row"]),
                str(anomaly["column"]),
                str(anomaly["value"])
            ])

        anomaly_table = Table(
            anomaly_data,
            colWidths=[
                1 * inch,
                2 * inch,
                2 * inch
            ]
        )

        anomaly_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        content.append(
            anomaly_table
        )

    else:

        content.append(
            Paragraph(
                "No unusual numerical values were detected.",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # AI BUSINESS INSIGHTS
    # -------------------------------------------------

    content.append(
        Paragraph(
            "6. AI-Generated Business Insights",
            styles["Heading2"]
        )
    )

    if business_insights:

        insight_lines = (
            business_insights
            .split("\n")
        )

        for line in insight_lines:

            line = line.strip()

            if line:

                # Remove basic Markdown symbols
                line = line.replace("**", "")

                content.append(
                    Paragraph(
                        line,
                        styles["BodyText"]
                    )
                )

                content.append(
                    Spacer(1, 5)
                )

    else:

        content.append(
            Paragraph(
                "AI business insights were not available.",
                styles["BodyText"]
            )
        )

    # -------------------------------------------------
    # BUILD PDF
    # -------------------------------------------------

    document.build(content)