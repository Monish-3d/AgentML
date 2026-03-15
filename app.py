import streamlit as st
import pandas as pd
import json

from core.schema_detector import detect_schema
from preprocessing.quick_preprocess import quick_encode

from eda.eda_engine import dataset_summary, statistics, missing_values
from eda.distribution import compute_skewness
from eda.correlation import correlation_matrix
from eda.health_score import compute_health_score

from agents.health_score_agent import generate_health_explanation

from utils.visualizations import plot_histograms, plot_correlation,plot_pairPlot

st.title("AgentML Dataset Analyzer")

uploaded_file = st.file_uploader("Upload dataset", type=["csv", "xlsx"])

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    # metadata
    target = st.selectbox("Select Target Column", df.columns)

    problem_type = st.selectbox(
        "Problem Type",
        ["classification", "regression"]
    )

    if st.button("Run Analysis"):

        # quick preprocessing
        df, logs = quick_encode(df)

        st.write("### Quick Preprocessing Applied")
        st.write(logs)

        # schema
        schema = detect_schema(df)

        st.write("### Schema Detection")
        st.write(schema)

        # EDA
        summary = dataset_summary(df)
        stats = statistics(df)
        missing = missing_values(df)
        skewness = compute_skewness(df)
        corr = correlation_matrix(df)

        health = compute_health_score(df, skewness)

        st.write("### Dataset Summary")
        st.write(summary)

        st.write("### Missing Values")
        st.write(missing)

        st.write("### Statistics")
        st.write(stats)

        st.write("### Skewness")
        st.write(skewness)

        st.write("### Dataset Health Score")
        st.metric("Health Score", health)

        # detect highly correlated features
        high_corr = []

        if corr is not None:
            for c1 in corr.columns:
                for c2 in corr.columns:
                    if c1 != c2 and abs(corr.loc[c1, c2]) > 0.8:
                        high_corr.append((c1, c2))

        missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        skewed_cols = [k for k,v in skewness.items() if abs(v) > 1]

        report = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_ratio": missing_ratio,
            "skewed_features": skewed_cols,
            "high_correlations": high_corr[:5],
            "health_score": health
        }

        #report_json = json.dumps(report, indent=2)
        try:
            explanation = generate_health_explanation(report)
        except Exception as e:
            st.warning(f"error : {e}")
            explanation = "AI explanation could not be generated at the moment. Showing dataset statistics instead."
            
        
        st.write(explanation)

        # visualizations
        st.write("### Histograms")
        st.write("##### It shows the distribution of a numerical feature by grouping values into ranges and displaying how many data points fall into each range")

        figs = plot_histograms(df)

        for fig in figs:
            st.pyplot(fig)

        # st.write("### Pair Plot")
        # st.write("##### It visualizes relationships between multiple features by plotting all possible feature pairs with scatterplots")
        # fig = plot_pairPlot(df)

        st.pyplot(fig)

        # kde plot -> It estimates and visualizes the probability density of a continuous variable, showing where values are concentrated smoothly instead of in discrete bins.

        if corr is not None:

            st.write("### Correlation Matrix")
            st.write("##### It measures how strongly two features in a dataset are related by comparing their values across all rows")

            fig = plot_correlation(corr)

            st.pyplot(fig)

    st.write("### Dataset Preview")
    st.dataframe(df.head())   
        