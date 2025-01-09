import streamlit as st
import pandas as pd
from squid_game import generate_synthetic_data, calculate_metrics, create_dashboard

st.set_page_config(layout="wide")

st.title("Netflix OpenConnect ISP Analytics Dashboard")

# Sidebar controls
st.sidebar.header("Dashboard Controls")
days = st.sidebar.slider("Days of Data", 7, 90, 30)
cache_efficiency = st.sidebar.slider("Cache Efficiency", 0.8, 1.0, 0.95)
peak_traffic = st.sidebar.slider("Peak Traffic (Gbps)", 50, 200, 100)

# Generate data
df = generate_synthetic_data(days=days)

# Calculate metrics
metrics = calculate_metrics(df)

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Peak Traffic (Gbps)", f"{metrics['peak_traffic']:.1f}")
with col2:
    st.metric("95th Percentile", f"{metrics['p95_traffic']:.1f}")
with col3:
    st.metric("Cache Hit Rate", f"{metrics['avg_cache_hit']:.2%}")
with col4:
    st.metric("Monthly Savings", f"${metrics['total_savings']:,.2f}")

# Display dashboard
st.plotly_chart(create_dashboard(df), use_container_width=True)

# Detailed metrics tables
st.header("Detailed Metrics")
tabs = st.tabs(["Infrastructure", "Network", "Cache", "Cost Analysis"])

with tabs[0]:
    st.subheader("Infrastructure Metrics")
    inf_metrics = pd.DataFrame({
        'Metric': ['Power Usage (kW/h)', 'Cooling Cost ($/month)', 'Rack Space (U)', 'Port Cost ($/month)'],
        'Value': [3.2, 1200, 42, 2000],
        'Trend': ['↑', '↓', '→', '↓']
    })
    st.table(inf_metrics)

with tabs[1]:
    st.subheader("Network Performance")
    st.line_chart(df[['traffic_gbps', 'transit_savings_gbps']])

with tabs[2]:
    st.subheader("Cache Performance")
    st.line_chart(df['cache_hit_rate'])

with tabs[3]:
    st.subheader("Cost Analysis")
    st.line_chart(df['cost_savings'].cumsum())

# Download section
st.download_button(
    label="Download Full Report",
    data=df.to_csv().encode('utf-8'),
    file_name='isp_metrics_report.csv',
    mime='text/csv',
)