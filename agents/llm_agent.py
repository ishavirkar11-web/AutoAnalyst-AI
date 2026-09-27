import ollama


# ============================================================
# ASK LLM
# ============================================================

def ask_llm(question, df, results):

    dataset_context = f"""
Dataset columns:
{list(df.columns)}

Number of rows:
{len(df)}

Number of columns:
{len(df.columns)}

Calculated analysis:
{results}
"""

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "system",
                "content": """
You are AutoAnalyst AI, an AI data analysis assistant.

Answer the user's question using ONLY the information
provided in the dataset context.

STRICT RULES:

- Never invent numbers.
- Never invent dates or years.
- Never invent products.
- Never invent regions.
- Never invent statistics.
- Never assume information that is not provided.
- If the requested information is unavailable, say:
  "This information is not available in the dataset."
- Keep the answer simple and concise.
"""
            },
            {
                "role": "user",
                "content": f"""
{dataset_context}

User question:
{question}
"""
            }
        ]
    )

    return response["message"]["content"]


# ============================================================
# EXPLAIN ANOMALIES
# ============================================================

def explain_anomalies(anomalies, df):

    if not anomalies:

        return """
### ✅ No Anomalies Detected

The automated anomaly detection system did not
identify any unusual numerical values in the dataset.
"""

    explanation = """
### 🚨 Detected Anomalies

"""

    for anomaly in anomalies:

        row = anomaly.get("row", "Unknown")
        column = anomaly.get("column", "Unknown")
        value = anomaly.get("value", "Unknown")

        explanation += f"""
**Row {row}**

The value **{value}** in the **{column}** column
was identified as unusual compared with the other
numerical observations.

This does **not necessarily mean that the value is incorrect**.
It may represent a genuine business observation or
a possible data-quality issue.

The value should be reviewed by a data analyst
before making a final decision.

---

"""

    return explanation


# ============================================================
# GENERATE BUSINESS INSIGHTS
# ============================================================

def generate_business_insights(
    df,
    results,
    trend_results=None,
    anomalies=None
):

    if anomalies is None:
        anomalies = []


    # --------------------------------------------------------
    # PYTHON-CALCULATED VALUES
    # --------------------------------------------------------

    total_revenue = results.get(
        "total_revenue",
        0
    )

    average_revenue = results.get(
        "average_revenue",
        0
    )

    total_quantity = results.get(
        "total_quantity",
        0
    )

    top_product = results.get(
        "top_product",
        "Not available"
    )

    top_product_revenue = results.get(
        "top_product_revenue",
        0
    )

    top_region = results.get(
        "top_region",
        "Not available"
    )

    top_region_revenue = results.get(
        "top_region_revenue",
        0
    )


    # --------------------------------------------------------
    # TREND VALUES
    # --------------------------------------------------------

    overall_trend = "Not available"
    highest_month = "Not available"
    highest_month_revenue = 0
    lowest_month = "Not available"
    lowest_month_revenue = 0


    if trend_results is not None:

        overall_trend = trend_results.get(
            "overall_trend",
            "Not available"
        )

        highest_month = trend_results.get(
            "highest_month",
            "Not available"
        )

        highest_month_revenue = trend_results.get(
            "highest_month_revenue",
            0
        )

        lowest_month = trend_results.get(
            "lowest_month",
            "Not available"
        )

        lowest_month_revenue = trend_results.get(
            "lowest_month_revenue",
            0
        )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    ai_context = f"""
The Python analysis identified these facts:

Top Product:
{top_product}

Top Region:
{top_region}

Overall Revenue Trend:
{overall_trend}

Number of anomalies:
{len(anomalies)}
"""


    try:

        response = ollama.chat(
            model="qwen2.5:0.5b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are AutoAnalyst AI.

Python has already calculated the numerical analysis.

Your task is ONLY to provide exactly THREE
short business recommendations.

STRICT RULES:

1. Return exactly 3 bullet points.
2. Do not mention numbers.
3. Do not mention revenue amounts.
4. Do not mention dates.
5. Do not mention years.
6. Do not invent facts.
7. Do not explain causes of anomalies.
8. Do not create statistics.
9. Do not claim information that is not provided.
10. Keep recommendations practical and suitable
    for a college engineering project.

Use these facts only:

- The top product is provided.
- The top region is provided.
- The overall revenue trend is provided.
- Anomaly count is provided.

Example style:

- Focus on products that show strong performance.
- Review regional performance when planning business strategies.
- Continue monitoring the revenue trend and unusual values.
"""
                },
                {
                    "role": "user",
                    "content": ai_context
                }
            ]
        )

        recommendations = response["message"]["content"]

    except Exception:

        recommendations = """
- Focus on products that show strong performance.
- Review regional performance when planning business strategies.
- Continue monitoring the revenue trend and unusual values.
"""


    # ========================================================
    # FINAL FACTUAL REPORT
    # ========================================================

    report = f"""
### Executive Summary

The dataset contains **{len(df)} rows**
and **{len(df.columns)} columns**.

The total recorded revenue is
**₹{total_revenue:,.0f}**.

The average revenue is
**₹{average_revenue:,.0f}**.

The overall revenue trend is
**{overall_trend}**.


### Key Findings

- **Total Revenue:** ₹{total_revenue:,.0f}
- **Average Revenue:** ₹{average_revenue:,.0f}
- **Total Quantity Sold:** {total_quantity}
- **Top Product:** {top_product}
- **Top Product Revenue:** ₹{top_product_revenue:,.0f}
- **Top Region:** {top_region}
- **Top Region Revenue:** ₹{top_region_revenue:,.0f}


### Trend Insight

- **Highest Revenue Month:** {highest_month}
- **Highest Month Revenue:** ₹{highest_month_revenue:,.0f}
- **Lowest Revenue Month:** {lowest_month}
- **Lowest Month Revenue:** ₹{lowest_month_revenue:,.0f}
- **Overall Revenue Trend:** {overall_trend}


### Anomaly Insight

The automated anomaly detection system identified
**{len(anomalies)} unusual value(s)**.

An unusual value does not automatically indicate
an error. The detected values should be reviewed
by a data analyst.


### Business Recommendations

{recommendations}
"""

    return report