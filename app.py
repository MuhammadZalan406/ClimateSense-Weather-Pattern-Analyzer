# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from utils import WeatherAnalyzer

st.set_page_config(
    page_title="ClimateSense - Weather Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    .css-1d391kg {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/weather.png", width=80)
    st.title(" ClimateSense")
    st.markdown("---")
    
    st.subheader(" Controls")
    years = st.slider(" Years of Data", 5, 20, 10, help="Select number of years to simulate")
    seed = st.number_input(" Random Seed", 1, 100, 42, help="For reproducible results")
    
    st.markdown("---")
    st.markdown("** Analysis Options**")
    show_heatmaps = st.checkbox("Show Heatmaps", value=True)
    show_anomalies = st.checkbox("Show Anomalies", value=True)
    show_trends = st.checkbox("Show Trends", value=True)
    
    st.markdown("---")
    st.caption("Built with  using Streamlit")

st.title(" ClimateSense – Weather Pattern Analyzer")
st.markdown("*10-Year Temperature & Rainfall Analysis for Climate Tech & Agriculture AI*")
st.markdown("---")

@st.cache_resource
def load_analyzer(years, seed):
    return WeatherAnalyzer(years=years, seed=seed)

analyzer = load_analyzer(years, seed)

stats = analyzer.get_statistics()
extremes = analyzer.get_extremes()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FF6B6B;">
        <h3> {stats['temp_mean']}°C</h3>
        <p style="color: #666;">Avg Temperature</p>
        <small> {stats['temp_max']}°C /  {stats['temp_min']}°C</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #4ECDC4;">
        <h3> {stats['rain_mean']} mm</h3>
        <p style="color: #666;">Avg Rainfall</p>
        <small> {stats['rain_max']} mm /  {stats['rain_min']} mm</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FFE66D;">
        <h3> {extremes['hottest']['value']}°C</h3>
        <p style="color: #666;">Hottest Month</p>
        <small>{extremes['hottest']['month']} Y{extremes['hottest']['year']}</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #4D96FF;">
        <h3> {extremes['coldest']['value']}°C</h3>
        <p style="color: #666;">Coldest Month</p>
        <small>{extremes['coldest']['month']} Y{extremes['coldest']['year']}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

with st.expander(" View Raw Data", expanded=False):
    df = analyzer.get_dataframe()
    st.dataframe(df, use_container_width=True, height=400)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download Data as CSV",
        data=csv,
        file_name='weather_data.csv',
        mime='text/csv',
    )

if show_trends:
    st.subheader(" Seasonal Patterns (10-Year Average)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_avg, rain_avg = analyzer.get_seasonal_patterns()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=analyzer.months_names,
            y=temp_avg,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title=' Monthly Temperature Trend',
            xaxis_title='Month',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=analyzer.months_names,
            y=rain_avg,
            name='Rainfall (mm)',
            marker_color='#4ECDC4',
            marker_line_color='#2C7A7A',
            marker_line_width=1.5
        ))
        fig.update_layout(
            title=' Monthly Rainfall Trend',
            xaxis_title='Month',
            yaxis_title='Rainfall (mm)',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

if show_heatmaps:
    st.subheader(" Heatmaps – 10-Year View")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.imshow(
            analyzer.temperature,
            labels=dict(x="Month", y="Year", color="Temperature (°C)"),
            x=analyzer.months_names,
            y=[f"Year {i+1}" for i in range(analyzer.years)],
            color_continuous_scale="RdBu_r",
            aspect="auto",
            title=" Temperature Heatmap"
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.imshow(
            analyzer.rainfall,
            labels=dict(x="Month", y="Year", color="Rainfall (mm)"),
            x=analyzer.months_names,
            y=[f"Year {i+1}" for i in range(analyzer.years)],
            color_continuous_scale="Blues",
            aspect="auto",
            title=" Rainfall Heatmap"
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

if show_anomalies:
    st.subheader(" Anomaly Detection")
    
    anomalies = analyzer.detect_anomalies(threshold=2)
    
    if anomalies:
        st.warning(f" **{len(anomalies)} anomalies detected** out of {analyzer.years * 12} months")
        
        anomaly_df = pd.DataFrame(anomalies)
        st.dataframe(anomaly_df, use_container_width=True)
        
        anomaly_years = [a['year'] for a in anomalies]
        anomaly_months = [analyzer.months_names.index(a['month']) for a in anomalies]
        anomaly_temps = [a['temperature'] for a in anomalies]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[f"{a['year']}-{a['month']}" for a in anomalies],
            y=anomaly_temps,
            mode='markers',
            marker=dict(size=20, color='red', symbol='x'),
            name='Anomalies'
        ))
        fig.update_layout(
            title=' Anomaly Locations (Red = Outliers)',
            xaxis_title='Year-Month',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success(" No anomalies detected! Weather is stable.")

st.subheader(" Extreme Events")
cols = st.columns(4)

extreme_data = [
    (" Hottest", extremes['hottest']['value'], f"{extremes['hottest']['month']} Y{extremes['hottest']['year']}", "#FF6B6B"),
    (" Coldest", extremes['coldest']['value'], f"{extremes['coldest']['month']} Y{extremes['coldest']['year']}", "#4D96FF"),
    (" Wettest", extremes['wettest']['value'], f"{extremes['wettest']['month']} Y{extremes['wettest']['year']}", "#4ECDC4"),
    (" Driest", extremes['driest']['value'], f"{extremes['driest']['month']} Y{extremes['driest']['year']}", "#FFE66D")
]

for col, (label, value, detail, color) in zip(cols, extreme_data):
    with col:
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 15px; text-align: center; 
                    border-bottom: 4px solid {color}; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <h3 style="margin: 0; color: {color};">{value}</h3>
            <p style="margin: 5px 0; font-weight: 500;">{label}</p>
            <small style="color: #888;">{detail}</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p> ClimateSense v1.0 – Built for Climate Tech & Agriculture AI</p>
    <p style="font-size: 12px;">Data simulated using Normal + Binomial distributions</p>
</div>
""", unsafe_allow_html=True)