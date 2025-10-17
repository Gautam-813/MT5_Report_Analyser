"""
Dark Mode Support for Professional Dashboard
Modern theme switching with consistent styling
"""

import streamlit as st

def get_theme_config():
    """Get current theme configuration"""
    
    # Check if dark mode is enabled
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    return st.session_state.dark_mode

def toggle_dark_mode():
    """Toggle dark mode on/off"""
    st.session_state.dark_mode = not st.session_state.get('dark_mode', False)

def apply_dark_mode_css():
    """Apply enhanced dark mode CSS styling with perfect contrast"""
    
    dark_mode = get_theme_config()
    
    if dark_mode:
        # Enhanced Dark mode CSS with perfect contrast
        st.markdown("""
        <style>
            /* Dark Mode Styling - Enhanced */
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                color: #f1f5f9 !important;
                min-height: 100vh;
            }
            
            /* Enhanced Header - Dark */
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
                filter: brightness(1.2);
                animation: headerGlowDark 3s ease-in-out infinite alternate;
            }
            
            @keyframes headerGlowDark {
                from { filter: brightness(1.2) drop-shadow(0 0 20px rgba(96, 165, 250, 0.3)); }
                to { filter: brightness(1.4) drop-shadow(0 0 30px rgba(167, 139, 250, 0.4)); }
            }
            
            /* Professional Cards - Dark Enhanced */
            .pro-card {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                color: #f1f5f9 !important;
                padding: 2rem;
                border-radius: 16px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 
                    0 10px 25px -5px rgba(0, 0, 0, 0.5),
                    0 8px 10px -6px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(148, 163, 184, 0.1);
                margin: 1.5rem 0;
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
                border-color: rgba(96, 165, 250, 0.4);
            }
            
            .pro-card:hover::before {
                opacity: 1;
            }
            
            /* Enhanced Metrics - Dark */
            .metric-container {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                color: #f1f5f9 !important;
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 5px solid #60a5fa;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 
                    0 4px 6px -1px rgba(0, 0, 0, 0.3),
                    0 2px 4px -1px rgba(0, 0, 0, 0.2);
                margin: 1rem 0;
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
                color: #f1f5f9 !important;
                margin-bottom: 0.25rem;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .metric-label {
                font-size: 0.95rem;
                color: #cbd5e1 !important;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            /* Status Indicators - Dark Enhanced */
            .status-excellent {
                background: linear-gradient(135deg, #059669 0%, #047857 50%, #065f46 100%);
                color: white !important;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(5, 150, 105, 0.6);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            .status-good {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%);
                color: white !important;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(37, 99, 235, 0.6);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            .status-warning {
                background: linear-gradient(135deg, #d97706 0%, #b45309 50%, #92400e 100%);
                color: white !important;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(217, 119, 6, 0.6);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            .status-danger {
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
                color: white !important;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(220, 38, 38, 0.6);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Alert Boxes - Dark Enhanced */
            .alert-success {
                background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
                border: 2px solid #059669;
                border-radius: 12px;
                padding: 1.5rem;
                color: #d1fae5 !important;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
            }
            
            .alert-warning {
                background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
                border: 2px solid #d97706;
                border-radius: 12px;
                padding: 1.5rem;
                color: #fef3c7 !important;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3);
            }
            
            .alert-danger {
                background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);
                border: 2px solid #dc2626;
                border-radius: 12px;
                padding: 1.5rem;
                color: #fecaca !important;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
            }
            
            /* Sidebar Enhancements - Dark */
            .sidebar-section {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 
                    0 4px 6px -1px rgba(0, 0, 0, 0.3),
                    0 2px 4px -1px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            
            .sidebar-section:hover {
                box-shadow: 
                    0 8px 15px -3px rgba(0, 0, 0, 0.4),
                    0 4px 6px -2px rgba(0, 0, 0, 0.3);
                transform: translateY(-2px);
            }
            
            /* Streamlit Components - Dark */
            .stMetric {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                padding: 1rem;
                border-radius: 12px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .stMetric label {
                color: #cbd5e1 !important;
            }
            
            .stMetric [data-testid="metric-value"] {
                color: #f1f5f9 !important;
            }
            
            .stDataFrame {
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(148, 163, 184, 0.2);
                background: #1e293b;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
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
                box-shadow: 0 4px 15px rgba(96, 165, 250, 0.6);
            }
            
            /* Button Enhancements - Dark */
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
                box-shadow: 0 4px 15px rgba(96, 165, 250, 0.6);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(96, 165, 250, 0.8);
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            }
            
            /* Text and Input Contrast - Dark */
            .stSelectbox > div > div {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                border: 2px solid rgba(148, 163, 184, 0.3);
                border-radius: 8px;
                color: #f1f5f9 !important;
            }
            
            .stTextInput > div > div > input {
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                border: 2px solid rgba(148, 163, 184, 0.3);
                border-radius: 8px;
                color: #f1f5f9 !important;
            }
            
            /* Perfect Text Contrast */
            .stMarkdown, .stText, p, span, div {
                color: #f1f5f9 !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #f1f5f9 !important;
            }
            
            /* Custom Scrollbar - Dark */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0f172a;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #60a5fa, #a78bfa);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            }
            
            .status-danger {
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                color: white !important;
                box-shadow: 0 2px 4px rgba(220, 38, 38, 0.4);
            }
            
            /* Enhanced Metrics - Dark */
            .metric-container {
                background: linear-gradient(145deg, #374151 0%, #1f2937 100%);
                border-radius: 10px;
                padding: 1.2rem;
                border-left: 4px solid #60a5fa;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: all 0.2s ease;
            }
            
            .metric-container:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            .metric-value {
                font-size: 2rem;
                font-weight: 700;
                color: #e2e8f0 !important;
                margin-bottom: 0.25rem;
            }
            
            .metric-label {
                font-size: 0.875rem;
                color: #9ca3af !important;
                font-weight: 500;
            }
            
            /* Alert Boxes - Dark */
            .alert-success {
                background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
                border: 1px solid #059669;
                border-radius: 8px;
                padding: 1rem;
                color: #d1fae5 !important;
                margin: 1rem 0;
            }
            
            .alert-warning {
                background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
                border: 1px solid #d97706;
                border-radius: 8px;
                padding: 1rem;
                color: #fef3c7 !important;
                margin: 1rem 0;
            }
            
            .alert-danger {
                background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);
                border: 1px solid #dc2626;
                border-radius: 8px;
                padding: 1rem;
                color: #fecaca !important;
                margin: 1rem 0;
            }
            
            /* Sidebar - Dark */
            .sidebar-section {
                background: linear-gradient(145deg, #374151 0%, #1f2937 100%);
                border-radius: 10px;
                padding: 1.2rem;
                margin: 1rem 0;
                border: 1px solid #4b5563;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            /* Streamlit Components - Dark */
            .stSelectbox > div > div {
                background-color: #374151;
                color: #e2e8f0;
                border-color: #4b5563;
            }
            
            .stSlider > div > div > div {
                background-color: #374151;
            }
            
            .stFileUploader > div {
                background-color: #374151;
                border-color: #4b5563;
            }
            
            /* Progress Bars - Dark */
            .progress-container {
                background: #1f2937;
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                margin: 0.5rem 0;
            }
            
            /* Override Streamlit defaults */
            .stApp .metric-card, .stApp .pro-card, .stApp .sidebar-section {
                color: #e2e8f0 !important;
            }
            
            /* Tabs - Dark */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #374151;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #4b5563;
                color: #e2e8f0;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #60a5fa;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    
    else:
        # Light mode CSS (existing styling)
        st.markdown("""
        <style>
            /* Light Mode Styling (Default) */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #1a202c;
            }
            
            /* Keep existing light mode styles */
        </style>
        """, unsafe_allow_html=True)

def create_theme_toggle():
    """Create theme toggle button in sidebar"""
    
    dark_mode = get_theme_config()
    
    # Theme toggle button
    if st.button(
        f"🌙 Dark Mode" if not dark_mode else "☀️ Light Mode",
        help="Toggle between light and dark themes",
        key="theme_toggle"
    ):
        toggle_dark_mode()
        st.rerun()
    
    return get_theme_config()

def get_chart_theme():
    """Get appropriate chart theme based on current mode"""
    
    dark_mode = get_theme_config()
    return 'dark' if dark_mode else 'light'

def get_plotly_template():
    """Get Plotly template based on current theme"""
    
    dark_mode = get_theme_config()
    
    if dark_mode:
        return {
            'layout': {
                'plot_bgcolor': '#1e1e1e',
                'paper_bgcolor': '#1e1e1e',
                'font': {'color': '#e2e8f0'},
                'colorway': ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb7185'],
                'xaxis': {
                    'gridcolor': '#374151',
                    'linecolor': '#4b5563',
                    'tickcolor': '#4b5563'
                },
                'yaxis': {
                    'gridcolor': '#374151',
                    'linecolor': '#4b5563',
                    'tickcolor': '#4b5563'
                }
            }
        }
    else:
        return {
            'layout': {
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'font': {'color': '#1f2937'},
                'colorway': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],
                'xaxis': {
                    'gridcolor': '#f3f4f6',
                    'linecolor': '#d1d5db',
                    'tickcolor': '#d1d5db'
                },
                'yaxis': {
                    'gridcolor': '#f3f4f6',
                    'linecolor': '#d1d5db',
                    'tickcolor': '#d1d5db'
                }
            }
        }