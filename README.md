# 🤖 AutoAnalyst AI

### AI-Powered Autonomous Data Analysis Agent

AutoAnalyst AI is an intelligent data analysis system designed to automate the complete data analysis workflow.

It allows users to upload CSV or Excel datasets and automatically performs data cleaning, statistical analysis, visualization, trend analysis, revenue prediction, anomaly detection, AI-powered business insights, natural-language data Q&A, and PDF report generation.

---

## 📌 Project Overview

Data analysis normally requires multiple manual steps such as cleaning data, calculating statistics, creating charts, identifying trends, detecting anomalies, and preparing reports.

AutoAnalyst AI combines these tasks into a single automated platform.

The system uses Python-based data analysis, machine learning, visualization libraries, and a local AI language model to provide intelligent and automated analytical assistance.

---

## 🎯 Objectives

- Automate the data analysis process
- Reduce manual data preparation
- Automatically detect important dataset columns
- Clean and preprocess uploaded datasets
- Generate statistical summaries
- Create automatic data visualizations
- Identify revenue trends
- Predict future revenue
- Detect unusual numerical values
- Generate AI-powered business recommendations
- Allow users to ask questions about their dataset
- Generate downloadable PDF reports

---

## 🚀 Key Features

### 📁 1. CSV & Excel Upload

Users can upload:

- CSV files
- Excel `.xlsx` files

The system automatically loads the uploaded dataset.

---

### 🧹 2. Automatic Data Cleaning

AutoAnalyst AI automatically:

- Removes duplicate rows
- Handles missing numerical values
- Handles missing text values
- Validates uploaded datasets

---

### 🔍 3. Automatic Column Detection

The system identifies important columns such as:

- Date
- Revenue
- Quantity
- Product
- Category
- Region

Column detection is based on column names and common keywords.

---

### 📊 4. Automated Data Analysis

The system calculates:

- Total Revenue
- Average Revenue
- Total Quantity
- Top Product
- Top Product Revenue
- Top Region
- Top Region Revenue

---

### 📈 5. Automatic Visualization

AutoAnalyst AI generates interactive charts for:

- Revenue by Product
- Revenue by Region
- Quantity by Category

Charts are generated using Plotly.

---

### 📅 6. Trend Analysis

The system analyzes monthly revenue and identifies:

- Highest Revenue Month
- Lowest Revenue Month
- Overall Revenue Trend

The trend can be classified as:

- Increasing
- Decreasing
- Stable

---

### 🔮 7. Revenue Prediction

Future revenue is predicted using **Linear Regression**.

The system generates predictions for the next three months based on historical monthly revenue.

---

### 🚨 8. Anomaly Detection

AutoAnalyst AI uses the **Interquartile Range (IQR) method** to identify unusual numerical values.

Detected values are presented to the user for further review.

---

### 🧠 9. AI Business Insights

The system generates an automated business analysis containing:

- Executive Summary
- Key Findings
- Trend Insights
- Anomaly Insights
- Business Recommendations

The project uses a local LLM through Ollama.

---

### 🤖 10. Natural-Language Q&A

Users can ask questions about their uploaded dataset.

Example questions:

> What is the top product?

> What is the total revenue?

> What is the top region?

The AI assistant answers using the available dataset analysis.

---

### 📄 11. PDF Report Generation

AutoAnalyst AI can generate a downloadable PDF report containing:

- Dataset information
- Statistical analysis
- Business KPIs
- Trend analysis
- Predictions
- Anomaly information
- AI-generated insights

---

## 🏗️ System Architecture

```text
                 User
                  |
                  v
          Upload CSV / Excel
                  |
                  v
          Data Loading Module
                  |
                  v
         Data Cleaning Module
                  |
                  v
       Automatic Column Detection
                  |
                  v
           Analysis Engine
           |       |       |
           v       v       v
        Charts   Trends   KPIs
           |       |       |
           +-------+-------+
                   |
                   v
            ML Prediction
                   |
                   v
          Anomaly Detection
                   |
                   v
              AI Agent
           +-------+-------+
           |               |
           v               v
    Business Insights     Q&A
           |               |
           +-------+-------+
                   |
                   v
              PDF Report

```
## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and prediction |
| Plotly | Interactive visualization |
| Streamlit | Web application interface |
| Ollama | Local AI language model |
| Qwen 2.5 | Local LLM |
| OpenPyXL | Excel file processing |
| ReportLab | PDF report generation |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📂 Project Structure

```text
AutoAnalyst-AI/
│
├── agents/
│   ├── llm_agent.py
│   └── qa_agent.py
│
├── analysis/
│   ├── analytics.py
│   ├── anomaly_detector.py
│   ├── column_detector.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── predictor.py
│   └── trend_analyzer.py
│
├── data/
│   └── sales.csv
│
├── reports/
│   └── report_generator.py
│
├── visualizations/
│   └── charts.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```