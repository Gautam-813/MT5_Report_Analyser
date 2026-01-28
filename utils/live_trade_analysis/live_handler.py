"""
Live Trade Handler
Main processing logic for live trading analysis
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
from .advanced_live_charts import (
    create_daily_performance_calendar,
    create_cumulative_pnl_curve,
    create_weekday_performance_analysis
)

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
    
    def get_live_summary_metrics(self):
        """Get comprehensive live trading summary metrics"""
        if self.analyzer is None:
            return {}
        
        try:
            # Get analyzer metrics
            analyzer_stats = self.analyzer.get_live_summary_stats()
            
            # Combine with parsed summary if available
            combined_stats = {**self.summary_dict, **analyzer_stats}
            
            # Add account information
            combined_stats['account_info'] = self.account_info
            
            return combined_stats
            
        except Exception as e:
            st.error(f"Error calculating summary metrics: {str(e)}")
            return {}
    
    def create_live_dashboard(self):
        """Create comprehensive live trading dashboard"""
        if self.analyzer is None:
            st.error("No analyzer available. Please upload a live trading report first.")
            return
        
        try:
            # Get analysis data
            summary_stats = self.get_live_summary_metrics()
            session_stats = self.analyzer.get_session_performance()
            daily_stats = self.analyzer.get_daily_performance()
            hourly_stats = self.analyzer.get_hourly_performance()
            symbol_stats = self.analyzer.get_symbol_performance()
            risk_metrics = self.analyzer.get_risk_metrics()
            
            # Calculate time range information once at the top
            first_trade = None
            last_trade = None
            total_days = 0
            trading_days = 0
            
            if not self.positions_df.empty:
                first_trade = self.positions_df['time'].min()
                last_trade = self.positions_df['time'].max()
                total_days = (last_trade.date() - first_trade.date()).days + 1
                trading_days = len(self.positions_df['time'].dt.date.unique())
            
            # Account Information Section
            st.subheader("📊 Account Information")
            if self.account_info:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Account Name", self.account_info.get('name', 'N/A'))
                with col2:
                    st.metric("Account Number", self.account_info.get('account_number', 'N/A'))
                with col3:
                    st.metric("Currency", self.account_info.get('currency', 'N/A'))
                with col4:
                    st.metric("Company", self.account_info.get('company', 'N/A'))
            
            # Key Performance Metrics (from actual report)
            st.subheader("📈 Key Performance Metrics")
            
            # First row - Main metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                total_profit = summary_stats.get('total_net_profit', 0)
                st.metric("Total Net Profit", f"${total_profit:.2f}")
            
            with col2:
                gross_profit = summary_stats.get('gross_profit', 0)
                st.metric("Gross Profit", f"${gross_profit:.2f}")
            
            with col3:
                gross_loss = summary_stats.get('gross_loss', 0)
                st.metric("Gross Loss", f"${gross_loss:.2f}")
            
            with col4:
                profit_factor = summary_stats.get('profit_factor', 0)
                st.metric("Profit Factor", f"{profit_factor:.2f}")
            
            with col5:
                expected_payoff = summary_stats.get('expected_payoff', 0)
                st.metric("Expected Payoff", f"{expected_payoff:.2f}")
            
            # Second row - Additional metrics
            col6, col7, col8, col9, col10 = st.columns(5)
            
            with col6:
                recovery_factor = summary_stats.get('recovery_factor', 0)
                st.metric("Recovery Factor", f"{recovery_factor:.2f}")
            
            with col7:
                sharpe_ratio = summary_stats.get('sharpe_ratio', 0)
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            
            with col8:
                total_trades = summary_stats.get('total_trades', 0)
                st.metric("Total Trades", f"{total_trades}")
            
            with col9:
                win_rate = summary_stats.get('profit_trades_pct', 0)
                st.metric("Win Rate", f"{win_rate:.1f}%")
            
            with col10:
                max_dd = summary_stats.get('balance_drawdown_maximal', 'N/A')
                st.metric("Max Drawdown", f"{max_dd}")
            
            # Buy vs Sell Trade Analysis
            st.subheader("📊 Buy vs Sell Trade Analysis")
            buy_sell_fig = create_buy_sell_analysis(self.positions_df, "Buy vs Sell Trade Analysis")
            st.plotly_chart(buy_sell_fig, use_container_width=True)
            
            # Session-wise Analysis
            st.subheader("🕐 Session-wise Profit & Loss Analysis")
            
            # Show session data context
            if first_trade is not None and last_trade is not None:
                st.markdown(f"""
                **📊 Session Analysis Context:**
                - **Data Period**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')}
                - **Trading Days**: {trading_days} days  
                - **Sessions**: Asian (0-8h), European (8-16h), US (16-24h)
                - **Note**: Each session shows aggregated data across all {trading_days} trading days
                """)
            
            session_fig = create_session_wise_analysis(session_stats, "Session-wise Performance")
            st.plotly_chart(session_fig, use_container_width=True)
            
            # Hourly Performance Chart
            st.subheader("⏰ Hourly Performance Chart")
            
            if not hourly_stats.empty:
                # Show hourly chart context
                if first_trade is not None and last_trade is not None:
                    st.markdown(f"""
                    **📊 Hourly Performance Context:**
                    - **Time Blocks**: Each bar represents 1-hour trading window (e.g., 8-9 = 8:00 AM to 9:00 AM)
                    - **Data Period**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')}
                    - **Trading Days**: {trading_days} days
                    - **Note**: Data aggregated across all {trading_days} trading days
                    """)
                
                hourly_fig = create_hourly_performance_chart(hourly_stats, "Hourly Trading Performance")
                st.plotly_chart(hourly_fig, use_container_width=True)
            else:
                st.info("No hourly performance data available")
            
            # Advanced Analysis Section
            st.subheader("📊 Advanced Performance Analysis")
            
            if first_trade is not None and last_trade is not None:
                st.markdown(f"""
                **📈 Advanced Analysis Context:**
                - **Data Period**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')}
                - **Trading Days**: {trading_days} days
                - **Total Trades**: {len(self.positions_df)} trades
                - **Advanced Insights**: Deeper analysis for pattern recognition and optimization
                """)
            
            # Create tabs for advanced charts
            adv_tab1, adv_tab2, adv_tab3 = st.tabs([
                "📅 Daily Calendar", 
                "📈 Cumulative P&L", 
                "📊 Weekday Analysis"
            ])
            
            with adv_tab1:
                st.markdown("**Daily Performance Calendar** - Each day shown as colored circle (Green=Profit, Red=Loss)")
                calendar_fig = create_daily_performance_calendar(self.positions_df, "Daily Performance Calendar")
                st.plotly_chart(calendar_fig, use_container_width=True)
            
            with adv_tab2:
                st.markdown("**Cumulative P&L Progression** - Account growth over time with drawdown analysis")
                cumulative_fig = create_cumulative_pnl_curve(self.positions_df, "Cumulative P&L and Drawdown")
                st.plotly_chart(cumulative_fig, use_container_width=True)
            
            with adv_tab3:
                st.markdown("**Weekday Performance** - Performance breakdown by day of the week")
                weekday_fig = create_weekday_performance_analysis(self.positions_df, "Performance by Weekday")
                st.plotly_chart(weekday_fig, use_container_width=True)
            
            # Detailed Statistics Tables
            st.subheader("📋 Detailed Statistics")
            
            # Show data time range information
            if first_trade is not None and last_trade is not None:
                st.info(f"📅 **Data Time Range**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')} "
                       f"({total_days} calendar days, {trading_days} trading days)")
            
            # Create tabs for different statistics
            tab1, tab2, tab3, tab4 = st.tabs(["Daily Stats", "Session Stats", "Hourly Stats", "Symbol Stats"])
            
            with tab1:
                if not daily_stats.empty:
                    st.dataframe(daily_stats, use_container_width=True)
                else:
                    st.info("No daily statistics available")
            
            with tab2:
                if not session_stats.empty:
                    st.dataframe(session_stats, use_container_width=True)
                else:
                    st.info("No session statistics available")
            
            with tab3:
                if not hourly_stats.empty:
                    # Show hourly data context
                    if first_trade is not None and last_trade is not None:
                        st.markdown(f"""
                        **📊 Hourly Performance Analysis Context:**
                        - **Data Period**: {first_trade.strftime('%B %d, %Y')} to {last_trade.strftime('%B %d, %Y')}
                        - **Trading Days**: {trading_days} days
                        - **Total Trades**: {len(self.positions_df)} trades
                        - **Note**: Each hour shows aggregated data across all {trading_days} trading days
                        """)
                    
                    st.dataframe(hourly_stats, use_container_width=True)
                else:
                    st.info("No hourly statistics available")
            
            with tab4:
                if not symbol_stats.empty:
                    st.dataframe(symbol_stats, use_container_width=True)
                else:
                    st.info("No symbol statistics available")
            
            # Additional Report Metrics
            st.subheader("📊 Additional Report Metrics")
            
            # Trade breakdown
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                short_trades = summary_stats.get('short_trades', 0)
                st.metric("Short Trades", f"{short_trades}")
            
            with col2:
                long_trades = summary_stats.get('long_trades', 0)
                st.metric("Long Trades", f"{long_trades}")
            
            with col3:
                largest_profit = summary_stats.get('largest_profit_trade', 0)
                st.metric("Largest Profit Trade", f"${largest_profit:.2f}")
            
            with col4:
                largest_loss = summary_stats.get('largest_loss_trade', 0)
                st.metric("Largest Loss Trade", f"${largest_loss:.2f}")
            
            # Consecutive trades metrics
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                max_wins = summary_stats.get('max_consecutive_wins', 0)
                st.metric("Max Consecutive Wins", f"{max_wins}")
            
            with col6:
                max_losses = summary_stats.get('max_consecutive_losses', 0)
                st.metric("Max Consecutive Losses", f"{max_losses}")
            
            with col7:
                avg_profit = summary_stats.get('average_profit_trade', 0)
                st.metric("Average Profit Trade", f"${avg_profit:.2f}")
            
            with col8:
                avg_loss = summary_stats.get('average_loss_trade', 0)
                st.metric("Average Loss Trade", f"${avg_loss:.2f}")
            
        except Exception as e:
            st.error(f"Error creating live dashboard: {str(e)}")
    
    def export_live_summary(self):
        """Export live trading summary to downloadable format"""
        if self.analyzer is None:
            return None
        
        try:
            summary_stats = self.get_live_summary_metrics()
            
            # Create summary report
            report_lines = []
            report_lines.append("LIVE TRADING ANALYSIS REPORT")
            report_lines.append("=" * 50)
            report_lines.append("")
            
            # Account Information
            if self.account_info:
                report_lines.append("ACCOUNT INFORMATION:")
                report_lines.append(f"Name: {self.account_info.get('name', 'N/A')}")
                report_lines.append(f"Account: {self.account_info.get('account_number', 'N/A')}")
                report_lines.append(f"Currency: {self.account_info.get('currency', 'N/A')}")
                report_lines.append(f"Company: {self.account_info.get('company', 'N/A')}")
                report_lines.append("")
            
            # Performance Summary
            report_lines.append("PERFORMANCE SUMMARY:")
            report_lines.append(f"Total Net Profit: ${summary_stats.get('total_net_profit', 0):.2f}")
            report_lines.append(f"Gross Profit: ${summary_stats.get('gross_profit', 0):.2f}")
            report_lines.append(f"Gross Loss: ${summary_stats.get('gross_loss', 0):.2f}")
            report_lines.append(f"Profit Factor: {summary_stats.get('profit_factor', 0):.2f}")
            report_lines.append(f"Win Rate: {summary_stats.get('win_rate', 0):.1f}%")
            report_lines.append(f"Total Trades: {summary_stats.get('total_trades', 0)}")
            report_lines.append("")
            
            # Risk Metrics
            risk_metrics = self.analyzer.get_risk_metrics()
            if risk_metrics:
                report_lines.append("RISK ANALYSIS:")
                report_lines.append(f"Maximum Drawdown: ${risk_metrics.get('max_drawdown', 0):.2f}")
                report_lines.append(f"Sharpe Ratio: {risk_metrics.get('sharpe_ratio', 0):.3f}")
                report_lines.append(f"Sortino Ratio: {risk_metrics.get('sortino_ratio', 0):.3f}")
                report_lines.append(f"VaR 95%: ${risk_metrics.get('var_95', 0):.2f}")
                report_lines.append(f"VaR 99%: ${risk_metrics.get('var_99', 0):.2f}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            st.error(f"Error exporting summary: {str(e)}")
            return None


def process_live_report(uploaded_file):
    """Helper function to process live trading report"""
    handler = LiveTradeHandler()
    success = handler.process_live_report(uploaded_file)
    
    if success:
        return handler
    else:
        return None