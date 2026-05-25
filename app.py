# app.py – PhonePe Insights Dashboard with Multiple Themes
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from datetime import datetime
import plotly.io as pio

st.set_page_config(page_title="PhonePe Pulse Insights", layout="wide", page_icon="📱")

# ------------------- SESSION STATE INIT -------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Default"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ------------------- THEME DEFINITIONS -------------------
def get_theme_style(theme):
    if theme == "Neon":
        bg = "#0a0f0a"
        card_gradient = "linear-gradient(135deg, #00ff88, #00bcd4)"
        accent = "#00ff88"
        text = "#ffffff"
        plotly_template = "plotly_dark"
        chart_bg = "#111a11"
    elif theme == "Cyan":
        bg = "#0a1a2a"
        card_gradient = "linear-gradient(135deg, #00e5ff, #00796b)"
        accent = "#00e5ff"
        text = "#e0f7fa"
        plotly_template = "plotly_dark"
        chart_bg = "#0f2a3a"
    elif theme == "Sunset":
        bg = "#1f0f1a"
        card_gradient = "linear-gradient(135deg, #ff6b6b, #ff8e53)"
        accent = "#ffaa66"
        text = "#ffe0cc"
        plotly_template = "plotly_dark"
        chart_bg = "#2a1a1f"
    else:  # Default
        if st.session_state.get("dark_mode", False):
            bg = "#0f0f1a"
            card_gradient = "linear-gradient(135deg, #3b82f6, #8b5cf6)"
            accent = "#8b5cf6"
            text = "#ffffff"
            plotly_template = "plotly_dark"
            chart_bg = "#1e1e2f"
        else:
            bg = "#f8fafc"
            card_gradient = "linear-gradient(135deg, #3b82f6, #8b5cf6)"
            accent = "#3b82f6"
            text = "#1e293b"
            plotly_template = "plotly_white"
            chart_bg = "#ffffff"
    return bg, card_gradient, accent, text, plotly_template, chart_bg

# ------------------- APPLY THEME CSS -------------------
def apply_theme():
    bg, grad, accent, txt, template, chart_bg = get_theme_style(st.session_state.theme)
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg}; }}
        .metric-card {{
            background: {grad};
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
            transition: transform 0.2s;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-value {{ font-size: 2rem; font-weight: bold; }}
        .metric-label {{ font-size: 0.9rem; opacity: 0.95; }}
        .dashboard-title {{
            font-size: 2.5rem;
            font-weight: 800;
            background: {grad};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stSelectbox label, .stSlider label, .stRadio label, .stCheckbox label {{
            color: {accent} !important;
            font-weight: 500;
        }}
        [data-testid="stSidebar"] {{
            background: {bg};
            border-right: 2px solid {accent};
        }}
        .sidebar-section {{
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 0.8rem;
            margin-bottom: 1.2rem;
        }}
        .sidebar-section-title {{
            color: {accent};
        }}
        .stButton button {{
            background: {grad};
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }}
        .stButton button:hover {{
            opacity: 0.9;
            transform: scale(1.02);
        }}
        .stDataFrame, .stTable {{
            background: {chart_bg};
            border-radius: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)
    pio.templates.default = template

apply_theme()

# ------------------- SIDEBAR -------------------
st.sidebar.markdown("""
<style>
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem 0;
        border-bottom: 2px solid #3b82f6;
        margin-bottom: 1.5rem;
        color: white;
    }
    hr { margin: 0.5rem 0; border-color: #4b5563; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">📱 PhonePe<br>Insights</div>', unsafe_allow_html=True)

# Theme selector
st.sidebar.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🎨 Theme</div>', unsafe_allow_html=True)
theme_options = ["Default", "Neon", "Cyan", "Sunset"]
selected_theme = st.sidebar.selectbox("Choose Theme", theme_options, index=theme_options.index(st.session_state.theme), key="theme_selector")
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# Data source
st.sidebar.markdown('<div class="sidebar-section"><div class="sidebar-section-title">📂 Data Source</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv", key="csv_upload")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ------------------- DATA LOADING -------------------
@st.cache_data
def load_transaction_data(uploaded_file=None):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        default_path = "aggregated_transaction.csv"
        if not os.path.exists(default_path):
            return pd.DataFrame()
        df = pd.read_csv(default_path)
    df.columns = df.columns.str.lower()
    if 'transaction_count' not in df.columns and 'count' in df.columns:
        df.rename(columns={'count': 'transaction_count'}, inplace=True)
    if 'transaction_amount' not in df.columns and 'amount' in df.columns:
        df.rename(columns={'amount': 'transaction_amount'}, inplace=True)
    return df

@st.cache_data
def load_user_data():
    default_path = "top_user_state.csv"
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
        df.columns = df.columns.str.lower()
        return df
    return pd.DataFrame()

with st.spinner("Loading data..."):
    df_raw = load_transaction_data(uploaded_file)

if df_raw.empty:
    st.error("No data. Please upload a valid CSV or ensure 'aggregated_transaction.csv' exists.")
    st.stop()

# Prepare data
df_raw['year'] = df_raw['year'].astype(int)
df_raw['quarter'] = df_raw['quarter'].astype(int)
df_raw['transaction_count'] = pd.to_numeric(df_raw['transaction_count'], errors='coerce').fillna(0)
df_raw['transaction_amount'] = pd.to_numeric(df_raw['transaction_amount'], errors='coerce').fillna(0)

# Quarter range slider
years_list = sorted(df_raw['year'].unique())
quarters_labels = [f"{y} Q{q}" for y in years_list for q in range(1,5)]

st.sidebar.markdown('<div class="sidebar-section"><div class="sidebar-section-title">⏰ Time Range</div>', unsafe_allow_html=True)
range_idx = st.sidebar.slider("Quarter Range", 0, len(quarters_labels)-1, (0, len(quarters_labels)-1), key="range_slider")
start_label = quarters_labels[range_idx[0]]
end_label = quarters_labels[range_idx[1]]
start_y, start_q = map(int, start_label.split(" Q"))
end_y, end_q = map(int, end_label.split(" Q"))
st.sidebar.markdown('</div>', unsafe_allow_html=True)

mask_range = ((df_raw['year'] > start_y) | ((df_raw['year'] == start_y) & (df_raw['quarter'] >= start_q))) & \
             ((df_raw['year'] < end_y) | ((df_raw['year'] == end_y) & (df_raw['quarter'] <= end_q)))
df_range = df_raw[mask_range]

# Filters
st.sidebar.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🔍 Filters</div>', unsafe_allow_html=True)
years_avail = sorted(df_range['year'].unique())
selected_year = st.sidebar.selectbox("Year", years_avail, key="year_select")
quarters_avail = sorted(df_range[df_range['year']==selected_year]['quarter'].unique())
selected_quarter = st.sidebar.selectbox("Quarter", quarters_avail, key="quarter_select")
states_avail = ["All"] + sorted(df_range['state'].unique())
selected_state = st.sidebar.selectbox("State", states_avail, key="state_select")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Apply main filters
mask_main = (df_range['year'] == selected_year) & (df_range['quarter'] == selected_quarter)
if selected_state != "All":
    mask_main &= (df_range['state'] == selected_state)
df_main = df_range[mask_main]

if df_main.empty:
    st.warning("No data for selected filters")
    st.stop()

# ------------------- DASHBOARD MAIN -------------------
st.markdown('<div class="dashboard-title">📱 PhonePe Pulse Insights</div>', unsafe_allow_html=True)
st.caption("Interactive dashboard with vibrant themes | Neon · Cyan · Sunset")

# KPIs
total_tx = df_main['transaction_count'].sum()
total_amt = df_main['transaction_amount'].sum() / 1e7
prev_q = selected_quarter-1 if selected_quarter>1 else 4
prev_year = selected_year if selected_quarter>1 else selected_year-1
mask_prev = (df_range['year']==prev_year) & (df_range['quarter']==prev_q)
if selected_state != "All":
    mask_prev &= (df_range['state']==selected_state)
prev_tx = df_range[mask_prev]['transaction_count'].sum()
growth = ((total_tx - prev_tx)/prev_tx)*100 if prev_tx else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📊 Total Transactions</div><div class="metric-value">{total_tx:,.0f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">💰 Total Value (₹ Cr)</div><div class="metric-value">{total_amt:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    color_g = "#10b981" if growth >=0 else "#ef4444"
    st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, {color_g}, #1f2937);"><div class="metric-label">📈 Growth vs Prev Qtr</div><div class="metric-value">{growth:+.1f}%</div></div>', unsafe_allow_html=True)
with col4:
    user_df = load_user_data()
    if not user_df.empty:
        mask_user = (user_df['year']==selected_year) & (user_df['quarter']==selected_quarter)
        if selected_state != "All":
            mask_user &= (user_df['state']==selected_state)
        users = user_df[mask_user]['registered_users'].sum()
        user_val = f"{users:,.0f}"
    else:
        user_val = "N/A"
    st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);"><div class="metric-label">👥 Registered Users</div><div class="metric-value">{user_val}</div></div>', unsafe_allow_html=True)

st.markdown("---")
top_state = df_main.groupby('state')['transaction_count'].sum().idxmax()
top_value = df_main.groupby('state')['transaction_count'].sum().max()
st.info(f"🏆 **Top Performing State:** {top_state} with {top_value:,.0f} transactions")
if growth != 0:
    direction = "increased" if growth>0 else "decreased"
    st.success(f"📈 **Quarterly Change:** Transactions {direction} by {abs(growth):.1f}% compared to previous quarter")

# ------------------- CHARTS -------------------
template = get_theme_style(st.session_state.theme)[4]  # plotly_template

# Map
st.subheader("🗺️ Transaction Volume by State")
map_df = df_main.groupby('state')['transaction_count'].sum().reset_index()
fig_map = px.choropleth(map_df, locations='state', locationmode='country names',
                        color='transaction_count', color_continuous_scale='Viridis',
                        template=template)
st.plotly_chart(fig_map, use_container_width=True, key="map")

# Treemap
st.subheader("🌳 Treemap – State Volume")
fig_treemap = px.treemap(map_df, path=['state'], values='transaction_count',
                         color='transaction_count', color_continuous_scale='Teal', template=template)
st.plotly_chart(fig_treemap, use_container_width=True, key="treemap")

# Trend with forecast
st.subheader("📈 Transaction Trend Over Quarters")
trend_df = df_range.groupby(['year','quarter'])['transaction_count'].sum().reset_index()
trend_df['period'] = trend_df['year'].astype(str)+"-Q"+trend_df['quarter'].astype(str)
fig_trend = px.line(trend_df, x='period', y='transaction_count', markers=True, template=template)
if len(trend_df) >= 4:
    X = np.arange(len(trend_df)).reshape(-1,1)
    y = trend_df['transaction_count'].values
    model = LinearRegression().fit(X,y)
    forecast = model.predict([[len(trend_df)]])[0]
    fig_trend.add_annotation(x=trend_df['period'].iloc[-1], y=forecast,
                             text=f"Forecast: {forecast:,.0f}", showarrow=True)
st.plotly_chart(fig_trend, use_container_width=True, key="trend")

# Donut
st.subheader("🍩 Transaction Type Share")
type_df = df_main.groupby('transaction_type')['transaction_count'].sum().reset_index()
fig_donut = px.pie(type_df, names='transaction_type', values='transaction_count', hole=0.4, template=template)
st.plotly_chart(fig_donut, use_container_width=True, key="donut")

# Heatmap
st.subheader("🔥 State vs Type Heatmap")
heat_df = df_main.pivot_table(index='state', columns='transaction_type', values='transaction_count', aggfunc='sum', fill_value=0)
fig_heat = px.imshow(heat_df, text_auto='.2s', aspect='auto', template=template)
st.plotly_chart(fig_heat, use_container_width=True, key="heatmap")

# Top 10
st.subheader("🏆 Top 10 States")
top10 = df_main.groupby('state')['transaction_count'].sum().nlargest(10).reset_index()
fig_top = px.bar(top10, x='transaction_count', y='state', orientation='h', text='transaction_count', template=template)
st.plotly_chart(fig_top, use_container_width=True, key="top10")

# YoY Growth
st.subheader("📅 Year-over-Year Growth")
yoy_df = df_range[df_range['quarter']==selected_quarter].groupby('year')['transaction_count'].sum().reset_index()
yoy_df['prev'] = yoy_df['transaction_count'].shift(1)
yoy_df['growth'] = ((yoy_df['transaction_count'] - yoy_df['prev'])/yoy_df['prev'])*100
yoy_df = yoy_df.dropna()
fig_yoy = px.bar(yoy_df, x='year', y='growth', color='growth', color_continuous_scale='RdYlGn', template=template)
st.plotly_chart(fig_yoy, use_container_width=True, key="yoy")

# Scatter
st.subheader("📊 Count vs Amount")
scatter_df = df_main.groupby('state')[['transaction_count','transaction_amount']].sum().reset_index()
fig_scatter = px.scatter(scatter_df, x='transaction_count', y='transaction_amount', text='state', size='transaction_count', template=template)
st.plotly_chart(fig_scatter, use_container_width=True, key="scatter")

# Violin
st.subheader("🎻 Distribution by Type")
fig_violin = px.violin(df_main, x='transaction_type', y='transaction_amount', box=True, points='all', template=template)
st.plotly_chart(fig_violin, use_container_width=True, key="violin")

# Sunburst
st.subheader("☀️ Hierarchy")
sunburst_df = df_main.groupby(['state','transaction_type'])['transaction_count'].sum().reset_index()
fig_sunburst = px.sunburst(sunburst_df, path=['state','transaction_type'], values='transaction_count', template=template)
st.plotly_chart(fig_sunburst, use_container_width=True, key="sunburst")

# Data Table
st.subheader("📋 Raw Data")
st.dataframe(df_main, use_container_width=True, height=400)
csv = df_main.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name=f"phonepe_{selected_year}_Q{selected_quarter}.csv", mime='text/csv', key="download")

st.caption(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")