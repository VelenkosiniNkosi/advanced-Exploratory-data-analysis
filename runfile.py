import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    # -----------------------------
    # BULLETPROOF FILE READER
    # -----------------------------
    try:
        file_content = uploaded_file.read().decode("utf-8")

        if "\t" in file_content:
            df = pd.read_csv(io.StringIO(file_content), sep="\t")
        else:
            df = pd.read_csv(io.StringIO(file_content))

    except Exception:
        st.error("Error reading file. Please check your CSV format.")
        st.stop()

    # -----------------------------
    # CLEAN + FIX STRUCTURE
    # -----------------------------
    df.columns = df.columns.str.strip()

    # Debug (remove later if you want)
    st.write("Detected Columns:", df.columns)

    if len(df.columns) == 4:
        df.columns = [
            "Perceived_Usefulness",
            "Ease_of_Use",
            "Adoption_Intention",
            "Barriers"
        ]

    elif len(df.columns) == 1:
        df = df[df.columns[0]].str.split("\t", expand=True)
        df.columns = [
            "Perceived_Usefulness",
            "Ease_of_Use",
            "Adoption_Intention",
            "Barriers"
        ]

    else:
        st.error("Dataset format is incorrect. Expected exactly 4 columns.")
        st.stop()

    # Convert to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # Check if empty
    if df.empty:
        st.error("Dataset is empty or corrupted.")
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
