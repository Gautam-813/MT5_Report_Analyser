"""
WebSocket optimization utilities for Streamlit
Helps prevent WebSocket connection issues during heavy processing
"""

import time
import streamlit as st

def safe_chart_display(chart_func, *args, **kwargs):
    """
    Safely display charts with WebSocket optimization
    """
    try:
        # Add small delay to prevent WebSocket overload
        time.sleep(0.1)
        
        # Generate and display chart
        fig = chart_func(*args, **kwargs)
        st.plotly_chart(fig, use_container_width=True)
        
        return True
    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")
        return False

def batch_process_with_delays(items, process_func, delay=0.2):
    """
    Process items in batches with delays to prevent WebSocket issues
    """
    results = []
    
    for i, item in enumerate(items):
        try:
            result = process_func(item)
            results.append(result)
            
            # Add delay between items
            if i < len(items) - 1:  # Don't delay after last item
                time.sleep(delay)
                
        except Exception as e:
            print(f"Error processing item {i}: {str(e)}")
            results.append(None)
    
    return results

def optimize_streamlit_performance():
    """
    Apply performance optimizations for Streamlit
    """
    # Configure Streamlit for better performance
    if hasattr(st, 'set_option'):
        try:
            # Reduce WebSocket message frequency
            st.set_option('client.showErrorDetails', False)
            st.set_option('client.toolbarMode', 'minimal')
        except:
            pass  # Ignore if options don't exist