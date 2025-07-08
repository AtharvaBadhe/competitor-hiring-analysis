
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Competitor Hiring Insights for Papaya Sales Team", layout="wide")

# Title and Introduction
st.title("Competitor Hiring Insights – Papaya Sales Enablement Dashboard")
st.markdown("""
This dashboard is designed for **Papaya's Sales Team** to understand competitor hiring signals and gain a clear strategic edge.

It answers key questions like:
- Who is hiring the most?
- What kinds of roles are they focusing on?
- Where are they expanding?
- What does it mean for our sales strategy?
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("clustered_jobs.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
competitors = st.sidebar.multiselect("Select Competitors", options=df["competitor"].unique(), default=df["competitor"].unique())
departments = st.sidebar.multiselect("Select Departments", options=df["department"].unique(), default=df["department"].unique())
regions = st.sidebar.multiselect("Select Regions", options=df["region"].unique(), default=df["region"].unique())

filtered_df = df[
    (df["competitor"].isin(competitors)) &
    (df["department"].isin(departments)) &
    (df["region"].isin(regions))
]

# Section: Hiring Volume
st.header("📈 Which Competitors Are Growing Fast?")
volume_fig = px.bar(
    filtered_df.groupby("competitor")["count"].sum().reset_index(),
    x="competitor", y="count",
    labels={"count": "Number of Roles", "competitor": "Competitor"},
    title="Total Roles Hired by Each Competitor"
)
st.plotly_chart(volume_fig, use_container_width=True)

st.markdown("""
- **Deel** is scaling aggressively with 227 roles globally – especially in Sales and Payroll.
- **CXC Global** is regionally focused, mostly hiring in APAC tech.
- **Remote** and **Multiplier** show more targeted, specialized hiring.
- **People 2.0** is stable, backend-heavy.

**💡 What Papaya Sales Should Do:** Focus on accounts where Deel is active and pitch faster deployment, localized compliance, and strong client service.
""")

# Section: Hiring by Department
st.header("🏢 What Roles Are They Prioritizing?")
dept_fig = px.bar(
    filtered_df.groupby("department")["count"].sum().reset_index(),
    x="department", y="count",
    labels={"count": "Number of Roles", "department": "Department"},
    title="Department-wise Hiring"
)
st.plotly_chart(dept_fig, use_container_width=True)

# Section: Region x Department Heatmap
st.header("🌍 Where Are They Expanding?")
heatmap_data = filtered_df.pivot_table(values='count', index='region', columns='department', aggfunc='sum', fill_value=0)
heatmap_fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index,
    colorscale='Viridis', showscale=True
))
heatmap_fig.update_layout(title="Hiring by Region and Department", xaxis_title="Department", yaxis_title="Region")
st.plotly_chart(heatmap_fig, use_container_width=True)

# Section: Role Clusters
st.header("🧠 What Kind of Teams Are They Building?")
cluster_fig = px.bar(
    filtered_df.groupby(["competitor", "cluster_name"])["count"].sum().reset_index(),
    x="competitor", y="count", color="cluster_name", barmode="group",
    title="Role Themes Across Competitors"
)
st.plotly_chart(cluster_fig, use_container_width=True)

# Section: Competitor-wise Sales Insights
st.header("🎯 Sales Playbook – How to Counter Competitors")
st.markdown("""
### Deel
- **What They're Doing**: Hiring across 227 roles globally, focusing on Payroll and Sales.
- **Why It Matters**: They're going after enterprise deals and scaling fast.
- **How Papaya Should Counter**: Emphasize onboarding speed, local compliance depth, and easy integrations.

---
### CXC Global
- **What They're Doing**: Hiring mainly in APAC for Tech and Strategy roles.
- **Why It Matters**: They're trying to build a delivery hub.
- **How Papaya Should Counter**: Pitch APAC-readiness, integrations, and shorter implementation cycles.

---
### Remote
- **What They're Doing**: Hiring in Support and Enablement roles.
- **Why It Matters**: They’re focused on CX and post-sale success.
- **How Papaya Should Counter**: Emphasize your customer success team and stronger in-country support.

---
### Multiplier
- **What They're Doing**: Targeting compliance and payroll in LATAM and SEA.
- **Why It Matters**: They’re positioning as compliance-first in emerging markets.
- **How Papaya Should Counter**: Highlight your tax automation, localized regulatory coverage, and partner ecosystem.

---
### People 2.0
- **What They're Doing**: Light hiring focused on backend operations.
- **Why It Matters**: They’re stable but slower moving.
- **How Papaya Should Counter**: Win with agility, integrations, and analytics dashboards.
""")

# Footer
st.markdown("---")
st.markdown("Prepared by Atharva Badhe | Wavess.io | For Papaya Global – July 2025")
