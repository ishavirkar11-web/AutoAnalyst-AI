import io
import streamlit as st
import pandas as pd

from analysis.data_loader import load_data
from analysis.data_cleaner import clean_data
from analysis.column_detector import detect_columns
from analysis.analytics import analyze_data

from visualizations.charts import (
    revenue_by_product,
    revenue_by_region,
    quantity_by_category
)

from analysis.trend_analyzer import analyze_trends
from analysis.predictor import predict_revenue
from analysis.anomaly_detector import detect_anomalies

from agents.llm_agent import (
    explain_anomalies,
    generate_business_insights
)

from agents.qa_agent import answer_question
from reports.report_generator import generate_pdf_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AutoAnalyst AI",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AutoAnalyst AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Automated Data Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Upload a CSV or Excel dataset to automatically clean, "
    "analyze, visualize, predict and generate AI-powered "
    "business insights."
)


# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">📁 Upload Dataset</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)


if uploaded_file is None:

    st.info(
        "👆 Upload a CSV or Excel dataset to begin."
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data(uploaded_file)

except Exception as e:

    st.error(
        f"❌ Could not load the dataset: {e}"
    )

    st.stop()


st.success(
    "Dataset uploaded successfully!"
)


# ============================================================
# BASIC DATASET VALIDATION
# ============================================================

if len(df) < 2:

    st.warning(
        "⚠️ The dataset contains fewer than 2 rows. "
        "Some analysis features may not work correctly."
    )


if len(df.columns) < 2:

    st.warning(
        "⚠️ The dataset contains very few columns. "
        "Automatic analysis may be limited."
    )


numeric_columns = df.select_dtypes(
    include="number"
).columns


if len(numeric_columns) == 0:

    st.error(
        "❌ No numerical columns were detected. "
        "AutoAnalyst requires at least one numerical "
        "column for statistical analysis."
    )

    st.stop()


# ============================================================
# DETECT COLUMNS
# ============================================================

detected_columns = detect_columns(
    df
)


# ============================================================
# REVENUE COLUMN VALIDATION
# ============================================================

if "revenue" not in detected_columns:

    st.warning(
        "⚠️ A Revenue/Sales/Amount column was not detected. "
        "Revenue-based analysis and prediction may be unavailable."
    )


# ============================================================
# DISPLAY DETECTED COLUMNS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔍 Automatically Detected Columns'
    '</div>',
    unsafe_allow_html=True
)


detect1, detect2, detect3 = st.columns(3)


with detect1:

    st.write(
        f"**Date:** "
        f"`{detected_columns.get('date', 'Not detected')}`"
    )

    st.write(
        f"**Product:** "
        f"`{detected_columns.get('product', 'Not detected')}`"
    )


with detect2:

    st.write(
        f"**Category:** "
        f"`{detected_columns.get('category', 'Not detected')}`"
    )

    st.write(
        f"**Region:** "
        f"`{detected_columns.get('region', 'Not detected')}`"
    )


with detect3:

    st.write(
        f"**Quantity:** "
        f"`{detected_columns.get('quantity', 'Not detected')}`"
    )

    st.write(
        f"**Revenue:** "
        f"`{detected_columns.get('revenue', 'Not detected')}`"
    )


# ============================================================
# CLEAN DATA
# ============================================================

try:

    cleaned_df = clean_data(
        df
    )

except Exception as e:

    st.error(
        f"❌ Data cleaning failed: {e}"
    )

    st.stop()


# ============================================================
# ANALYSIS
# ============================================================

try:

    results = analyze_data(
        cleaned_df,
        detected_columns
    )

except Exception as e:

    st.error(
        f"❌ Data analysis failed: {e}"
    )

    st.stop()


# ============================================================
# GET ANALYSIS VALUES
# ============================================================

revenue = results.get(
    "total_revenue",
    0
)

average_revenue = results.get(
    "average_revenue",
    0
)

quantity = results.get(
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


# ============================================================
# TREND ANALYSIS
# ============================================================

try:

    trend_results = analyze_trends(
        cleaned_df,
        detected_columns
    )

except Exception:

    trend_results = None


# ============================================================
# REVENUE PREDICTION
# ============================================================

try:

    prediction_results = predict_revenue(
        cleaned_df,
        detected_columns,
        future_periods=3
    )

except Exception:

    prediction_results = None


# ============================================================
# ANOMALY DETECTION
# ============================================================

try:

    anomalies = detect_anomalies(
        cleaned_df
    )

except Exception:

    anomalies = []


# ============================================================
# MAIN DASHBOARD TABS
# ============================================================

tab_analysis, tab_trends, tab_prediction, tab_anomaly, tab_ai, tab_qa = st.tabs(
    [
        "📊 Analysis",
        "📈 Trends",
        "🔮 Prediction",
        "🚨 Anomalies",
        "🧠 AI Insights",
        "🤖 Q&A"
    ]
)


# ============================================================
# TAB 1 — ANALYSIS
# ============================================================

with tab_analysis:

    st.markdown(
        '<div class="section-title">'
        '📊 Dataset Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------------

    st.subheader(
        "📋 Dataset Overview"
    )

    overview1, overview2, overview3, overview4 = st.columns(4)


    with overview1:

        st.metric(
            "Rows",
            len(df)
        )


    with overview2:

        st.metric(
            "Columns",
            len(df.columns)
        )


    with overview3:

        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )


    with overview4:

        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )


    # --------------------------------------------------------
    # ORIGINAL DATASET
    # --------------------------------------------------------

    st.subheader(
        "📊 Original Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CLEANED DATASET
    # --------------------------------------------------------

    st.subheader(
        "🧹 Cleaned Dataset"
    )

    st.dataframe(
        cleaned_df,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CLEANING RESULTS
    # --------------------------------------------------------

    st.subheader(
        "✅ Cleaning Results"
    )

    clean1, clean2, clean3 = st.columns(3)


    with clean1:

        st.metric(
            "Original Rows",
            len(df)
        )


    with clean2:

        st.metric(
            "Cleaned Rows",
            len(cleaned_df)
        )


    with clean3:

        st.metric(
            "Remaining Missing Values",
            int(
                cleaned_df.isnull().sum().sum()
            )
        )


    # --------------------------------------------------------
    # STATISTICAL SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "📈 Statistical Summary"
    )

    try:

        statistical_summary = cleaned_df.describe()

        st.dataframe(
            statistical_summary,
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Statistical summary unavailable: {e}"
        )


    # --------------------------------------------------------
    # KEY BUSINESS INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "💡 Key Business Insights"
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


    with kpi1:

        st.metric(
            "💰 Total Revenue",
            f"₹{revenue:,.0f}"
        )


    with kpi2:

        st.metric(
            "📊 Average Revenue",
            f"₹{average_revenue:,.0f}"
        )


    with kpi3:

        st.metric(
            "📦 Total Quantity",
            f"{quantity}"
        )


    with kpi4:

        st.metric(
            "🏆 Top Product",
            top_product
        )


    # --------------------------------------------------------
    # AUTOMATIC INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "🔎 Automatically Generated Insights"
    )


    st.write(
        f"🏆 **Top Product:** {top_product}"
    )


    st.write(
        f"💰 **Top Product Revenue:** "
        f"₹{top_product_revenue:,.0f}"
    )


    st.write(
        f"🌍 **Top Region:** {top_region}"
    )


    st.write(
        f"💰 **Top Region Revenue:** "
        f"₹{top_region_revenue:,.0f}"
    )


    # --------------------------------------------------------
    # AUTOMATIC VISUALIZATIONS
    # --------------------------------------------------------

    st.subheader(
        "📊 Automatic Visualizations"
    )


    try:

        chart1 = revenue_by_product(
            cleaned_df,
            detected_columns
        )

    except Exception:

        chart1 = None


    try:

        chart2 = revenue_by_region(
            cleaned_df,
            detected_columns
        )

    except Exception:

        chart2 = None


    try:

        chart3 = quantity_by_category(
            cleaned_df,
            detected_columns
        )

    except Exception:

        chart3 = None


    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        if chart1 is not None:

            st.plotly_chart(
                chart1,
                use_container_width=True
            )

        else:

            st.info(
                "Product revenue chart is unavailable."
            )


    with chart_col2:

        if chart2 is not None:

            st.plotly_chart(
                chart2,
                use_container_width=True
            )

        else:

            st.info(
                "Regional revenue chart is unavailable."
            )


    if chart3 is not None:

        st.plotly_chart(
            chart3,
            use_container_width=True
        )

    else:

        st.info(
            "Category quantity chart is unavailable."
        )


# ============================================================
# TAB 2 — TRENDS
# ============================================================

with tab_trends:

    st.markdown(
        '<div class="section-title">'
        '📈 Automatic Trend Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    if trend_results is not None:

        st.subheader(
            "📊 Monthly Revenue"
        )

        st.dataframe(
            trend_results["monthly_revenue"],
            use_container_width=True
        )


        trend1, trend2, trend3 = st.columns(3)


        with trend1:

            st.metric(
                "Overall Trend",
                trend_results["overall_trend"]
            )


        with trend2:

            st.metric(
                "Highest Revenue Month",
                trend_results["highest_month"]
            )


        with trend3:

            st.metric(
                "Lowest Revenue Month",
                trend_results["lowest_month"]
            )


        st.subheader(
            "🔎 Trend Insights"
        )


        st.write(
            f"📈 **Highest Revenue Month:** "
            f"{trend_results['highest_month']}"
        )


        st.write(
            f"Revenue: "
            f"₹{trend_results['highest_month_revenue']:,.0f}"
        )


        st.write(
            f"📉 **Lowest Revenue Month:** "
            f"{trend_results['lowest_month']}"
        )


        st.write(
            f"Revenue: "
            f"₹{trend_results['lowest_month_revenue']:,.0f}"
        )


        st.write(
            f"📊 **Overall Revenue Trend:** "
            f"{trend_results['overall_trend']}"
        )


    else:

        st.warning(
            "⚠️ Trend analysis requires valid "
            "date and revenue data."
        )


# ============================================================
# TAB 3 — PREDICTION
# ============================================================

with tab_prediction:

    st.markdown(
        '<div class="section-title">'
        '🔮 Future Revenue Prediction'
        '</div>',
        unsafe_allow_html=True
    )


    if prediction_results is not None:

        st.subheader(
            "📊 Predicted Revenue for Next 3 Months"
        )


        st.dataframe(
            prediction_results,
            use_container_width=True
        )


        prediction1, prediction2 = st.columns(2)


        with prediction1:

            st.metric(
                "Average Predicted Revenue",
                f"₹{prediction_results['Predicted Revenue'].mean():,.0f}"
            )


        with prediction2:

            st.metric(
                "Prediction Periods",
                len(prediction_results)
            )


        st.info(
            "Prediction is generated using "
            "Linear Regression based on historical "
            "monthly revenue."
        )


    else:

        st.warning(
            "⚠️ Revenue prediction requires "
            "sufficient date and revenue data."
        )


# ============================================================
# TAB 4 — ANOMALIES
# ============================================================

with tab_anomaly:

    st.markdown(
        '<div class="section-title">'
        '🚨 Automatic Anomaly Detection'
        '</div>',
        unsafe_allow_html=True
    )


    if anomalies:

        st.warning(
            f"⚠️ {len(anomalies)} unusual value(s) detected."
        )


        anomaly_df = pd.DataFrame(
            anomalies
        )


        st.dataframe(
            anomaly_df,
            use_container_width=True
        )


    else:

        st.success(
            "✅ No unusual values were detected."
        )


    st.subheader(
        "🤖 AI Explanation of Anomalies"
    )


    try:

        anomaly_explanation = explain_anomalies(
            anomalies,
            cleaned_df
        )


        st.markdown(
            anomaly_explanation
        )


    except Exception as e:

        st.error(
            f"❌ AI anomaly explanation failed: {e}"
        )


# ============================================================
# TAB 5 — AI INSIGHTS
# ============================================================

with tab_ai:

    st.markdown(
        '<div class="section-title">'
        '🧠 AI-Generated Business Insights'
        '</div>',
        unsafe_allow_html=True
    )


    try:

        business_insights = generate_business_insights(
            cleaned_df,
            results,
            trend_results,
            anomalies
        )


        st.markdown(
            business_insights
        )


    except Exception as e:

        business_insights = ""

        st.error(
            f"❌ AI business insights failed: {e}"
        )


    # --------------------------------------------------------
    # PDF REPORT
    # --------------------------------------------------------

    st.subheader(
        "📄 Download Analysis Report"
    )


    st.write(
        "Generate a complete PDF report containing "
        "dataset analysis, trends, predictions, "
        "anomalies and AI-generated insights."
    )


    try:

        pdf_buffer = io.BytesIO()


        generate_pdf_report(
            pdf_buffer,
            cleaned_df,
            results,
            trend_results,
            prediction_results,
            anomalies,
            business_insights
        )


        pdf_buffer.seek(0)


        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="AutoAnalyst_Report.pdf",
            mime="application/pdf"
        )


    except Exception as e:

        st.error(
            f"❌ PDF report generation failed: {e}"
        )


# ============================================================
# TAB 6 — Q&A
# ============================================================

with tab_qa:

    st.markdown(
        '<div class="section-title">'
        '🤖 Ask AutoAnalyst AI'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Ask questions about your uploaded dataset."
    )


    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is the top product?"
    )


    if question:

        with st.spinner(
            "🤖 AutoAnalyst AI is analyzing your question..."
        ):

            try:

                answer = answer_question(
                    question,
                    cleaned_df,
                    results
                )


                st.markdown(
                    "### 🤖 AutoAnalyst AI"
                )


                st.write(
                    answer
                )


            except Exception as e:

                st.error(
                    f"❌ AI could not answer the question: {e}"
                )