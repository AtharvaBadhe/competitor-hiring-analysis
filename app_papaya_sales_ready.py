
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Papaya Global - Competitor Hiring Dashboard", layout="wide")

# Title and executive summary
st.title("Competitor Hiring Insights – Papaya Sales Enablement Dashboard")

st.markdown("""
Based on the analysis:
- **CXC Global** (APAC Sales Growth, Platform Innovators): Focused hiring in APAC across technical and leadership roles suggests a regional tech hub strategy. Strengthen platform integrations, localized support, and engineering presence to stay competitive.
- **Deel** (Broad hiring across functions): Aggressive hiring in Sales, Marketing, and Payroll reflects global enterprise scaling. Counter with tailored onboarding flows, automation, and trust-focused compliance solutions.
- **Multiplier** (Compliance & Cross-border Operations): High emphasis on payroll and compliance roles indicates specialization in cross-border delivery. Enhance LATAM-specific features and promote unified platform experience to challenge them.
- **People 2.0** (Backend Ops Stability): Hiring patterns suggest operational maturity and backend stability. Differentiate with advanced automation, client analytics, and seamless integration options.
- **Remote** (Client Enablement & Global Support): Hiring signals a remote-first support and enablement model. Prioritize localized onboarding, integration flexibility, and support SLAs to compete in service quality.
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/clustered_jobs.csv")

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
- Deel’s high volume shows aggressive expansion across core functions—this gives them speed in enterprise sales cycles.
- CXC’s smaller count but technical APAC hiring is strategic and efficient—less noise, more precision.
- Remote and Multiplier show more focused plays in client support and compliance respectively.
- People 2.0 seems to focus on stable delivery, not expansion.

💡 **Sales Tip:** Where Deel scales fast, Papaya should pitch faster time-to-value. Against CXC, stress plug-and-play integrations.
"""")

# Section: Department Hiring
st.header("🏢 What Roles Are They Prioritizing?")
dept_fig = px.bar(
    filtered_df.groupby("department")["count"].sum().reset_index(),
    x="department", y="count",
    labels={"count": "Number of Roles", "department": "Department"},
    title="Department-wise Hiring Across Competitors"
)
st.plotly_chart(dept_fig, use_container_width=True)

# Section: Regional Heatmap
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

# Sales-focused competitor breakdown
st.header("🎯 Sales Playbook – Countering Each Competitor")

st.markdown("""
### Deel
- **What They’re Doing**: Hiring 227 roles—mostly Sales and Payroll—suggests they’re scaling globally with enterprise clients.
- **Why It Matters**: Deel will likely enter deals with promises of global coverage and massive reach.
- **How Papaya Can Win**: Stress our speed to onboard, ability to localize faster, and offer hands-on compliance partnership.

---
### CXC Global
- **What They’re Doing**: Focused hiring in APAC across tech and leadership signals a product-driven regional expansion.
- **Why It Matters**: Expect them to appear in APAC RFPs, especially where companies want technical ownership.
- **How Papaya Can Win**: Push integration ease, API flexibility, and full compliance visibility in APAC.

---
### Remote
- **What They’re Doing**: Focused hiring in Support and Sales—building client enablement and CX teams.
- **Why It Matters**: Expect them to promise strong onboarding and global service quality.
- **How Papaya Can Win**: Show superior SLA structure, in-country teams, and CX metrics.

---
### Multiplier
- **What They’re Doing**: Heavy hiring in compliance and payroll; targeting cross-border capabilities, especially in LATAM.
- **Why It Matters**: Expect them to dominate small enterprise deals in emerging markets.
- **How Papaya Can Win**: Emphasize automation in tax compliance, ease of scale, and Latin America case studies.

---
### People 2.0
- **What They’re Doing**: Backend-heavy roles and light hiring suggest delivery stability, not innovation.
- **Why It Matters**: Likely to appeal to clients needing reliability, not speed or integration.
- **How Papaya Can Win**: Differentiate with faster go-lives, customer analytics, and transparent platform maturity.
"""")

# Footer
st.markdown("---")
st.markdown("Prepared by Atharva Badhe | Wavess.io | For Papaya Global – July 2025")
