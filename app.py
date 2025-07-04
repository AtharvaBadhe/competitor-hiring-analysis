import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(page_title="Competitor Hiring Intelligence Dashboard", layout="wide")

# Title and introduction
st.title("Competitor Hiring Intelligence Dashboard")
st.markdown("""
This dashboard analyzes hiring strategies of five competitors (Deel, CXC Global, Remote, Multiplier, People 2.0) to inform sales and product strategies. It uses job data to identify role, department, and region priorities, extract key skills via NLP, cluster competitors by hiring themes, and visualize insights.
""")

# Load data
@st.cache_data
def load_data():
    try:
        clustered_jobs = pd.read_csv("data/clustered_jobs.csv")
        keyword_summary = pd.read_csv("data/keyword_summary.csv")
        return clustered_jobs, keyword_summary
    except FileNotFoundError as e:
        st.error(f"Error: Data file not found. Ensure 'data/clustered_jobs.csv' and 'keyword_summary.csv' exist. {e}")
        return None, None

clustered_jobs, keyword_summary = load_data()
if clustered_jobs is None or keyword_summary is None:
    st.stop()

# Executive Summary
st.header("Executive Summary")
st.markdown("""
- **Deel dominates hiring** with 227 roles (72 Sales/Marketing, 68 Payroll), signaling aggressive global expansion.
- **CXC Global** focuses on APAC tech roles (e.g., Digital Workplace Product Manager), emphasizing leadership and execution.
- **Multiplier** prioritizes compliance and payroll (keywords: payroll=0.31, compliance=0.287), targeting cross-border solutions.
- **People 2.0** emphasizes backend services (compliance=0.53, payroll=0.599), focusing on operational efficiency.
- **Remote** focuses on client enablement (compliance=0.58, support=0.121), integrating solutions for global clients.
- **Strategic Insight**: Prioritize compliance features in LATAM to counter Multiplier; enhance tech offerings to compete with CXC Global in APAC.
""")

# Sidebar filters
st.sidebar.header("Filters")
competitor_filter = st.sidebar.multiselect("Select Competitor", options=clustered_jobs['competitor'].unique(), default=clustered_jobs['competitor'].unique())
department_filter = st.sidebar.multiselect("Select Department", options=clustered_jobs['department'].unique(), default=clustered_jobs['department'].unique())
region_filter = st.sidebar.multiselect("Select Region", options=clustered_jobs['region'].unique(), default=clustered_jobs['region'].unique())

# Filter data
filtered_jobs = clustered_jobs[
    (clustered_jobs['competitor'].isin(competitor_filter)) &
    (clustered_jobs['department'].isin(department_filter)) &
    (clustered_jobs['region'].isin(region_filter))
]

# Visualizations
st.header("Hiring Trends")

# Competitor Hiring Volume
st.subheader("Hiring Volume by Competitor")
volume_fig = px.bar(
    filtered_jobs.groupby('competitor')['count'].sum().reset_index(),
    x='competitor', y='count', title="Hiring Volume by Competitor",
    labels={'count': 'Number of Roles', 'competitor': 'Competitor'}
)
volume_fig.update_layout(showlegend=False)
st.plotly_chart(volume_fig, use_container_width=True)

# Department Distribution
st.subheader("Hiring by Department")
dept_fig = px.bar(
    filtered_jobs.groupby('department')['count'].sum().reset_index(),
    x='department', y='count', title="Hiring by Department",
    labels={'count': 'Number of Roles', 'department': 'Department'}
)
dept_fig.update_layout(showlegend=False)
st.plotly_chart(dept_fig, use_container_width=True)

# Region vs Department Heatmap
st.subheader("Hiring by Region and Department")
heatmap_data = filtered_jobs.pivot_table(values='count', index='region', columns='department', aggfunc='sum', fill_value=0)
heatmap_fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index,
    colorscale='Viridis', showscale=True
))
heatmap_fig.update_layout(title="Hiring by Region and Department", xaxis_title="Department", yaxis_title="Region")
st.plotly_chart(heatmap_fig, use_container_width=True)

# Optional: Temporal Trend (if you have timestamp column in data)
# st.subheader("Hiring Over Time")
# time_fig = px.line(....)  # Add temporal plot here
# st.plotly_chart(time_fig, use_container_width=True)

# Keyword Analysis
st.header("Keyword Analysis")
st.subheader("Top Keywords by Competitor")
keyword_fig = px.bar(
    keyword_summary.melt(id_vars='competitor', var_name='keyword', value_name='tfidf_score'),
    x='competitor', y='tfidf_score', color='keyword', barmode='group',
    title="Top Keywords by Competitor", labels={'tfidf_score': 'TF-IDF Score', 'competitor': 'Competitor'}
)
keyword_fig.update_layout(legend_title="Keyword")
st.plotly_chart(keyword_fig, use_container_width=True)

# Keyword Table
st.subheader("Keyword Importance Table")
st.dataframe(keyword_summary.style.format("{:.3f}", subset=keyword_summary.columns[1:]))

# Cluster Analysis
st.header("Cluster Analysis")
st.subheader("Role Clusters by Competitor")
cluster_fig = px.bar(
    filtered_jobs.groupby(['cluster_name', 'competitor'])['count'].sum().reset_index(),
    x='competitor', y='count', color='cluster_name', barmode='group',
    title="Role Clusters by Competitor", labels={'count': 'Number of Roles', 'competitor': 'Competitor'}
)
cluster_fig.update_layout(legend_title="Cluster (Role Theme)")
st.plotly_chart(cluster_fig, use_container_width=True)

# Strategic Insights
st.header("Strategic Insights")
st.markdown("""
Based on the analysis:
- **CXC Global** (APAC Sales Growth, Platform Innovators): Focused hiring in APAC across technical and leadership roles suggests a regional tech hub strategy. Strengthen platform integrations, localized support, and engineering presence to stay competitive.
- **Deel** (Broad hiring across functions): Aggressive hiring in Sales, Marketing, and Payroll reflects global enterprise scaling. Counter with tailored onboarding flows, automation, and trust-focused compliance solutions.
- **Multiplier** (Compliance & Cross-border Operations): High emphasis on payroll and compliance roles indicates specialization in cross-border delivery. Enhance LATAM-specific features and promote unified platform experience to challenge them.
- **People 2.0** (Backend Ops Stability): Hiring patterns suggest operational maturity and backend stability. Differentiate with advanced automation, client analytics, and seamless integration options.
- **Remote** (Client Enablement & Global Support): Hiring signals a remote-first support and enablement model. Prioritize localized onboarding, integration flexibility, and support SLAs to compete in service quality.
""")


# Footer
st.markdown("---")
st.markdown("**Developed by Atharva Badhe** | Data sourced from `jobs_data.csv` | Generated on July 4, 2025")
