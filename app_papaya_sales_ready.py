
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Papaya Global - Competitor Hiring Dashboard", layout="wide")
st.title("Competitor Hiring Insights – Papaya Sales Enablement Dashboard")

# Executive Summary (Papaya-focused)
st.markdown("""
Based on the analysis:
- **CXC Global** (APAC Sales + Tech hires): Building a tech hub in APAC — sell with strong integration & local engineering presence.
- **Deel** (Enterprise scale): Hiring globally in Sales, Payroll & R&D — counter with fast onboarding, compliance and deeper service.
- **Multiplier** (Cross-border compliance): Growing in LATAM with compliance-heavy roles — Papaya should highlight LATAM-specific tax, case studies, and ease of roll-out.
- **People 2.0** (Ops-stable): Focused on backend ops — Papaya wins with speed, analytics, and modern user experience.
- **Remote** (Support-first): Hiring in support/enablement — compete with SLAs, in-country teams, and premium onboarding.
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/clustered_jobs.csv")

df = load_data()

# Filters
st.sidebar.header("Filters")
competitor_filter = st.sidebar.multiselect("Select Competitors", options=df["competitor"].unique(), default=df["competitor"].unique())
department_filter = st.sidebar.multiselect("Select Departments", options=df["department"].unique(), default=df["department"].unique())
region_filter = st.sidebar.multiselect("Select Regions", options=df["region"].unique(), default=df["region"].unique())

filtered_df = df[
    (df["competitor"].isin(competitor_filter)) &
    (df["department"].isin(department_filter)) &
    (df["region"].isin(region_filter))
]

# Charts
st.header(" Which Competitors Are Growing Fast?")
vol_fig = px.bar(filtered_df.groupby("competitor")["count"].sum().reset_index(), x="competitor", y="count")
st.plotly_chart(vol_fig, use_container_width=True)

st.header(" What Roles Are They Prioritizing?")
dept_fig = px.bar(filtered_df.groupby("department")["count"].sum().reset_index(), x="department", y="count")
st.plotly_chart(dept_fig, use_container_width=True)

st.header(" Where Are They Expanding?")
heat_data = filtered_df.pivot_table(values="count", index="region", columns="department", aggfunc="sum", fill_value=0)
heatmap = go.Figure(data=go.Heatmap(z=heat_data.values, x=heat_data.columns, y=heat_data.index, colorscale="Viridis"))
heatmap.update_layout(xaxis_title="Department", yaxis_title="Region")
st.plotly_chart(heatmap, use_container_width=True)

st.header(" What Kind of Teams Are They Building?")
cluster_fig = px.bar(filtered_df.groupby(["competitor", "cluster_name"])["count"].sum().reset_index(),
                     x="competitor", y="count", color="cluster_name", barmode="group")
st.plotly_chart(cluster_fig, use_container_width=True)

# Sales Playbook with "If X then Y" logic
st.header(" Sales Playbook – How Papaya Can Win")

st.markdown("""
### Deel
- **What They're Doing**: Hiring 227 roles in Sales, Payroll, and R&D across regions.
- **Why It Matters**: They're aggressively targeting global enterprise accounts.
- **How Papaya Should Counter**:
  1. Pitch our faster onboarding timeline — we're ready in weeks, not months.
  2. Emphasize our local compliance team presence and trusted integrations.
  3. Offer our client support differentiator: response time + hands-on implementation.
  - *Example: If Deel is hiring more Sales & Payroll in EMEA, then Papaya should target CFOs in those regions with speed-to-value demos and tax automation highlights.*

---
### CXC Global
- **What They're Doing**: Hiring in Tech, Strategy, and Product across APAC.
- **Why It Matters**: They're building a delivery center and tech expansion play.
- **How Papaya Should Counter**:
  1. Lead with our plug-and-play integrations for APAC systems.
  2. Offer APAC case studies to show delivery confidence.
  3. Promise short roll-out cycles, API support, and real-time platform visibility.
  - *Example: If CXC is hiring APAC engineers and leaders, then Papaya should highlight how quickly we integrate into local ERPs and scale across countries.*

---
### Remote
- **What They're Doing**: Hiring in Support and Enablement roles globally.
- **Why It Matters**: They position themselves around customer service.
- **How Papaya Should Counter**:
  1. Share CX metrics: response time, resolution rate.
  2. Promote SLAs, onboarding surveys, and NPS benchmarks.
  3. Highlight our local support teams and multilingual capability.
  - *Example: If Remote is expanding their support team in EMEA, then Papaya should pitch our 24/7 multilingual helpdesk and proven onboarding playbooks.*

---
### Multiplier
- **What They're Doing**: Building compliance and payroll teams, especially in LATAM.
- **Why It Matters**: They're betting on compliance-first expansion in emerging markets.
- **How Papaya Should Counter**:
  1. Show automation in tax compliance & filings.
  2. Highlight LATAM onboarding success stories.
  3. Bundle services (payroll + HR + compliance) under one SLA.
  - *Example: If Multiplier is hiring for LATAM compliance, then Papaya should proactively offer region-specific ROI calculators and onboarding guarantees.*

---
### People 2.0
- **What They're Doing**: Light hiring focused on backend operations.
- **Why It Matters**: Mature, delivery-first model — not innovation led.
- **How Papaya Should Counter**:
  1. Show time-to-live advantage and visual dashboards.
  2. Talk about end-user adoption and platform simplicity.
  3. Push new feature roadmap, analytics, and integration power.
  - *Example: If People 2.0 is not investing in client experience, then Papaya should focus on platform design and quick wins that wow the end user.*
""")

# Footer
st.markdown("---")
st.markdown("Prepared by Atharva Badhe | Wavess.io | For Papaya Global – July 2025")
