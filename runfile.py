import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    # -----------------------------
    # ROBUST CSV READER (FINAL FIX)
    # -----------------------------
    try:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)

        # If only one column → wrong delimiter
        if len(df.columns) == 1:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep="\t")

    except Exception:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep="\t")

    # Clean column names
    df.columns = df.columns.str.strip()

    # If still broken (all data in one column), split manually
    if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(",", expand=True)
        df.columns = [
            "Perceived_Usefulness",
            "Ease_of_Use",
            "Adoption_Intention",
            "Barriers"
        ]

    # Ensure correct column names
    expected_columns = [
        "Perceived_Usefulness",
        "Ease_of_Use",
        "Adoption_Intention",
        "Barriers"
    ]

    if len(df.columns) == 4:
        df.columns = expected_columns

    # Convert all values to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # Handle empty dataset
    if df.empty:
        st.error("Uploaded file is empty or incorrectly formatted.")
        st.stop()

    # -----------------------------
    # DISPLAY DATA
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # -----------------------------
    # SIDEBAR FILTER
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
    # METRICS
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
    # CORRELATION
    # -----------------------------
    st.subheader("Relationship Analysis (Correlation)")

    correlation = df_filtered.corr()
    st.dataframe(correlation)

    # -----------------------------
    # HEATMAP
    # -----------------------------
    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.subheader("Interpretation of Results")

    st.write("""
    - Positive values indicate variables increase together.
    - Negative values indicate inverse relationships.

    Insights:
    - Perceived usefulness may not strongly predict adoption in all contexts.
    - Ease of use shows moderate influence.
    - Barriers can significantly affect adoption depending on environment.
    """)

else:
    st.info("Please upload a CSV file to begin analysis.")
