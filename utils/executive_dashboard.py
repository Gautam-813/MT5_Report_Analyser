"""
Executive Summary Dashboard
C-Suite ready reports and KPI dashboards
Based on institutional reporting standards from Goldman Sachs, JP Morgan, and hedge funds
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class ExecutiveDashboard:
    """
    Executive-level dashboard for C-suite and senior management
    Provides high-level KPIs and strategic insights
    """
    
    def __init__(self, trades_df, risk_metrics, advanced_risk_metrics):
        """Initialize with comprehensive trading data"""
        try:
            self.trades_df = trades_df.copy() if trades_df is not None and not trades_df.empty else pd.DataFrame()
            self.risk_metrics = risk_metrics if risk_metrics else {}
            self.advanced_risk_metrics = advanced_risk_metrics if advanced_risk_metrics else {}
            self.kpis = self._calculate_executive_kpis()
        except Exception:
            self.trades_df = pd.DataFrame()
            self.risk_metrics = {}
            self.advanced_risk_metrics = {}
            self.kpis = {}
    
    def _calculate_executive_kpis(self):
        """Calculate key performance indicators for executives"""
        try:
            if self.trades_df.empty:
                return self._get_empty_kpis()
            
            profits = pd.to_numeric(self.trades_df['profit'], errors='coerce').dropna()
            
            # Core Business Metrics
            total_trades = len(profits)
            total_pnl = profits.sum()
            win_rate = (profits > 0).sum() / len(profits) * 100 if len(profits) > 0 else 0
            
            # Risk-Adjusted Performance
            profit_factor = self.risk_metrics.get('profit_factor', 0)
            sharpe_ratio = self.risk_metrics.get('sharpe_ratio', 0)
            calmar_ratio = self.advanced_risk_metrics.get('calmar_ratio', {}).get('calmar_ratio', 0)
            
            # Risk Metrics
            var_95 = self.advanced_risk_metrics.get('var_analysis', {}).get('var_95_percent', 0)
            max_drawdown = self.advanced_risk_metrics.get('calmar_ratio', {}).get('max_drawdown_percent', 0)
            
            # Performance Rating
            overall_rating = self._calculate_executive_rating(win_rate, profit_factor, sharpe_ratio)
            
            return {
                'total_pnl': total_pnl,
                'total_trades': total_trades,
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'sharpe_ratio': sharpe_ratio,
                'calmar_ratio': calmar_ratio,
                'var_95': var_95,
                'max_drawdown': max_drawdown,
                'overall_rating': overall_rating,
                'risk_level': self._assess_risk_level(),
                'performance_trend': self._calculate_performance_trend(),
                'strategic_recommendations': self._generate_strategic_recommendations()
            }
            
        except Exception:
            return self._get_empty_kpis()
    
    def _get_empty_kpis(self):
        """Return empty KPIs structure"""
        return {
            'total_pnl': 0,
            'total_trades': 0,
            'win_rate': 0,
            'profit_factor': 0,
            'sharpe_ratio': 0,
            'calmar_ratio': 0,
            'var_95': 0,
            'max_drawdown': 0,
            'overall_rating': 'Insufficient Data',
            'risk_level': 'Unknown',
            'performance_trend': 'Neutral',
            'strategic_recommendations': ['Collect more trading data for analysis']
        }
    
    def create_executive_summary_card(self):
        """Create one-page executive summary"""
        try:
            kpis = self.kpis
            
            # Determine status colors
            pnl_color = "#10b981" if kpis['total_pnl'] >= 0 else "#ef4444"
            rating_color = self._get_rating_color(kpis['overall_rating'])
            risk_color = self._get_risk_color(kpis['risk_level'])
            
            summary_html = f"""
            <div style="
                background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
                border: 2px solid #60a5fa;
                border-radius: 20px;
                padding: 2rem;
                margin: 1rem 0;
                color: #ffffff;
                box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6);
            ">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h1 style="font-size: 2.5rem; font-weight: 900; color: #60a5fa; margin: 0;">
                        📊 EXECUTIVE SUMMARY
                    </h1>
                    <p style="font-size: 1.2rem; color: #cbd5e1; margin: 0.5rem 0;">
                        Strategic Trading Performance Overview
                    </p>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
                    
                    <div style="text-align: center; padding: 1.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.3);">
                        <div style="font-size: 2.5rem; font-weight: 800; color: {pnl_color};">
                            ${kpis['total_pnl']:,.2f}
                        </div>
                        <div style="font-size: 1rem; color: #cbd5e1; font-weight: 600;">
                            TOTAL P&L
                        </div>
                    </div>
                    
                    <div style="text-align: center; padding: 1.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
                        <div style="font-size: 2.5rem; font-weight: 800; color: #3b82f6;">
                            {kpis['win_rate']:.1f}%
                        </div>
                        <div style="font-size: 1rem; color: #cbd5e1; font-weight: 600;">
                            WIN RATE
                        </div>
                    </div>
                    
                    <div style="text-align: center; padding: 1.5rem; background: rgba(245, 158, 11, 0.1); border-radius: 15px; border: 1px solid rgba(245, 158, 11, 0.3);">
                        <div style="font-size: 2.5rem; font-weight: 800; color: #f59e0b;">
                            {kpis['profit_factor']:.2f}
                        </div>
                        <div style="font-size: 1rem; color: #cbd5e1; font-weight: 600;">
                            PROFIT FACTOR
                        </div>
                    </div>
                    
                    <div style="text-align: center; padding: 1.5rem; background: rgba(168, 85, 247, 0.1); border-radius: 15px; border: 1px solid rgba(168, 85, 247, 0.3);">
                        <div style="font-size: 2.5rem; font-weight: 800; color: #a855f7;">
                            {kpis['total_trades']:,}
                        </div>
                        <div style="font-size: 1rem; color: #cbd5e1; font-weight: 600;">
                            TOTAL TRADES
                        </div>
                    </div>
                    
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin: 2rem 0;">
                    
                    <div style="text-align: center;">
                        <div style="
                            background: {rating_color}; 
                            color: white; 
                            padding: 1rem 2rem; 
                            border-radius: 25px; 
                            font-weight: 700; 
                            font-size: 1.1rem;
                            box-shadow: 0 4px 15px rgba(96, 165, 250, 0.4);
                        ">
                            {kpis['overall_rating']}
                        </div>
                        <div style="margin-top: 0.5rem; color: #cbd5e1; font-weight: 600;">
                            OVERALL RATING
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <div style="
                            background: {risk_color}; 
                            color: white; 
                            padding: 1rem 2rem; 
                            border-radius: 25px; 
                            font-weight: 700; 
                            font-size: 1.1rem;
                            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
                        ">
                            {kpis['risk_level']}
                        </div>
                        <div style="margin-top: 0.5rem; color: #cbd5e1; font-weight: 600;">
                            RISK LEVEL
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <div style="
                            background: linear-gradient(135deg, #10b981, #059669); 
                            color: white; 
                            padding: 1rem 2rem; 
                            border-radius: 25px; 
                            font-weight: 700; 
                            font-size: 1.1rem;
                            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                        ">
                            {kpis['performance_trend']}
                        </div>
                        <div style="margin-top: 0.5rem; color: #cbd5e1; font-weight: 600;">
                            TREND
                        </div>
                    </div>
                    
                </div>
                
                <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 15px; border-left: 5px solid #3b82f6;">
                    <h3 style="color: #3b82f6; margin: 0 0 1rem 0; font-size: 1.3rem;">
                        🎯 STRATEGIC RECOMMENDATIONS
                    </h3>
                    <ul style="margin: 0; padding-left: 1.5rem; color: #f1f5f9;">
            """
            
            for recommendation in kpis['strategic_recommendations'][:3]:  # Top 3 recommendations
                summary_html += f"<li style='margin: 0.5rem 0; font-size: 1.1rem;'>{recommendation}</li>"
            
            summary_html += """
                    </ul>
                </div>
                
            </div>
            """
            
            return summary_html
            
        except Exception:
            return "<div style='color: #ef4444;'>Error generating executive summary</div>"
    
    def create_kpi_dashboard(self):
        """Create comprehensive KPI dashboard"""
        try:
            fig = make_subplots(
                rows=2, cols=3,
                subplot_titles=[
                    'Performance Score', 'Risk Assessment', 'Profit Trend',
                    'Win Rate Analysis', 'Risk Metrics', 'Strategic Position'
                ],
                specs=[
                    [{"type": "indicator"}, {"type": "indicator"}, {"type": "scatter"}],
                    [{"type": "bar"}, {"type": "scatter"}, {"type": "pie"}]
                ]
            )
            
            kpis = self.kpis
            
            # Performance Score Gauge
            performance_score = min(100, max(0, (kpis['win_rate'] + kpis['profit_factor'] * 20 + kpis['sharpe_ratio'] * 30)))
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=performance_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Performance Score"},
                    delta={'reference': 70},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#10b981"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ef4444"},
                            {'range': [50, 70], 'color': "#f59e0b"},
                            {'range': [70, 85], 'color': "#3b82f6"},
                            {'range': [85, 100], 'color': "#10b981"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ),
                row=1, col=1
            )
            
            # Risk Assessment Gauge
            risk_score = max(0, min(100, 100 - abs(kpis['var_95']) * 10 - kpis['max_drawdown']))
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=risk_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Risk Score"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#f59e0b"},
                        'steps': [
                            {'range': [0, 30], 'color': "#ef4444"},
                            {'range': [30, 60], 'color': "#f59e0b"},
                            {'range': [60, 80], 'color': "#3b82f6"},
                            {'range': [80, 100], 'color': "#10b981"}
                        ]
                    }
                ),
                row=1, col=2
            )
            
            # Add more charts...
            # (Additional charts would be implemented here)
            
            fig.update_layout(
                height=800,
                showlegend=False,
                title_text="Executive KPI Dashboard",
                title_x=0.5,
                paper_bgcolor='#0f172a',
                plot_bgcolor='#0f172a',
                font=dict(color='#ffffff')
            )
            
            return fig
            
        except Exception:
            # Return empty figure on error
            fig = go.Figure()
            fig.add_annotation(
                text="Error generating KPI dashboard",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="#ef4444", size=16)
            )
            return fig
    
    def create_traffic_light_system(self):
        """Create traffic light system for quick status assessment"""
        try:
            kpis = self.kpis
            
            # Define thresholds
            indicators = [
                {
                    'name': 'Profitability',
                    'value': kpis['total_pnl'],
                    'status': 'green' if kpis['total_pnl'] > 0 else 'red',
                    'threshold': 0
                },
                {
                    'name': 'Win Rate',
                    'value': f"{kpis['win_rate']:.1f}%",
                    'status': 'green' if kpis['win_rate'] >= 60 else 'yellow' if kpis['win_rate'] >= 50 else 'red',
                    'threshold': '60%'
                },
                {
                    'name': 'Risk Management',
                    'value': f"{kpis['max_drawdown']:.1f}%",
                    'status': 'green' if kpis['max_drawdown'] <= 10 else 'yellow' if kpis['max_drawdown'] <= 20 else 'red',
                    'threshold': '10%'
                },
                {
                    'name': 'Profit Factor',
                    'value': f"{kpis['profit_factor']:.2f}",
                    'status': 'green' if kpis['profit_factor'] >= 1.5 else 'yellow' if kpis['profit_factor'] >= 1.2 else 'red',
                    'threshold': '1.5'
                }
            ]
            
            traffic_light_html = """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
            """
            
            for indicator in indicators:
                color_map = {
                    'green': '#10b981',
                    'yellow': '#f59e0b', 
                    'red': '#ef4444'
                }
                
                icon_map = {
                    'green': '🟢',
                    'yellow': '🟡',
                    'red': '🔴'
                }
                
                color = color_map[indicator['status']]
                icon = icon_map[indicator['status']]
                
                traffic_light_html += f"""
                <div style="
                    background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
                    border: 2px solid {color};
                    border-radius: 15px;
                    padding: 1.5rem;
                    text-align: center;
                    color: #ffffff;
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {color};">
                        {indicator['name']}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 800; margin: 0.5rem 0;">
                        {indicator['value']}
                    </div>
                    <div style="font-size: 0.9rem; color: #cbd5e1;">
                        Target: {indicator['threshold']}
                    </div>
                </div>
                """
            
            traffic_light_html += "</div>"
            
            return traffic_light_html
            
        except Exception:
            return "<div style='color: #ef4444;'>Error generating traffic light system</div>"
    
    def generate_executive_recommendations(self):
        """Generate C-suite level strategic recommendations"""
        try:
            kpis = self.kpis
            recommendations = []
            
            # Profitability recommendations
            if kpis['total_pnl'] < 0:
                recommendations.append({
                    'priority': 'CRITICAL',
                    'category': 'Profitability',
                    'recommendation': 'Immediate strategy review required - current approach is unprofitable',
                    'action': 'Halt trading and conduct comprehensive strategy audit',
                    'timeline': 'Immediate'
                })
            
            # Risk management recommendations
            if kpis['max_drawdown'] > 20:
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Risk Management',
                    'recommendation': 'Excessive drawdown risk detected - implement stricter risk controls',
                    'action': 'Reduce position sizes and implement daily loss limits',
                    'timeline': '1 week'
                })
            
            # Performance optimization
            if kpis['win_rate'] < 50:
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Performance',
                    'recommendation': 'Win rate below industry standards - improve trade selection',
                    'action': 'Implement enhanced entry criteria and market analysis',
                    'timeline': '2 weeks'
                })
            
            # Strategic recommendations
            if kpis['sharpe_ratio'] < 1.0:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Strategy',
                    'recommendation': 'Risk-adjusted returns need improvement',
                    'action': 'Optimize risk/reward ratios and reduce volatility',
                    'timeline': '1 month'
                })
            
            return recommendations
            
        except Exception:
            return [{
                'priority': 'LOW',
                'category': 'System',
                'recommendation': 'Collect more data for comprehensive analysis',
                'action': 'Continue trading and gather performance data',
                'timeline': 'Ongoing'
            }]
    
    # Helper methods
    def _calculate_executive_rating(self, win_rate, profit_factor, sharpe_ratio):
        """Calculate overall executive rating"""
        try:
            score = 0
            
            # Win rate component (0-40 points)
            if win_rate >= 70:
                score += 40
            elif win_rate >= 60:
                score += 30
            elif win_rate >= 50:
                score += 20
            elif win_rate >= 40:
                score += 10
            
            # Profit factor component (0-35 points)
            if profit_factor >= 2.0:
                score += 35
            elif profit_factor >= 1.5:
                score += 25
            elif profit_factor >= 1.2:
                score += 15
            elif profit_factor >= 1.0:
                score += 5
            
            # Sharpe ratio component (0-25 points)
            if sharpe_ratio >= 1.5:
                score += 25
            elif sharpe_ratio >= 1.0:
                score += 20
            elif sharpe_ratio >= 0.5:
                score += 10
            elif sharpe_ratio >= 0.0:
                score += 5
            
            # Convert to rating
            if score >= 80:
                return "EXCELLENT"
            elif score >= 60:
                return "GOOD"
            elif score >= 40:
                return "AVERAGE"
            else:
                return "POOR"
                
        except Exception:
            return "UNKNOWN"
    
    def _assess_risk_level(self):
        """Assess overall risk level"""
        try:
            var_95 = abs(self.advanced_risk_metrics.get('var_analysis', {}).get('var_95_percent', 0))
            max_dd = self.advanced_risk_metrics.get('calmar_ratio', {}).get('max_drawdown_percent', 0)
            
            if var_95 > 10 or max_dd > 25:
                return "HIGH RISK"
            elif var_95 > 5 or max_dd > 15:
                return "MODERATE RISK"
            else:
                return "LOW RISK"
                
        except Exception:
            return "UNKNOWN RISK"
    
    def _calculate_performance_trend(self):
        """Calculate performance trend"""
        try:
            if self.trades_df.empty:
                return "NEUTRAL"
            
            # Simple trend analysis based on recent performance
            profits = pd.to_numeric(self.trades_df['profit'], errors='coerce').dropna()
            
            if len(profits) < 10:
                return "INSUFFICIENT DATA"
            
            # Compare first half vs second half
            mid_point = len(profits) // 2
            first_half = profits[:mid_point].mean()
            second_half = profits[mid_point:].mean()
            
            if second_half > first_half * 1.1:
                return "IMPROVING"
            elif second_half < first_half * 0.9:
                return "DECLINING"
            else:
                return "STABLE"
                
        except Exception:
            return "NEUTRAL"
    
    def _generate_strategic_recommendations(self):
        """Generate strategic recommendations"""
        try:
            recommendations = []
            kpis = self.kpis
            
            if kpis['total_pnl'] > 0:
                recommendations.append("Scale successful strategies with increased capital allocation")
            else:
                recommendations.append("Conduct immediate strategy review and risk assessment")
            
            if kpis['win_rate'] < 60:
                recommendations.append("Implement enhanced trade selection criteria")
            
            if kpis['profit_factor'] < 1.5:
                recommendations.append("Optimize risk/reward ratios for better profitability")
            
            recommendations.append("Establish regular performance review meetings")
            recommendations.append("Implement automated risk monitoring systems")
            
            return recommendations
            
        except Exception:
            return ["Collect more trading data for strategic analysis"]
    
    def _get_rating_color(self, rating):
        """Get color for rating"""
        color_map = {
            'EXCELLENT': '#10b981',
            'GOOD': '#3b82f6',
            'AVERAGE': '#f59e0b',
            'POOR': '#ef4444',
            'UNKNOWN': '#6b7280'
        }
        return color_map.get(rating, '#6b7280')
    
    def _get_risk_color(self, risk_level):
        """Get color for risk level"""
        if 'LOW' in risk_level:
            return '#10b981'
        elif 'MODERATE' in risk_level:
            return '#f59e0b'
        elif 'HIGH' in risk_level:
            return '#ef4444'
        else:
            return '#6b7280'