"""
Dashboard loading utilities with comprehensive progress tracking
"""

import streamlit as st
import time

class DashboardLoader:
    def __init__(self):
        self.total_steps = 0
        self.current_step = 0
        self.progress_bar = None
        self.status_text = None
        
    def initialize(self, total_steps):
        """Initialize the dashboard loader with total steps"""
        self.total_steps = total_steps
        self.current_step = 0
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        
    def update_progress(self, step_name, delay=0.1):
        """Update progress with step name"""
        if self.progress_bar is None:
            return
            
        self.current_step += 1
        progress = min(self.current_step / self.total_steps, 1.0)
        
        self.progress_bar.progress(progress)
        self.status_text.text(f"🎯 {step_name}... ({self.current_step}/{self.total_steps})")
        
        # Small delay to show progress
        time.sleep(delay)
        
    def complete(self):
        """Complete the loading process"""
        if self.progress_bar:
            self.progress_bar.progress(1.0)
            self.status_text.text("✅ Dashboard generation complete!")
            time.sleep(0.5)
            self.progress_bar.empty()
            self.status_text.empty()

# Global loader instance
dashboard_loader = DashboardLoader()

def with_loading(step_name, func, *args, **kwargs):
    """Execute function with loading indicator"""
    try:
        dashboard_loader.update_progress(step_name)
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        st.error(f"Error in {step_name}: {str(e)}")
        return None

def show_comprehensive_loading_screen():
    """Show comprehensive loading screen for entire dashboard"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>🎯 Generating Professional Dashboard</h2>
        <p>Creating comprehensive charts, tables, and analytics...</p>
        <p><em>Large files may take 1-2 minutes. Please be patient.</em></p>
        <div style="margin: 1rem 0;">
            <div style="display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        </div>
    </div>
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize loader with estimated steps
    dashboard_loader.initialize(total_steps=20)  # Increased for more granular progress
    
    return dashboard_loader