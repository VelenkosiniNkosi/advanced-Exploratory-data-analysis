import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Sidebar filter
    st.sidebar.header("Filter Data")

    min_usefulness = st.sidebar.slider(
        "Minimum Perceived Usefulness",
        float(df["Perceived_Usefulness"].min()),
        float(df["Perceived_Usefulness"].max()),
        float(df["Perceived_Usefulness"].min())
    )

    filtered_df = df[df["Perceived_Usefulness"] >= min_usefulness]

    # Metrics
    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Perceived Usefulness", round(filtered_df["Perceived_Usefulness"].mean(), 2))
    col2.metric("Average Ease of Use", round(filtered_df["Ease_of_Use"].mean(), 2))
    col3.metric("Adoption Intention", round(filtered_df["Adoption_Intention"].mean(), 2))
    col4.metric("Barriers Level", round(filtered_df["Barriers"].mean(), 2))

    # Correlation
    st.subheader("Correlation Analysis")

    corr_matrix = filtered_df.corr(numeric_only=True)

    st.write("Correlation Matrix")
    st.dataframe(corr_matrix)

    # Built-in heatmap alternative
    st.subheader("Correlation Heatmap")
    st.dataframe(corr_matrix.style.background_gradient(cmap="coolwarm"))

    # Bar chart
    st.subheader("Average Scores")

    avg_data = pd.DataFrame({
        "Metric": ["Usefulness", "Ease of Use", "Adoption", "Barriers"],
        "Value": [
            filtered_df["Perceived_Usefulness"].mean(),
            filtered_df["Ease_of_Use"].mean(),
            filtered_df["Adoption_Intention"].mean(),
            filtered_df["Barriers"].mean()
        ]
    })

    st.bar_chart(avg_data.set_index("Metric"))

    # Explanation
    st.subheader("Understanding the Results")

    st.write("""
    This dashboard explores factors influencing adoption of AI-assisted coding tools.

    Key Findings:

    - Perceived Usefulness shows a slight negative relationship with adoption.
      This may suggest users are skeptical about real-world benefits.

    - Ease of Use shows a weak positive relationship.
      Simpler tools slightly encourage adoption.

    - Barriers show a weak positive relationship.
      This may indicate complex external factors affecting decision-making.

    These findings highlight that adoption is influenced by more than just functionality,
    including trust, awareness, and contextual challenges in developing economies.
    """)
