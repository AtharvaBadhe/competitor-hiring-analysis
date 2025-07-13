import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# --- Manual User Name Input Authentication ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.title("Coinme Enterprise Analytics Dashboard 🚀")

if not st.session_state.user_name:
    st.subheader("Please enter your name to access the dashboard:")
    user_name = st.text_input("Name:", "")
    if user_name:
        st.session_state.user_name = user_name
        st.success(f"Welcome, {user_name}!")
        st.experimental_rerun()
    else:
        st.stop()
else:
    st.success(f"Welcome, {st.session_state.user_name}!")

# --- Set page config ---
st.set_page_config(
    page_title="Coinme Enterprise Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def generate_synthetic_data():
    start_date = datetime.now() - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
    np.random.seed(42)
    initial_btc_price = 30000
    btc_returns = np.random.normal(0.001, 0.04, len(dates))
    btc_prices = [initial_btc_price]
    for i in range(1, len(dates)):
        new_price = btc_prices[-1] * (1 + btc_returns[i])
        btc_prices.append(max(new_price, 15000))
    df = pd.DataFrame({
        'Date': dates,
        'BTC_Price': btc_prices
    })
    base_users = 50000
    user_growth = np.random.normal(0.02, 0.01, len(dates))
    df['Daily_Active_Users'] = np.maximum(
        base_users * np.cumprod(1 + user_growth/30),
        base_users * 0.8
    ).astype(int)
    df['Transaction_Volume_USD'] = (
        df['Daily_Active_Users'] *
        np.random.uniform(50, 200, len(dates)) *
        (1 + (df['BTC_Price'] / df['BTC_Price'].iloc[0] - 1) * 0.3)
    )
    df['Revenue_USD'] = df['Transaction_Volume_USD'] * np.random.uniform(0.02, 0.05, len(dates))
    partnership_events = np.random.poisson(0.1, len(dates))
    df['New_Partnerships'] = partnership_events
    df['Cumulative_Partnerships'] = df['New_Partnerships'].cumsum()
    df['Compliance_Score'] = np.random.uniform(85, 98, len(dates))
    df['Market_Sentiment'] = np.random.choice(['Bullish', 'Neutral', 'Bearish'],
                                              len(dates), p=[0.4, 0.4, 0.2])
    fundraising_events = []
    fundraising_dates = np.random.choice(dates, size=5, replace=False)
    for date in fundraising_dates:
        fundraising_events.append({
            'Date': date,
            'Round': np.random.choice(['Seed', 'Series A', 'Series B', 'Growth']),
            'Amount': np.random.randint(5, 50) * 1000000,
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
    latest_data = df.tail(30)
    previous_data = df.tail(60).head(30)
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
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['BTC_Price'],
        mode='lines',
        name='Bitcoin Price',
        line=dict(color='#f7931a', width=2),
        hovertemplate='Date: %{x}<br>Price: $%{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(
        title='Bitcoin Price Over Time',
        xaxis_title='Date',
        yaxis_title='BTC Price (USD)',
        template='plotly_white',
        height=400
    )
    return fig

df, fundraising_df = generate_synthetic_data()
metrics = calculate_key_metrics(df)

st.subheader("Key Metrics (Last 30 Days)")
st.markdown(
    f"""
    - **Current BTC Price:** ${metrics['Current_BTC_Price']:,.0f}
    - **BTC Price Change:** {metrics['BTC_Price_Change']:.2f}%
    - **Daily Active Users:** {metrics['Daily_Active_Users']}
    - **User Growth:** {metrics['User_Growth']:.2f}%
    - **Monthly Revenue:** ${metrics['Monthly_Revenue']:,.0f}
    - **Revenue Growth:** {metrics['Revenue_Growth']:.2f}%
    - **Total Partnerships:** {metrics['Total_Partnerships']}
    - **Avg. Compliance Score:** {metrics['Avg_Compliance_Score']:.2f}
    - **Total Volume:** ${metrics['Total_Volume']:,.0f}
    """
)

st.plotly_chart(create_btc_price_chart(df), use_container_width=True)
