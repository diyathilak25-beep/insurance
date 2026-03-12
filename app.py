import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import numpy as np

st.set_page_config(layout="wide", page_title="Insurance Bias Dashboard")

# --- Helper Functions ---
def get_age_group(age):
    if age <= 25: return '18-25'
    if age <= 35: return '26-35'
    if age <= 45: return '36-45'
    if age <= 55: return '46-55'
    return '56+'

def get_bmi_cat(bmi):
    if bmi < 18.5: return 'Underweight'
    if bmi < 25: return 'Normal'
    if bmi < 30: return 'Overweight'
    return 'Obese'

# --- Sidebar ---
st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Insurance CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['age_group'] = df['age'].apply(get_age_group)
    df['bmi_category'] = df['bmi'].apply(get_bmi_cat)
    
    page = st.sidebar.radio("Navigation", ["Overview", "Pivot Tables", "Bias Metrics", "Intersectional Analysis"])

    # --- Page 1: Overview ---
    if page == "Overview":
        st.title("📊 Insurance Data Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", len(df))
        col2.metric("Avg Charges", f"${df['charges'].mean():,.2f}")
        col3.metric("Median Charges", f"${df['charges'].median():,.2f}")
        col4.metric("% Smokers", f"{(df['smoker'] == 'yes').mean():.1%}")
        
        fig = px.bar(df.groupby('region')['charges'].mean().reset_index(), x='region', y='charges', title="Avg Charges by Region")
        st.plotly_chart(fig, use_container_width=True)

    # --- Page 2: Pivot Tables ---
    elif page == "Pivot Tables":
        st.title("🔍 Bias Detection Pivot Tables")
        
        # Table 1: Sex x Smoker
        st.subheader("Charges by Sex & Smoker Status")
        pivot1 = df.pivot_table(index='sex', columns='smoker', values='charges', aggfunc='mean')
        st.dataframe(pivot1.style.background_gradient(cmap='Reds'))
        st.caption("⚠️ Interpretation: If smoker premiums differ significantly by sex, this indicates potential gender bias in underwriting.")

        # Table 2: Region x Sex
        st.subheader("Charges by Region & Sex")
        pivot2 = df.pivot_table(index='region', columns='sex', values='charges', aggfunc='mean')
        pivot2['Disparity Ratio'] = pivot2['male'] / pivot2['female']
        st.dataframe(pivot2)

    # --- Page 3: Bias Metrics ---
    elif page == "Bias Metrics":
        st.title("⚖️ Statistical Bias Metrics")
        
        # DIR Calculation
        st.subheader("Disparate Impact Ratio (DIR)")
        # Example for Sex
        male_avg = df[df['sex']=='male']['charges'].mean()
        female_avg = df[df['sex']=='female']['charges'].mean()
        dir_val = male_avg / female_avg
        st.metric("DIR (Male/Female)", f"{dir_val:.2f}", delta_color="inverse")
        
        # T-Test
        t_stat, p_val = stats.ttest_ind(df[df['sex']=='male']['charges'], df[df['sex']=='female']['charges'])
        st.write(f"**T-Test P-Value (Sex):** {p_val:.4f}")
        if p_val < 0.05: st.error("Statistically Significant Difference Detected!")

    # --- Page 4: Intersectional ---
    elif page == "Intersectional Analysis":
        st.title("🌐 Intersectional Analysis")
        fig = px.imshow(df.pivot_table(index='region', columns='sex', values='charges', aggfunc='mean'), title="Heatmap: Region x Sex")
        st.plotly_chart(fig)

else:
    st.info("Please upload a CSV file to begin.")
