import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    # -----------------------------
    # Robust CSV Reader (VERY IMPORTANT)
    # -----------------------------
    try:
        df = pd.read_csv(uploaded_file)

        # If file is incorrectly formatted (1 column only)
        if len(df.columns) == 1:
            df = pd.read_csv(uploaded_file, sep="\t")

    except Exception:
        df = pd.read_csv(uploaded_file, sep="\t")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Force correct column names if needed
    expected_columns = [
        "Perceived_Usefulness",
        "Ease_of_Use",
        "Adoption_Intention",
        "Barriers"
    ]

    if len(df.columns) == 4:
        df.columns = expected_columns

    # Convert all values to numeric (important)
    df = df.apply(pd.to_numeric, errors='coerce')

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("Filter Data")

    min_usefulness = st.sidebar.slider(
        "Minimum Perceived Usefulness",
        float(df["Perceived_Usefulness"].min()),
        float(df["Perceived_Usefulness"].max()),
        float(df["Perceived_Usefulness"].min())
    )

    df_filtered = df[df["Perceived_Usefulness"] >= min_usefulness]

    # -----------------------------
    # CLEAR METRICS (NO ABBREVIATIONS)
    # -----------------------------
    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Perceived Usefulness",
        round(df_filtered["Perceived_Usefulness"].mean(), 2)
    )

    col2.metric(
        "Average Ease of Use",
        round(df_filtered["Ease_of_Use"].mean(), 2)
    )

    col3.metric(
        "Average Adoption Intention",
        round(df_filtered["Adoption_Intention"].mean(), 2)
    )

    col4.metric(
        "Average Barriers to Adoption",
        round(df_filtered["Barriers"].mean(), 2)
    )

    # -----------------------------
    # CORRELATION ANALYSIS
    # -----------------------------
    st.subheader("Relationship Analysis (Correlation)")

    correlation = df_filtered.corr()

    st.write("Correlation Matrix:")
    st.dataframe(correlation)

    # -----------------------------
    # HEATMAP
    # -----------------------------
    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)

    st.pyplot(fig)

    # -----------------------------
    # INTERPRETATION SECTION
    # -----------------------------
    st.subheader("Interpretation of Results")

    st.write("""
    - A positive value indicates that two factors increase together.
    - A negative value indicates an inverse relationship.
    
    Key insights:
    - Perceived Usefulness may not always strongly influence adoption intention in developing environments.
    - Ease of Use shows a weak relationship, suggesting other external factors may dominate.
    - Barriers may behave differently depending on user context and access to technology.
    """)

else:
    st.info("Please upload a CSV file to begin analysis.")
