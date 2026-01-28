#!/usr/bin/env python3
"""
Fix script to ensure advanced charts are visible in live trading analysis
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_current_integration():
    """Test the current integration status"""
    print("🔍 Testing Current Advanced Charts Integration...")
    
    # Test 1: Check if advanced charts file exists
    advanced_charts_path = "utils/live_trade_analysis/advanced_live_charts.py"
    if os.path.exists(advanced_charts_path):
        print("✅ Advanced charts file exists")
    else:
        print("❌ Advanced charts file missing")
        return False
    
    # Test 2: Check if imports work
    try:
        from utils.live_trade_analysis.advanced_live_charts import (
            create_daily_performance_calendar,
            create_cumulative_pnl_curve,
            create_trade_size_vs_profit_scatter,
            create_weekday_performance_analysis,
            create_win_loss_streak_analysis
        )
        print("✅ Advanced charts imports successful")
    except Exception as e:
        print(f"❌ Advanced charts import failed: {e}")
        return False
    
    # Test 3: Check if live_handler imports advanced charts
    try:
        with open("utils/live_trade_analysis/live_handler.py", 'r') as f:
            content = f.read()
        
        required_imports = [
            "create_daily_performance_calendar",
            "create_cumulative_pnl_curve", 
            "create_trade_size_vs_profit_scatter",
            "create_weekday_performance_analysis",
            "create_win_loss_streak_analysis"
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp not in content:
                missing_imports.append(imp)
        
        if missing_imports:
            print(f"❌ Missing imports in live_handler.py: {missing_imports}")
            return False
        else:
            print("✅ All advanced chart imports found in live_handler.py")
    
    except Exception as e:
        print(f"❌ Error checking live_handler.py: {e}")
        return False
    
    # Test 4: Check if advanced charts section exists in create_live_dashboard
    try:
        if "Advanced Performance Analysis" in content and "st.tabs" in content:
            print("✅ Advanced charts section found in create_live_dashboard")
        else:
            print("❌ Advanced charts section missing in create_live_dashboard")
            return False
    except:
        print("❌ Error checking dashboard method")
        return False
    
    # Test 5: Check main app integration
    try:
        with open("enhanced_app.py", 'r') as f:
            app_content = f.read()
        
        if "Live Trading History" in app_content and "live_handler.create_live_dashboard()" in app_content:
            print("✅ Live trading analysis integrated in main app")
        else:
            print("❌ Live trading analysis not properly integrated in main app")
            return False
    except Exception as e:
        print(f"❌ Error checking main app: {e}")
        return False
    
    print("\n🎉 All integration tests passed!")
    print("📊 Advanced charts should be visible when doing live trade analysis.")
    return True

def create_debug_version():
    """Create a debug version of live_handler with enhanced error handling"""
    print("\n🔧 Creating debug version of live_handler...")
    
    debug_content = '''"""
Live Trade Handler - Debug Version
Enhanced error handling and logging for advanced charts
"""

import pandas as pd
import streamlit as st
from .live_parser import LiveTradeParser, parse_live_report
from .live_analyzer import LiveTradeAnalyzer
from .live_visualizations import (
    create_buy_sell_analysis,
    create_session_wise_analysis,
    create_hourly_performance_chart
)

# Advanced charts with error handling
try:
    from .advanced_live_charts import (
        create_daily_performance_calendar,
        create_cumulative_pnl_curve,
        create_trade_size_vs_profit_scatter,
        create_weekday_performance_analysis,
        create_win_loss_streak_analysis
    )
    ADVANCED_CHARTS_AVAILABLE = True
    print("✅ Advanced charts imported successfully")
except Exception as e:
    ADVANCED_CHARTS_AVAILABLE = False
    print(f"❌ Advanced charts import failed: {e}")

class LiveTradeHandler:
    """Main handler for live trading analysis workflow"""
    
    def __init__(self):
        self.positions_df = pd.DataFrame()
        self.deals_df = pd.DataFrame()
        self.summary_dict = {}
        self.account_info = {}
        self.analyzer = None
        
    def process_live_report(self, uploaded_file):
        """Process uploaded live trading report"""
        try:
            # Parse the live report
            self.positions_df, self.deals_df, self.summary_dict, self.account_info = parse_live_report(uploaded_file)
            
            # Initialize analyzer
            if not self.positions_df.empty:
                self.analyzer = LiveTradeAnalyzer(
                    positions_df=self.positions_df,
                    deals_df=self.deals_df,
                    account_info=self.account_info
                )
                return True
            else:
                st.error("No position data found in the uploaded file.")
                return False
                
        except Exception as e:
            st.error(f"Error processing live report: {str(e)}")
            return False
    
    def create_live_dashboard(self):
        """Create comprehensive live trading dashboard with debug info"""
        st.info(f"🔍 DEBUG: Advanced charts available: {ADVANCED_CHARTS_AVAILABLE}")
        st.info(f"🔍 DEBUG: Positions data: {len(self.positions_df)} rows")
        
        if self.analyzer is None:
            st.error("No analyzer available. Please upload a live trading report first.")
            return
        
        try:
            # ... (rest of the dashboard code would go here)
            
            # Advanced Analysis Section - ALWAYS SHOW
            st.subheader("📊 Advanced Performance Analysis")
            
            if ADVANCED_CHARTS_AVAILABLE:
                st.success("✅ Advanced charts are available and will be displayed below")
                
                # Create tabs for advanced charts
                adv_tab1, adv_tab2, adv_tab3, adv_tab4, adv_tab5 = st.tabs([
                    "📅 Daily Calendar", 
                    "📈 Cumulative P&L", 
                    "💰 Size vs Profit", 
                    "📊 Weekday Analysis", 
                    "🎯 Win/Loss Streaks"
                ])
                
                with adv_tab1:
                    st.markdown("**Daily Performance Calendar** - Each day shown as colored circle (Green=Profit, Red=Loss)")
                    try:
                        calendar_fig = create_daily_performance_calendar(self.positions_df, "Daily Performance Calendar")
                        st.plotly_chart(calendar_fig, use_container_width=True)
                        st.success("✅ Daily calendar chart displayed")
                    except Exception as e:
                        st.error(f"❌ Daily calendar error: {e}")
                
                with adv_tab2:
                    st.markdown("**Cumulative P&L Progression** - Account growth over time with drawdown analysis")
                    try:
                        cumulative_fig = create_cumulative_pnl_curve(self.positions_df, "Cumulative P&L and Drawdown")
                        st.plotly_chart(cumulative_fig, use_container_width=True)
                        st.success("✅ Cumulative P&L chart displayed")
                    except Exception as e:
                        st.error(f"❌ Cumulative P&L error: {e}")
                
                with adv_tab3:
                    st.markdown("**Trade Size vs Profit** - Relationship between volume and profitability")
                    try:
                        scatter_fig = create_trade_size_vs_profit_scatter(self.positions_df, "Volume vs Profit Analysis")
                        st.plotly_chart(scatter_fig, use_container_width=True)
                        st.success("✅ Size vs Profit scatter displayed")
                    except Exception as e:
                        st.error(f"❌ Size vs Profit error: {e}")
                
                with adv_tab4:
                    st.markdown("**Weekday Performance** - Performance breakdown by day of the week")
                    try:
                        weekday_fig = create_weekday_performance_analysis(self.positions_df, "Performance by Weekday")
                        st.plotly_chart(weekday_fig, use_container_width=True)
                        st.success("✅ Weekday analysis chart displayed")
                    except Exception as e:
                        st.error(f"❌ Weekday analysis error: {e}")
                
                with adv_tab5:
                    st.markdown("**Win/Loss Streaks** - Consecutive winning and losing patterns over time")
                    try:
                        streak_fig = create_win_loss_streak_analysis(self.positions_df, "Win/Loss Streak Analysis")
                        st.plotly_chart(streak_fig, use_container_width=True)
                        st.success("✅ Win/Loss streak chart displayed")
                    except Exception as e:
                        st.error(f"❌ Win/Loss streak error: {e}")
            else:
                st.error("❌ Advanced charts are not available. Check import errors above.")
                st.info("📋 Advanced charts should include: Daily Calendar, Cumulative P&L, Size vs Profit, Weekday Analysis, Win/Loss Streaks")
            
        except Exception as e:
            st.error(f"Error creating live dashboard: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def process_live_report(uploaded_file):
    """Helper function to process live trading report"""
    handler = LiveTradeHandler()
    success = handler.process_live_report(uploaded_file)
    
    if success:
        return handler
    else:
        return None
'''
    
    # Write debug version
    with open("utils/live_trade_analysis/live_handler_debug.py", 'w') as f:
        f.write(debug_content)
    
    print("✅ Debug version created: utils/live_trade_analysis/live_handler_debug.py")
    print("📋 You can temporarily replace live_handler.py with this debug version to see detailed error messages")

def main():
    """Main function"""
    print("🚀 Advanced Charts Integration Diagnostic Tool")
    print("=" * 50)
    
    # Test current integration
    if test_current_integration():
        print("\n✅ Integration appears to be working correctly!")
        print("\n🔍 If you're still not seeing advanced charts, the issue might be:")
        print("1. 📄 Live trading report is not being processed correctly")
        print("2. 🔄 Need to restart Streamlit app after recent changes")
        print("3. 📊 Data format issues preventing chart generation")
        print("4. 🖥️ UI scrolling - advanced charts might be below current view")
        
        print("\n💡 Recommended actions:")
        print("1. Restart the Streamlit app: Ctrl+C then 'streamlit run enhanced_app.py'")
        print("2. Upload your live trading report and scroll down to 'Advanced Performance Analysis' section")
        print("3. Look for 5 tabs: Daily Calendar, Cumulative P&L, Size vs Profit, Weekday Analysis, Win/Loss Streaks")
        
        # Create debug version anyway
        create_debug_version()
        
    else:
        print("\n❌ Integration issues detected!")
        print("Creating debug version to help identify the problem...")
        create_debug_version()

if __name__ == "__main__":
    main()