"""
Enhanced Styling Module
Modern CSS and styling enhancements based on latest UI/UX trends
"""

def get_modern_css():
    """Get modern CSS styling inspired by top fintech platforms"""
    
    return """
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* CSS Variables for Consistent Theming */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #06b6d4;
        --background: #0f172a;
        --surface: #1e293b;
        --surface-light: #334155;
        --text: #f1f5f9;
        --text-muted: #64748b;
        --border: rgba(99, 102, 241, 0.2);
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 20px 40px rgba(0, 0, 0, 0.15);
        --radius: 12px;
        --radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Global Enhancements */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, var(--background) 0%, #1e293b 100%);
        color: var(--text);
        line-height: 1.6;
    }
    
    /* Modern Card Styling */
    .modern-card {
        background: linear-gradient(145deg, var(--surface) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .modern-card:hover::before {
        opacity: 1;
    }
    
    /* Enhanced Metrics Display */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-item {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .metric-item:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    
    .metric-change.positive {
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
    }
    
    .metric-change.negative {
        background: rgba(239, 68, 68, 0.2);
        color: var(--danger);
    }
    
    /* Modern Button Styling */
    .modern-button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .modern-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    .modern-button:active {
        transform: translateY(0);
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--surface);
        padding: 0.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background: transparent;
        border-radius: 8px;
        color: var(--text-muted);
        font-weight: 600;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(99, 102, 241, 0.1);
        color: var(--primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    /* Modern Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--surface) 0%, var(--background) 100%);
        border-right: 1px solid var(--border);
    }
    
    .sidebar-section {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin: 1.5rem 0;
        transition: var(--transition);
    }
    
    .sidebar-section:hover {
        box-shadow: var(--shadow);
        transform: translateY(-2px);
        border-color: var(--primary);
    }
    
    /* Enhanced Input Styling */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--surface) !important;
        border: 2px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        transition: var(--transition) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Modern Progress Bars */
    .progress-modern {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        height: 100%;
        border-radius: 10px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    /* Status Indicators */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-excellent {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .status-good {
        background: linear-gradient(135deg, var(--info) 0%, #0891b2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }
    
    .status-warning {
        background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    
    .status-danger {
        background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Modern Alerts */
    .alert-modern {
        border-radius: var(--radius);
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
        position: relative;
        overflow: hidden;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border-left-color: var(--success);
        color: var(--text);
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border-left-color: var(--warning);
        color: var(--text);
    }
    
    .alert-danger {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: var(--danger);
        color: var(--text);
    }
    
    .alert-info {
        background: rgba(6, 182, 212, 0.1);
        border-left-color: var(--info);
        color: var(--text);
    }
    
    /* Animations */
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Grid Layout */
    .metric-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Utility Classes */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.4s ease-out;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-dark), var(--secondary));
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .modern-card {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .metric-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
    
    /* Dark Theme Enhancements */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, div, span, label, strong, em, li, td, th {
        color: var(--text) !important;
    }
    
    /* Force text visibility */
    * {
        color: var(--text) !important;
    }
    
    /* Exception for buttons and special elements */
    .stButton > button, .modern-button {
        color: white !important;
    }
    
    /* Enhanced data tables */
    .stDataFrame {
        border-radius: var(--radius);
        overflow: hidden;
        background-color: var(--surface);
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }
    
    /* Modern loading states */
    .stSpinner {
        border-color: var(--primary) !important;
    }
    
    /* Enhanced metrics */
    .stMetric {
        background: var(--surface);
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    
    .stMetric:hover {
        box-shadow: var(--shadow);
        transform: translateY(-2px);
    }
    </style>
    """

def get_interactive_enhancements():
    """Get JavaScript enhancements for interactivity"""
    
    return """
    <script>
    // Modern UI Enhancements
    document.addEventListener('DOMContentLoaded', function() {
        
        // Add fadeIn animation to cards
        const cards = document.querySelectorAll('.modern-card, .metric-item');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('fade-in');
        });
        
        // Add hover effects to metrics
        const metrics = document.querySelectorAll('.stMetric');
        metrics.forEach(metric => {
            metric.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(99, 102, 241, 0.15)';
            });
            
            metric.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            });
        });
        
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Add loading states to buttons
        const buttons = document.querySelectorAll('.stButton > button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const originalText = this.textContent;
                this.textContent = 'Processing...';
                this.disabled = true;
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 2000);
            });
        });
        
        // Progressive enhancement for charts
        const charts = document.querySelectorAll('.js-plotly-plot');
        charts.forEach(chart => {
            chart.style.opacity = '0';
            chart.style.transform = 'translateY(20px)';
            chart.style.transition = 'all 0.6s ease-out';
            
            setTimeout(() => {
                chart.style.opacity = '1';
                chart.style.transform = 'translateY(0)';
            }, 300);
        });
    });
    
    // Utility functions for modern interactions
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert-modern alert-${type} slide-in`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span>${type === 'success' ? '✅' : type === 'warning' ? '⚠️' : type === 'danger' ? '🚨' : '💡'}</span>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: none; border: none; color: inherit; 
                    font-size: 1.2rem; cursor: pointer; margin-left: auto;
                ">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    function animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.round(current);
            
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                element.textContent = end;
                clearInterval(timer);
            }
        }, 16);
    }
    </script>
    """