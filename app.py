import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings

# Suppress FutureWarning from Plotly
warnings.filterwarnings('ignore', category=FutureWarning)

# Set page config
st.set_page_config(page_title="Competitor Hiring Intelligence", layout="wide")

# Title
st.title("Competitor Hiring Intelligence Dashboard")

# Load data
@st.cache_data
def load_data():
    csv_path = "data\output\clustered_jobs.csv"
    keyword_path = "data\output\keyword_summary.csv"
    if not os.path.exists(csv_path) or not os.path.exists(keyword_path):
        st.error(f"Data files not found at {csv_path} or {keyword_path}. Ensure 'clustered_jobs.csv' and 'keyword_summary.csv' are in the 'data' directory.")
        return None, None
    df = pd.read_csv(csv_path)
    keyword_df = pd.read_csv(keyword_path)
    return df, keyword_df

df, keyword_df = load_data()

if df is not None and keyword_df is not None:
    # Executive summary
    st.header("Strategic Insights")
    st.markdown("""
    - **Deel**: Aggressively expanding with **227 roles**, focusing on **sales/marketing (72)** and **payroll (48)** in **EU, APAC, LATAM**.
    - **CXC Global**: **12 tech roles** in **APAC**, building a **digital transformation hub** (e.g., ServiceNow, MuleSoft).
    - **Remote**: **4 roles** in **EMEA/Global**, pushing **remote-first client acquisition**.
    - **Multiplier**: **4 roles** in **APAC/LATAM**, developing **embedded EOR solutions**.
    - **People 2.0**: Single **Payroll and Billing Specialist** in **EMEA (Germany)**, focusing on operational efficiency.
    - **Action**: Prioritize enterprise pitches against Deel; highlight compliance in LATAM against Multiplier.
    """)

    # Sidebar filters
    st.sidebar.header("Filters")
    competitor = st.sidebar.multiselect("Select Competitor", options=df['competitor'].unique(), default=df['competitor'].unique())
    department = st.sidebar.multiselect("Select Department", options=df['department'].unique(), default=df['department'].unique())
    region = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
    
    # Filter data
    filtered_df = df[df['competitor'].isin(competitor) & df['department'].isin(department) & df['region'].isin(region)]
    
    # Role counts by competitor
    st.header("Competitor Hiring Volume")
    role_counts = filtered_df.groupby('competitor')['count'].sum().reset_index()
    fig1 = px.bar(role_counts, x='count', y='competitor', title="Hiring by Competitor", color='competitor')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("**Business Insights**: Deel’s 227 roles signal intense enterprise competition; CXC’s APAC tech focus offers niche opportunities.")

    # Department distribution
    st.header("Department Distribution")
    dept_counts = filtered_df.groupby('department')['count'].sum().reset_index()
    fig2 = px.bar(dept_counts, x='count', y='department', title="Hiring by Department", color='department')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("**Business Insights**: High Sales/Payroll hiring (Deel) suggests market expansion; emphasize compliance in pitches.")

    # Heatmap
    st.header("Hiring by Region and Department")
    pivot = filtered_df.pivot_table(values='count', index='competitor', columns=['region', 'department'], aggfunc='sum', fill_value=0)
    fig3 = go.Figure(data=go.Heatmap(z=pivot.values, x=[f"{r}-{d}" for r, d in pivot.columns], y=pivot.index, colorscale='Blues'))
    fig3.update_layout(title="Hiring Volume by Competitor, Region, and Department")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("**Business Insights**: Deel’s Global Payroll/Sales focus requires enterprise-grade solutions; CXC’s APAC Tech hiring demands integration expertise.")

    # Top keywords
    st.header("Top Keywords by Competitor")
    fig4 = px.bar(keyword_df.melt(id_vars='competitor', var_name='keyword', value_name='tfidf_score'), 
                  x='competitor', y='tfidf_score', color='keyword', barmode='group')
    fig4.update_layout(title='Top Keywords by Competitor', xaxis_title='Competitor', yaxis_title='TF-IDF Score')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("**Business Insights**: Deel’s ‘compliance’ focus suggests EOR priority; Multiplier’s ‘EOR’ emphasis targets LATAM.")

    # Clusters
    st.header("Hiring Theme Clusters")
    cluster_counts = filtered_df.groupby(['competitor', 'cluster_name'])['count'].sum().reset_index()
    fig5 = px.bar(cluster_counts, x='competitor', y='count', color='cluster_name', title="Competitor Hiring Themes")
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("**Business Insights**: ‘Platform Innovators’ (Deel, Multiplier) focus on tech/EOR; compete with innovative features.")
else:
    st.error("Failed to load data. Please check the 'data' directory and ensure both CSV files are present.")
