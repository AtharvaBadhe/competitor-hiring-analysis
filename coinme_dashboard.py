import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
import hashlib
import json
import os
from typing import Dict, List, Optional
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
    .login-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #1f77b4;
        max-width: 400px;
        margin: 2rem auto;
    }
    .user-info {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .admin-panel {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Authentication System
class AuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.sessions_file = "sessions.json"
        self.activity_log_file = "activity_log.json"
        self.initialize_files()
    
    def initialize_files(self):
        """Initialize authentication files if they don't exist"""
        # Default admin user
        default_users = {
            "admin": {
                "password": self.hash_password("admin123"),
                "role": "admin",
                "email": "admin@coinme.com",
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "is_active": True
            }
        }
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f, indent=2)
        
        if not os.path.exists(self.activity_log_file):
            with open(self.activity_log_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_activity_log(self) -> List:
        """Load activity log from file"""
        try:
            with open(self.activity_log_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_activity_log(self, log: List):
        """Save activity log to file"""
        with open(self.activity_log_file, 'w') as f:
            json.dump(log, f, indent=2)
    
    def log_activity(self, username: str, action: str, details: str = ""):
        """Log user activity"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "details": details,
            "ip_address": "127.0.0.1"  # In production, get real IP
        }
        
        log = self.load_activity_log()
        log.append(activity)
        
        # Keep only last 1000 entries
        if len(log) > 1000:
            log = log[-1000:]
        
        self.save_activity_log(log)
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user credentials"""
        users = self.load_users()
        
        if username in users:
            user = users[username]
            if user.get('is_active', True) and user['password'] == self.hash_password(password):
                # Update last login
                user['last_login'] = datetime.now().isoformat()
                users[username] = user
                self.save_users(users)
                
                # Log login
                self.log_activity(username, "login", "Successful login")
                
                return {
                    "username": username,
                    "role": user.get('role', 'user'),
                    "email": user.get('email', ''),
                    "last_login": user.get('last_login')
                }
        
        # Log failed login attempt
        self.log_activity(username, "login_failed", "Failed login attempt")
        return None
    
    def create_user(self, username: str, password: str, email: str, role: str = "user") -> bool:
        """Create new user"""
        users = self.load_users()
        
        if username in users:
            return False
        
        users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True
        }
        
        self.save_users(users)
        self.log_activity("admin", "user_created", f"Created user: {username}")
        return True
    
    def deactivate_user(self, username: str) -> bool:
        """Deactivate user"""
        users = self.load_users()
        
        if username in users:
            users[username]['is_active'] = False
            self.save_users(users)
            self.log_activity("admin", "user_deactivated", f"Deactivated user: {username}")
            return True
        
        return False
    
    def get_all_users(self) -> Dict:
        """Get all users (admin only)"""
        return self.load_users()
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        users = self.load_users()
        activity_log = self.load_activity_log()
        
        total_users = len(users)
        active_users = sum(1 for user in users.values() if user.get('is_active', True))
        admin_users = sum(1 for user in users.values() if user.get('role') == 'admin')
        
        # Recent activity (last 24 hours)
        recent_activities = [
            activity for activity in activity_log
            if datetime.fromisoformat(activity['timestamp']) > datetime.now() - timedelta(hours=24)
        ]
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "recent_activities": len(recent_activities),
            "last_activity": activity_log[-1]['timestamp'] if activity_log else None
        }

# Initialize authentication system
auth_system = AuthenticationSystem()

def login_page():
    """Display login page"""
    st.markdown('<div class="main-header">🔐 Coinme Dashboard Login</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("### Please enter your credentials")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login", key="login_btn"):
                if username and password:
                    user = auth_system.authenticate_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            if st.button("Demo Login", key="demo_btn"):
                st.info("**Demo Credentials:**\n\nUsername: admin\nPassword: admin123")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Default Admin Credentials:**")
        st.markdown("- Username: `admin`")
        st.markdown("- Password: `admin123`")
        st.markdown("*Please change the default password after first login*")

def admin_panel():
    """Admin panel for user management"""
    st.subheader("👑 Admin Panel")
    
    tab1, tab2, tab3 = st.tabs(["User Management", "User Statistics", "Activity Log"])
    
    with tab1:
        st.markdown("### Create New User")
        
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
            
            with col2:
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ["user", "admin"])
            
            if st.form_submit_button("Create User"):
                if new_username and new_password and new_email:
                    if auth_system.create_user(new_username, new_password, new_email, new_role):
                        st.success(f"User {new_username} created successfully!")
                        st.rerun()
                    else:
                        st.error("User already exists!")
                else:
                    st.error("Please fill all fields")
        
        st.markdown("### Manage Existing Users")
        
        users = auth_system.get_all_users()
        
        for username, user_data in users.items():
            if username == st.session_state.user['username']:
                continue  # Skip current user
            
            with st.expander(f"👤 {username} ({user_data.get('role', 'user')})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Email:** {user_data.get('email', 'N/A')}")
                    st.write(f"**Role:** {user_data.get('role', 'user')}")
                
                with col2:
                    st.write(f"**Created:** {user_data.get('created_at', 'N/A')[:10]}")
                    st.write(f"**Last Login:** {user_data.get('last_login', 'Never')[:10] if user_data.get('last_login') else 'Never'}")
                
                with col3:
                    status = "Active" if user_data.get('is_active', True) else "Inactive"
                    st.write(f"**Status:** {status}")
                    
                    if user_data.get('is_active', True):
                        if st.button(f"Deactivate {username}", key=f"deactivate_{username}"):
                            if auth_system.deactivate_user(username):
                                st.success(f"User {username} deactivated!")
                                st.rerun()
    
    with tab2:
        st.markdown("### User Statistics")
        
        stats = auth_system.get_user_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", stats['total_users'])
        
        with col2:
            st.metric("Active Users", stats['active_users'])
        
        with col3:
            st.metric("Admin Users", stats['admin_users'])
        
        with col4:
            st.metric("Recent Activities (24h)", stats['recent_activities'])
        
        # User creation timeline
        users = auth_system.get_all_users()
        user_dates = []
        
        for username, user_data in users.items():
            if 'created_at' in user_data:
                user_dates.append({
                    'date': datetime.fromisoformat(user_data['created_at']).date(),
                    'username': username,
                    'role': user_data.get('role', 'user')
                })
        
        if user_dates:
            df_users = pd.DataFrame(user_dates)
            user_timeline = df_users.groupby('date').size().reset_index(name='new_users')
            
            fig = px.line(user_timeline, x='date', y='new_users', 
                         title='User Registration Timeline',
                         labels={'date': 'Date', 'new_users': 'New Users'})
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Activity Log")
        
        activity_log = auth_system.load_activity_log()
        
        if activity_log:
            # Show recent activities
            recent_activities = activity_log[-50:]  # Last 50 activities
            
            df_activities = pd.DataFrame(recent_activities)
            df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
            df_activities = df_activities.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                df_activities[['timestamp', 'username', 'action', 'details']],
                use_container_width=True
            )
            
            # Activity summary
            st.markdown("### Activity Summary")
            
            action_counts = df_activities['action'].value_counts()
            
            fig = px.bar(
                x=action_counts.index,
                y=action_counts.values,
                title='Activity Types Distribution',
                labels={'x': 'Action Type', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity log available")

def user_info_sidebar():
    """Display user info in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 User Information")
    
    user = st.session_state.user
    
    st.sidebar.markdown(f'<div class="user-info">', unsafe_allow_html=True)
    st.sidebar.write(f"**Username:** {user['username']}")
    st.sidebar.write(f"**Role:** {user['role'].title()}")
    st.sidebar.write(f"**Email:** {user['email']}")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout"):
        auth_system.log_activity(user['username'], "logout", "User logged out")
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()

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

def generate_wavess_value_propositions():
    """Generate realistic Wavess.io value propositions based on actual business intelligence capabilities"""
    
    value_props = [
        {
            "title": "🔍 Fundraising Signal Detection",
            "description": "Monitor public fundraising announcements and SEC filings across the crypto industry",
            "benefits": ["Faster market response", "Competitor funding awareness", "Industry benchmarking"]
        },
        {
            "title": "👥 Hiring Intelligence",
            "description": "Analyze job postings and LinkedIn activity for talent market insights",
            "benefits": ["Spot talent trends", "Understand competitor scaling", "Executive movement tracking"]
        },
        {
            "title": "📊 Market Intelligence",
            "description": "Track expansion announcements and regulatory changes in real-time",
            "benefits": ["Identify market opportunities", "Understand competitor moves", "Regulatory impact awareness"]
        },
        {
            "title": "🎯 Sales & Marketing Activation",
            "description": "Automate alerts and trigger sales outreach based on growth signals",
            "benefits": ["Improved sales timing", "Better targeting", "Enhanced partnership opportunities"]
        }
    ]
    
    return value_props

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
    recommendations.append("⚡ **Technology Innovation**: Invest in blockchain infrastructure and DeFi integrations to stay
