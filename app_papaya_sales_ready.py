import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Papaya Global - Competitor Hiring Dashboard", layout="wide")
st.title("Competitor Hiring Insights – Papaya Sales Enablement Dashboard")

# Executive Summary
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
    return pd.read_csv("dat/clustered_jobs.csv")

df = load_data()
competitor_tabs = ["All", "Deel", "CXC Global", "Remote", "Multiplier", "People 2.0"]
tab_objs = st.tabs(competitor_tabs)

# Interactive tabs
for tab, name in zip(tab_objs, competitor_tabs):
    with tab:
        if name == "All":
            filtered_df = df.copy()
        else:
            filtered_df = df[df["competitor"] == name]

        st.subheader(f"📊 Insights for: {name}")

        # Hiring Volume
        st.markdown("#### Hiring Volume")
        fig1 = px.bar(filtered_df.groupby("competitor")["count"].sum().reset_index(),
                      x="competitor", y="count")
        st.plotly_chart(fig1, use_container_width=True)

        # Department Distribution
        st.markdown("#### Hiring by Department")
        dept_fig = px.bar(filtered_df.groupby("department")["count"].sum().reset_index(),
                          x="department", y="count")
        st.plotly_chart(dept_fig, use_container_width=True)

        # Region vs Department
        st.markdown("#### Hiring by Region and Department")
        heatmap_data = filtered_df.pivot_table(values='count', index='region', columns='department',
                                               aggfunc='sum', fill_value=0)
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis'
        ))
        heatmap_fig.update_layout(xaxis_title="Department", yaxis_title="Region")
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # Role Clusters
        st.markdown("#### Role Clusters")
        cluster_fig = px.bar(filtered_df.groupby("cluster_name")["count"].sum().reset_index(),
                             x="cluster_name", y="count")
        st.plotly_chart(cluster_fig, use_container_width=True)

# Final Sales Battle Cards
st.header("🛡️ Sales Battle Cards – Counter Strategy Snapshot")

battle_data = pd.DataFrame({
    "Competitor": ["Deel", "CXC Global", "Remote", "Multiplier", "People 2.0"],
    "What They’re Doing": [
        "Global hiring in Sales and Payroll",
        "Tech leadership hiring in APAC",
        "Support & Enablement roles",
        "Compliance and payroll in LATAM",
        "Stable ops, low innovation"
    ],
    "What Papaya Should Say": [
        "Stress faster onboarding and local compliance",
        "Highlight APAC integration speed and flexibility",
        "Offer stronger CX, support SLAs, and in-country teams",
        "Promote automation and LATAM tax capabilities",
        "Differentiate with speed, analytics, and UX"
    ],
    "Deal Threat": ["High", "Medium", "Medium", "Medium", "Low"]
})

st.dataframe(battle_data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Prepared by Atharva Badhe | Wavess.io | For Papaya Global – July 2025")
