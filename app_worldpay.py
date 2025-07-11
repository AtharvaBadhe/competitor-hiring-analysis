import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page configuration for professional look
st.set_page_config(page_title="Hiring Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("Hiring Intelligence Dashboard")
st.markdown("**Prepared by Wavess - Internal Use Only | Worldpay Co-Build Report**", unsafe_allow_html=True)

# Sidebar for company filter
st.sidebar.header("Filter by Company")
companies = ["All", "Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"]
selected_company = st.sidebar.selectbox("Select Company", companies)

# Executive Summary Section
st.markdown("### Executive Summary")
st.markdown("""
- Worldpay is scaling sales aggressively but underinvesting in GTM coordination and post-sale (Page 1).
- Competitors are either building GTM machines (Stripe, Checkout.com) or scaling (Page 1).
- Wavess enables signal-driven GTM, helping Worldpay align launches, prioritize features, and reduce go-to-market waste (Page 24).
""")

# Competitor Snapshot Table
st.markdown("### Competitor Snapshot")
data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Open Roles": [
        "121 Product, 42 Sales, 49 Marketing, 21 GTM Ops, 5 CS (Page 3)",
        "9 Product, 20 Sales, 8 Marketing, 1 GTM Ops (Page 4)",
        "Sales-dominated, exact count unclear (Page 8)",
        "7 Product, 44 Sales, 13 Marketing, 6 CS, 11 Finance (Page 5)",
        "7 Product, 4 Marketing, 23 Finance, Sales/GTM Ops unclear (Page 5)",
        "106 Sales, 7 GTM Ops, 9 CS (Page 6)"
    ],
    "GTM Focus": [
        "Sales strategy, pricing operations, EMEA GTM programs (Page 3)",
        "Undersupported, likely split across functions (Page 4)",
        "Unclear, sales-driven (Page 8)",
        "Shared across product/marketing, no dedicated GTM Ops (Page 5)",
        "Building sales enablement, pricing strategy (Page 5)",
        "Business enablement, no RevOps (Page 6)"
    ],
    "Product Focus": [
        "Terminal, Connect, Revenue Automation, Stripe Tax, Experimental Labs (Page 3)",
        "KYC, card payments, regulated products (Page 4)",
        "Reactive to sales/migration, legacy modernization (Page 8)",
        "UX, embedded finance, SMB tooling (Page 5)",
        "Replicating/optimizing proven payment models (Page 5)",
        "Internal extensions, not market-driven (Page 6)"
    ]
}
df = pd.DataFrame(data)
if selected_company != "All":
    df = df[df["Company"] == selected_company]
st.dataframe(df, use_container_width=True)

# Hiring Breakdown by Department (Bar Chart)
st.markdown("### Hiring Breakdown by Department")
hiring_data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Product": [121, 9, 0, 7, 7, 0],
    "Sales": [42, 20, 0, 44, 0, 106],
    "Marketing": [49, 8, 0, 13, 4, 0],
    "GTM Ops": [21, 1, 0, 0, 0, 7],
    "Customer Success": [5, 0, 0, 6, 0, 9],
    "Finance": [0, 0, 0, 11, 23, 0]
}
hiring_df = pd.DataFrame(hiring_data)
if selected_company != "All":
    hiring_df = hiring_df[hiring_df["Company"] == selected_company]
fig_bar = px.bar(
    hiring_df,
    x="Company",
    y=["Product", "Sales", "Marketing", "GTM Ops", "Customer Success", "Finance"],
    title="Hiring Breakdown by Department (Source: Pages 3–6)",
    barmode="group",
    labels={"value": "Number of Roles", "variable": "Department"}
)
fig_bar.update_layout(showlegend=True, hovermode="x")
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("*Note: Zero values indicate no explicit role counts in the report. Fiserv and Checkout.com Sales/GTM Ops are unclear due to truncation (Pages 5, 8).*")

# Functional Impact Radar
st.markdown("### Functional Impact Radar")
# Scoring methodology: Based on report descriptions (Pages 3–8)
# Strong (e.g., Stripe GTM Ops) = 8–10, Moderate (e.g., Adyen Product) = 4–7, Weak/None (e.g., Worldpay Product) = 0–3
radar_data = {
    "Function": ["Product", "GTM Ops", "Customer Success", "Marketing", "Finance-Product"],
    "Stripe": [9, 10, 2, 7, 6],  # Page 3: Strong product/GTM, weak CS
    "Adyen": [5, 1, 3, 3, 0],   # Page 4: Moderate product, weak GTM/marketing, no finance
    "Fiserv": [3, 0, 8, 0, 1],  # Page 8: Weak product, strong CS, no GTM/marketing
    "Square": [6, 1, 3, 5, 3],  # Page 5: Moderate product/marketing, weak GTM/CS
    "Checkout": [4, 4, 2, 3, 6], # Page 5: Weak product, moderate GTM/finance
    "Worldpay": [0, 2, 3, 1, 0]  # Page 6: No product/marketing, weak GTM/CS, no finance
}
radar_df = pd.DataFrame(radar_data)
if selected_company != "All":
    radar_df = radar_df[["Function", selected_company]]
for company in radar_df.columns[1:]:
    if selected_company == "All" or selected_company == company:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_df[company],
            theta=radar_df["Function"],
            fill="toself",
            name=company
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title=f"{company} Functional Impact (Source: Pages 3–8)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
st.markdown("*Note: Scores derived from report descriptions (Strong: 8–10, Moderate: 4–7, Weak/None: 0–3).*")

# Strategic Insights Section (Accordion Format)
st.markdown("### Strategic Insights")
with st.expander("Stripe – Fast, but Fragmented"):
    st.markdown("""
    - **What They're Doing**: Scaling via Experimental Labs, 21 RevOps/GTM roles, and 42 regional sales roles (China, Europe) (Page 3). Product experimentation outpaces GTM alignment, risking fragmentation (Page 7).
    - **Why It Matters**: Worldpay lacks GTM feedback loops, risking misaligned feature launches (Page 7).
    - **How to Counter**: Build tighter GTM feedback loops using Wavess to integrate Product, Sales, CS, and Finance (Page 27).
    - **Example**: Use Wavess to time launches against Stripe’s product experiments for better market fit (Page 27).
    """)
with st.expander("Adyen – Trust/Compliance Moat"):
    st.markdown("""
    - **What They're Doing**: Focused on 9 compliance-based product roles and 20 sales/partnership roles in LATAM/EMEA, with only 1 GTM Ops role (Page 4). Growth is regulated and trust-driven (Page 8).
    - **Why It Matters**: Worldpay lacks KYC/AML hires and regulated vertical plays, limiting high-barrier market entry (Page 13).
    - **How to Counter**: Move faster in emerging markets with signal-led GTM campaigns; focus on B2B SaaS or fintech APIs where Adyen is absent (Page 28).
    - **Example**: Use Wavess to track Adyen’s regional hiring and preempt market entry (Page 28).
    """)
with st.expander("Fiserv – Onboarding Heavy, but Slow"):
    st.markdown("""
    - **What They're Doing**: Dominated by sales and onboarding teams, with product reacting to legacy modernization (Page 8). Lacks RevOps and product agility (Page 33).
    - **Why It Matters**: Fiserv’s slow, bureaucratic approach creates openings for faster GTM execution (Page 33).
    - **How to Counter**: Offer modern onboarding and faster launch cycles to target accounts frustrated with Fiserv’s slowness (Page 33).
    - **Example**: Launch targeted campaigns highlighting Worldpay’s onboarding speed (Page 29).
    """)
with st.expander("Square – UX-led PLG, No RevOps"):
    st.markdown("""
    - **What They're Doing**: Focused on 7 UX/product roles, 44 sales roles (US, Japan), and 13 marketing roles, with no dedicated GTM Ops (Page 5). PLG-driven for SMBs (Page 14).
    - **Why It Matters**: Worldpay lacks design/PLG hires, missing lifecycle retention opportunities (Page 18).
    - **How to Counter**: Build structured onboarding and CS for mid-market/enterprise where Square’s self-serve model is weak (Page 32).
    - **Example**: Launch LinkedIn campaigns in regions where Square expands, highlighting onboarding expertise (Page 36).
    """)
with st.expander("Checkout.com – Building GTM Fast, Product Light"):
    st.markdown("""
    - **What They're Doing**: Hiring for sales enablement, pricing strategy, and 23 finance roles, with only 7 product roles (Page 5). Building GTM stack around stable products (Page 14).
    - **Why It Matters**: Worldpay can out-execute in regulated verticals where Checkout lacks compliance capabilities (Page 31).
    - **How to Counter**: Use Wavess for signal-led planning to build tighter Product-Sales-Finance loops (Page 31).
    - **Example**: Prioritize launches in AML or B2B fintech where Checkout is unprepared (Page 35).
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
if selected_company != "All":
    heatmap_df = heatmap_df[["GTM Area", selected_company]]
fig_heatmap = px.imshow(
    [[0 if x == "✅" else 1 for x in row] for row in heatmap_df.iloc[:, 1:].values],
    x=heatmap_df.columns[1:],
    y=heatmap_df["GTM Area"],
    color_continuous_scale="Reds",
    title="Worldpay Exposure Heatmap (Red = Gap, White = Strength, Source: Pages 15–20)"
)
fig_heatmap.update_layout(coloraxis_colorbar_title="Gap Level")
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("*Click on heatmap cells to review gaps. Worldpay gaps are highlighted in red (Pages 17–20).*")

# Wavess Opportunity Panel
st.markdown("### How Wavess Helps Worldpay")
st.markdown("""
- Prioritize smarter product launches based on market signals (Page 24).
- Expose GTM readiness gaps before they cost revenue (Page 36).
- Connect Finance, GTM, and Product for real-time decision making (Page 25).
- Run risk scoring on upcoming launches using hiring and competitor activity (Page 36).
""")
st.markdown("*Source: Pages 24–36*")import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page configuration for professional look
st.set_page_config(page_title="Hiring Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("Hiring Intelligence Dashboard")
st.markdown("**Prepared by Wavess - Internal Use Only | Worldpay Co-Build Report**", unsafe_allow_html=True)

# Sidebar for company filter
st.sidebar.header("Filter by Company")
companies = ["All", "Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"]
selected_company = st.sidebar.selectbox("Select Company", companies)

# Executive Summary Section
st.markdown("### Executive Summary")
st.markdown("""
- Worldpay is scaling sales aggressively but underinvesting in GTM coordination and post-sale (Page 1).
- Competitors are either building GTM machines (Stripe, Checkout.com) or scaling (Page 1).
- Wavess enables signal-driven GTM, helping Worldpay align launches, prioritize features, and reduce go-to-market waste (Page 24).
""")

# Competitor Snapshot Table
st.markdown("### Competitor Snapshot")
data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Open Roles": [
        "121 Product, 42 Sales, 49 Marketing, 21 GTM Ops, 5 CS (Page 3)",
        "9 Product, 20 Sales, 8 Marketing, 1 GTM Ops (Page 4)",
        "Sales-dominated, exact count unclear (Page 8)",
        "7 Product, 44 Sales, 13 Marketing, 6 CS, 11 Finance (Page 5)",
        "7 Product, 4 Marketing, 23 Finance, Sales/GTM Ops unclear (Page 5)",
        "106 Sales, 7 GTM Ops, 9 CS (Page 6)"
    ],
    "GTM Focus": [
        "Sales strategy, pricing operations, EMEA GTM programs (Page 3)",
        "Undersupported, likely split across functions (Page 4)",
        "Unclear, sales-driven (Page 8)",
        "Shared across product/marketing, no dedicated GTM Ops (Page 5)",
        "Building sales enablement, pricing strategy (Page 5)",
        "Business enablement, no RevOps (Page 6)"
    ],
    "Product Focus": [
        "Terminal, Connect, Revenue Automation, Stripe Tax, Experimental Labs (Page 3)",
        "KYC, card payments, regulated products (Page 4)",
        "Reactive to sales/migration, legacy modernization (Page 8)",
        "UX, embedded finance, SMB tooling (Page 5)",
        "Replicating/optimizing proven payment models (Page 5)",
        "Internal extensions, not market-driven (Page 6)"
    ]
}
df = pd.DataFrame(data)
if selected_company != "All":
    df = df[df["Company"] == selected_company]
st.dataframe(df, use_container_width=True)

# Hiring Breakdown by Department (Bar Chart)
st.markdown("### Hiring Breakdown by Department")
hiring_data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Product": [121, 9, 0, 7, 7, 0],
    "Sales": [42, 20, 0, 44, 0, 106],
    "Marketing": [49, 8, 0, 13, 4, 0],
    "GTM Ops": [21, 1, 0, 0, 0, 7],
    "Customer Success": [5, 0, 0, 6, 0, 9],
    "Finance": [0, 0, 0, 11, 23, 0]
}
hiring_df = pd.DataFrame(hiring_data)
if selected_company != "All":
    hiring_df = hiring_df[hiring_df["Company"] == selected_company]
fig_bar = px.bar(
    hiring_df,
    x="Company",
    y=["Product", "Sales", "Marketing", "GTM Ops", "Customer Success", "Finance"],
    title="Hiring Breakdown by Department (Source: Pages 3–6)",
    barmode="group",
    labels={"value": "Number of Roles", "variable": "Department"}
)
fig_bar.update_layout(showlegend=True, hovermode="x")
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("*Note: Zero values indicate no explicit role counts in the report. Fiserv and Checkout.com Sales/GTM Ops are unclear due to truncation (Pages 5, 8).*")

# Functional Impact Radar
st.markdown("### Functional Impact Radar")
# Scoring methodology: Based on report descriptions (Pages 3–8)
# Strong (e.g., Stripe GTM Ops) = 8–10, Moderate (e.g., Adyen Product) = 4–7, Weak/None (e.g., Worldpay Product) = 0–3
radar_data = {
    "Function": ["Product", "GTM Ops", "Customer Success", "Marketing", "Finance-Product"],
    "Stripe": [9, 10, 2, 7, 6],  # Page 3: Strong product/GTM, weak CS
    "Adyen": [5, 1, 3, 3, 0],   # Page 4: Moderate product, weak GTM/marketing, no finance
    "Fiserv": [3, 0, 8, 0, 1],  # Page 8: Weak product, strong CS, no GTM/marketing
    "Square": [6, 1, 3, 5, 3],  # Page 5: Moderate product/marketing, weak GTM/CS
    "Checkout": [4, 4, 2, 3, 6], # Page 5: Weak product, moderate GTM/finance
    "Worldpay": [0, 2, 3, 1, 0]  # Page 6: No product/marketing, weak GTM/CS, no finance
}
radar_df = pd.DataFrame(radar_data)
if selected_company != "All":
    radar_df = radar_df[["Function", selected_company]]
for company in radar_df.columns[1:]:
    if selected_company == "All" or selected_company == company:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_df[company],
            theta=radar_df["Function"],
            fill="toself",
            name=company
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title=f"{company} Functional Impact (Source: Pages 3–8)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
st.markdown("*Note: Scores derived from report descriptions (Strong: 8–10, Moderate: 4–7, Weak/None: 0–3).*")

# Strategic Insights Section (Accordion Format)
st.markdown("### Strategic Insights")
with st.expander("Stripe – Fast, but Fragmented"):
    st.markdown("""
    - **What They're Doing**: Scaling via Experimental Labs, 21 RevOps/GTM roles, and 42 regional sales roles (China, Europe) (Page 3). Product experimentation outpaces GTM alignment, risking fragmentation (Page 7).
    - **Why It Matters**: Worldpay lacks GTM feedback loops, risking misaligned feature launches (Page 7).
    - **How to Counter**: Build tighter GTM feedback loops using Wavess to integrate Product, Sales, CS, and Finance (Page 27).
    - **Example**: Use Wavess to time launches against Stripe’s product experiments for better market fit (Page 27).
    """)
with st.expander("Adyen – Trust/Compliance Moat"):
    st.markdown("""
    - **What They're Doing**: Focused on 9 compliance-based product roles and 20 sales/partnership roles in LATAM/EMEA, with only 1 GTM Ops role (Page 4). Growth is regulated and trust-driven (Page 8).
    - **Why It Matters**: Worldpay lacks KYC/AML hires and regulated vertical plays, limiting high-barrier market entry (Page 13).
    - **How to Counter**: Move faster in emerging markets with signal-led GTM campaigns; focus on B2B SaaS or fintech APIs where Adyen is absent (Page 28).
    - **Example**: Use Wavess to track Adyen’s regional hiring and preempt market entry (Page 28).
    """)
with st.expander("Fiserv – Onboarding Heavy, but Slow"):
    st.markdown("""
    - **What They're Doing**: Dominated by sales and onboarding teams, with product reacting to legacy modernization (Page 8). Lacks RevOps and product agility (Page 33).
    - **Why It Matters**: Fiserv’s slow, bureaucratic approach creates openings for faster GTM execution (Page 33).
    - **How to Counter**: Offer modern onboarding and faster launch cycles to target accounts frustrated with Fiserv’s slowness (Page 33).
    - **Example**: Launch targeted campaigns highlighting Worldpay’s onboarding speed (Page 29).
    """)
with st.expander("Square – UX-led PLG, No RevOps"):
    st.markdown("""
    - **What They're Doing**: Focused on 7 UX/product roles, 44 sales roles (US, Japan), and 13 marketing roles, with no dedicated GTM Ops (Page 5). PLG-driven for SMBs (Page 14).
    - **Why It Matters**: Worldpay lacks design/PLG hires, missing lifecycle retention opportunities (Page 18).
    - **How to Counter**: Build structured onboarding and CS for mid-market/enterprise where Square’s self-serve model is weak (Page 32).
    - **Example**: Launch LinkedIn campaigns in regions where Square expands, highlighting onboarding expertise (Page 36).
    """)
with st.expander("Checkout.com – Building GTM Fast, Product Light"):
    st.markdown("""
    - **What They're Doing**: Hiring for sales enablement, pricing strategy, and 23 finance roles, with only 7 product roles (Page 5). Building GTM stack around stable products (Page 14).
    - **Why It Matters**: Worldpay can out-execute in regulated verticals where Checkout lacks compliance capabilities (Page 31).
    - **How to Counter**: Use Wavess for signal-led planning to build tighter Product-Sales-Finance loops (Page 31).
    - **Example**: Prioritize launches in AML or B2B fintech where Checkout is unprepared (Page 35).
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
if selected_company != "All":
    heatmap_df = heatmap_df[["GTM Area", selected_company]]
fig_heatmap = px.imshow(
    [[0 if x == "✅" else 1 for x in row] for row in heatmap_df.iloc[:, 1:].values],
    x=heatmap_df.columns[1:],
    y=heatmap_df["GTM Area"],
    color_continuous_scale="Reds",
    title="Worldpay Exposure Heatmap (Red = Gap, White = Strength, Source: Pages 15–20)"
)
fig_heatmap.update_layout(coloraxis_colorbar_title="Gap Level")
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("*Click on heatmap cells to review gaps. Worldpay gaps are highlighted in red (Pages 17–20).*")

# Wavess Opportunity Panel
st.markdown("### How Wavess Helps Worldpay")
st.markdown("""
- Prioritize smarter product launches based on market signals (Page 24).
- Expose GTM readiness gaps before they cost revenue (Page 36).
- Connect Finance, GTM, and Product for real-time decision making (Page 25).
- Run risk scoring on upcoming launches using hiring and competitor activity (Page 36).
""")
st.markdown("*Source: Pages 24–36*")
