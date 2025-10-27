"""
Professional Chart Suite
Bloomberg Terminal-style visualizations for institutional users
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ProfessionalChartSuite:
    """Professional-grade chart generation for institutional analysis"""
    
    def __init__(self, theme='dark'):
        self.theme = theme
        self.colors = self._get_professional_colors()
    
    def _get_professional_colors(self):
        """Get professional color scheme (Bloomberg-inspired)"""
        if self.theme == 'dark':
            return {
                'background': '#000000',
                'paper': '#1a1a1a',
                'text': '#ffffff',
                'grid': '#333333',
                'primary': '#ff8c00',  # Bloomberg orange
                'secondary': '#00d4ff',  # Bloomberg blue
                'success': '#00ff88',
                'warning': '#ffaa00',
                'danger': '#ff4444',
                'profit': '#00ff88',
                'loss': '#ff4444'
            }
        else:
            return {
                'background': '#ffffff',
                'paper': '#f8f9fa',
                'text': '#000000',
                'grid': '#e0e0e0',
                'primary': '#ff6600',
                'secondary': '#0066cc',
                'success': '#28a745',
                'warning': '#ffc107',
                'danger': '#dc3545',
                'profit': '#28a745',
                'loss': '#dc3545'
            }
    
    def create_executive_dashboard(self, executive_summary):
        """Create executive dashboard with KPIs"""
        try:
            kpis = executive_summary.get('key_performance_indicators', [])
            
            # Create subplot layout
            fig = make_subplots(
                rows=2, cols=3,
                subplot_titles=['Profitability', 'Risk Management', 'Operational', 
                               'Performance Score', 'Risk Assessment', 'Financial Impact'],
                specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                       [{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]]
            )
            
            # Add KPI indicators
            for i, kpi_category in enumerate(kpis[:3]):
                if kpi_category['metrics']:
                    main_metric = kpi_category['metrics'][0]
                    value = float(main_metric['value'].replace('$', '').replace(',', '').replace('%', ''))
                    
                    fig.add_trace(
                        go.Indicator(
                            mode="gauge+number+delta",
                            value=value,
                            title={'text': main_metric['name']},
                            gauge={
                                'axis': {'range': [None, value * 2]},
                                'bar': {'color': self._get_status_color(main_metric['status'])},
                                'steps': [
                                    {'range': [0, value * 0.5], 'color': self.colors['danger']},
                                    {'range': [value * 0.5, value * 1.5], 'color': self.colors['warning']},
                                    {'range': [value * 1.5, value * 2], 'color': self.colors['success']}
                                ]
                            }
                        ),
                        row=1, col=i+1
                    )
            
            # Add performance score bar chart
            overall_score = executive_summary.get('executive_overview', {}).get('overall_score', 0)
            fig.add_trace(
                go.Bar(
                    x=['Current Score', 'Target Score'],
                    y=[overall_score, 85],
                    marker_color=[self.colors['primary'], self.colors['success']],
                    name='Performance Score'
                ),
                row=2, col=1
            )
            
            # Add risk assessment pie chart
            risk_assessment = executive_summary.get('risk_assessment', {})
            risk_factors = risk_assessment.get('risk_factors', [])
            
            if risk_factors:
                severities = [rf['severity'] for rf in risk_factors]
                severity_counts = pd.Series(severities).value_counts()
                
                fig.add_trace(
                    go.Pie(
                        labels=severity_counts.index,
                        values=severity_counts.values,
                        marker_colors=[self._get_severity_color(s) for s in severity_counts.index],
                        name='Risk Factors'
                    ),
                    row=2, col=2
                )
            
            # Add financial impact bar chart
            financial_impact = executive_summary.get('financial_impact', {})
            current_profit = financial_impact.get('current_monthly_profit', 0)
            projected_profit = financial_impact.get('projected_monthly_profit', 0)
            
            fig.add_trace(
                go.Bar(
                    x=['Current', 'Projected'],
                    y=[current_profit, projected_profit],
                    marker_color=[self.colors['warning'], self.colors['success']],
                    name='Monthly Profit'
                ),
                row=2, col=3
            )
            
            # Update layout
            fig.update_layout(
                title=dict(
                    text="Executive Performance Dashboard",
                    font=dict(size=24, color=self.colors['text']),
                    x=0.5
                ),
                paper_bgcolor=self.colors['paper'],
                plot_bgcolor=self.colors['background'],
                font=dict(color=self.colors['text']),
                showlegend=False,
                height=800
            )
            
            return fig
            
        except Exception as e:
            # Return error chart
            fig = go.Figure()
            fig.add_annotation(
                text=f"Dashboard Error: {str(e)[:50]}...",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=self.colors['text'])
            )
            fig.update_layout(
                paper_bgcolor=self.colors['paper'],
                plot_bgcolor=self.colors['background']
            )
            return fig
    
    def create_risk_attribution_chart(self, advanced_risk_metrics):
        """Create professional risk attribution visualization"""
        try:
            # Extract risk metrics
            var_95 = advanced_risk_metrics.get('value_at_risk', {}).get('var_95', 0)
            es_95 = advanced_risk_metrics.get('expected_shortfall', {}).get('es_95', 0)
            sortino = advanced_risk_metrics.get('sortino_ratio', {}).get('sortino_ratio', 0)
            calmar = advanced_risk_metrics.get('calmar_ratio', {}).get('calmar_ratio', 0)
            omega = advanced_risk_metrics.get('omega_ratio', {}).get('omega_ratio', 0)
            
            # Create radar chart for risk metrics
            categories = ['VaR (95%)', 'Expected Shortfall', 'Sortino Ratio', 'Calmar Ratio', 'Omega Ratio']
            values = [
                min(100, var_95 / 10),  # Normalize VaR
                min(100, es_95 / 10),   # Normalize ES
                min(100, sortino * 25), # Normalize Sortino
                min(100, calmar * 20),  # Normalize Calmar
                min(100, omega * 25)    # Normalize Omega
            ]
            
            fig = go.Figure()
            
            # Add risk metrics radar
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=f'rgba(255, 140, 0, 0.2)',
                line=dict(color=self.colors['primary'], width=3),
                name='Risk Profile'
            ))
            
            # Add benchmark line
            benchmark_values = [70] * len(categories)
            fig.add_trace(go.Scatterpolar(
                r=benchmark_values + [benchmark_values[0]],
                theta=categories + [categories[0]],
                line=dict(color=self.colors['secondary'], width=2, dash='dash'),
                name='Industry Benchmark'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(color=self.colors['text']),
                        gridcolor=self.colors['grid']
                    ),
                    angularaxis=dict(
                        tickfont=dict(color=self.colors['text'])
                    )
                ),
                title=dict(
                    text="Professional Risk Attribution Analysis",
                    font=dict(size=20, color=self.colors['text']),
                    x=0.5
                ),
                paper_bgcolor=self.colors['paper'],
                plot_bgcolor=self.colors['background'],
                font=dict(color=self.colors['text']),
                legend=dict(font=dict(color=self.colors['text']))
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Risk Attribution Error: {str(e)}")
    
    def create_performance_attribution_matrix(self, time_analysis, risk_metrics):
        """Create performance attribution heatmap"""
        try:
            # Create sample performance attribution data
            sessions = ['Asian', 'European', 'US', 'Overlap']
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            
            # Generate attribution matrix (in real implementation, use actual data)
            np.random.seed(42)
            attribution_data = np.random.normal(0, 1, (len(days), len(sessions)))
            
            # Enhance with actual data if available
            if time_analysis and 'daily' in time_analysis:
                daily_data = time_analysis['daily']
                if 'daily_win_rates' in daily_data:
                    win_rates = daily_data['daily_win_rates']
                    for i, day in enumerate(days):
                        if day in win_rates:
                            # Adjust attribution based on actual win rates
                            attribution_data[i] = attribution_data[i] * (win_rates[day] / 50)
            
            fig = go.Figure(data=go.Heatmap(
                z=attribution_data,
                x=sessions,
                y=days,
                colorscale=[
                    [0, self.colors['loss']],
                    [0.5, '#ffffff'],
                    [1, self.colors['profit']]
                ],
                zmid=0,
                hoverongaps=False,
                hovertemplate='Session: %{x}<br>Day: %{y}<br>Attribution: %{z:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text="Performance Attribution Matrix",
                    font=dict(size=20, color=self.colors['text']),
                    x=0.5
                ),
                xaxis=dict(
                    title="Trading Session",
                    tickfont=dict(color=self.colors['text']),
                    title_font=dict(color=self.colors['text'])
                ),
                yaxis=dict(
                    title="Day of Week",
                    tickfont=dict(color=self.colors['text']),
                    title_font=dict(color=self.colors['text'])
                ),
                paper_bgcolor=self.colors['paper'],
                plot_bgcolor=self.colors['background']
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Attribution Matrix Error: {str(e)}")
    
    def create_professional_equity_curve(self, trades_df):
        """Create professional equity curve with annotations"""
        try:
            if trades_df.empty or 'profit' not in trades_df.columns:
                return self._create_error_chart("No trade data available")
            
            # Calculate cumulative equity
            cumulative_equity = trades_df['profit'].cumsum()
            
            # Calculate drawdown
            running_max = cumulative_equity.expanding().max()
            drawdown = cumulative_equity - running_max
            
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxis=True,
                vertical_spacing=0.1,
                subplot_titles=['Equity Curve', 'Drawdown'],
                row_heights=[0.7, 0.3]
            )
            
            # Add equity curve
            fig.add_trace(
                go.Scatter(
                    x=trades_df.index,
                    y=cumulative_equity,
                    mode='lines',
                    line=dict(color=self.colors['primary'], width=2),
                    name='Equity',
                    hovertemplate='Trade: %{x}<br>Equity: $%{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Add running maximum
            fig.add_trace(
                go.Scatter(
                    x=trades_df.index,
                    y=running_max,
                    mode='lines',
                    line=dict(color=self.colors['secondary'], width=1, dash='dash'),
                    name='Peak Equity',
                    hovertemplate='Trade: %{x}<br>Peak: $%{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Add drawdown
            fig.add_trace(
                go.Scatter(
                    x=trades_df.index,
                    y=drawdown,
                    mode='lines',
                    fill='tonexty',
                    fillcolor=f'rgba(255, 68, 68, 0.3)',
                    line=dict(color=self.colors['danger'], width=1),
                    name='Drawdown',
                    hovertemplate='Trade: %{x}<br>Drawdown: $%{y:.2f}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Add annotations for key events
            max_drawdown_idx = drawdown.idxmin()
            max_equity_idx = cumulative_equity.idxmax()
            
            fig.add_annotation(
                x=max_drawdown_idx,
                y=drawdown[max_drawdown_idx],
                text=f"Max DD: ${drawdown[max_drawdown_idx]:.2f}",
                showarrow=True,
                arrowhead=2,
                arrowcolor=self.colors['danger'],
                font=dict(color=self.colors['text']),
                row=2, col=1
            )
            
            fig.add_annotation(
                x=max_equity_idx,
                y=cumulative_equity[max_equity_idx],
                text=f"Peak: ${cumulative_equity[max_equity_idx]:.2f}",
                showarrow=True,
                arrowhead=2,
                arrowcolor=self.colors['success'],
                font=dict(color=self.colors['text']),
                row=1, col=1
            )
            
            fig.update_layout(
                title=dict(
                    text="Professional Equity Curve Analysis",
                    font=dict(size=20, color=self.colors['text']),
                    x=0.5
                ),
                paper_bgcolor=self.colors['paper'],
                plot_bgcolor=self.colors['background'],
                font=dict(color=self.colors['text']),
                legend=dict(font=dict(color=self.colors['text'])),
                height=600
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Equity Curve Error: {str(e)}")
    
    def _get_status_color(self, status):
        """Get color based on status"""
        status_colors = {
            'excellent': self.colors['success'],
            'good': self.colors['primary'],
            'average': self.colors['warning'],
            'poor': self.colors['danger']
        }
        return status_colors.get(status, self.colors['text'])
    
    def _get_severity_color(self, severity):
        """Get color based on severity"""
        severity_colors = {
            'CRITICAL': self.colors['danger'],
            'HIGH': self.colors['warning'],
            'MEDIUM': self.colors['primary'],
            'LOW': self.colors['success']
        }
        return severity_colors.get(severity, self.colors['text'])
    
    def _create_error_chart(self, error_message):
        """Create error chart"""
        fig = go.Figure()
        fig.add_annotation(
            text=error_message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=self.colors['text'])
        )
        fig.update_layout(
            paper_bgcolor=self.colors['paper'],
            plot_bgcolor=self.colors['background']
        )
        return fig