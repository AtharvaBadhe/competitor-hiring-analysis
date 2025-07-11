import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="GTM Hiring Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E4057;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2E4057;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E4057;
        margin: 1rem 0;
    }
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
    }
    .risk-medium {
        color: #F57C00;
        font-weight: bold;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">GTM Hiring Intelligence Dashboard</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Section",
    ["Executive Summary", "Competitor Overview", "Hiring Breakdown", "Strategic Gaps", "Competitive Threats", "Opportunities"]
)

# Data preparation
competitors_data = {
    'Company': ['Stripe', 'Adyen', 'Fiserv', 'Square', 'Checkout.com', 'Target Company'],
    'Open_Roles': [660, 224, 439, 131, 120, 218],
    'Revenue_B': [16.0, 2.3, 20.5, 21.0, 0.358, 4.9],
    'GTM_Focus': ['96 GTM roles', '1 GTM ops', 'GTM unclear', 'GTM-lite', 'GTM building', 'Sales-heavy'],
    'Product_Expansion': ['Experimental ML, Terminal, Tax, Finance', 'Compliance, LATAM/EMEA growth', 'Focus on implementation & sales', 'Data science, design-led UX hiring', 'Data connectivity, growth PMs', 'No product/GTM hiring depth']
}

threat_scores = {
    'Company': ['Stripe', 'Adyen', 'Fiserv', 'Square', 'Checkout.com'],
    'Speed_to_Launch': [9, 6, 3, 8, 8],
    'Market_Trust': [6, 10, 8, 8, 6],
    'GTM_Coordination': [9, 4, 5, 4, 7],
    'Post_Sale_Execution': [5, 9, 10, 6, 5],
    'Threat_Score': [9.0, 8.5, 6.5, 7.0, 7.5]
}

strategic_gaps = {
    'Strategic_Area': ['GTM Ops & Enablement', 'Product-Finance Sync', 'Region-Specific Scaling', 'Post-Sale Delivery', 'UX/Data-Led Growth', 'Compliance/Trust Product'],
    'Competitors_Doing': ['Stripe, Checkout building full GTM stacks', 'Stripe embeds finance into product; Checkout builds pricing ops', 'Adyen + Square hire by region and local language', 'Fiserv over-hires for onboarding, Square builds PLG systems', 'Square hiring in design, PLG, analytics', 'Adyen builds KYC, regulated infra'],
    'Target_Company_Doing': ['Almost none', 'No GTM-to-finance alignment', 'Target Company hires generic sales', 'Target Company has minimal CS/implementation', 'Target Company has no design, PLG, or insight hires', 'No visible hiring for regulated markets'],
    'Risk_Level': ['High', 'High', 'Medium', 'High', 'Medium', 'Medium']
}

# Executive Summary Page
if page == "Executive Summary":
    # CSS styling for the page
    st.markdown("""
    <style>
    .section-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 1px solid #e0e6ed;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .metric-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-box h3 {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    .metric-box p {
        color: #34495e;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
        text-align: justify;
    }
    
    .key-finding {
        border-left: 4px solid #e74c3c;
    }
    
    .competitive-landscape {
        border-left: 4px solid #f39c12;
    }
    
    .strategic-risk {
        border-left: 4px solid #e67e22;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    # Three columns layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-box key-finding">
            <h3> Key Finding</h3>
            <p>Target company is scaling sales aggressively but underinvesting in GTM coordination and post-sale infrastructure</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box competitive-landscape">
            <h3> Competitive Landscape</h3>
            <p>Competitors are building GTM machines (Stripe, Checkout.com) or scaling regional/trust-based growth (Adyen)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box strategic-risk">
            <h3> Strategic Risk</h3>
            <p>Target company risks inefficient launches, misaligned revenue planning, and lower retention</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown('<div class="section-header">Key Metrics Overview</div>', unsafe_allow_html=True)
    
    df_competitors = pd.DataFrame(competitors_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_roles = px.bar(df_competitors, x='Company', y='Open_Roles', 
                          title='Open Roles by Company',
                          color='Open_Roles',
                          color_continuous_scale='Blues')
        fig_roles.update_layout(showlegend=False)
        st.plotly_chart(fig_roles, use_container_width=True)
    
    with col2:
        fig_revenue = px.bar(df_competitors, x='Company', y='Revenue_B', 
                           title='Revenue (Billions USD) by Company',
                           color='Revenue_B',
                           color_continuous_scale='Greens')
        fig_revenue.update_layout(showlegend=False)
        st.plotly_chart(fig_revenue, use_container_width=True)

# Competitor Overview Page
elif page == "Competitor Overview":
    st.markdown('<div class="section-header">Competitor Hiring Overview</div>', unsafe_allow_html=True)
    
    df_competitors = pd.DataFrame(competitors_data)
    
    # Display comprehensive competitor table
    st.subheader("Comprehensive Competitor Analysis")
    
    # Create a formatted dataframe for display
    display_df = df_competitors.copy()
    display_df['Revenue (B)'] = display_df['Revenue_B'].apply(lambda x: f"${x}B")
    display_df = display_df[['Company', 'Open_Roles', 'Revenue (B)', 'GTM_Focus', 'Product_Expansion']]
    display_df.columns = ['Company', 'Open Roles', 'Revenue', 'GTM Focus', 'Product Expansion Signals']
    
    st.dataframe(display_df, use_container_width=True)
    
    # GTM Focus Analysis
    st.subheader("GTM Investment Analysis")
    
    gtm_analysis = {
        'Company': ['Stripe', 'Adyen', 'Fiserv', 'Square', 'Checkout.com', 'Target Company'],
        'GTM_Investment_Level': ['High', 'Very Low', 'Unclear', 'Low', 'Building', 'Sales-Heavy'],
        'GTM_Roles': [96, 1, 0, 0, 15, 7],
        'Strategic_Focus': ['Experimental expansion', 'Regional compliance', 'Enterprise implementation', 'Design-led UX', 'Data connectivity', 'No depth']
    }
    
    df_gtm = pd.DataFrame(gtm_analysis)
    
    fig_gtm = px.bar(df_gtm, x='Company', y='GTM_Roles', 
                     title='GTM Roles by Company',
                     color='GTM_Investment_Level',
                     color_discrete_map={
                         'High': '#2E4057',
                         'Very Low': '#D32F2F',
                         'Unclear': '#F57C00',
                         'Low': '#FF5722',
                         'Building': '#388E3C',
                         'Sales-Heavy': '#1976D2'
                     })
    
    st.plotly_chart(fig_gtm, use_container_width=True)

# Hiring Breakdown Page
elif page == "Hiring Breakdown":
    st.markdown('<div class="section-header">Strategic Hiring Breakdown</div>', unsafe_allow_html=True)
    
    # Company selection
    company_details = {
        'Stripe': {
            'Product': 121,
            'Sales': 42,
            'Marketing': 49,
            'GTM Operations': 21,
            'Customer Success': 5,
            'Revenue/Finance': 15
        },
        'Adyen': {
            'Product': 9,
            'Sales': 20,
            'Marketing': 8,
            'GTM Operations': 1,
            'Customer Success': 0,
            'Revenue/Finance': 0
        },
        'Fiserv': {
            'Product': 34,
            'Sales': 147,
            'Marketing': 5,
            'GTM Operations': 0,
            'Customer Success': 184,
            'Revenue/Finance': 0
        },
        'Square': {
            'Product': 7,
            'Sales': 44,
            'Marketing': 13,
            'GTM Operations': 0,
            'Customer Success': 6,
            'Revenue/Finance': 11
        },
        'Checkout.com': {
            'Product': 7,
            'Sales': 35,
            'Marketing': 4,
            'GTM Operations': 8,
            'Customer Success': 0,
            'Revenue/Finance': 23
        },
        'Target Company': {
            'Product': 0,
            'Sales': 106,
            'Marketing': 2,
            'GTM Operations': 7,
            'Customer Success': 9,
            'Revenue/Finance': 0
        }
    }
    
    selected_company = st.selectbox("Select Company for Detailed Breakdown", list(company_details.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for selected company
        company_data = company_details[selected_company]
        fig_pie = px.pie(values=list(company_data.values()), names=list(company_data.keys()),
                        title=f"{selected_company} - Hiring Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart comparison
        departments = list(company_details['Stripe'].keys())
        companies = list(company_details.keys())
        
        dept_selected = st.selectbox("Select Department for Comparison", departments)
        
        dept_data = [company_details[company][dept_selected] for company in companies]
        
        fig_bar = px.bar(x=companies, y=dept_data,
                        title=f"{dept_selected} Roles Across Companies")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Strategic insights
    st.subheader("Strategic Insights")
    
    insights = {
        'Stripe': "Innovation at Scale, Fractured GTM - Building experimental products with strong GTM coordination",
        'Adyen': "Regionally Focused, Risk-Controlled Growth - Compliance-led roadmap with minimal GTM ops",
        'Fiserv': "Enterprise-Heavy, Implementation First - Sales-led GTM with massive implementation focus",
        'Square': "Design & Data-First, But Light on GTM Rigor - UX-focused with minimal GTM coordination",
        'Checkout.com': "Lean, Data-First GTM Builder - Building GTM structures from scratch",
        'Target Company': "Sales-First, Strategy-Later - Overindexed on sales without enablement infrastructure"
    }
    
    st.info(insights[selected_company])

# Strategic Gaps Page
elif page == "Strategic Gaps":
    st.markdown('<div class="section-header">Strategic Gaps Analysis</div>', unsafe_allow_html=True)
    
    df_gaps = pd.DataFrame(strategic_gaps)
    
    # Risk level distribution
    risk_counts = df_gaps['Risk_Level'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_risk = px.pie(values=risk_counts.values, names=risk_counts.index,
                         title="Risk Level Distribution",
                         color_discrete_map={'High': '#D32F2F', 'Medium': '#F57C00', 'Low': '#388E3C'})
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Risk level by area
        fig_bar_risk = px.bar(df_gaps, x='Strategic_Area', y=[1]*len(df_gaps),
                             color='Risk_Level',
                             title="Strategic Areas by Risk Level",
                             color_discrete_map={'High': '#D32F2F', 'Medium': '#F57C00', 'Low': '#388E3C'})
        fig_bar_risk.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar_risk, use_container_width=True)
    
    # Detailed gaps table
    st.subheader("Detailed Strategic Gaps")
    
    for idx, row in df_gaps.iterrows():
        with st.expander(f"{row['Strategic_Area']} - {row['Risk_Level']} Risk"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**What Competitors Are Doing:**")
                st.write(row['Competitors_Doing'])
            
            with col2:
                st.markdown("**What Target Company Is Doing:**")
                st.write(row['Target_Company_Doing'])
            
            # Risk level styling
            risk_class = f"risk-{row['Risk_Level'].lower()}"
            st.markdown(f'<p class="{risk_class}">Risk Level: {row["Risk_Level"]}</p>', unsafe_allow_html=True)

# Competitive Threats Page
elif page == "Competitive Threats":
    st.markdown('<div class="section-header">Competitive Threat Analysis</div>', unsafe_allow_html=True)
    
    df_threats = pd.DataFrame(threat_scores)
    
    # Threat score visualization
    fig_threat = px.bar(df_threats, x='Company', y='Threat_Score',
                       title="Overall Threat Score by Competitor",
                       color='Threat_Score',
                       color_continuous_scale='Reds')
    fig_threat.update_layout(showlegend=False)
    st.plotly_chart(fig_threat, use_container_width=True)
    
    # Radar chart for competitor capabilities
    st.subheader("Competitor Capabilities Radar")
    
    selected_competitors = st.multiselect(
        "Select Competitors to Compare",
        df_threats['Company'].tolist(),
        default=['Stripe', 'Adyen', 'Checkout.com']
    )
    
    if selected_competitors:
        fig_radar = go.Figure()
        
        categories = ['Speed_to_Launch', 'Market_Trust', 'GTM_Coordination', 'Post_Sale_Execution']
        
        for company in selected_competitors:
            company_data = df_threats[df_threats['Company'] == company].iloc[0]
            values = [company_data[cat] for cat in categories]
            values.append(values[0])  # Close the radar chart
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=company
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Competitor Capabilities Comparison"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Threat assessment summary
    st.subheader("Threat Assessment Summary")
    
    threat_summary = {
        'Stripe': "Threat = speed and sophistication. Will out-iterate without signal-based launch timing.",
        'Adyen': "Threat = trust and regulation. Will dominate regulated verticals without compliance-focused GTM.",
        'Checkout.com': "Threat = operational efficiency. Building exact GTM machine that target company lacks.",
        'Fiserv': "Less of a threat - slow to move, but strong at retaining once in.",
        'Square': "SMB overlap, PLG strength. Threat increases if they go upmarket."
    }
    
    for company, assessment in threat_summary.items():
        st.info(f"**{company}:** {assessment}")

# Opportunities Page
elif page == "Opportunities":
    st.markdown('<div class="section-header">Strategic Opportunities</div>', unsafe_allow_html=True)
    
    # Winnable rivals
    st.subheader("Most Winnable Rivals")
    
    winnable_data = {
        'Competitor': ['Checkout.com', 'Square', 'Fiserv', 'Adyen', 'Stripe'],
        'Chance_to_Win': ['Highest', 'High', 'Medium', 'Lower', 'Low'],
        'Reason': [
            'Still building GTM muscle; Target can out-execute and out-coordinate',
            'Weak in GTM systems and regulated verticals',
            'Legacy weakness, but strong retention',
            'Trust moat; hard to unseat in core markets',
            'Too fast and well-coordinated — not the fight to pick yet'
        ],
        'Win_Score': [9, 8, 6, 4, 2]
    }
    
    df_winnable = pd.DataFrame(winnable_data)
    
    fig_winnable = px.bar(df_winnable, x='Competitor', y='Win_Score',
                         title="Competitive Opportunity Score",
                         color='Win_Score',
                         color_continuous_scale='Greens')
    fig_winnable.update_layout(showlegend=False)
    st.plotly_chart(fig_winnable, use_container_width=True)
    
    # Detailed opportunities
    st.subheader("Detailed Opportunity Analysis")
    
    for idx, row in df_winnable.iterrows():
        with st.expander(f"{row['Competitor']} - {row['Chance_to_Win']} Opportunity"):
            st.write(f"**Winning Chance:** {row['Chance_to_Win']}")
            st.write(f"**Strategy:** {row['Reason']}")
    
    # Cross-market opportunities
    st.subheader("Cross-Market Opportunities")
    
    opportunities = [
        "Own the 'GTM Clarity' Position - Position as fintech with fewer, smarter launches",
        "Localize Fast Where Others Are Slow - Target key regions with weak competitor presence",
        "Create First Closed-Loop GTM-Finance-Product System - Bridge GTM and finance tracks",
        "Turn Competitor Hiring Into Strategic Action - Use hiring patterns for strategic advantage",
        "Build AI-Led Enablement - Outscale with infrastructure vs headcount"
    ]
    
    for i, opp in enumerate(opportunities, 1):
        st.success(f"**Opportunity {i}:** {opp}")
    
    # Immediate actions
    st.subheader("Immediate Strategic Actions")
    
    actions = [
        "Launch signal-led GTM play into 1 regulated vertical (AML, B2B fintech)",
        "Stand up 3-person GTM coordination pod (PMM, Enablement, RevOps-lite)",
        "Run pre-launch risk assessment on next 2-3 feature rollouts",
        "Deploy counter-positioning campaigns where Square expands regionally",
        "Integrate GTM failure tracking into Finance dashboard"
    ]
    
    for i, action in enumerate(actions, 1):
        st.info(f"**Action {i}:** {action}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        GTM Hiring Intelligence Dashboard | Strategic Analysis & Competitive Intelligence
    </div>
    """, 
    unsafe_allow_html=True
)
