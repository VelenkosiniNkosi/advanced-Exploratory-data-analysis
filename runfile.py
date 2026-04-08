import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("This dashboard helps explain what influences startups to adopt AI coding tools.")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    # Load and clean dataset
    df = pd.read_csv(uploaded_file, delimiter=';', decimal=',')
    df = df.drop(columns=['Corr_PU_BI','Corr_PEOU_BI','Corr_B_BI'], errors='ignore')
    df = df.apply(pd.to_numeric, errors='coerce')

    st.subheader("Dataset Preview")
    st.write(df.head())

    # Rename for clarity
    df = df.rename(columns={
        'PU_avg': 'Perceived Usefulness',
        'PEOU_avg': 'Ease of Use',
        'BI_avg': 'Adoption Intention',
        'B_avg': 'Barriers to Adoption'
    })

    # --- Key Metrics ---
    st.subheader("Key Insights (Average Scores out of 5)")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Perceived Usefulness", round(df['Perceived Usefulness'].mean(),2))
    col2.metric("Ease of Use", round(df['Ease of Use'].mean(),2))
    col3.metric("Adoption Intention", round(df['Adoption Intention'].mean(),2))
    col4.metric("Barriers to Adoption", round(df['Barriers to Adoption'].mean(),2))

    # --- Explanation ---
    st.info("""
    These scores are based on a scale from 1 to 5:
    - 1 = Strongly Disagree
    - 5 = Strongly Agree
    
    Higher scores mean stronger agreement with each factor.
    """)

    # --- Correlation Analysis ---
    st.subheader("What Influences Adoption?")

    usefulness_vs_adoption = df['Perceived Usefulness'].corr(df['Adoption Intention'])
    ease_vs_adoption = df['Ease of Use'].corr(df['Adoption Intention'])
    barriers_vs_adoption = df['Barriers to Adoption'].corr(df['Adoption Intention'])

    st.write({
        "Usefulness vs Adoption": usefulness_vs_adoption,
        "Ease of Use vs Adoption": ease_vs_adoption,
        "Barriers vs Adoption": barriers_vs_adoption
    })

    # --- Human Explanation ---
    st.subheader("Simple Interpretation (For Everyone)")

    if usefulness_vs_adoption < 0:
        st.write("Usefulness does not strongly increase adoption. This suggests users may not yet trust AI tools to improve their work.")

    if abs(ease_vs_adoption) < 0.2:
        st.write("Ease of use has very little impact on whether people adopt AI tools.")

    if barriers_vs_adoption > 0:
        st.write("Barriers do not strongly stop adoption. Some users still try AI tools despite challenges.")

    # --- Visuals ---
    st.subheader("Visual Analysis")

    fig1, ax1 = plt.subplots()
    ax1.scatter(df['Perceived Usefulness'], df['Adoption Intention'])
    ax1.set_xlabel("Perceived Usefulness")
    ax1.set_ylabel("Adoption Intention")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.scatter(df['Barriers to Adoption'], df['Adoption Intention'])
    ax2.set_xlabel("Barriers to Adoption")
    ax2.set_ylabel("Adoption Intention")
    st.pyplot(fig2)

    # --- Final Insight ---
    st.subheader("Final Conclusion")

    st.success("""
    The results suggest that adoption of AI coding tools in startups is not driven mainly by usefulness or ease of use.
    Instead, other factors such as trust, awareness, and experience may play a bigger role.
    
    This means startups should focus on educating users and building trust in AI tools rather than only improving features.
    """)
