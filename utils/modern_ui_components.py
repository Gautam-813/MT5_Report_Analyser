"""
Modern UI Components
Advanced UI/UX components based on latest fintech design trends
"""

import streamlit as st
import plotly.graph_objects as go
import time

class ModernUIComponents:
    """Modern UI components for enhanced user experience"""
    
    def __init__(self):
        self.colors = self._get_modern_colors()
    
    def _get_modern_colors(self):
        """Modern color palette inspired by top fintech apps"""
        return {
            'primary': '#6366f1',      # Modern indigo
            'secondary': '#8b5cf6',    # Modern purple  
            'success': '#10b981',      # Modern green
            'warning': '#f59e0b',      # Modern amber
            'danger': '#ef4444',       # Modern red
            'info': '#06b6d4',        # Modern cyan
            'background': '#0f172a',   # Deep dark
            'surface': '#1e293b',      # Card background
            'text': '#f1f5f9',        # Light text
            'muted': '#64748b'         # Muted text
        }
    
    def create_animated_metric_card(self, title, value, change=None, icon="📊", status="neutral"):
        """Create animated metric card with modern styling"""
        
        # Determine colors based on status
        status_colors = {
            'excellent': self.colors['success'],
            'good': self.colors['info'],
            'warning': self.colors['warning'],
            'danger': self.colors['danger'],
            'neutral': self.colors['primary']
        }
        
        color = status_colors.get(status, self.colors['primary'])
        
        # Create change indicator
        change_html = ""
        if change is not None:
            change_color = self.colors['success'] if change >= 0 else self.colors['danger']
            change_icon = "↗️" if change >= 0 else "↘️"
            change_html = f"""
            <div style="display: flex; align-items: center; gap: 0.25rem; margin-top: 0.5rem;">
                <span style="color: {change_color}; font-size: 0.9rem;">{change_icon}</span>
                <span style="color: {change_color}; font-size: 0.9rem; font-weight: 600;">
                    {abs(change):.1f}%
                </span>
            </div>
            """
        
        st.markdown(f"""
        <div class="modern-metric-card" style="
            background: linear-gradient(145deg, {self.colors['surface']} 0%, rgba(99, 102, 241, 0.05) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-4px) scale(1.02)'; this.style.boxShadow='0 20px 40px rgba(99, 102, 241, 0.15)';" 
           onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 4px 6px rgba(0, 0, 0, 0.1)';">
            
            <!-- Animated background gradient -->
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, {color}, rgba(99, 102, 241, 0.5));
                animation: shimmer 2s infinite;
            "></div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <span style="
                            color: {self.colors['muted']};
                            font-size: 0.9rem;
                            font-weight: 500;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        ">{title}</span>
                    </div>
                    
                    <div style="
                        font-size: 2rem;
                        font-weight: 700;
                        color: {color};
                        line-height: 1;
                        margin-bottom: 0.5rem;
                    ">{value}</div>
                    
                    {change_html}
                </div>
            </div>
        </div>
        
        <style>
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .modern-metric-card:hover {{
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_progress_indicator(self, current, target, title, subtitle=""):
        """Create modern progress indicator with animations"""
        
        percentage = min(100, (current / target * 100)) if target > 0 else 0
        
        st.markdown(f"""
        <div style="
            background: {self.colors['surface']};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(99, 102, 241, 0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h4 style="margin: 0; color: {self.colors['text']}; font-size: 1.1rem;">{title}</h4>
                    {f'<p style="margin: 0.25rem 0 0 0; color: {self.colors["muted"]}; font-size: 0.9rem;">{subtitle}</p>' if subtitle else ''}
                </div>
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: {self.colors['primary']};
                ">{percentage:.1f}%</div>
            </div>
            
            <div style="
                background: rgba(99, 102, 241, 0.1);
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    background: linear-gradient(90deg, {self.colors['primary']}, {self.colors['secondary']});
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 10px;
                    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                    overflow: hidden;
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                        animation: progress-shimmer 2s infinite;
                    "></div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.8rem; color: {self.colors['muted']};">
                <span>Current: {current}</span>
                <span>Target: {target}</span>
            </div>
        </div>
        
        <style>
        @keyframes progress-shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_interactive_notification(self, message, type="info", action_text=None, dismissible=True):
        """Create modern notification with actions"""
        
        type_config = {
            'success': {'color': self.colors['success'], 'icon': '✅', 'bg': 'rgba(16, 185, 129, 0.1)'},
            'warning': {'color': self.colors['warning'], 'icon': '⚠️', 'bg': 'rgba(245, 158, 11, 0.1)'},
            'danger': {'color': self.colors['danger'], 'icon': '🚨', 'bg': 'rgba(239, 68, 68, 0.1)'},
            'info': {'color': self.colors['info'], 'icon': '💡', 'bg': 'rgba(6, 182, 212, 0.1)'}
        }
        
        config = type_config.get(type, type_config['info'])
        
        action_html = ""
        if action_text:
            action_html = f"""
            <button style="
                background: {config['color']};
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 6px;
                font-size: 0.9rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            " onmouseover="this.style.opacity='0.8';" onmouseout="this.style.opacity='1';">
                {action_text}
            </button>
            """
        
        dismiss_html = ""
        if dismissible:
            dismiss_html = f"""
            <button onclick="this.parentElement.style.display='none';" style="
                background: none;
                border: none;
                color: {self.colors['muted']};
                font-size: 1.2rem;
                cursor: pointer;
                padding: 0;
                margin-left: 1rem;
            ">×</button>
            """
        
        st.markdown(f"""
        <div style="
            background: {config['bg']};
            border: 1px solid {config['color']};
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            animation: slideIn 0.3s ease-out;
        ">
            <span style="font-size: 1.2rem;">{config['icon']}</span>
            <div style="flex: 1; color: {self.colors['text']};">{message}</div>
            {action_html}
            {dismiss_html}
        </div>
        
        <style>
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_modern_tabs(self, tabs_config):
        """Create modern tab interface with smooth transitions"""
        
        # Create tab headers
        tab_headers = []
        for i, (title, icon) in enumerate(tabs_config):
            tab_headers.append(f"""
            <div class="modern-tab" data-tab="{i}" style="
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-weight: 600;
                color: {self.colors['muted']};
                background: transparent;
            " onclick="switchTab({i})">
                <span>{icon}</span>
                <span>{title}</span>
            </div>
            """)
        
        st.markdown(f"""
        <div style="
            background: {self.colors['surface']};
            border-radius: 12px;
            padding: 0.5rem;
            margin: 1rem 0;
            display: flex;
            gap: 0.5rem;
            overflow-x: auto;
        ">
            {''.join(tab_headers)}
        </div>
        
        <style>
        .modern-tab:hover {{
            background: rgba(99, 102, 241, 0.1) !important;
            color: {self.colors['primary']} !important;
        }}
        
        .modern-tab.active {{
            background: {self.colors['primary']} !important;
            color: white !important;
        }}
        </style>
        
        <script>
        function switchTab(index) {{
            // Remove active class from all tabs
            document.querySelectorAll('.modern-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Add active class to clicked tab
            document.querySelector(`[data-tab="${{index}}"]`).classList.add('active');
        }}
        
        // Set first tab as active by default
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelector('[data-tab="0"]').classList.add('active');
        }});
        </script>
        """, unsafe_allow_html=True)
    
    def create_loading_animation(self, message="Processing your analysis..."):
        """Create modern loading animation"""
        
        st.markdown(f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            text-align: center;
        ">
            <div class="modern-loader" style="
                width: 60px;
                height: 60px;
                border: 3px solid rgba(99, 102, 241, 0.1);
                border-top: 3px solid {self.colors['primary']};
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-bottom: 1.5rem;
            "></div>
            
            <h3 style="
                color: {self.colors['text']};
                margin: 0 0 0.5rem 0;
                font-weight: 600;
            ">{message}</h3>
            
            <p style="
                color: {self.colors['muted']};
                margin: 0;
                font-size: 0.9rem;
            ">This may take a few moments...</p>
            
            <div style="
                display: flex;
                gap: 0.25rem;
                margin-top: 1rem;
            ">
                <div class="dot" style="
                    width: 8px;
                    height: 8px;
                    background: {self.colors['primary']};
                    border-radius: 50%;
                    animation: bounce 1.4s infinite ease-in-out both;
                "></div>
                <div class="dot" style="
                    width: 8px;
                    height: 8px;
                    background: {self.colors['primary']};
                    border-radius: 50%;
                    animation: bounce 1.4s infinite ease-in-out both;
                    animation-delay: -0.32s;
                "></div>
                <div class="dot" style="
                    width: 8px;
                    height: 8px;
                    background: {self.colors['primary']};
                    border-radius: 50%;
                    animation: bounce 1.4s infinite ease-in-out both;
                    animation-delay: -0.16s;
                "></div>
            </div>
        </div>
        
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @keyframes bounce {{
            0%, 80%, 100% {{
                transform: scale(0);
            }}
            40% {{
                transform: scale(1);
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_smart_tooltip(self, content, tooltip_text):
        """Create interactive tooltip with rich content"""
        
        st.markdown(f"""
        <div class="tooltip-container" style="position: relative; display: inline-block;">
            {content}
            <div class="tooltip" style="
                visibility: hidden;
                opacity: 0;
                position: absolute;
                bottom: 125%;
                left: 50%;
                margin-left: -120px;
                width: 240px;
                background: {self.colors['surface']};
                color: {self.colors['text']};
                text-align: center;
                border-radius: 8px;
                padding: 1rem;
                z-index: 1000;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(99, 102, 241, 0.2);
                transition: all 0.3s;
                font-size: 0.9rem;
                line-height: 1.4;
            ">
                {tooltip_text}
                <div style="
                    position: absolute;
                    top: 100%;
                    left: 50%;
                    margin-left: -5px;
                    width: 0;
                    height: 0;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid {self.colors['surface']};
                "></div>
            </div>
        </div>
        
        <style>
        .tooltip-container:hover .tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateY(-5px);
        }}
        </style>
        """, unsafe_allow_html=True)