"""
Advanced Dashboard Integration
Optional integration of advanced charts into the live trading dashboard
"""

import streamlit as st
from .advanced_live_charts import (
    create_daily_performance_calendar,
    create_cumulative_pnl_curve,
    create_trade_size_vs_profit_scatter,
    create_weekday_performance_analysis,
    create_win_loss_streak_analysis
)

def add_advanced_charts_to_dashboard(handler, first_trade=None, last_trade=None, trading_days=0):
    """
    Add advanced charts to the live trading dashboard
    
    Parameters:
    - handler: LiveTradeHandler instance
    - first_trade: First trade datetime
    - last_trade: Last trade datetime  
    - trading_days: Number of trading days
    """
    
    if handler is None or handler.positions_df.empty:
        st.info("No data available for advanced charts")
        return
    
    # Advanced Charts Section
    st.subheader("📊 Advanced Performance Analysis")
    
    # Show context information
    if first_trade and last_trade:
        st.markdown(f"""
        **📈 Advanced Analysis Context:**
        - **Data Period**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')}
        - **Trading Days**: {trading_days} days
        - **Total Trades**: {len(handler.positions_df)} trades
        - **Charts**: Advanced visualizations for deeper insights
        """)
    
    # Create tabs for advanced charts
    adv_tab1, adv_tab2, adv_tab3, adv_tab4, adv_tab5 = st.tabs([
        "📅 Daily Calendar", 
        "📈 Cumulative P&L", 
        "💰 Size vs Profit", 
        "📊 Weekday Analysis", 
        "🎯 Win/Loss Streaks"
    ])
    
    with adv_tab1:
        st.subheader("📅 Daily Performance Calendar")
        st.markdown("""
        **What this shows**: Each day as a colored circle - green for profitable days, red for losing days.
        The size and intensity show the magnitude of profit/loss.
        """)
        
        calendar_fig = create_daily_performance_calendar(
            handler.positions_df, 
            "Daily Performance Calendar"
        )
        st.plotly_chart(calendar_fig, use_container_width=True)
    
    with adv_tab2:
        st.subheader("📈 Cumulative P&L Progression")
        st.markdown("""
        **What this shows**: Your account growth over time with drawdown periods.
        The top chart shows cumulative profit, bottom shows drawdown from peaks.
        """)
        
        cumulative_fig = create_cumulative_pnl_curve(
            handler.positions_df,
            "Cumulative P&L and Drawdown Analysis"
        )
        st.plotly_chart(cumulative_fig, use_container_width=True)
    
    with adv_tab3:
        st.subheader("💰 Trade Size vs Profit Analysis")
        st.markdown("""
        **What this shows**: Relationship between trade size (volume) and profitability.
        Green dots = profitable trades, Red dots = losing trades.
        """)
        
        scatter_fig = create_trade_size_vs_profit_scatter(
            handler.positions_df,
            "Trade Volume vs Profit Relationship"
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
    
    with adv_tab4:
        st.subheader("📊 Weekday Performance Analysis")
        st.markdown("""
        **What this shows**: Performance breakdown by day of the week.
        Helps identify which days are most/least profitable for your trading style.
        """)
        
        weekday_fig = create_weekday_performance_analysis(
            handler.positions_df,
            "Performance by Day of Week"
        )
        st.plotly_chart(weekday_fig, use_container_width=True)
    
    with adv_tab5:
        st.subheader("🎯 Win/Loss Streak Analysis")
        st.markdown("""
        **What this shows**: Consecutive winning and losing streaks over time.
        Top chart shows streak lengths, bottom shows their profit impact.
        """)
        
        streak_fig = create_win_loss_streak_analysis(
            handler.positions_df,
            "Consecutive Win/Loss Streak Analysis"
        )
        st.plotly_chart(streak_fig, use_container_width=True)

def create_advanced_charts_sidebar_toggle():
    """Create sidebar toggle for advanced charts"""
    
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 📊 **Advanced Charts**")
        
        show_advanced = st.checkbox(
            "Show Advanced Analysis",
            value=False,
            help="Enable advanced charts for deeper trading insights"
        )
        
        if show_advanced:
            st.info("💡 Advanced charts provide deeper insights into your trading patterns and performance.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return show_advanced