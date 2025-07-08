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

# Load clustered role data
@st.cache_data
def load_data():
    return pd.read_csv("data/clustered_jobs.csv")

df = load_data()

# Tabs per competitor
competitor_tabs = ["All", "Deel", "CXC Global", "Remote", "Multiplier", "People 2.0"]
tab_objs = st.tabs(competitor_tabs)

for tab, name in zip(tab_objs, competitor_tabs):
    with tab:
        # Filter data
        filtered = df if name == "All" else df[df["competitor"] == name]
        st.subheader(f"📊 Insights for: {name}")

        # Hiring volume chart
        st.markdown("#### Hiring Volume")
        vol_fig = px.bar(
            filtered.groupby("competitor")["count"].sum().reset_index(),
            x="competitor", y="count"
        )
        st.plotly_chart(vol_fig, use_container_width=True)

        # Department distribution
        st.markdown("#### Hiring by Department")
        dept_fig = px.bar(
            filtered.groupby("department")["count"].sum().reset_index(),
            x="department", y="count"
        )
        st.plotly_chart(dept_fig, use_container_width=True)

        # Region & department heatmap
        st.markdown("#### Hiring by Region and Department")
        heat = filtered.pivot_table(values="count", index="region", columns="department", aggfunc="sum", fill_value=0)
        heatmap = go.Figure(data=go.Heatmap(z=heat.values, x=heat.columns, y=heat.index, colorscale="Viridis"))
        heatmap.update_layout(xaxis_title="Department", yaxis_title="Region")
        st.plotly_chart(heatmap, use_container_width=True)

        # Role cluster breakdown
        st.markdown("#### Role Clusters (Team Type)")
        clust_fig = px.bar(
            filtered.groupby("cluster_name")["count"].sum().reset_index(),
            x="cluster_name", y="count"
        )
        st.plotly_chart(clust_fig, use_container_width=True)

# Sales Battle Cards – Expanded with 2–3 actionable insights
st.header("🛡️ Sales Battle Cards – How Papaya Wins")

battle_data = pd.DataFrame({
    "Competitor": ["Deel", "CXC Global", "Remote", "Multiplier", "People 2.0"],
    "What They’re Doing": [
        "Global hiring in Sales, Payroll & R&D",
        "Tech & leadership hiring in APAC",
        "Hiring support & enablement teams",
        "Building compliance & payroll ops in LATAM",
        "Stable backend operations, light hiring"
    ],
    "Papaya Should Say…": [
        "1. We onboard 2× faster—ready in weeks not months.\n"
        "2. Our compliance stays local with SLAs and audits.\n"
        "3. Our customer support is global but personal.",

        "1. Our platform integrates with APAC-specific systems.\n"
        "2. We staff local engineers for faster customizations.\n"
        "3. Our rollout timeline is shorter with minimal touchpoints.",

        "1. We guarantee 24/7 in-country support.\n"
        "2. We focus on CX—live dashboards and ticket SLAs.\n"
        "3. We ease transitions with data mapping and tool connectors.",

        "1. Papaya automates tax changes in LATAM automatically.\n"
        "2. We offer case studies of LATAM implementations.\n"
        "3. Partner-ready for cross-border compliance scaling.",

        "1. Our platform rolls out faster and simpler.\n"
        "2. We provide analytics dashboards, not static reports.\n"
        "3. UX-focused — low training, high adoption."
    ],
    "Deal Threat": ["High", "Medium", "Medium", "Medium", "Low"]
})

st.dataframe(battle_data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Prepared by Atharva Badhe | Wavess.io | For Papaya Global – July 2025")
