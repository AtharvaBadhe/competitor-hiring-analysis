import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Coinme Enterprise Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_synthetic_data():
    """Generate comprehensive synthetic data for Coinme analysis"""
    
    # Date range
    start_date = datetime.now() - timedelta(days=730)  # 2 years of data
    dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
    
    # Generate synthetic Bitcoin prices with realistic volatility
    np.random.seed(42)
    initial_btc_price = 30000
    btc_returns = np.random.normal(0.001, 0.04, len(dates))  # Daily returns
    btc_prices = [initial_btc_price]
    
    for i in range(1, len(dates)):
        new_price = btc_prices[-1] * (1 + btc_returns[i])
        btc_prices.append(max(new_price, 15000))  # Floor price
    
    # Create main dataframe
    df = pd.DataFrame({
        'Date': dates,
        'BTC_Price': btc_prices
    })
    
    # Generate Coinme business metrics
    base_users = 50000
    user_growth = np.random.normal(0.02, 0.01, len(dates))  # Monthly growth rate
    df['Daily_Active_Users'] = np.maximum(
        base_users * np.cumprod(1 + user_growth/30),
        base_users * 0.8
    ).astype(int)
    
    # Transaction volume correlated with BTC price and user growth
    df['Transaction_Volume_USD'] = (
        df['Daily_Active_Users'] * 
        np.random.uniform(50, 200, len(dates)) * 
        (1 + (df['BTC_Price'] / df['BTC_Price'].iloc[0] - 1) * 0.3)
    )
    
    # Revenue metrics
    df['Revenue_USD'] = df['Transaction_Volume_USD'] * np.random.uniform(0.02, 0.05, len(dates))
    
    # Enterprise partnerships
    partnership_events = np.random.poisson(0.1, len(dates))  # Average 1 partnership per 10 days
    df['New_Partnerships'] = partnership_events
    df['Cumulative_Partnerships'] = df['New_Partnerships'].cumsum()
    
    # Regulatory compliance score
    df['Compliance_Score'] = np.random.uniform(85, 98, len(dates))
    
    # Market sentiment
    df['Market_Sentiment'] = np.random.choice(['Bullish', 'Neutral', 'Bearish'], 
                                            len(dates), p=[0.4, 0.4, 0.2])
    
    # Fundraising signals
    fundraising_events = []
    fundraising_dates = np.random.choice(dates, size=5, replace=False)
    
    for date in fundraising_dates:
        fundraising_events.append({
            'Date': date,
            'Round': np.random.choice(['Seed', 'Series A', 'Series B', 'Growth']),
            'Amount': np.random.randint(5, 50) * 1000000,  # $5M to $50M
            'Lead_Investor': np.random.choice([
                'Andreessen Horowitz', 'Coinbase Ventures', 'Pantera Capital',
                'Digital Currency Group', 'Blockchain Capital'
            ]),
            'Valuation': np.random.randint(100, 500) * 1000000
        })
    
    fundraising_df = pd.DataFrame(fundraising_events)
    
    return df, fundraising_df

@st.cache_data
def calculate_key_metrics(df):
    """Calculate key business metrics"""
    
    latest_data = df.tail(30)  # Last 30 days
    previous_data = df.tail(60).head(30)  # Previous 30 days
    
    metrics = {
        'Current_BTC_Price': df['BTC_Price'].iloc[-1],
        'BTC_Price_Change': (df['BTC_Price'].iloc[-1] / df['BTC_Price'].iloc[-30] - 1) * 100,
        'Daily_Active_Users': int(latest_data['Daily_Active_Users'].mean()),
        'User_Growth': ((latest_data['Daily_Active_Users'].mean() / 
                        previous_data['Daily_Active_Users'].mean() - 1) * 100),
        'Monthly_Revenue': latest_data['Revenue_USD'].sum(),
        'Revenue_Growth': ((latest_data['Revenue_USD'].sum() / 
                           previous_data['Revenue_USD'].sum() - 1) * 100),
        'Total_Partnerships': df['Cumulative_Partnerships'].iloc[-1],
        'Avg_Compliance_Score': latest_data['Compliance_Score'].mean(),
        'Total_Volume': latest_data['Transaction_Volume_USD'].sum()
    }
    
    return metrics

def create_btc_price_chart(df):
    """Create Bitcoin price chart with Coinme context"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['BTC_Price'],
        mode='lines',
        name='Bitcoin Price',
        line=dict(color='#f7931a', width=2),
        hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Bitcoin Price Trend - Market Context for Coinme',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_user_growth_chart(df):
    """Create user growth visualization"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Daily_Active_Users'],
        mode='lines',
        name='Daily Active Users',
        line=dict(color='#1f77b4', width=2),
        fill='tonexty',
        hovertemplate='<b>Date:</b> %{x}<br><b>Users:</b> %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Coinme User Growth Trajectory',
        xaxis_title='Date',
        yaxis_title='Daily Active Users',
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_revenue_chart(df):
    """Create revenue analysis chart"""
    
    # Monthly aggregation
    df_monthly = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Revenue_USD': 'sum',
        'Transaction_Volume_USD': 'sum'
    }).reset_index()
    df_monthly['Date'] = df_monthly['Date'].dt.to_timestamp()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_monthly['Date'],
        y=df_monthly['Revenue_USD'],
        name='Monthly Revenue',
        marker_color='#28a745',
        hovertemplate='<b>Month:</b> %{x}<br><b>Revenue:</b> $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Coinme Monthly Revenue Growth',
        xaxis_title='Month',
        yaxis_title='Revenue (USD)',
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_partnership_chart(df):
    """Create partnership growth chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Cumulative_Partnerships'],
        mode='lines+markers',
        name='Total Partnerships',
        line=dict(color='#17a2b8', width=3),
        marker=dict(size=6),
        hovertemplate='<b>Date:</b> %{x}<br><b>Partnerships:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Coinme Strategic Partnership Growth',
        xaxis_title='Date',
        yaxis_title='Cumulative Partnerships',
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_correlation_analysis(df):
    """Create correlation analysis between metrics"""
    
    # Calculate correlations
    correlation_data = df[['BTC_Price', 'Daily_Active_Users', 'Transaction_Volume_USD', 
                          'Revenue_USD', 'Compliance_Score']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.columns,
        colorscale='RdYlBu',
        zmid=0,
        text=correlation_data.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 12},
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Correlation Matrix: Key Business Metrics',
        height=500,
        width=600
    )
    
    return fig

def display_fundraising_timeline(fundraising_df):
    """Display fundraising timeline"""
    
    if len(fundraising_df) > 0:
        st.subheader("🎯 Fundraising Timeline")
        
        for _, round_data in fundraising_df.iterrows():
            with st.expander(f"{round_data['Round']} Round - ${round_data['Amount']:,.0f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Date:** {round_data['Date'].strftime('%B %d, %Y')}")
                    st.write(f"**Amount:** ${round_data['Amount']:,.0f}")
                
                with col2:
                    st.write(f"**Lead Investor:** {round_data['Lead_Investor']}")
                    st.write(f"**Valuation:** ${round_data['Valuation']:,.0f}")

def generate_insights(metrics, df):
    """Generate strategic insights"""
    
    insights = []
    
    # User growth insights
    if metrics['User_Growth'] > 10:
        insights.append("🚀 **Strong User Growth**: Coinme is experiencing exceptional user acquisition with growth exceeding 10% month-over-month.")
    elif metrics['User_Growth'] > 5:
        insights.append("📈 **Healthy User Growth**: Steady user base expansion indicates strong market traction.")
    else:
        insights.append("⚠️ **User Growth Opportunity**: Consider enhancing user acquisition strategies.")
    
    # Revenue insights
    if metrics['Revenue_Growth'] > 15:
        insights.append("💰 **Revenue Acceleration**: Outstanding revenue growth suggests strong business model execution.")
    elif metrics['Revenue_Growth'] > 5:
        insights.append("💵 **Steady Revenue Growth**: Consistent revenue expansion demonstrates business stability.")
    
    # Bitcoin correlation
    btc_change = metrics['BTC_Price_Change']
    if abs(btc_change) > 20:
        insights.append(f"🌊 **High Market Volatility**: Bitcoin price {'surge' if btc_change > 0 else 'decline'} of {abs(btc_change):.1f}% may impact user activity.")
    
    # Compliance insights
    if metrics['Avg_Compliance_Score'] > 95:
        insights.append("🛡️ **Excellent Compliance**: Outstanding regulatory compliance score positions Coinme well for institutional partnerships.")
    elif metrics['Avg_Compliance_Score'] > 90:
        insights.append("✅ **Strong Compliance**: Good regulatory standing supports business expansion opportunities.")
    
    # Partnership insights
    if metrics['Total_Partnerships'] > 20:
        insights.append("🤝 **Strategic Partnership Portfolio**: Extensive partnership network creates multiple revenue streams and market opportunities.")
    
    return insights

def generate_recommendations(metrics, df):
    """Generate strategic recommendations"""
    
    recommendations = []
    
    # Growth recommendations
    if metrics['User_Growth'] < 5:
        recommendations.append("🎯 **User Acquisition**: Implement referral programs and strategic marketing campaigns to accelerate user growth.")
    
    # Revenue optimization
    if metrics['Revenue_Growth'] < 10:
        recommendations.append("💡 **Revenue Optimization**: Explore premium service tiers and enhanced transaction fee structures.")
    
    # Market expansion
    recommendations.append("🌍 **Geographic Expansion**: Consider expanding to new markets with favorable regulatory environments.")
    
    # Technology investment
    recommendations.append("⚡ **Technology Innovation**: Invest in blockchain infrastructure and DeFi integrations to stay competitive.")
    
    # Partnership strategy
    if metrics['Total_Partnerships'] < 15:
        recommendations.append("🤝 **Partnership Development**: Pursue strategic alliances with traditional financial institutions.")
    
    # Risk management
    recommendations.append("🛡️ **Risk Mitigation**: Maintain strong compliance standards and diversify revenue streams.")
    
    return recommendations

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<div class="main-header">🚀 Coinme Enterprise Analytics Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()
    
    # Load data
    with st.spinner("Loading Coinme analytics data..."):
        df, fundraising_df = generate_synthetic_data()
        metrics = calculate_key_metrics(df)
    
    # Key metrics section
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Bitcoin Price",
            value=f"${metrics['Current_BTC_Price']:,.0f}",
            delta=f"{metrics['BTC_Price_Change']:+.1f}%"
        )
    
    with col2:
        st.metric(
            label="👥 Daily Active Users",
            value=f"{metrics['Daily_Active_Users']:,}",
            delta=f"{metrics['User_Growth']:+.1f}%"
        )
    
    with col3:
        st.metric(
            label="💵 Monthly Revenue",
            value=f"${metrics['Monthly_Revenue']:,.0f}",
            delta=f"{metrics['Revenue_Growth']:+.1f}%"
        )
    
    with col4:
        st.metric(
            label="🤝 Total Partnerships",
            value=f"{metrics['Total_Partnerships']:,}",
            delta="Active"
        )
    
    st.markdown("---")
    
    # Charts section
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Context", "👥 User Analytics", "💰 Revenue Analysis", "🤝 Partnerships"])
    
    with tab1:
        st.plotly_chart(create_btc_price_chart(df), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_correlation_analysis(df), use_container_width=True)
        
        with col2:
            # Market sentiment distribution
            sentiment_counts = df['Market_Sentiment'].value_counts()
            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Market Sentiment Distribution"
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with tab2:
        st.plotly_chart(create_user_growth_chart(df), use_container_width=True)
        
        # Additional user metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📱 Avg. Compliance Score", f"{metrics['Avg_Compliance_Score']:.1f}%")
        with col2:
            st.metric("📊 Total Volume", f"${metrics['Total_Volume']:,.0f}")
    
    with tab3:
        st.plotly_chart(create_revenue_chart(df), use_container_width=True)
        
        # Revenue insights
        revenue_per_user = metrics['Monthly_Revenue'] / metrics['Daily_Active_Users']
        st.metric("💰 Revenue per User", f"${revenue_per_user:.2f}")
    
    with tab4:
        st.plotly_chart(create_partnership_chart(df), use_container_width=True)
        display_fundraising_timeline(fundraising_df)
    
    st.markdown("---")
    
    # Insights and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Strategic Insights")
        insights = generate_insights(metrics, df)
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Strategic Recommendations")
        recommendations = generate_recommendations(metrics, df)
        for rec in recommendations:
            st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Dashboard Note**: This analysis uses synthetic data for demonstration purposes. All metrics and insights are generated for the Coinme fundraising case study.")

if __name__ == "__main__":
    main()
