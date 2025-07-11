import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page configuration for professional presentation
st.set_page_config(page_title="Hiring Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title and subtitle
st.title("Hiring Intelligence Dashboard")
st.markdown("<p style='font-size:18px; color:#666666;'><i>Prepared by Wavess for Worldpay</i></p>", unsafe_allow_html=True)

# Sidebar for company filter
st.sidebar.header("Filter by Company")
companies = ["All", "Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"]
selected_company = st.sidebar.selectbox("Select Company", companies)

# Executive Summary
st.header("Executive Summary")
st.markdown("""
- Worldpay is scaling sales aggressively but underinvesting in go-to-market coordination and post-sale operations.
- Competitors are building go-to-market machines (Stripe, Checkout.com) or focusing on regional depth (Adyen).
- Wavess enables signal-driven go-to-market strategies, aligning launches, prioritizing features, and reducing inefficiencies.
""")

# Competitor Snapshot
st.header("Competitor Snapshot")
data = {
    "Company": ["Stripe", "Adyen", "Fiserv", "Square", "Checkout.com", "Worldpay"],
    "Open Roles": [
        "121 Product, 42 Sales, 49 Marketing, 21 GTM Ops, 5 Customer Success",
        "9 Product, 20 Sales, 8 Marketing, 1 GTM Ops",
        "Sales-dominated, count not specified",
        "7 Product, 44 Sales, 13 Marketing, 6 Customer Success, 11 Finance",
        "7 Product, 4 Marketing, 23 Finance, Sales/GTM Ops not specified",
        "106 Sales, 7 GTM Ops, 9 Customer Success"
    ],
    "GTM Focus": [
        "Sales strategy, pricing operations, EMEA programs",
        "Undersupported, split across functions",
        "Sales-driven, structure unclear",
        "Shared across product and marketing, no dedicated GTM Ops",
        "Building sales enablement and pricing strategy",
        "Business enablement, no Revenue Operations"
    ],
    "Product Focus": [
        "Terminal, Connect, Revenue Automation, Stripe Tax, Experimental Labs",
        "KYC, card payments, regulated products",
        "Reactive to sales and legacy modernization",
        "UX, embedded finance, SMB tooling",
        "Replicating and optimizing proven payment models",
        "Internal extensions, not market-driven"
    ]
}
df = pd.DataFrame(data)
if selected_company != "All":
    df = df[df["Company"] == selected_company]
st.dataframe(df, use_container_width=True)

# Hiring Breakdown by Department
st.header("Hiring Breakdown by Department")
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
    title="Hiring by Department",
    barmode="group",
    labels={"value": "Number of Open Roles", "variable": "Department"},
    color_discrete_sequence=px.colors.qualitative.T10
)
fig_bar.update_layout(
    showlegend=True,
    hovermode="x",
    title_x=0.5,
    font=dict(size=12),
    plot_bgcolor="white",
    paper_bgcolor="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Functional Impact Radar
st.header("Functional Impact")
radar_data = {
    "Function": ["Product", "GTM Ops", "Customer Success", "Marketing", "Finance-Product"],
    "Stripe": [9, 10, 2, 7, 6],  # Strong product/GTM, weak CS, moderate finance-product
    "Adyen": [5, 1, 3, 3, 0],   # Moderate product, weak GTM/marketing, no finance-product
    "Fiserv": [3, 0, 8, 0, 1],  # Weak product, strong CS, no GTM/marketing, minimal finance
    "Square": [6, 1, 3, 5, 3],  # Moderate product/marketing, weak GTM/CS, low finance
    "Checkout": [4, 4, 2, 3, 6], # Weak product, moderate GTM/finance, low CS/marketing
    "Worldpay": [0, 2, 3, 1, 0]  # No product/marketing, weak GTM/CS, no finance-product
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
            name=company,
            line=dict(color="#636EFA")
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title=f"{company} Functional Impact",
            title_x=0.5,
            font=dict(size=12),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# Strategic Insights
st.header("Strategic Insights")
with st.expander("Stripe: Rapid Scaling with Fragmentation Risks"):
    st.markdown("""
    - **Strategy**: Scaling through Experimental Labs, 21 Revenue Operations/GTM roles, and 42 regional sales roles (China, Europe). Product experimentation outpaces go-to-market alignment, risking fragmentation.
    - **Implications for Worldpay**: Lack of go-to-market feedback loops risks misaligned feature launches.
    - **Actionable Steps**: Build tighter feedback loops using Wavess to integrate Product, Sales, Customer Success, and Finance. Time launches against Stripe’s product experiments for better market fit.
    """)
with st.expander("Adyen: Trust and Compliance-Driven Growth"):
    st.markdown("""
    - **Strategy**: Focused on 9 compliance-based product roles and 20 sales/partnership roles in LATAM/EMEA, with minimal GTM Operations support. Growth emphasizes regulated, trust-driven markets.
    - **Implications for Worldpay**: Limited KYC/AML hiring and regulated vertical expertise restrict high-barrier market entry.
    - **Actionable Steps**: Accelerate emerging market presence with signal-driven go-to-market campaigns. Target B2B SaaS or fintech APIs where Adyen is absent, using Wavess to track regional hiring.
    """)
with st.expander("Fiserv: Sales and Onboarding Focus, Limited Agility"):
    st.markdown("""
    - **Strategy**: Dominated by sales and onboarding teams, with product development reacting to legacy modernization needs. Lacks Revenue Operations and product agility.
    - **Implications for Worldpay**: Fiserv’s slow, bureaucratic approach creates opportunities for faster go-to-market execution.
    - **Actionable Steps**: Offer modern onboarding and accelerated launch cycles to capture accounts frustrated with Fiserv’s delays. Launch campaigns highlighting Worldpay’s onboarding efficiency.
    """)
with st.expander("Square: UX-Driven Product-Led Growth"):
    st.markdown("""
    - **Strategy**: Focused on 7 UX/product roles, 44 sales roles (US, Japan), and 13 marketing roles, with no dedicated GTM Operations. Emphasizes product-led growth for SMBs.
    - **Implications for Worldpay**: Lack of design and product-led growth hiring limits lifecycle retention opportunities.
    - **Actionable Steps**: Develop structured onboarding and Customer Success for mid-market and enterprise segments where Square’s self-serve model is weak. Launch targeted LinkedIn campaigns in Square’s expansion regions.
    """)
with st.expander("Checkout.com: Building GTM with Lean Product"):
    st.markdown("""
    - **Strategy**: Hiring for sales enablement, pricing strategy, and 23 finance roles, with only 7 product roles. Building go-to-market stack around stable products.
    - **Implications for Worldpay**: Opportunities to out-execute in regulated verticals where Checkout lacks compliance capabilities.
    - **Actionable Steps**: Use Wavess for signal-driven planning to strengthen Product-Sales-Finance alignment. Prioritize launches in AML or B2B fintech where Checkout is unprepared.
    """)

# Worldpay Exposure Heatmap
st.header("Worldpay Exposure Heatmap")
heatmap_data = {
    "GTM Area": ["Revenue Operations", "Regional Strategy", "Product Feedback", "Finance Integration", "Onboarding & Customer Success"],
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
    title="Worldpay Go-to-Market Gaps",
    labels={"color": "Gap Level"}
)
fig_heatmap.update_layout(
    coloraxis_colorbar_title="Gap Level",
    title_x=0.5,
    font=dict(size=12),
    plot_bgcolor="white",
    paper_bgcolor="white"
)
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("Red indicates gaps; white indicates strengths. Click cells to explore gaps.")

# Wavess Opportunity
st.header("Wavess Opportunity for Worldpay")
st.markdown("""
- Prioritize product launches using market signals.
- Identify go-to-market readiness gaps to protect revenue.
- Integrate Finance, GTM, and Product for real-time decisions.
- Assess launch risks using competitor and hiring data.
""")
