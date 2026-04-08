import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("Analyzing barriers and adoption factors in developing economies")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    # Load and clean dataset
    df = pd.read_csv(uploaded_file, delimiter=';', decimal=',')
    
    # Drop unwanted columns
    df = df.drop(columns=['Corr_PU_BI','Corr_PEOU_BI','Corr_B_BI'], errors='ignore')
    
    # Convert to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    st.subheader("Dataset Preview")
    st.write(df.head())

    # --- Metrics ---
    st.subheader("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Avg Usefulness", round(df['PU_avg'].mean(),2))
    col2.metric("Avg Ease of Use", round(df['PEOU_avg'].mean(),2))
    col3.metric("Adoption Intention", round(df['BI_avg'].mean(),2))
    col4.metric("Barriers Level", round(df['B_avg'].mean(),2))

    # --- Correlation ---
    st.subheader("Correlation Analysis")

    pu_bi = df['PU_avg'].corr(df['BI_avg'])
    peou_bi = df['PEOU_avg'].corr(df['BI_avg'])
    b_bi = df['B_avg'].corr(df['BI_avg'])

    st.write({
        "PU vs BI": pu_bi,
        "PEOU vs BI": peou_bi,
        "Barriers vs BI": b_bi
    })

    # --- Visualization ---
    st.subheader("Visual Insights")

    fig, ax = plt.subplots()
    ax.scatter(df['PU_avg'], df['BI_avg'])
    ax.set_xlabel("Usefulness")
    ax.set_ylabel("Adoption Intention")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.scatter(df['B_avg'], df['BI_avg'])
    ax2.set_xlabel("Barriers")
    ax2.set_ylabel("Adoption Intention")
    st.pyplot(fig2)

    # --- Insight Section ---
    st.subheader("Insights")
    
    if b_bi < 0:
        st.warning("Barriers negatively impact adoption. Reducing barriers can improve AI tool usage.")
    
    if pu_bi > 0:
        st.success("Higher perceived usefulness increases adoption intention.")

    if peou_bi > 0:
        st.info("Ease of use positively influences adoption.")
