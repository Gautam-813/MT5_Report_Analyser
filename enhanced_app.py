"""
Enhanced MT5 Strategy Tester Report Analyzer
Professional, Interactive Dashboard with Advanced Features
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Import our custom modules
from utils.parser import parse_uploaded_report
from utils.analyzer import MT5DataAnalyzer
from utils.safe_formatting import (
    safe_format_currency, safe_format_number, safe_format_integer, 
    safe_format_percentage, safe_format_ratio
)
from utils.visualizations import (
    create_daily_pnl_heatmap,
    create_session_performance_chart,
    create_equity_curve,
    create_hourly_performance_chart,
    create_loss_distribution_chart,
    create_session_comparison_chart,
    create_worst_days_chart,
    create_metrics_gauge_chart,
    # New bar charts
    create_entries_by_hours_chart,
    create_entries_by_weekdays_chart,
    create_entries_by_months_chart,
    create_pnl_by_hours_chart,
    create_pnl_by_weekdays_chart,
    create_pnl_by_months_chart
)

# Professional features
from utils.monte_carlo import MonteCarloSimulator, create_monte_carlo_dashboard
from utils.pdf_generator import ProfessionalReportGenerator, create_pdf_download_button
from utils.dark_mode import apply_dark_mode_css, create_theme_toggle, get_chart_theme
from utils.enhanced_charts import (
    create_professional_equity_curve,
    create_advanced_risk_dashboard,
    create_interactive_performance_heatmap,
    create_session_performance_radar
)
from utils.interactive_components import (
    create_interactive_equity_curve,
    create_performance_heatmap,
    create_risk_gauge_dashboard,
    create_trade_distribution_analysis,
    create_comparison_tool
)

# Enhanced page configuration
st.set_page_config(
    page_title="MT5 Pro Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/mt5-analyzer',
        'Report a bug': 'https://github.com/your-repo/mt5-analyzer/issues',
        'About': "# MT5 Professional Report Analyzer\nAdvanced trading strategy analysis tool"
    }
)

# Professional DARK THEME CSS for perfect readability
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Dark Theme Styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
        line-height: 1.6;
    }
    
    /* Streamlit Components Dark Theme */
    .stApp > div {
        background-color: #0f172a;
    }
    
    /* Sidebar Dark Theme */
    .css-1d391kg {
        background-color: #1e293b;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: transparent;
        color: #f1f5f9;
    }
    
    /* Remove Streamlit branding and padding */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp > div > div > div > div > section > div {
        padding-top: 1rem;
    }
    
    /* Dark Theme Header with Animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
        text-shadow: 0 4px 8px rgba(255,255,255,0.1);
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.1); }
    }
    
    /* Dark Theme Professional Cards */
    .pro-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: #f1f5f9;
        box-shadow: 
            0 10px 25px -5px rgba(0, 0, 0, 0.4),
            0 8px 10px -6px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .pro-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .pro-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 20px 40px -10px rgba(0, 0, 0, 0.6),
            0 16px 20px -12px rgba(0, 0, 0, 0.4);
        border-color: rgba(96, 165, 250, 0.5);
    }
    
    .pro-card:hover::before {
        opacity: 1;
    }
    
    /* Status Indicators - Enhanced */
    .status-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-good {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Dark Theme Metrics - Premium Design */
    .metric-container {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #60a5fa;
        margin: 1rem 0;
        color: #f1f5f9;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.3),
            0 2px 4px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.1));
        pointer-events: none;
    }
    
    .metric-container:hover {
        transform: translateX(4px);
        box-shadow: 
            0 8px 15px -3px rgba(0, 0, 0, 0.4),
            0 4px 6px -2px rgba(0, 0, 0, 0.3);
        border-left-color: #3b82f6;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #cbd5e1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Dark Theme Interactive Elements */
    .filter-container {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #f1f5f9;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Dark Theme Progress Bars */
    .progress-container {
        background: linear-gradient(90deg, #374151, #4b5563);
        border-radius: 15px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 15px;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .progress-excellent { 
        background: linear-gradient(90deg, #10b981, #059669, #047857);
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
    }
    .progress-good { 
        background: linear-gradient(90deg, #3b82f6, #1d4ed8, #1e40af);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }
    .progress-warning { 
        background: linear-gradient(90deg, #f59e0b, #d97706, #b45309);
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
    }
    .progress-danger { 
        background: linear-gradient(90deg, #ef4444, #dc2626, #b91c1c);
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
    }
    
    /* Sidebar Enhancements - Premium Dark Theme */
    .sidebar-section {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #f1f5f9;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.3),
            0 2px 4px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        box-shadow: 
            0 8px 15px -3px rgba(0, 0, 0, 0.1),
            0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    /* Alert Boxes - Enhanced Dark Theme */
    .alert-success {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        color: #d1fae5;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .alert-success::before {
        content: '✅';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        color: #fef3c7;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .alert-warning::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        color: #fecaca;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .alert-danger::before {
        content: '🚨';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* Dark Theme Streamlit Components */
    .stMetric {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #f1f5f9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        background-color: #1e293b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background: transparent;
        border-radius: 8px;
        color: #cbd5e1;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(96, 165, 250, 0.4);
    }
    
    /* Dark Theme Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(96, 165, 250, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(96, 165, 250, 0.6);
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    }
    
    /* Dark Theme Input Enhancements */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        color: #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #60a5fa;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        border: 2px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        color: #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }
    
    /* Dark Theme Loading Animation */
    .stSpinner {
        border-color: #60a5fa !important;
    }
    
    /* Dark Theme Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    }
    
    /* MAXIMUM TEXT VISIBILITY - FORCE WHITE TEXT EVERYWHERE */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, div, span, label, strong, em, li, td, th {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* Force all Streamlit text elements to be white */
    [data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
    }
    
    /* Metric text visibility */
    .stMetric label, .stMetric div {
        color: #ffffff !important;
    }
    
    /* Sidebar text visibility */
    .css-1d391kg *, .css-1lcbmhc * {
        color: #ffffff !important;
    }
    
    /* Sidebar Dark Theme with Perfect Text Visibility */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    /* Force sidebar text to be white */
    .css-1d391kg * {
        color: #ffffff !important;
    }
    
    /* Success/Info/Warning Messages with Perfect Visibility */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.2) !important;
        border: 1px solid #10b981 !important;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: rgba(96, 165, 250, 0.2) !important;
        border: 1px solid #60a5fa !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.2) !important;
        border: 1px solid #f59e0b !important;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.2) !important;
        border: 1px solid #ef4444 !important;
        color: #ffffff !important;
    }
    
    /* ULTIMATE TEXT VISIBILITY OVERRIDE */
    * {
        color: #ffffff !important;
    }
    
    /* Exception for buttons and special elements that need their own colors */
    .stButton > button {
        color: white !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    }
    
    /* FINAL OVERRIDE - MAXIMUM TEXT VISIBILITY */
    .stApp, .stApp *, [data-testid] *, .main *, .sidebar * {
        color: #ffffff !important;
    }
    
    /* Keep button colors proper */
    .stButton > button, .stDownloadButton > button {
        color: white !important;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

def create_performance_score(risk_metrics):
    """Calculate overall performance score"""
    score = 0
    max_score = 100
    
    # Profit Factor (25 points)
    pf = risk_metrics.get('profit_factor', 0)
    if pf >= 2.0:
        score += 25
    elif pf >= 1.5:
        score += 20
    elif pf >= 1.2:
        score += 15
    elif pf >= 1.0:
        score += 10
    
    # Win Rate (25 points)
    wr = risk_metrics.get('win_rate', 0)
    if wr >= 70:
        score += 25
    elif wr >= 60:
        score += 20
    elif wr >= 50:
        score += 15
    elif wr >= 40:
        score += 10
    
    # Sharpe Ratio (25 points)
    sr = risk_metrics.get('sharpe_ratio', 0)
    if sr >= 2.0:
        score += 25
    elif sr >= 1.0:
        score += 20
    elif sr >= 0.5:
        score += 15
    elif sr >= 0.0:
        score += 10
    
    # Risk Management (25 points) - Based on profit factor instead of drawdown
    pf_bonus = risk_metrics.get('profit_factor', 1.0)
    if pf_bonus >= 3.0:
        score += 25
    elif pf_bonus >= 2.5:
        score += 20
    elif pf_bonus >= 2.0:
        score += 15
    elif pf_bonus >= 1.5:
        score += 10
    
    return min(score, max_score)

def get_performance_status(score):
    """Get performance status based on score"""
    if score >= 80:
        return "Excellent", "status-excellent", "#10b981"
    elif score >= 60:
        return "Good", "status-good", "#3b82f6"
    elif score >= 40:
        return "Average", "status-warning", "#f59e0b"
    else:
        return "Poor", "status-danger", "#ef4444"

def create_enhanced_sidebar():
    """Create enhanced sidebar with professional styling"""
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎛️ **Control Panel**")
        
        # File Upload Section
        st.markdown("#### 📁 **Upload Report**")
        uploaded_file = st.file_uploader(
            "Choose MT5 Report (HTML or CSV)",
            type=['html', 'htm', 'csv'],
            help="Upload the HTML report generated by MT5 Strategy Tester"
        )
        
        if uploaded_file:
            st.success("✅ Report uploaded successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis Settings - Always show, with defaults
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ **Analysis Settings**")
        
        # Chart Theme
        chart_theme = st.selectbox(
            "🎨 Chart Theme",
            ["Light", "Dark", "Auto"],
            help="Choose chart theme for better visibility"
        )
        
        # Analysis Depth
        analysis_depth = st.selectbox(
            "🔍 Analysis Depth",
            ["Standard", "Detailed", "Expert"],
            help="Choose level of analysis detail"
        )
        
        # Risk Tolerance
        risk_tolerance = st.slider(
            "⚠️ Risk Tolerance",
            min_value=1,
            max_value=10,
            value=5,
            help="Adjust risk assessment sensitivity"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return uploaded_file, chart_theme.lower(), analysis_depth, risk_tolerance

def create_performance_dashboard(risk_metrics, summary_dict):
    """Create enhanced performance dashboard"""
    
    # Calculate performance score
    score = create_performance_score(risk_metrics)
    status, status_class, status_color = get_performance_status(score)
    
    # Performance Overview
    st.markdown("## 🎯 **Performance Overview**")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="pro-card">
            <h3>Overall Performance Score</h3>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 3rem; font-weight: 700; color: {status_color};">{score}</div>
                <div>
                    <div class="{status_class}">{status}</div>
                    <div class="progress-container">
                        <div class="progress-bar progress-{status.lower()}" style="width: {score}%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        profit = risk_metrics.get('total_profit', 0)
        profit_color = "#10b981" if profit >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {profit_color};">{safe_format_currency(profit)}</div>
            <div class="metric-label">Total Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = risk_metrics.get('win_rate', 0)
        wr_color = "#10b981" if win_rate >= 60 else "#f59e0b" if win_rate >= 50 else "#ef4444"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {wr_color};">{win_rate:.1f}%</div>
            <div class="metric-label">Win Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sharpe = risk_metrics.get('sharpe_ratio', 0)
        sharpe_color = "#10b981" if sharpe >= 1.0 else "#f59e0b" if sharpe >= 0.5 else "#ef4444"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {sharpe_color};">{sharpe:.2f}</div>
            <div class="metric-label">Sharpe Ratio</div>
        </div>
        """, unsafe_allow_html=True)

def create_risk_alerts(risk_metrics, analysis_depth):
    """Create risk assessment alerts"""
    
    st.markdown("## ⚠️ **Risk Assessment**")
    
    alerts = []
    
    # Check profit factor
    pf = risk_metrics.get('profit_factor', 0)
    if pf < 1.0:
        alerts.append(("danger", "🚨 Strategy is losing money", f"Profit factor {pf:.2f} indicates losses exceed profits"))
    elif pf < 1.2:
        alerts.append(("warning", "⚠️ Low profitability", f"Profit factor {pf:.2f} shows minimal edge"))
    
    # Check profit consistency instead of drawdown
    total_profit = risk_metrics.get('total_profit', 0)
    if total_profit < 0:
        alerts.append(("danger", "🚨 Strategy is losing money", f"Total profit is negative: ${total_profit:.2f}"))
    
    # Check win rate
    wr = risk_metrics.get('win_rate', 0)
    if wr < 40:
        alerts.append(("danger", "🚨 Very low win rate", f"Only {wr:.1f}% of trades are profitable"))
    elif wr < 50:
        alerts.append(("warning", "⚠️ Below average win rate", f"Win rate of {wr:.1f}% needs improvement"))
    
    # Display alerts
    if alerts:
        for alert_type, title, message in alerts:
            st.markdown(f"""
            <div class="alert-{alert_type}">
                <strong>{title}</strong><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
            <strong>✅ No major risk concerns detected</strong><br>
            Your strategy shows acceptable risk characteristics.
        </div>
        """, unsafe_allow_html=True)

def calculate_performance_score(risk_metrics):
    """Calculate overall performance score (0-100)"""
    try:
        # Weighted scoring system
        profit_factor = risk_metrics.get('profit_factor', 1.0)
        win_rate = risk_metrics.get('win_rate', 50.0)
        sharpe_ratio = risk_metrics.get('sharpe_ratio', 0.0)
        
        # Score components (0-25 each) - No drawdown
        pf_score = min(25, max(0, (profit_factor - 1.0) * 12.5))  # 1.0-3.0 range
        wr_score = min(25, max(0, (win_rate - 40) / 2.4))  # 40-100% range
        sr_score = min(25, max(0, (sharpe_ratio + 1) * 12.5))  # -1 to 1 range
        consistency_score = min(25, max(0, profit_factor * 8))  # Consistency based on profit factor
        
        total_score = pf_score + wr_score + sr_score + consistency_score
        return round(total_score, 1)
    except:
        return 50.0

def assess_risk_level(risk_metrics):
    """Assess overall risk level"""
    try:
        profit_factor = risk_metrics.get('profit_factor', 1.0)
        win_rate = risk_metrics.get('win_rate', 50.0)
        
        if profit_factor < 1.1 or win_rate < 40:
            return "High Risk"
        elif profit_factor < 1.3 or win_rate < 50:
            return "Medium Risk"
        else:
            return "Low Risk"
    except:
        return "Unknown Risk"

def generate_recommendations(risk_metrics):
    """Generate automated recommendations"""
    recommendations = []
    
    try:
        profit_factor = risk_metrics.get('profit_factor', 1.0)
        win_rate = risk_metrics.get('win_rate', 50.0)
        
        if profit_factor < 1.2:
            recommendations.append("🔧 Improve profit factor by optimizing entry/exit rules")
        
        if win_rate < 50:
            recommendations.append("🎯 Increase win rate through better trade selection")
        
        if profit_factor < 1.5:
            recommendations.append("⚠️ Focus on higher quality trades for better consistency")
        
        if len(recommendations) == 0:
            recommendations.append("✅ Strategy shows good performance characteristics")
            
    except:
        recommendations.append("📊 Analyze more data for better recommendations")
    
    return recommendations

def create_interactive_filters(trades_df):
    """Create interactive filtering options"""
    
    st.markdown("## 🔍 **Interactive Analysis**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        min_date = trades_df['time'].min().date()
        max_date = trades_df['time'].max().date()
        
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    with col2:
        # Session filter
        if 'session' in trades_df.columns:
            sessions = ['All'] + list(trades_df['session'].unique())
            selected_session = st.selectbox("🌍 Trading Session", sessions)
        else:
            selected_session = 'All'
    
    with col3:
        # Profit filter
        profit_filter = st.selectbox(
            "💰 Profit Filter",
            ["All Trades", "Profitable Only", "Losses Only", "Break-even"]
        )
    
    # Apply filters
    filtered_df = trades_df.copy()
    
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['time'].dt.date >= start_date) &
            (filtered_df['time'].dt.date <= end_date)
        ]
    
    # Session filter
    if selected_session != 'All' and 'session' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['session'] == selected_session]
    
    # Profit filter
    if profit_filter == "Profitable Only":
        filtered_df = filtered_df[filtered_df['profit'] > 0]
    elif profit_filter == "Losses Only":
        filtered_df = filtered_df[filtered_df['profit'] < 0]
    elif profit_filter == "Break-even":
        filtered_df = filtered_df[filtered_df['profit'] == 0]
    
    # Show filter results
    if len(filtered_df) != len(trades_df):
        st.info(f"📊 Showing {len(filtered_df):,} of {len(trades_df):,} trades after filtering")
    
    return filtered_df

def main():
    # Enhanced header
    st.markdown('<h1 class="main-header">📊 MT5 Professional Report Analyzer</h1>', unsafe_allow_html=True)
    
    # Create enhanced sidebar
    uploaded_file, chart_theme, analysis_depth, risk_tolerance = create_enhanced_sidebar()
    
    if uploaded_file is None:
        # Welcome screen
        st.markdown("""
        <div class="pro-card" style="text-align: center; padding: 3rem;">
            <h2>🚀 Welcome to MT5 Professional Analyzer</h2>
            <p style="font-size: 1.2rem; color: #6b7280; margin: 2rem 0;">
                Upload your MT5 Strategy Tester report to get started with advanced analysis
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">📊</div>
                    <div>Advanced Analytics</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">🎯</div>
                    <div>Risk Assessment</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">📈</div>
                    <div>Interactive Charts</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Process uploaded file
    print(f"🔍 DEBUG: Processing uploaded file: {uploaded_file.name}")
    with st.spinner("🔄 Processing your MT5 report..."):
        try:
            trades_df, summary_dict = parse_uploaded_report(uploaded_file)
            print(f"✅ DEBUG: File parsed - {len(trades_df)} trades, {len(summary_dict)} summary items")
            
            if trades_df.empty:
                print("❌ DEBUG: No trades found - will show error and return")
                st.error("❌ No trade data found in the report. Please check the file format.")
                return
            
            # Initialize analyzer
            analyzer = MT5DataAnalyzer(trades_df)
            print("✅ DEBUG: Analyzer initialized successfully")
            
        except Exception as e:
            print(f"❌ DEBUG: File processing failed - {str(e)}")
            st.error(f"❌ Error processing report: {str(e)}")
            return
    
    # Get analysis data
    print("🔍 DEBUG: Getting risk metrics from analyzer")
    risk_metrics = analyzer.get_risk_metrics(summary_dict)
    print(f"✅ DEBUG: Risk metrics calculated - {len(risk_metrics)} metrics")
    
    # Create performance dashboard
    create_performance_dashboard(risk_metrics, summary_dict)
    
    # Create risk alerts
    create_risk_alerts(risk_metrics, analysis_depth)
    
    # Interactive filters
    filtered_df = create_interactive_filters(trades_df)
    
    # Update analyzer with filtered data
    if not filtered_df.empty and len(filtered_df) != len(trades_df):
        analyzer = MT5DataAnalyzer(filtered_df)
        risk_metrics = analyzer.get_risk_metrics(summary_dict)
    
    # Core Data Display Section
    st.markdown("---")
    st.markdown("## 📊 **Strategy Analysis Dashboard**")
    
    # Create main analysis tabs
    main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
        "📈 Charts & Visualizations",
        "📋 Data Tables", 
        "📊 Performance Metrics",
        "🎯 Risk Analysis"
    ])
    
    with main_tab1:
        st.markdown("### 📈 **Equity Curve**")
        equity_fig = create_equity_curve(filtered_df)
        st.plotly_chart(equity_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗓️ **Daily P&L Heatmap**")
            try:
                # Get daily stats for heatmap (not raw filtered_df)
                daily_stats = analyzer.get_daily_analysis()
                if not daily_stats.empty:
                    heatmap_fig = create_daily_pnl_heatmap(daily_stats)
                    st.plotly_chart(heatmap_fig, use_container_width=True)
                else:
                    st.info("📊 No daily data available for heatmap")
            except Exception as e:
                st.warning(f"⚠️ Could not create daily heatmap: {str(e)}")
        
        with col2:
            st.markdown("### 🌍 **Session Performance**")
            try:
                # Get session stats for chart (not raw filtered_df)
                session_stats = analyzer.get_session_analysis()
                if not session_stats.empty:
                    session_fig = create_session_performance_chart(session_stats)
                    st.plotly_chart(session_fig, use_container_width=True)
                else:
                    st.info("📊 No session data available for analysis")
            except Exception as e:
                st.warning(f"⚠️ Could not create session chart: {str(e)}")
        
        st.markdown("### ⏰ **Hourly Performance**")
        try:
            # Get hourly stats from analyzer
            hourly_stats = analyzer.get_hourly_analysis()
            if not hourly_stats.empty:
                hourly_fig = create_hourly_performance_chart(hourly_stats)
                st.plotly_chart(hourly_fig, use_container_width=True)
            else:
                st.info("📊 No hourly data available for performance analysis")
        except Exception as e:
            st.warning(f"⚠️ Could not create hourly chart: {str(e)}")
    
    with main_tab2:
        st.markdown("### 📋 **Complete MT5 Summary Statistics**")
        
        # Display all summary statistics in organized sections
        if summary_dict:
            # Create expandable sections for different metric categories
            with st.expander("💰 **Profit & Loss Metrics**", expanded=True):
                profit_metrics = {k: v for k, v in summary_dict.items() 
                                if any(word in k.lower() for word in ['profit', 'loss', 'payoff'])}
                if profit_metrics:
                    df_profit = pd.DataFrame(list(profit_metrics.items()), columns=['Metric', 'Value'])
                    st.dataframe(df_profit, use_container_width=True, hide_index=True)
            
            with st.expander("📊 **Trade Statistics**"):
                trade_metrics = {k: v for k, v in summary_dict.items() 
                               if any(word in k.lower() for word in ['trade', 'deal', 'win', 'consecutive'])}
                if trade_metrics:
                    df_trades = pd.DataFrame(list(trade_metrics.items()), columns=['Metric', 'Value'])
                    st.dataframe(df_trades, use_container_width=True, hide_index=True)
            
            with st.expander("📊 **Performance & Risk Metrics**"):
                risk_metrics_dict = {k: v for k, v in summary_dict.items() 
                                   if any(word in k.lower() for word in ['factor', 'ratio', 'correlation']) 
                                   and 'drawdown' not in k.lower()}
                if risk_metrics_dict:
                    df_risk = pd.DataFrame(list(risk_metrics_dict.items()), columns=['Metric', 'Value'])
                    st.dataframe(df_risk, use_container_width=True, hide_index=True)
            
            with st.expander("⚙️ **System & Account Info**"):
                system_metrics = {k: v for k, v in summary_dict.items() 
                                if any(word in k.lower() for word in ['deposit', 'leverage', 'currency', 'bars', 'ticks'])}
                if system_metrics:
                    df_system = pd.DataFrame(list(system_metrics.items()), columns=['Metric', 'Value'])
                    st.dataframe(df_system, use_container_width=True, hide_index=True)
        
        st.markdown("### 📅 **Daily Performance Analysis**")
        
        # Get daily analysis
        daily_stats = analyzer.get_daily_analysis()
        
        if not daily_stats.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 **Top 10 Profit Days**")
                top_profit_days = daily_stats.nlargest(10, 'profit_sum')[['date', 'profit_sum', 'profit_count', 'win_rate']]
                top_profit_days['profit_sum'] = top_profit_days['profit_sum'].apply(lambda x: f"${x:.2f}")
                top_profit_days['win_rate'] = top_profit_days['win_rate'].apply(lambda x: f"{x:.1f}%")
                top_profit_days.columns = ['Date', 'Daily Profit', 'Trades', 'Win Rate']
                st.dataframe(top_profit_days, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("#### 📉 **Top 10 Loss Days**")
                top_loss_days = daily_stats.nsmallest(10, 'profit_sum')[['date', 'profit_sum', 'profit_count', 'win_rate']]
                top_loss_days['profit_sum'] = top_loss_days['profit_sum'].apply(lambda x: f"${x:.2f}")
                top_loss_days['win_rate'] = top_loss_days['win_rate'].apply(lambda x: f"{x:.1f}%")
                top_loss_days.columns = ['Date', 'Daily Loss', 'Trades', 'Win Rate']
                st.dataframe(top_loss_days, use_container_width=True, hide_index=True)
            
            st.markdown("#### 📊 **Full Daily Data Table**")
            # Show all daily data with proper formatting
            display_daily = daily_stats.copy()
            display_daily['profit_sum'] = display_daily['profit_sum'].apply(lambda x: f"${x:.2f}")
            display_daily['profit_mean'] = display_daily['profit_mean'].apply(lambda x: f"${x:.2f}")
            display_daily['win_rate'] = display_daily['win_rate'].apply(lambda x: f"{x:.1f}%")
            
            # Rename columns for better display (no fake drawdown)
            display_daily.columns = ['Date', 'Total P&L', 'Trades', 'Avg P&L', 'Std Dev', 'Min P&L', 'Max P&L', 
                                   'Loss Sum', 'Win Sum', 'Loss Count', 'Win Count', 'Win Rate']
            
            st.dataframe(display_daily, use_container_width=True, hide_index=True)
            
            # Download button for daily data
            daily_csv = daily_stats.to_csv(index=False)
            st.download_button(
                label="📥 Download Daily Analysis (CSV)",
                data=daily_csv,
                file_name=f"daily_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        st.markdown("### 🌍 **Detailed Session Analysis**")
        
        # Get session analysis
        session_stats = analyzer.get_session_analysis()
        
        if not session_stats.empty:
            # Show best performing session
            best_session = session_stats.loc[session_stats['profit_sum'].idxmax()]
            worst_session = session_stats.loc[session_stats['profit_sum'].idxmin()]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🏆 Best Session", 
                    best_session['session'],
                    f"${best_session['profit_sum']:.2f}"
                )
            
            with col2:
                st.metric(
                    "📉 Worst Session", 
                    worst_session['session'],
                    f"${worst_session['profit_sum']:.2f}"
                )
            
            with col3:
                total_session_profit = session_stats['profit_sum'].sum()
                st.metric(
                    "💰 Total Profit", 
                    f"${total_session_profit:.2f}",
                    f"{len(session_stats)} sessions"
                )
            
            st.markdown("#### 📊 **Full Session Data Table**")
            # Format session data for display
            display_session = session_stats.copy()
            display_session['profit_sum'] = display_session['profit_sum'].apply(lambda x: f"${x:.2f}")
            display_session['profit_mean'] = display_session['profit_mean'].apply(lambda x: f"${x:.2f}")
            display_session['win_rate'] = display_session['win_rate'].apply(lambda x: f"{x:.1f}%")
            
            # Rename columns
            display_session.columns = ['Session', 'Total P&L', 'Trades', 'Avg P&L', 'Std Dev', 'Min P&L', 'Max P&L',
                                     'Loss Sum', 'Win Sum', 'Loss Count', 'Win Count', 'Win Rate', 'Avg Loss', 'Avg Win']
            
            st.dataframe(display_session, use_container_width=True, hide_index=True)
            
            # Download button for session data
            session_csv = session_stats.to_csv(index=False)
            st.download_button(
                label="📥 Download Session Analysis (CSV)",
                data=session_csv,
                file_name=f"session_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        st.markdown("### 📈 **Individual Trades Data**")
        if not filtered_df.empty:
            # Show trade data with proper formatting
            display_df = filtered_df.copy()
            
            # Format columns for better display
            if 'profit' in display_df.columns:
                display_df['profit'] = display_df['profit'].apply(lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A")
            if 'time' in display_df.columns:
                display_df['time'] = display_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(display_df, use_container_width=True)
            
            # Download button for trade data
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Trade Data (CSV)",
                data=csv_data,
                file_name=f"trade_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with main_tab3:
        st.markdown("### 🎯 **Key Performance Indicators**")
        
        # Create KPI cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_trades = len(filtered_df)
            st.metric("Total Trades", f"{total_trades:,}")
        
        with col2:
            total_profit = filtered_df['profit'].sum() if 'profit' in filtered_df.columns else 0
            st.metric("Total Profit", f"${total_profit:.2f}")
        
        with col3:
            win_rate = (len(filtered_df[filtered_df['profit'] > 0]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        with col4:
            avg_profit = filtered_df['profit'].mean() if 'profit' in filtered_df.columns else 0
            st.metric("Avg Profit/Trade", f"${avg_profit:.2f}")
        
        # Performance gauge chart
        st.markdown("### 📊 **Performance Gauge**")
        try:
            gauge_fig = create_metrics_gauge_chart(risk_metrics)
            st.plotly_chart(gauge_fig, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Could not create performance gauge: {str(e)}")
        
        # Loss distribution
        st.markdown("### 📉 **Loss Distribution Analysis**")
        try:
            loss_fig = create_loss_distribution_chart(filtered_df)
            st.plotly_chart(loss_fig, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Could not create loss distribution chart: {str(e)}")
    
    with main_tab4:
        st.markdown("### ⚠️ **Risk Analysis Dashboard**")
        
        # Risk metrics display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 **Trading Performance Metrics**")
            
            # Key trading metrics (no drawdown)
            key_metrics = [
                ('Total Trades', risk_metrics.get('total_trades', 0)),
                ('Win Rate', f"{risk_metrics.get('win_rate', 0):.1f}%"),
                ('Profit Factor', f"{risk_metrics.get('profit_factor', 0):.2f}"),
                ('Risk-Reward Ratio', f"{risk_metrics.get('risk_reward_ratio', 0):.2f}"),
                ('Average Win', f"${risk_metrics.get('avg_winning_trade', 0):.2f}"),
                ('Average Loss', f"${risk_metrics.get('avg_losing_trade', 0):.2f}"),
                ('Largest Win', f"${risk_metrics.get('largest_win', 0):.2f}"),
                ('Largest Loss', f"${risk_metrics.get('largest_loss', 0):.2f}"),
                ('Longest Win Streak', risk_metrics.get('longest_win_streak', 0)),
                ('Longest Loss Streak', risk_metrics.get('longest_loss_streak', 0)),
                ('Current Win Streak', risk_metrics.get('consecutive_wins', 0)),
                ('Current Loss Streak', risk_metrics.get('consecutive_losses', 0))
            ]
            
            metrics_df = pd.DataFrame(key_metrics, columns=['Metric', 'Value'])
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 📈 **Session Comparison**")
            try:
                # Get session stats for comparison (not raw filtered_df)
                session_stats = analyzer.get_session_analysis()
                if not session_stats.empty:
                    session_comp_fig = create_session_comparison_chart(session_stats)
                    st.plotly_chart(session_comp_fig, use_container_width=True)
                else:
                    st.info("📊 No session data available for comparison")
            except Exception as e:
                st.warning(f"⚠️ Could not create session comparison: {str(e)}")
        
        # Worst performing days
        st.markdown("### 📉 **Worst Performing Days**")
        try:
            # Get daily stats for worst days analysis
            daily_stats = analyzer.get_daily_analysis()
            if not daily_stats.empty:
                worst_days = daily_stats.nsmallest(10, 'profit_sum')
                worst_days_fig = create_worst_days_chart(worst_days)
                st.plotly_chart(worst_days_fig, use_container_width=True)
            else:
                st.info("📊 No daily data available for worst days analysis")
        except Exception as e:
            st.warning(f"⚠️ Could not create worst days chart: {str(e)}")
    
    # Professional Features Dashboard
    print("🔍 DEBUG: About to show Professional Analytics Suite")
    st.markdown("---")
    st.success("🎯 **PROFESSIONAL ANALYTICS SUITE IS HERE!** - Scroll down to see 6 tabs below")
    st.markdown("## 🎯 **Professional Analytics Suite**")
    print("✅ DEBUG: Professional Analytics Suite header displayed")
    
    # Create tabs for professional features
    print("🔍 DEBUG: Creating 6 tabs for Professional Analytics Suite")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Advanced Charts", 
        "🎲 Monte Carlo Risk", 
        "📄 Professional Reports", 
        "🔍 Performance Attribution",
        "⚡ Interactive Analysis",
        "📊 Time Analysis Charts"
    ])
    print("✅ DEBUG: All 6 tabs created successfully")
    
    with tab1:
        st.markdown("### 📈 **Enhanced Equity Curve**")
        if 'create_professional_equity_curve' in globals():
            equity_fig = create_professional_equity_curve(filtered_df, get_chart_theme())
            st.plotly_chart(equity_fig, use_container_width=True)
        
        # Advanced Risk Dashboard moved to main Risk Analysis tab to avoid duplication
    
    with tab2:
        st.markdown("### 🎲 **Monte Carlo Risk Simulation**")
        if analysis_depth in ["Detailed", "Expert"]:
            # Monte Carlo settings
            col1, col2 = st.columns(2)
            with col1:
                num_simulations = st.slider("Number of Simulations", 100, 5000, 1000, 100)
            with col2:
                confidence_level = st.selectbox("Confidence Level", [90, 95, 99], index=1)
            
            # Run Monte Carlo simulation
            monte_carlo_results = create_monte_carlo_dashboard(filtered_df, num_simulations)
            
            if monte_carlo_results:
                # Display VaR and Expected Shortfall
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Value at Risk (95%)", f"${monte_carlo_results.get('var_95', 0):.2f}")
                with col2:
                    st.metric("Expected Shortfall", f"${monte_carlo_results.get('expected_shortfall', 0):.2f}")
                with col3:
                    st.metric("Loss Probability", f"{monte_carlo_results.get('loss_probability', 0):.1f}%")
        else:
            st.info("💡 Enable 'Detailed' or 'Expert' analysis depth to access Monte Carlo simulation")
    
    with tab3:
        st.markdown("### 📄 **Professional Report Generation**")
        
        # Report settings
        col1, col2 = st.columns(2)
        with col1:
            report_title = st.text_input("Report Title", "MT5 Strategy Analysis Report")
        with col2:
            include_charts = st.checkbox("Include Charts", True)
        
        # Generate PDF report
        if st.button("🔄 Generate Professional PDF Report", type="primary"):
            with st.spinner("📄 Generating professional report..."):
                try:
                    # Prepare analysis results
                    analysis_results = {
                        'performance_score': calculate_performance_score(risk_metrics),
                        'risk_assessment': assess_risk_level(risk_metrics),
                        'recommendations': generate_recommendations(risk_metrics),
                        'monte_carlo': monte_carlo_results if 'monte_carlo_results' in locals() else None
                    }
                    
                    # Create PDF
                    generator = ProfessionalReportGenerator(
                        filtered_df, summary_dict, risk_metrics, analysis_results
                    )
                    
                    pdf_buffer = generator.generate_report(
                        title=report_title,
                        include_charts=include_charts
                    )
                    
                    # Create download button
                    st.download_button(
                        label="📄 Download Professional PDF Report",
                        data=pdf_buffer,
                        file_name=f"{report_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                    st.success("✅ Professional report generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
    
    with tab4:
        st.markdown("### 🔍 **Multi-Factor Performance Analysis**")
        
        # Performance attribution by session
        if 'session' in filtered_df.columns:
            session_performance = filtered_df.groupby('session')['profit'].agg(['sum', 'count', 'mean']).round(2)
            st.dataframe(session_performance, use_container_width=True)
        
        # Session performance radar
        if 'session' in filtered_df.columns:
            # Get proper session stats from analyzer
            session_stats = analyzer.get_session_analysis()
            if not session_stats.empty:
                radar_fig = create_session_performance_radar(session_stats, get_chart_theme())
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                st.info("📊 No session data available for radar chart")
    
    with tab5:
        st.markdown("### ⚡ **Advanced Interactive Tools**")
        
        # Interactive components dashboard
        gauge_fig = create_risk_gauge_dashboard(risk_metrics)
        st.plotly_chart(gauge_fig, use_container_width=True)
        
        # Trade distribution analysis
        dist_fig = create_trade_distribution_analysis(filtered_df)
        st.plotly_chart(dist_fig, use_container_width=True)
    
    with tab6:
        print("🔍 DEBUG: Entering Tab 6 - Time Analysis Charts")
        st.success("🎉 **YOU FOUND THE 6 BAR CHARTS!** - They are being created below...")
        st.markdown("### 📊 **ALL 6 TIME ANALYSIS CHARTS**")
        st.markdown("**All your requested bar charts in one place - side by side view**")
        print("✅ DEBUG: Tab 6 headers displayed")
        
        # ALL 6 CHARTS SIDE BY SIDE
        print("🔍 DEBUG: About to create all 6 charts")
        st.markdown("#### 📊 **Complete Time Analysis - All 6 Charts**")
        
        # First row: 3 Entry charts
        print("🔍 DEBUG: Creating first row - 3 Entry charts")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            print("🔍 DEBUG: Creating Chart 1 - Entries by Hours")
            st.markdown("##### 🕐 **Entries by Hours**")
            try:
                entries_hours_fig = create_entries_by_hours_chart(filtered_df, get_chart_theme())
                st.plotly_chart(entries_hours_fig, use_container_width=True)
                print("✅ DEBUG: Chart 1 - Entries by Hours displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 1 failed - {str(e)}")
                st.warning(f"⚠️ Could not create entries by hours chart: {str(e)}")
        
        with col2:
            print("🔍 DEBUG: Creating Chart 2 - Entries by Weekdays")
            st.markdown("##### 📅 **Entries by Weekdays**")
            try:
                entries_weekdays_fig = create_entries_by_weekdays_chart(filtered_df, get_chart_theme())
                st.plotly_chart(entries_weekdays_fig, use_container_width=True)
                print("✅ DEBUG: Chart 2 - Entries by Weekdays displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 2 failed - {str(e)}")
                st.warning(f"⚠️ Could not create entries by weekdays chart: {str(e)}")
        
        with col3:
            print("🔍 DEBUG: Creating Chart 3 - Entries by Months")
            st.markdown("##### 📆 **Entries by Months**")
            try:
                entries_months_fig = create_entries_by_months_chart(filtered_df, get_chart_theme())
                st.plotly_chart(entries_months_fig, use_container_width=True)
                print("✅ DEBUG: Chart 3 - Entries by Months displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 3 failed - {str(e)}")
                st.warning(f"⚠️ Could not create entries by months chart: {str(e)}")
        
        # Second row: 3 P&L charts
        print("🔍 DEBUG: Creating second row - 3 P&L charts")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            print("🔍 DEBUG: Creating Chart 4 - P&L by Hours")
            st.markdown("##### 💰 **P&L by Hours**")
            try:
                pnl_hours_fig = create_pnl_by_hours_chart(filtered_df, get_chart_theme())
                st.plotly_chart(pnl_hours_fig, use_container_width=True)
                print("✅ DEBUG: Chart 4 - P&L by Hours displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 4 failed - {str(e)}")
                st.warning(f"⚠️ Could not create P&L by hours chart: {str(e)}")
        
        with col2:
            print("🔍 DEBUG: Creating Chart 5 - P&L by Weekdays")
            st.markdown("##### 💰 **P&L by Weekdays**")
            try:
                pnl_weekdays_fig = create_pnl_by_weekdays_chart(filtered_df, get_chart_theme())
                st.plotly_chart(pnl_weekdays_fig, use_container_width=True)
                print("✅ DEBUG: Chart 5 - P&L by Weekdays displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 5 failed - {str(e)}")
                st.warning(f"⚠️ Could not create P&L by weekdays chart: {str(e)}")
        
        with col3:
            print("🔍 DEBUG: Creating Chart 6 - P&L by Months")
            st.markdown("##### 💰 **P&L by Months**")
            try:
                pnl_months_fig = create_pnl_by_months_chart(filtered_df, get_chart_theme())
                st.plotly_chart(pnl_months_fig, use_container_width=True)
                print("✅ DEBUG: Chart 6 - P&L by Months displayed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Chart 6 failed - {str(e)}")
                st.warning(f"⚠️ Could not create P&L by months chart: {str(e)}")
        
        # Summary insights
        st.markdown("#### 🎯 **Time-Based Insights**")
        
        if not filtered_df.empty and 'time' in filtered_df.columns and 'profit' in filtered_df.columns:
            # Calculate insights
            df_insights = filtered_df.copy()
            df_insights['hour'] = df_insights['time'].dt.hour
            df_insights['weekday'] = df_insights['time'].dt.day_name()
            df_insights['month'] = df_insights['time'].dt.month_name()
            
            # Best performing times
            best_hour = df_insights.groupby('hour')['profit'].sum().idxmax()
            best_weekday = df_insights.groupby('weekday')['profit'].sum().idxmax()
            best_month = df_insights.groupby('month')['profit'].sum().idxmax()
            
            # Most active times
            most_active_hour = df_insights.groupby('hour').size().idxmax()
            most_active_weekday = df_insights.groupby('weekday').size().idxmax()
            most_active_month = df_insights.groupby('month').size().idxmax()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🏆 Best Hour", f"{best_hour}:00")
                st.metric("📊 Most Active Hour", f"{most_active_hour}:00")
            
            with col2:
                st.metric("🏆 Best Weekday", best_weekday)
                st.metric("📊 Most Active Weekday", most_active_weekday)
            
            with col3:
                st.metric("🏆 Best Month", best_month)
                st.metric("📊 Most Active Month", most_active_month)
    
    # Professional summary
    st.markdown("---")
    st.markdown("## 🎉 **Professional Analysis Complete**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Analysis Depth", analysis_depth)
    with col2:
        st.metric("Risk Tolerance", f"{risk_tolerance}/10")
    with col3:
        st.metric("Chart Theme", chart_theme.title())
    
    st.success("🎉 Professional-grade MT5 analysis dashboard loaded successfully!")
    print("🎉 DEBUG: DASHBOARD COMPLETED SUCCESSFULLY - All sections should be visible!")

if __name__ == "__main__":
    print("🚀 DEBUG: Starting enhanced_app.py")
    main()
    print("✅ DEBUG: main() function completed")