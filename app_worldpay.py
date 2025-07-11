import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configure page
st.set_page_config(
    page_title="GTM Hiring Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        background: #ffebee;
        border-left: 4px solid #f44336;
    }
    .risk-medium {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .risk-low {
        background: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">GTM Hiring Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Strategic Analysis of Competitor Hiring Patterns & GTM Opportunities</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_competitor_data():
    """Load competitor hiring and financial data"""
    data = {
        'Company': ['Alpha Corp', 'Beta Ltd', 'Gamma Inc', 'Delta Co', 'Epsilon LLC', 'Target Corp'],
        'Open_Roles': [660, 224, 439, 131, 120, 218],
        'Revenue_B': [16.0, 2.3, 20.5, 21.0, 0.358, 4.9],
        'GTM_Roles': [96, 1, 0, 0, 15, 7],
        'Product_Roles': [121, 9, 34, 7, 7, 0],
        'Sales_Roles': [42, 20, 147, 44, 25, 106],
        'Marketing_Roles': [49, 8, 5, 13, 4, 3],
        'CS_Roles': [5, 0, 184, 6, 0, 9],
        'Revenue_Finance_Roles': [15, 0, 0, 11, 23, 0],
        'Threat_Score': [9.0, 8.5, 6.5, 7.0, 7.5, 0]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_strategic_gaps():
    """Load strategic gap analysis data"""
    gaps = {
        'Gap_Category': ['GTM Ops & Enablement', 'Product-Finance Sync', 'Region-Specific Scaling', 
                        'Post-Sale Delivery', 'UX/Data-Led Growth', 'Compliance/Trust Product'],
        'Competitor_Investment': ['High', 'High', 'Medium', 'High', 'Medium', 'Medium'],
        'Target_Investment': ['Almost none', 'No alignment', 'Generic approach', 'Minimal', 'None', 'No visible hiring'],
        'Risk_Level': ['High', 'High', 'Medium', 'High', 'Medium', 'Medium']
    }
    return pd.DataFrame(gaps)

# Load data
df_competitors = load_competitor_data()
df_gaps = load_strategic_gaps()

# Sidebar
st.sidebar.header("Dashboard Navigation")
view_option = st.sidebar.selectbox(
    "Select Analysis View",
    ["Executive Summary", "Competitor Analysis", "Strategic Gaps", "Threat Assessment", "Opportunities"]
)

# Main content based on selection
if view_option == "Executive Summary":
    st.header("📈 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Competitors Analyzed", "6", "")
    with col2:
        st.metric("Total Open Roles", f"{df_competitors['Open_Roles'].sum():,}", "")
    with col3:
        st.metric("Avg Threat Score", f"{df_competitors['Threat_Score'].mean():.1f}", "")
    with col4:
        st.metric("High Risk Gaps", "4", "")
    
    st.markdown("---")
    
    # Key insights
    st.subheader("🎯 Key Strategic Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Critical Findings:**
        - Target Corp is scaling sales aggressively but underinvesting in GTM coordination
        - Competitors are building GTM machines while Target Corp focuses on volume
        - Risk of inefficient launches and misaligned revenue planning
        - 4 high-risk strategic gaps identified
        """)
    
    with col2:
        st.markdown("""
        **Immediate Actions Needed:**
        - Build GTM coordination infrastructure
        - Implement signal-led launch strategy
        - Align Product, Sales, and Finance teams
        - Develop region-specific GTM capabilities
        """)
    
    # Revenue vs GTM Investment scatter plot
    st.subheader("💰 Revenue vs GTM Investment Analysis")
    
    fig = px.scatter(df_competitors, 
                    x='Revenue_B', 
                    y='GTM_Roles',
                    size='Open_Roles',
                    color='Threat_Score',
                    hover_data=['Company', 'Open_Roles'],
                    labels={'Revenue_B': 'Revenue (Billions USD)', 'GTM_Roles': 'GTM Roles'},
                    title="Revenue vs GTM Investment (Bubble size = Total Open Roles)")
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif view_option == "Competitor Analysis":
    st.header("🏢 Competitor Analysis")
    
    # Company selection
    selected_company = st.selectbox("Select Company for Detailed Analysis", df_competitors['Company'].tolist())
    
    company_data = df_competitors[df_competitors['Company'] == selected_company].iloc[0]
    
    # Company overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Open Roles", f"{company_data['Open_Roles']:,}")
    with col2:
        st.metric("Revenue (B)", f"${company_data['Revenue_B']:.1f}B")
    with col3:
        st.metric("Threat Score", f"{company_data['Threat_Score']:.1f}/10")
    
    # Role distribution
    st.subheader("📊 Role Distribution")
    
    role_data = {
        'Role_Type': ['Product', 'Sales', 'Marketing', 'GTM Ops', 'Customer Success', 'Revenue/Finance'],
        'Count': [company_data['Product_Roles'], company_data['Sales_Roles'], 
                 company_data['Marketing_Roles'], company_data['GTM_Roles'],
                 company_data['CS_Roles'], company_data['Revenue_Finance_Roles']]
    }
    
    fig = px.bar(role_data, x='Role_Type', y='Count', 
                title=f"Hiring Distribution - {selected_company}")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Competitive comparison
    st.subheader("🔍 Competitive Positioning")
    
    # Create comparison metrics
    comparison_data = df_competitors.copy()
    comparison_data['GTM_Efficiency'] = comparison_data['GTM_Roles'] / comparison_data['Open_Roles'] * 100
    comparison_data['Revenue_per_Role'] = comparison_data['Revenue_B'] / comparison_data['Open_Roles'] * 1000
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('GTM Efficiency (%)', 'Revenue per Role (M)', 'Total Hiring Volume', 'Threat Score'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # GTM Efficiency
    fig.add_trace(
        go.Bar(x=comparison_data['Company'], y=comparison_data['GTM_Efficiency'], 
               name='GTM Efficiency'),
        row=1, col=1
    )
    
    # Revenue per Role
    fig.add_trace(
        go.Bar(x=comparison_data['Company'], y=comparison_data['Revenue_per_Role'], 
               name='Revenue per Role'),
        row=1, col=2
    )
    
    # Total Roles
    fig.add_trace(
        go.Bar(x=comparison_data['Company'], y=comparison_data['Open_Roles'], 
               name='Total Roles'),
        row=2, col=1
    )
    
    # Threat Score
    fig.add_trace(
        go.Bar(x=comparison_data['Company'], y=comparison_data['Threat_Score'], 
               name='Threat Score'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif view_option == "Strategic Gaps":
    st.header("⚠️ Strategic Gap Analysis")
    
    # Risk level distribution
    risk_counts = df_gaps['Risk_Level'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, 
                    title="Risk Level Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Gap Summary")
        for risk in ['High', 'Medium', 'Low']:
            count = risk_counts.get(risk, 0)
            st.metric(f"{risk} Risk Gaps", count)
    
    # Detailed gap analysis
    st.subheader("🔍 Detailed Gap Analysis")
    
    # Create gap severity matrix
    gap_matrix = df_gaps.copy()
    gap_matrix['Risk_Score'] = gap_matrix['Risk_Level'].map({'High': 3, 'Medium': 2, 'Low': 1})
    
    fig = px.bar(gap_matrix, x='Gap_Category', y='Risk_Score', 
                color='Risk_Level',
                title="Strategic Gap Risk Assessment",
                labels={'Risk_Score': 'Risk Score (1-3)', 'Gap_Category': 'Strategic Area'})
    
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Gap details table
    st.subheader("📊 Gap Details")
    
    # Style the dataframe based on risk level
    def highlight_risk(row):
        if row['Risk_Level'] == 'High':
            return ['background-color: #ffebee'] * len(row)
        elif row['Risk_Level'] == 'Medium':
            return ['background-color: #fff3e0'] * len(row)
        else:
            return ['background-color: #e8f5e8'] * len(row)
    
    styled_df = df_gaps.style.apply(highlight_risk, axis=1)
    st.dataframe(styled_df, use_container_width=True)

elif view_option == "Threat Assessment":
    st.header("🚨 Competitive Threat Assessment")
    
    # Threat score visualization
    threat_data = df_competitors[df_competitors['Company'] != 'Target Corp'].copy()
    threat_data = threat_data.sort_values('Threat_Score', ascending=True)
    
    fig = px.bar(threat_data, x='Threat_Score', y='Company', 
                orientation='h',
                color='Threat_Score',
                title="Competitive Threat Ranking",
                labels={'Threat_Score': 'Threat Score (0-10)'})
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Threat matrix
    st.subheader("🎯 Threat Matrix Analysis")
    
    # Create threat categories
    threat_categories = {
        'Alpha Corp': {'Speed': 'Very High', 'Trust': 'Medium', 'GTM': 'Strong', 'Post-Sale': 'Lean'},
        'Beta Ltd': {'Speed': 'Moderate', 'Trust': 'Very High', 'GTM': 'Basic', 'Post-Sale': 'Strong'},
        'Gamma Inc': {'Speed': 'Slow', 'Trust': 'High', 'GTM': 'Legacy', 'Post-Sale': 'Very Strong'},
        'Delta Co': {'Speed': 'Fast', 'Trust': 'High (SMB)', 'GTM': 'Weak', 'Post-Sale': 'Self-serve'},
        'Epsilon LLC': {'Speed': 'Fast', 'Trust': 'Medium', 'GTM': 'Building', 'Post-Sale': 'Unproven'}
    }
    
    selected_threat = st.selectbox("Select Competitor for Threat Analysis", list(threat_categories.keys()))
    
    threat_profile = threat_categories[selected_threat]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🔍 {selected_threat} Threat Profile")
        for category, level in threat_profile.items():
            st.markdown(f"**{category}**: {level}")
    
    with col2:
        # Radar chart for threat dimensions
        categories = list(threat_profile.keys())
        values = [3 if 'Very High' in v else 2.5 if 'High' in v else 2 if 'Medium' in v else 1.5 if 'Moderate' in v else 1 for v in threat_profile.values()]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_threat
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 3]
                )),
            showlegend=True,
            title=f"{selected_threat} Capability Assessment"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Competitive positioning
    st.subheader("📊 Competitive Positioning Matrix")
    
    # Create positioning data
    positioning_data = {
        'Company': ['Alpha Corp', 'Beta Ltd', 'Gamma Inc', 'Delta Co', 'Epsilon LLC'],
        'Innovation_Speed': [9, 5, 3, 7, 6],
        'Market_Trust': [6, 9, 8, 7, 5],
        'GTM_Maturity': [8, 3, 4, 3, 6]
    }
    
    pos_df = pd.DataFrame(positioning_data)
    
    fig = px.scatter(pos_df, x='Innovation_Speed', y='Market_Trust', 
                    size='GTM_Maturity', color='Company',
                    title="Competitive Positioning: Innovation vs Trust",
                    labels={'Innovation_Speed': 'Innovation Speed', 'Market_Trust': 'Market Trust'})
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif view_option == "Opportunities":
    st.header("🎯 Strategic Opportunities")
    
    # Opportunity matrix
    opportunities = {
        'Opportunity': ['GTM Clarity Position', 'Regional Localization', 'Closed-Loop GTM System', 
                       'Competitive Intelligence', 'AI-Led Enablement'],
        'Impact': [9, 7, 8, 6, 7],
        'Effort': [6, 8, 9, 4, 7],
        'Timeline': ['3-6 months', '6-12 months', '9-18 months', '1-3 months', '6-12 months']
    }
    
    opp_df = pd.DataFrame(opportunities)
    opp_df['Impact_Effort_Ratio'] = opp_df['Impact'] / opp_df['Effort']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(opp_df, x='Effort', y='Impact', 
                        size='Impact_Effort_Ratio',
                        color='Timeline',
                        hover_data=['Opportunity'],
                        title="Opportunity Impact vs Effort Matrix")
        
        # Add quadrant lines
        fig.add_hline(y=7, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=7, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top Opportunities")
        
        # Sort by impact/effort ratio
        top_opps = opp_df.sort_values('Impact_Effort_Ratio', ascending=False)
        
        for i, (_, row) in enumerate(top_opps.iterrows()):
            st.markdown(f"""
            **{i+1}. {row['Opportunity']}**
            - Impact: {row['Impact']}/10
            - Effort: {row['Effort']}/10
            - Timeline: {row['Timeline']}
            - Ratio: {row['Impact_Effort_Ratio']:.2f}
            """)
    
    # Actionable recommendations
    st.subheader("📋 Immediate Action Items")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Quick Wins (1-3 months):**
        1. Implement competitive intelligence tracking
        2. Set up GTM coordination pod (3 people)
        3. Launch signal-led GTM risk assessment
        4. Begin competitor movement monitoring
        """)
    
    with col2:
        st.markdown("""
        **Strategic Initiatives (6-18 months):**
        1. Build closed-loop GTM-Finance system
        2. Develop regional GTM capabilities
        3. Create AI-led enablement workflows
        4. Establish GTM clarity market position
        """)
    
    # Investment recommendations
    st.subheader("💰 Investment Recommendations")
    
    investment_data = {
        'Investment_Area': ['GTM Operations', 'Product Marketing', 'Revenue Operations', 
                           'Regional Expansion', 'Technology Infrastructure'],
        'Priority': ['High', 'High', 'Medium', 'Medium', 'Low'],
        'Investment_Range': ['$200K-400K', '$150K-300K', '$100K-200K', '$300K-500K', '$100K-300K']
    }
    
    inv_df = pd.DataFrame(investment_data)
    
    # Style investment table
    def highlight_priority(row):
        if row['Priority'] == 'High':
            return ['background-color: #ffebee'] * len(row)
        elif row['Priority'] == 'Medium':
            return ['background-color: #fff3e0'] * len(row)
        else:
            return ['background-color: #e8f5e8'] * len(row)
    
    styled_inv = inv_df.style.apply(highlight_priority, axis=1)
    st.dataframe(styled_inv, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Dashboard created for strategic GTM analysis and competitive intelligence**")
st.markdown("*Data sources: Competitor hiring analysis, market intelligence, strategic gap assessment*")
