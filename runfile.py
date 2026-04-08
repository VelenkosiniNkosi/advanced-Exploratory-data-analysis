import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    try:
        content = uploaded_file.read().decode("utf-8")

        # Show raw preview for debugging
        st.write("Raw File Preview:", content[:200])

        # Try normal read
        df = pd.read_csv(io.StringIO(content))

        # If failed (1 column or empty), force split
        if df.shape[1] <= 1:
            df = pd.read_csv(io.StringIO(content), sep="\t")

        # If STILL wrong → manual split
        if df.shape[1] <= 1:
            rows = content.strip().split("\n")
            data = [row.split("\t") for row in rows]
            df = pd.DataFrame(data)

        # Remove empty columns
        df = df.dropna(axis=1, how='all')

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # -----------------------------
    # FIX COLUMNS SAFELY
    # -----------------------------
    st.write("Detected shape:", df.shape)

    if df.shape[1] != 4:
        st.error("Dataset format is incorrect. Expected 4 columns.")
        st.stop()

    df.columns = [
        "Perceived_Usefulness",
        "Ease_of_Use",
        "Adoption_Intention",
        "Barriers"
    ]

    # Convert to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # -----------------------------
    # DISPLAY
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Sidebar filter
    st.sidebar.header("Filter Data")

    min_usefulness = st.sidebar.slider(
        "Minimum Perceived Usefulness",
        float(df["Perceived_Usefulness"].min()),
        float(df["Perceived_Usefulness"].max()),
        float(df["Perceived_Usefulness"].min())
    )

    df_filtered = df[df["Perceived_Usefulness"] >= min_usefulness]

    # Metrics
    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Perceived Usefulness", round(df_filtered["Perceived_Usefulness"].mean(), 2))
    col2.metric("Average Ease of Use", round(df_filtered["Ease_of_Use"].mean(), 2))
    col3.metric("Average Adoption Intention", round(df_filtered["Adoption_Intention"].mean(), 2))
    col4.metric("Average Barriers to Adoption", round(df_filtered["Barriers"].mean(), 2))

    # Correlation
    st.subheader("Correlation Analysis")
    corr = df_filtered.corr()
    st.dataframe(corr)

    # Heatmap
    st.subheader("Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

else:
    st.info("Please upload a CSV file to begin analysis.")
