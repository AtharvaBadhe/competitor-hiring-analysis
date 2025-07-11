import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page config
st.set_page_config(page_title="Hiring Intelligence Dashboard", layout="wide")

# Title
st.title("Hiring Intelligence Dashboard")

# Executive Summary Section
st.markdown("""
### Executive Summary
- **Worldpay is scaling sales rapidly**, but **lacks GTM coordination**, product feedback loops, and finance insight.
- **Competitors (Stripe, Checkout.com)** are building GTM machines or regional depth (Adyen).
- **Wavess enables signal-driven GTM**, helping Worldpay align launches, prioritize features, and reduce go-to-market waste.
""")

# Competitor Snapshot Table
st.markdown("### Competitor Snapshot")
data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Open Roles": [660, 224, 439, 131, 120, 218],
    "GTM Focus": ["96 GTM roles", "1 GTM Ops", "GTM unclear", "GTM-lite", "GTM building", "Sales-heavy"],
    "Product Focus": ["Experimental ML, Tax, Terminal", "Compliance, LATAM/EMEA", "Sales/Implementation heavy", "Data science, design", "Growth PMs, data connectors", "No GTM/Product hiring"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Hiring Breakdown by Department (Bar Chart)
st.markdown("### Hiring Breakdown by Department")
hiring_data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Product": [121, 9, 0, 7, 7, 0],  # Extracted from report
    "Sales": [42, 20, 439, 44, 0, 106],  # Sales roles or implied from report
    "Marketing": [49, 8, 0, 13, 4, 0],  # Marketing roles or implied
    "GTM Ops": [21, 1, 0, 0, 0, 7],  # GTM Ops roles
    "Customer Success": [5, 0, 0, 6, 0, 9],  # CS roles or implied
    "Finance": [0, 0, 0, 11, 23, 0]  # Finance roles or implied
}
hiring_df = pd.DataFrame(hiring_data)
fig_bar = px.bar(hiring_df, x="Company", y=["Product", "Sales", "Marketing", "GTM Ops", "Customer Success", "Finance"],
                 title="Hiring Breakdown by Department",
                 barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)

# Functional Impact Radar
st.markdown("### Functional Impact Radar")
radar_data = {
    "Function": ["Product", "GTM Ops", "Customer Success", "Marketing", "Finance-Product"],
    "Stripe": [9, 10, 1, 7, 6],
    "Adyen": [5, 0, 2, 1, 0],
    "Fiserv": [3, 0, 9, 0, 1],
    "Square": [7, 1, 2, 4, 2],
    "Checkout": [3, 3, 2, 2, 4],
    "Worldpay": [2, 1, 2, 1, 0]
}
radar_df = pd.DataFrame(radar_data)
for company in radar_df.columns[1:]:
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_df[company],
        theta=radar_df["Function"],
        fill='toself',
        name=company
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title=f"{company} Functional Impact"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Strategic Insights Section (Accordion Format)
st.markdown("### Strategic Insights")
with st.expander("Stripe – Fast, but Fragmented"):
    st.markdown("""
    - **What They're Doing:** Fast launches via Experimental Labs, RevOps, and regional Sales hiring.
    - **Why It Matters:** Worldpay lacks GTM feedback loops — may ship misaligned features.
    - **How to Counter:** Build a RevOps-lite pod + Wavess risk scoring.
    - **Example:** If Stripe launches 3 new terminals, use Wavess to delay your next POS launch until GTM risk is reduced.
    """)
with st.expander("Adyen – Trust/Compliance Moat"):
    st.markdown("""
    - **What They're Doing:** Focused on compliance-based products and LATAM/EMEA expansion.
    - **Why It Matters:** Worldpay lacks KYC/AML hires and regulated vertical plays, limiting high-barrier market entry.
    - **How to Counter:** Move faster in emerging markets with predictive hiring and signal tracking.
    - **Example:** Target B2B SaaS or fintech APIs where Adyen's compliance focus is less relevant.
    """)
with st.expander("Fiserv – Onboarding Heavy, but Slow"):
    st.markdown("""
    - **What They're Doing:** Dominated by sales and onboarding, with minimal product innovation.
    - **Why It Matters:** Fiserv's slow, legacy-based approach creates openings for faster GTM execution.
    - **How to Counter:** Offer modern, streamlined onboarding and faster launch cycles.
    - **Example:** Target accounts frustrated with Fiserv's slow vendor onboarding with tailored campaigns.
    """)
with st.expander("Square – UX-led PLG, No RevOps"):
    st.markdown("""
    - **What They're Doing:** Heavy focus on design, UX, and data science for SMB/micro-merchant PLG.
    - **Why It Matters:** Worldpay lacks design or PLG hires, missing lifecycle retention opportunities.
    - **How to Counter:** Build structured onboarding and CS to win mid-market and regulated enterprise.
    - **Example:** Launch targeted LinkedIn campaigns in regions where Square expands, highlighting onboarding strength.
    """)
with st.expander("Checkout.com – Building GTM Fast, Product Light"):
    st.markdown("""
    - **What They're Doing:** Aggressive hiring in GTM Ops, commercial leads, and finance control with a lean product team.
    - **Why It Matters:** Worldpay can out-execute in regulated verticals where Checkout lacks compliance capabilities.
    - **How to Counter:** Use Wavess for signal-led planning to build tighter Product-Sales-Finance loops.
    - **Example:** Prioritize launches in AML or B2B fintech where Checkout is unprepared.
    """)

# Worldpay Exposure Heatmap
st.markdown("### Worldpay Exposure Heatmap")
heatmap_data = {
    "GTM Area": ["RevOps / GTM Ops", "Region-Specific Strategy", "Product Feedback Loops", "Finance Integration", "Onboarding / CS"],
    "Stripe": ["✅", "✅", "✅", "✅", "❌"],
    "Adyen": ["❌", "✅", "✅", "❌", "✅"],
    "Checkout": ["✅", "✅", "❌", "✅", "❌"],
    "Square": ["❌", "✅", "✅", "❌", "❌"],
    "Worldpay": ["❌", "❌", "❌", "❌", "❌"]
}
heatmap_df = pd.DataFrame(heatmap_data)
fig_heatmap = px.imshow(
    [[0 if x == "✅" else 1 if x == "❌" else 0.5 for x in row] for row in heatmap_df.iloc[:, 1:].values],
    x=heatmap_df.columns[1:],
    y=heatmap_df["GTM Area"],
    color_continuous_scale="RdYlGn_r",
    title="Worldpay Exposure Heatmap (Red = Gap, Green = Strength)"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Wavess Opportunity Panel
st.markdown("""
### How Wavess Helps Worldpay
- **Prioritize smarter product launches** based on market signals.
- **Expose GTM readiness gaps** before they cost revenue.
- **Connect Finance + GTM + Product** for real-time decision making.
- **Run risk scoring** on upcoming launches using hiring and competitor activity.
""")
