# app.py – PhonePe Pulse Premium Insights Dashboard (100% Python-only)
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from datetime import datetime
import plotly.io as pio

# Set up page config
st.set_page_config(
    page_title="PhonePe Pulse Insights",
    layout="wide",
    page_icon="📱",
    initial_sidebar_state="expanded"
)

# ------------------- SESSION STATE INIT -------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Default"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ------------------- THEME DEFINITIONS -------------------
def get_theme_style(theme):
    if theme == "Neon":
        bg = "#030706"
        card_gradient = "linear-gradient(135deg, #00ff88, #00b8a9)"
        accent = "#00ff88"
        text = "#ffffff"
        plotly_template = "plotly_dark"
        chart_bg = "#080f0d"
        color_scale = "Viridis"
        line_color = "#00ff88"
    elif theme == "Cyan":
        bg = "#020b14"
        card_gradient = "linear-gradient(135deg, #00e5ff, #007799)"
        accent = "#00e5ff"
        text = "#e0f7fa"
        plotly_template = "plotly_dark"
        chart_bg = "#051321"
        color_scale = "Cyanyl"
        line_color = "#00e5ff"
    elif theme == "Sunset":
        bg = "#0d040a"
        card_gradient = "linear-gradient(135deg, #ff6b6b, #e056fd)"
        accent = "#ff7675"
        text = "#ffe0cc"
        plotly_template = "plotly_dark"
        chart_bg = "#170a13"
        color_scale = "Sunset"
        line_color = "#ff6b6b"
    else:  # Default
        if st.session_state.dark_mode:
            bg = "#0b0c10"
            card_gradient = "linear-gradient(135deg, #1f4068, #162447)"
            accent = "#66fcf1"
            text = "#ffffff"
            plotly_template = "plotly_dark"
            chart_bg = "#1f2833"
            color_scale = "Blues"
            line_color = "#66fcf1"
        else:
            bg = "#f4f6f9"
            card_gradient = "linear-gradient(135deg, #007bff, #00c6ff)"
            accent = "#007bff"
            text = "#212529"
            plotly_template = "plotly_white"
            chart_bg = "#ffffff"
            color_scale = "Blues"
            line_color = "#007bff"
    return bg, card_gradient, accent, text, plotly_template, chart_bg, color_scale, line_color

# Apply CSS dynamically
bg, grad, accent, txt, template, chart_bg, color_scale, line_color = get_theme_style(st.session_state.theme)

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    
    /* Premium Glassmorphic Cards */
    .metric-card {{
        background: {grad};
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255,255,255,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }}
    .metric-value {{ font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px; }}
    .metric-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 4px; }}
    
    /* Dashboard Title styling */
    .dashboard-header {{
        padding: 1.5rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .dashboard-title {{
        font-size: 2.8rem;
        font-weight: 900;
        background: {grad};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}
    
    /* Sidebar adjustments */
    [data-testid="stSidebar"] {{
        background-color: {bg} !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    
    .sidebar-card-title {{
        color: {accent};
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Tabs customization */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 6px;
        border-radius: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 6px;
        padding: 8px 16px;
        background-color: transparent;
        color: {txt};
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {accent} !important;
        color: #000000 !important;
        font-weight: 700;
    }}
    
    /* Styled metric containers */
    div[data-testid="stMetricValue"] {{
        color: {accent} !important;
    }}
</style>
""", unsafe_allow_html=True)
pio.templates.default = template

# ------------------- DATA LOADING CACHE -------------------
@st.cache_data
def load_transaction_data():
    if os.path.exists("aggregated_transaction.csv"):
        return pd.read_csv("aggregated_transaction.csv")
    return pd.DataFrame()

@st.cache_data
def load_user_data():
    if os.path.exists("top_user_state.csv"):
        return pd.read_csv("top_user_state.csv")
    return pd.DataFrame()

@st.cache_data
def load_device_data():
    if os.path.exists("user_devices.csv"):
        return pd.read_csv("user_devices.csv")
    return pd.DataFrame()

@st.cache_data
def load_map_trans_data():
    if os.path.exists("map_transaction.csv"):
        return pd.read_csv("map_transaction.csv")
    return pd.DataFrame()

@st.cache_data
def load_map_user_data():
    if os.path.exists("map_user.csv"):
        return pd.read_csv("map_user.csv")
    return pd.DataFrame()

@st.cache_data
def load_top_trans_pin():
    if os.path.exists("top_transaction_pincode.csv"):
        return pd.read_csv("top_transaction_pincode.csv")
    return pd.DataFrame()

@st.cache_data
def load_top_user_pin():
    if os.path.exists("top_user_pincode.csv"):
        return pd.read_csv("top_user_pincode.csv")
    return pd.DataFrame()

with st.spinner("Loading cached files..."):
    df_trans = load_transaction_data()
    df_users = load_user_data()
    df_devices = load_device_data()
    df_map_trans = load_map_trans_data()
    df_map_user = load_map_user_data()
    df_top_trans = load_top_trans_pin()
    df_top_user = load_top_user_pin()

if df_trans.empty:
    st.error("No data found. Please run `python extract_data.py` to extract phonepe pulse JSON datasets.")
    st.stop()

# ------------------- SIDEBAR SELECTION & FILTERS -------------------
st.sidebar.markdown(f'<div style="text-align: center; margin-bottom: 1.5rem;"><h2 style="color: {accent}; margin:0; font-weight: 800;">📱 PhonePe Pulse</h2><small style="opacity: 0.7;">Premium Analytics</small></div>', unsafe_allow_html=True)

# 1. Theme Configuration
st.sidebar.markdown('<div class="sidebar-card"><div class="sidebar-card-title">🎨 Aesthetics</div>', unsafe_allow_html=True)
theme_options = ["Default", "Neon", "Cyan", "Sunset"]
selected_theme = st.sidebar.selectbox("Choose Theme", theme_options, index=theme_options.index(st.session_state.theme))
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()

if st.session_state.theme == "Default":
    dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 2. Main Filters
st.sidebar.markdown('<div class="sidebar-card"><div class="sidebar-card-title">🔍 Main Filter</div>', unsafe_allow_html=True)
years_list = sorted(df_trans['year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years_list, index=len(years_list)-1)

quarters_list = sorted(df_trans[df_trans['year'] == selected_year]['quarter'].unique())
selected_quarter = st.sidebar.selectbox("Select Quarter", quarters_list, index=0)

states_list = ["All"] + sorted(df_trans['state'].unique())
selected_state = st.sidebar.selectbox("Select State", states_list, index=0)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 3. Time Slider (For Trend Tab)
st.sidebar.markdown('<div class="sidebar-card"><div class="sidebar-card-title">⏰ Multi-Quarter Trend Range</div>', unsafe_allow_html=True)
all_periods = sorted(df_trans.groupby(['year', 'quarter']).size().index)
periods_labels = [f"{y} Q{q}" for y, q in all_periods]
range_idx = st.sidebar.slider("Quarter Range", 0, len(periods_labels)-1, (0, len(periods_labels)-1))
start_label = periods_labels[range_idx[0]]
end_label = periods_labels[range_idx[1]]
start_y, start_q = all_periods[range_idx[0]]
end_y, end_q = all_periods[range_idx[1]]
st.sidebar.markdown('</div>', unsafe_allow_html=True)

if st.sidebar.button("🔄 Clear Filters & Caches"):
    st.cache_data.clear()
    st.rerun()

# Apply filters to dataframes
# Base filters
mask_trans = (df_trans['year'] == selected_year) & (df_trans['quarter'] == selected_quarter)
mask_users = (df_users['year'] == selected_year) & (df_users['quarter'] == selected_quarter) if not df_users.empty else None

if selected_state != "All":
    mask_trans &= (df_trans['state'] == selected_state)
    if mask_users is not None:
        mask_users &= (df_users['state'] == selected_state)

df_trans_filtered = df_trans[mask_trans]
df_users_filtered = df_users[mask_users] if (df_users is not None and mask_users is not None) else pd.DataFrame()

# Trend ranges mask
mask_trans_trend = ((df_trans['year'] > start_y) | ((df_trans['year'] == start_y) & (df_trans['quarter'] >= start_q))) & \
                  ((df_trans['year'] < end_y) | ((df_trans['year'] == end_y) & (df_trans['quarter'] <= end_q)))
if selected_state != "All":
    mask_trans_trend &= (df_trans['state'] == selected_state)
df_trans_trend = df_trans[mask_trans_trend]

# ------------------- MAIN INTERFACE -------------------
st.markdown(f"""
<div class="dashboard-header">
    <h1 class="dashboard-title">PhonePe Pulse Insights</h1>
    <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 1rem;">
        Interactive Visualization of Transaction & User Trends | Active Theme: <strong>{st.session_state.theme}</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------- KPI CARDS -------------------
# Calculate metrics
total_tx_count = df_trans_filtered['transaction_count'].sum()
total_tx_amount = df_trans_filtered['transaction_amount'].sum()

# Growth relative to previous quarter
prev_q = selected_quarter - 1 if selected_quarter > 1 else 4
prev_y = selected_year if selected_quarter > 1 else selected_year - 1
mask_prev = (df_trans['year'] == prev_y) & (df_trans['quarter'] == prev_q)
if selected_state != "All":
    mask_prev &= (df_trans['state'] == selected_state)
prev_tx_count = df_trans[mask_prev]['transaction_count'].sum()
growth_pct = ((total_tx_count - prev_tx_count) / prev_tx_count * 100) if prev_tx_count > 0 else 0.0

# User registered metrics
if not df_users_filtered.empty:
    total_reg_users = df_users_filtered['registered_users'].sum()
    total_app_opens = df_users_filtered['app_opens'].sum()
    user_val_str = f"{total_reg_users:,.0f}"
    app_opens_str = f"{total_app_opens:,.0f}"
else:
    total_reg_users = 0
    user_val_str = "No Data"
    app_opens_str = "No Data"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 Total Transactions</div>
        <div class="metric-value">{total_tx_count:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Total Amount</div>
        <div class="metric-value">₹ {total_tx_amount/1e7:,.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    growth_color = "#00ff88" if growth_pct >= 0 else "#ff4d4d"
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {growth_color}44, rgba(0,0,0,0.65)); border-color: {growth_color}88;">
        <div class="metric-label">📈 Quarterly Growth</div>
        <div class="metric-value" style="color: {growth_color};">{growth_pct:+.2f} %</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👥 Registered Users</div>
        <div class="metric-value">{user_val_str}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------- TAB LAYOUT -------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 Transaction Analytics", 
    "👥 User & Device Insights", 
    "🔍 Pincode & District Deep-Dive", 
    "📋 Raw Dataset & Export"
])

# State name mapping dictionary for geojson matching
state_geojson_mapping = {
    "Andaman & Nicobar Islands": "Andaman & Nicobar",
    "Dadra & Nagar Haveli & Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu"
}

# ------------------- TAB 1: TRANSACTION ANALYTICS -------------------
with tab1:
    col_map, col_pie = st.columns([1.5, 1], gap="medium")
    
    with col_map:
        st.markdown(f"### 🗺️ Geographic Transaction Distribution ({selected_year} Q{selected_quarter})")
        if selected_state == "All":
            map_df = df_trans_filtered.groupby('state')['transaction_amount'].sum().reset_index()
            # Map state names to GeoJSON conventions
            map_df['geojson_state'] = map_df['state'].replace(state_geojson_mapping)
            
            fig_map = px.choropleth(
                map_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey="properties.ST_NM",
                locations="geojson_state",
                color="transaction_amount",
                color_continuous_scale=color_scale,
                template=template,
                labels={'transaction_amount': 'Total Amount (₹)'}
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=450)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info(f"Filtering map for {selected_state}. Select 'All' states in the sidebar to view the national map.")
            # Show a local district level map if district data exists
            dist_df = df_map_trans[(df_map_trans['year'] == selected_year) & (df_map_trans['quarter'] == selected_quarter) & (df_map_trans['state'] == selected_state)]
            if not dist_df.empty:
                fig_dist = px.bar(
                    dist_df.sort_values(by='amount', ascending=True),
                    x='amount',
                    y='district',
                    orientation='h',
                    title=f"Districts in {selected_state} by Transaction Amount",
                    color='amount',
                    color_continuous_scale=color_scale,
                    template=template
                )
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.warning("No district level transaction data available.")

    with col_pie:
        st.markdown(f"### 🍩 Share by Transaction Category")
        type_df = df_trans_filtered.groupby('transaction_type')[['transaction_count', 'transaction_amount']].sum().reset_index()
        fig_donut = px.pie(
            type_df, 
            names='transaction_type', 
            values='transaction_amount', 
            hole=0.4, 
            template=template,
            color_discrete_sequence=px.colors.sequential.Sunset if st.session_state.theme == "Sunset" else px.colors.sequential.Viridis
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(margin={"r":10,"t":20,"l":10,"b":10}, height=450, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    
    # Trend with linear regression forecasting
    st.markdown(f"### 📈 Historical Transaction Trend & Future Forecasting ({start_label} to {end_label})")
    
    trend_df = df_trans_trend.groupby(['year', 'quarter'])[['transaction_count', 'transaction_amount']].sum().reset_index()
    trend_df['period'] = trend_df['year'].astype(str) + " Q" + trend_df['quarter'].astype(str)
    
    fig_trend = px.line(
        trend_df,
        x='period',
        y='transaction_amount',
        markers=True,
        template=template,
        line_shape='spline',
        labels={'transaction_amount': 'Total Amount (₹)'}
    )
    fig_trend.update_traces(line_color=line_color, line_width=3, marker=dict(size=8, color=line_color, symbol="circle"))

    # Multi-period linear regression forecast
    if len(trend_df) >= 3:
        X = np.arange(len(trend_df)).reshape(-1, 1)
        y = trend_df['transaction_amount'].values
        model = LinearRegression().fit(X, y)
        
        # Forecast next 2 quarters
        forecast_indices = np.array([len(trend_df), len(trend_df)+1]).reshape(-1, 1)
        predictions = model.predict(forecast_indices)
        
        # Build forecast dataframe
        last_y, last_q = trend_df['year'].iloc[-1], trend_df['quarter'].iloc[-1]
        fc_labels = []
        cy, cq = last_y, last_q
        for i in range(2):
            cq = cq + 1 if cq < 4 else 1
            cy = cy + 1 if cq == 1 else cy
            fc_labels.append(f"{cy} Q{cq} (Est)")
        
        # Add predictions to plot
        # Add dashed extension line representing the forecast
        forecast_x = [trend_df['period'].iloc[-1]] + fc_labels
        forecast_y = [trend_df['transaction_amount'].iloc[-1]] + list(predictions)
        
        fig_trend.add_scatter(
            x=forecast_x,
            y=forecast_y,
            mode='lines+markers',
            line=dict(dash='dash', color='#ff3f34', width=3),
            marker=dict(symbol='diamond', size=8, color='#ff3f34'),
            name='ML Forecast Model'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        st.caption("🤖 *The red dashed line represents a Linear Regression Forecast model trained on the historical multi-quarter trends selected.*")
    else:
        st.plotly_chart(fig_trend, use_container_width=True)
        st.warning("Insufficient data points in range (minimum 3 quarters required) to compute linear forecast.")

    # More visualizations: State Ranker and YoY Growth side by side
    st.markdown("---")
    col_bar1, col_bar2 = st.columns(2)
    
    with col_bar1:
        st.markdown("### 🏆 Top 10 States by Transaction Amount")
        top_states_df = df_trans_filtered.groupby('state')['transaction_amount'].sum().nlargest(10).reset_index()
        fig_top_bar = px.bar(
            top_states_df,
            x='transaction_amount',
            y='state',
            orientation='h',
            text_auto='.3s',
            color='transaction_amount',
            color_continuous_scale=color_scale,
            template=template
        )
        fig_top_bar.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=350)
        st.plotly_chart(fig_top_bar, use_container_width=True)

    with col_bar2:
        st.markdown("### 📅 Year-over-Year Growth comparison")
        yoy_df = df_trans[df_trans['quarter'] == selected_quarter].groupby(['year', 'state'])['transaction_amount'].sum().reset_index()
        if selected_state != "All":
            yoy_df = yoy_df[yoy_df['state'] == selected_state]
        yoy_agg = yoy_df.groupby('year')['transaction_amount'].sum().reset_index()
        yoy_agg['prev'] = yoy_agg['transaction_amount'].shift(1)
        yoy_agg['growth_pct'] = ((yoy_agg['transaction_amount'] - yoy_agg['prev']) / yoy_agg['prev']) * 100
        yoy_agg = yoy_agg.dropna()
        
        if not yoy_agg.empty:
            fig_yoy = px.bar(
                yoy_agg,
                x='year',
                y='growth_pct',
                color='growth_pct',
                color_continuous_scale='RdYlGn',
                text_auto='+0.1f',
                template=template,
                labels={'growth_pct': 'YoY Growth (%)'}
            )
            fig_yoy.update_layout(height=350)
            st.plotly_chart(fig_yoy, use_container_width=True)
        else:
            st.info("YoY Growth data not available (first year in dataset is baseline).")

# ------------------- TAB 2: USER & DEVICE INSIGHTS -------------------
with tab2:
    if df_users.empty:
        st.warning("User state dataset `top_user_state.csv` is empty or not loaded.")
    else:
        col_u_map, col_u_trend = st.columns([1.2, 1])
        
        with col_u_map:
            st.markdown(f"### 🗺️ Registered Users Geographic Heatmap ({selected_year} Q{selected_quarter})")
            if selected_state == "All":
                u_map_df = df_users_filtered.groupby('state')['registered_users'].sum().reset_index()
                u_map_df['geojson_state'] = u_map_df['state'].replace(state_geojson_mapping)
                
                fig_u_map = px.choropleth(
                    u_map_df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey="properties.ST_NM",
                    locations="geojson_state",
                    color="registered_users",
                    color_continuous_scale="sunset" if st.session_state.theme == "Sunset" else "viridis",
                    template=template,
                    labels={'registered_users': 'Users'}
                )
                fig_u_map.update_geos(fitbounds="locations", visible=False)
                fig_u_map.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=400)
                st.plotly_chart(fig_u_map, use_container_width=True)
            else:
                st.info(f"Filtering local user map for {selected_state}.")
                dist_u_df = df_map_user[(df_map_user['year'] == selected_year) & (df_map_user['quarter'] == selected_quarter) & (df_map_user['state'] == selected_state)]
                if not dist_u_df.empty:
                    fig_dist_u = px.bar(
                        dist_u_df.sort_values(by='registered_users', ascending=True),
                        x='registered_users',
                        y='district',
                        orientation='h',
                        title=f"Districts in {selected_state} by Registered Users",
                        color='registered_users',
                        color_continuous_scale="sunset" if st.session_state.theme == "Sunset" else "viridis",
                        template=template
                    )
                    st.plotly_chart(fig_dist_u, use_container_width=True)
                else:
                    st.warning("No district level user data available.")

        with col_u_trend:
            st.markdown("### 📈 Registered Users & App Opening Trend")
            # Apply time slider filter to user registrations
            mask_users_trend = ((df_users['year'] > start_y) | ((df_users['year'] == start_y) & (df_users['quarter'] >= start_q))) & \
                              ((df_users['year'] < end_y) | ((df_users['year'] == end_y) & (df_users['quarter'] <= end_q)))
            if selected_state != "All":
                mask_users_trend &= (df_users['state'] == selected_state)
            
            u_trend_df = df_users[mask_users_trend].groupby(['year', 'quarter'])[['registered_users', 'app_opens']].sum().reset_index()
            u_trend_df['period'] = u_trend_df['year'].astype(str) + " Q" + u_trend_df['quarter'].astype(str)
            
            if not u_trend_df.empty:
                fig_u_trend = px.line(
                    u_trend_df,
                    x='period',
                    y='registered_users',
                    markers=True,
                    template=template
                )
                fig_u_trend.update_traces(line_color=accent, line_width=3, marker=dict(size=8, color=accent))
                fig_u_trend.update_layout(height=400)
                st.plotly_chart(fig_u_trend, use_container_width=True)
            else:
                st.warning("No historical user trend data matches filters.")

        # 📱 Device / Brand Share breakdown
        st.markdown("---")
        st.markdown(f"### 📱 Mobile Device Brand Share Analysis ({selected_year} Q{selected_quarter})")
        if df_devices.empty:
            st.warning("Device brand database `user_devices.csv` is empty.")
        else:
            # Filter devices
            mask_dev = (df_devices['year'] == selected_year) & (df_devices['quarter'] == selected_quarter)
            if selected_state != "All":
                mask_dev &= (df_devices['state'] == selected_state)
            
            dev_filtered = df_devices[mask_dev]
            dev_agg = dev_filtered.groupby('brand')['count'].sum().reset_index().sort_values(by='count', ascending=False)
            
            if not dev_agg.empty:
                col_b1, col_b2 = st.columns([1, 1.2])
                with col_b1:
                    fig_dev_pie = px.pie(
                        dev_agg,
                        names='brand',
                        values='count',
                        title="Mobile OS/Brand Share Percentage",
                        template=template,
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig_dev_pie.update_traces(textposition='inside', textinfo='percent')
                    st.plotly_chart(fig_dev_pie, use_container_width=True)
                with col_b2:
                    fig_dev_bar = px.bar(
                        dev_agg,
                        x='count',
                        y='brand',
                        orientation='h',
                        title="Registered Users Count by Brand",
                        text_auto='.3s',
                        color='count',
                        color_continuous_scale=color_scale,
                        template=template
                    )
                    fig_dev_bar.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig_dev_bar, use_container_width=True)
            else:
                st.warning("No device brand registration data is available for current year/quarter.")

# ------------------- TAB 3: PINCODE & DISTRICT DEEP-DIVE -------------------
with tab3:
    st.markdown("### 🔍 Regional Deep-Dive Insights")
    
    # State selection for deep-dive (default to standard selected state, fallback to Tamil Nadu if 'All')
    dd_state = selected_state
    if dd_state == "All":
        dd_state = st.selectbox("Select State to inspect districts/pincodes:", sorted(df_trans['state'].unique()), index=0, key="dd_state_select")
    else:
        st.info(f"Showing deep dive for: **{dd_state}**")
        
    st.markdown("---")
    
    # 1. District level transaction vs user base comparison
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown(f"#### 🏙️ Top Districts in {dd_state} (Transactions)")
        mask_map_t = (df_map_trans['year'] == selected_year) & (df_map_trans['quarter'] == selected_quarter) & (df_map_trans['state'] == dd_state)
        df_m_t = df_map_trans[mask_map_t].sort_values(by='amount', ascending=False)
        
        if not df_m_t.empty:
            fig_dt = px.bar(
                df_m_t.head(10),
                x='amount',
                y='district',
                orientation='h',
                color='amount',
                color_continuous_scale=color_scale,
                template=template,
                text_auto='.2s',
                labels={'amount': 'Amount (₹)'}
            )
            fig_dt.update_layout(yaxis=dict(autorange="reversed"), height=350)
            st.plotly_chart(fig_dt, use_container_width=True)
        else:
            st.warning(f"No district transaction data for {dd_state}.")
            
    with col_d2:
        st.markdown(f"#### 🏙️ Top Districts in {dd_state} (Users)")
        mask_map_u = (df_map_user['year'] == selected_year) & (df_map_user['quarter'] == selected_quarter) & (df_map_user['state'] == dd_state)
        df_m_u = df_map_user[mask_map_u].sort_values(by='registered_users', ascending=False)
        
        if not df_m_u.empty:
            fig_du = px.bar(
                df_m_u.head(10),
                x='registered_users',
                y='district',
                orientation='h',
                color='registered_users',
                color_continuous_scale="sunset" if st.session_state.theme == "Sunset" else "viridis",
                template=template,
                text_auto='.2s'
            )
            fig_du.update_layout(yaxis=dict(autorange="reversed"), height=350)
            st.plotly_chart(fig_du, use_container_width=True)
        else:
            st.warning(f"No district user data for {dd_state}.")

    # 2. Pincode Top-10 Tables
    st.markdown("---")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown(f"#### 📍 Top 10 Pincodes (Transactions - {selected_year})")
        if df_top_trans.empty:
            st.warning("Pincode transaction CSV file is empty.")
        else:
            mask_p_t = (df_top_trans['year'] == selected_year) & (df_top_trans['quarter'] == selected_quarter) & (df_top_trans['state'] == dd_state)
            df_p_t_fil = df_top_trans[mask_p_t].sort_values(by='transaction_amount', ascending=False).head(10)
            if not df_p_t_fil.empty:
                st.dataframe(
                    df_p_t_fil[['pincode', 'transaction_count', 'transaction_amount']].rename(columns={
                        'pincode': 'Pincode',
                        'transaction_count': 'Total Count',
                        'transaction_amount': 'Total Amount (₹)'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info(f"No pincode transaction data for {dd_state}.")
                
    with col_p2:
        st.markdown(f"#### 📍 Top 10 Pincodes (Registered Users - {selected_year})")
        if df_top_user.empty:
            st.warning("Pincode user CSV file is empty.")
        else:
            mask_p_u = (df_top_user['year'] == selected_year) & (df_top_user['quarter'] == selected_quarter) & (df_top_user['state'] == dd_state)
            df_p_u_fil = df_top_user[mask_p_u].sort_values(by='registered_users', ascending=False).head(10)
            if not df_p_u_fil.empty:
                st.dataframe(
                    df_p_u_fil[['pincode', 'registered_users']].rename(columns={
                        'pincode': 'Pincode',
                        'registered_users': 'Registered Users'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info(f"No pincode user data for {dd_state}.")

# ------------------- TAB 4: RAW DATASET & EXPORT -------------------
with tab4:
    st.markdown("### 📋 Filtered Raw Transactions Table")
    st.dataframe(df_trans_filtered, use_container_width=True, height=350)
    
    # Download Button
    csv = df_trans_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Transactions CSV",
        data=csv,
        file_name=f"phonepe_transactions_{selected_year}_q{selected_quarter}_{selected_state}.csv",
        mime='text/csv',
        key="download_trans_csv"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Filtered Raw Users Table")
    if not df_users_filtered.empty:
        st.dataframe(df_users_filtered, use_container_width=True, height=300)
        u_csv = df_users_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Users CSV",
            data=u_csv,
            file_name=f"phonepe_users_{selected_year}_q{selected_quarter}_{selected_state}.csv",
            mime='text/csv',
            key="download_users_csv"
        )
    else:
        st.info("No user records matching the filtered selections.")

# Footer timestamp
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Antigravity AI Engine")