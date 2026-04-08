import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Adoption Dashboard", layout="wide")

st.title("AI-Assisted Coding Tools Adoption Dashboard")
st.write("This dashboard explains factors influencing the adoption of AI coding tools among startup developers.")

# Upload dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    # Load and clean dataset
    df = pd.read_csv(uploaded_file, delimiter=';', decimal=',')
    df = df.drop(columns=['Corr_PU_BI','Corr_PEOU_BI','Corr_B_BI'], errors='ignore')
    df = df.apply(pd.to_numeric, errors='coerce')

    # Rename columns for clarity
    df = df.rename(columns={
        'PU_avg': 'Perceived Usefulness',
        'PEOU_avg': 'Ease of Use',
        'BI_avg': 'Adoption Intention',
        'B_avg': 'Barriers to Adoption'
    })

    # Sidebar filters
    st.sidebar.header("Filter Data")

    min_usefulness = st.sidebar.slider("Minimum Perceived Usefulness", 1.0, 5.0, 1.0)
    min_ease = st.sidebar.slider("Minimum Ease of Use", 1.0, 5.0, 1.0)

    filtered_df = df[
        (df['Perceived Usefulness'] >= min_usefulness) &
        (df['Ease of Use'] >= min_ease)
    ]

    st.subheader("Filtered Dataset Preview")
    st.write(filtered_df.head())

    # Key metrics
    st.subheader("Key Metrics (Average Scores)")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Perceived Usefulness", round(filtered_df['Perceived Usefulness'].mean(), 2))
    col2.metric("Ease of Use", round(filtered_df['Ease of Use'].mean(), 2))
    col3.metric("Adoption Intention", round(filtered_df['Adoption Intention'].mean(), 2))
    col4.metric("Barriers to Adoption", round(filtered_df['Barriers to Adoption'].mean(), 2))

    st.info("All values are measured on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).")

    # Correlation analysis
    st.subheader("Correlation Analysis")

    corr_matrix = filtered_df[['Perceived Usefulness', 'Ease of Use', 'Adoption Intention', 'Barriers to Adoption']].corr()
    st.write(corr_matrix)

    # Heatmap
    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots()
    cax = ax.matshow(corr_matrix)
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    fig.colorbar(cax)

    for (i, j), val in enumerate(corr_matrix.values.flatten()):
        ax.text(j, i, f"{val:.2f}", ha='center', va='center')

    st.pyplot(fig)

    # Scatter plots
    st.subheader("Relationships Between Variables")

    fig1, ax1 = plt.subplots()
    ax1.scatter(filtered_df['Perceived Usefulness'], filtered_df['Adoption Intention'])
    ax1.set_xlabel("Perceived Usefulness")
    ax1.set_ylabel("Adoption Intention")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df['Barriers to Adoption'], filtered_df['Adoption Intention'])
    ax2.set_xlabel("Barriers to Adoption")
    ax2.set_ylabel("Adoption Intention")
    st.pyplot(fig2)

    # Interpretation
    st.subheader("Interpretation")

    pu_corr = corr_matrix.loc['Perceived Usefulness', 'Adoption Intention']
    peou_corr = corr_matrix.loc['Ease of Use', 'Adoption Intention']
    b_corr = corr_matrix.loc['Barriers to Adoption', 'Adoption Intention']

    if pu_corr < 0:
        st.write("Perceived usefulness does not strongly increase adoption in this dataset.")

    if abs(peou_corr) < 0.2:
        st.write("Ease of use has minimal influence on adoption decisions.")

    if b_corr > 0:
        st.write("Barriers do not significantly reduce adoption in this dataset.")

    # Final conclusion
    st.subheader("Conclusion")

    st.write("""
    The analysis shows that adoption of AI coding tools is not strongly influenced by usefulness or ease of use alone.
    This suggests that external factors such as trust, awareness, and access to resources may be more important.
    """)
