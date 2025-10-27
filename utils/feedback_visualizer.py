"""
Feedback Visualization Module
Creates interactive charts and visual feedback for trading analysis
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from .benchmark_standards import TradingBenchmarks

class FeedbackVisualizer:
    """Creates visual feedback components for trading analysis"""
    
    def __init__(self, theme='dark'):
        self.theme = theme
        self.colors = self._get_color_scheme()
    
    def _get_color_scheme(self):
        """Get color scheme based on theme"""
        if self.theme == 'dark':
            return {
                'excellent': '#10b981',
                'good': '#3b82f6', 
                'average': '#f59e0b',
                'poor': '#ef4444',
                'background': '#1e293b',
                'text': '#f1f5f9',
                'grid': '#374151'
            }
        else:
            return {
                'excellent': '#059669',
                'good': '#1d4ed8',
                'average': '#d97706', 
                'poor': '#dc2626',
                'background': '#ffffff',
                'text': '#1f2937',
                'grid': '#e5e7eb'
            }
    
    def create_benchmark_comparison_chart(self, benchmark_analysis):
        """Create benchmark comparison radar chart"""
        try:
            if not benchmark_analysis or not isinstance(benchmark_analysis, dict):
                return None
            
            metrics = []
            current_values = []
            benchmark_values = []
            colors = []
            
            for metric, analysis in benchmark_analysis.items():
                if not isinstance(analysis, dict) or 'percentile' not in analysis or 'rating' not in analysis:
                    continue
                    
                metrics.append(metric.replace('_', ' ').title())
                current_values.append(float(analysis.get('percentile', 50)))
                benchmark_values.append(70)  # Good benchmark percentile
                colors.append(self.colors.get(analysis.get('rating', 'average'), self.colors['average']))
            
            if not metrics:
                return None
            
            fig = go.Figure()
            
            # Add benchmark line
            fig.add_trace(go.Scatterpolar(
            r=benchmark_values + [benchmark_values[0]],
            theta=metrics + [metrics[0]],
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.1)',
            line=dict(color='rgba(59, 130, 246, 0.5)', width=2),
            name='Industry Benchmark (Good Level)',
            hovertemplate='%{theta}: %{r}th percentile<extra></extra>'
            ))
            
            # Add current performance
            fig.add_trace(go.Scatterpolar(
                r=current_values + [current_values[0]],
                theta=metrics + [metrics[0]],
                fill='toself',
                fillcolor='rgba(16, 185, 129, 0.2)',
                line=dict(color=self.colors['excellent'], width=3),
                name='Your Performance',
                hovertemplate='%{theta}: %{r}th percentile<extra></extra>'
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
                        tickfont=dict(color=self.colors['text'], size=12)
                    )
                ),
                showlegend=True,
                title=dict(
                    text="Performance vs Industry Benchmarks",
                    font=dict(size=18, color=self.colors['text']),
                    x=0.5
                ),
                paper_bgcolor=self.colors['background'],
                plot_bgcolor=self.colors['background'],
                font=dict(color=self.colors['text']),
                legend=dict(
                    font=dict(color=self.colors['text'])
                )
            )
            
            return fig
        except Exception as e:
            # Return empty figure on error
            fig = go.Figure()
            fig.add_annotation(
                text=f"Chart generation error: {str(e)[:50]}...",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
    
    def create_time_performance_heatmap(self, time_analysis):
        """Create time-based performance heatmap"""
        
        if 'hourly' not in time_analysis:
            return None
        
        # Create sample hourly data for visualization
        hours = list(range(24))
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        # Generate sample data based on analysis
        np.random.seed(42)
        data = np.random.normal(0, 1, (len(days), len(hours)))
        
        # Highlight best and worst hours from analysis
        best_hour = time_analysis['hourly']['best_hour']
        worst_hour = time_analysis['hourly']['worst_hour']
        
        # Boost best hour performance
        data[:, best_hour] += 2
        # Reduce worst hour performance  
        data[:, worst_hour] -= 2
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=hours,
            y=days,
            colorscale=[
                [0, self.colors['poor']],
                [0.25, self.colors['average']],
                [0.75, self.colors['good']],
                [1, self.colors['excellent']]
            ],
            hoverongaps=False,
            hovertemplate='Day: %{y}<br>Hour: %{x}:00<br>Performance: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="Trading Performance by Day and Hour",
                font=dict(size=18, color=self.colors['text']),
                x=0.5
            ),
            xaxis=dict(
                title="Hour (GMT)",
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            yaxis=dict(
                title="Day of Week",
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background']
        )
        
        return fig
    
    def create_recommendation_priority_chart(self, recommendations):
        """Create recommendation priority visualization"""
        
        if not recommendations:
            return None
        
        # Prepare data
        categories = [rec['category'] for rec in recommendations[:10]]  # Top 10
        priorities = [rec['priority_score'] for rec in recommendations[:10]]
        impacts = [rec['impact_score'] for rec in recommendations[:10]]
        titles = [rec['title'][:50] + '...' if len(rec['title']) > 50 else rec['title'] 
                 for rec in recommendations[:10]]
        
        # Create bubble chart
        fig = go.Figure()
        
        # Color mapping for priorities
        priority_colors = []
        for rec in recommendations[:10]:
            if rec['priority'] == 'CRITICAL':
                priority_colors.append(self.colors['poor'])
            elif rec['priority'] == 'HIGH':
                priority_colors.append(self.colors['average'])
            else:
                priority_colors.append(self.colors['good'])
        
        fig.add_trace(go.Scatter(
            x=priorities,
            y=impacts,
            mode='markers+text',
            marker=dict(
                size=[p/3 for p in priorities],  # Size based on priority
                color=priority_colors,
                opacity=0.7,
                line=dict(width=2, color=self.colors['text'])
            ),
            text=[f"{i+1}" for i in range(len(titles))],
            textposition="middle center",
            textfont=dict(color='white', size=12, family="Arial Black"),
            hovertemplate='<b>%{customdata}</b><br>' +
                         'Priority Score: %{x}<br>' +
                         'Impact Score: %{y}<br>' +
                         '<extra></extra>',
            customdata=titles,
            name='Recommendations'
        ))
        
        fig.update_layout(
            title=dict(
                text="Recommendation Priority vs Impact Analysis",
                font=dict(size=18, color=self.colors['text']),
                x=0.5
            ),
            xaxis=dict(
                title="Priority Score",
                range=[0, 100],
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text']),
                gridcolor=self.colors['grid']
            ),
            yaxis=dict(
                title="Impact Score", 
                range=[0, 100],
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text']),
                gridcolor=self.colors['grid']
            ),
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            showlegend=False
        )
        
        # Add quadrant labels
        fig.add_annotation(
            x=75, y=75,
            text="High Priority<br>High Impact",
            showarrow=False,
            font=dict(color=self.colors['text'], size=10),
            bgcolor="rgba(239, 68, 68, 0.1)",
            bordercolor=self.colors['poor']
        )
        
        fig.add_annotation(
            x=25, y=75,
            text="Low Priority<br>High Impact", 
            showarrow=False,
            font=dict(color=self.colors['text'], size=10),
            bgcolor="rgba(245, 158, 11, 0.1)",
            bordercolor=self.colors['average']
        )
        
        return fig
    
    def create_improvement_projection_chart(self, current_metrics, projected_metrics):
        """Create before/after improvement projection"""
        
        metrics = ['Win Rate (%)', 'Profit Factor', 'Sharpe Ratio']
        current = [
            current_metrics.get('win_rate', 50),
            current_metrics.get('profit_factor', 1.0),
            current_metrics.get('sharpe_ratio', 0.0)
        ]
        
        # Project improvements (example calculations)
        projected = [
            min(80, current[0] * 1.15),  # 15% improvement in win rate
            min(3.0, current[1] * 1.25),  # 25% improvement in profit factor
            min(2.0, current[2] + 0.5)    # +0.5 improvement in Sharpe ratio
        ]
        
        fig = go.Figure()
        
        # Current performance
        fig.add_trace(go.Bar(
            name='Current Performance',
            x=metrics,
            y=current,
            marker_color=self.colors['average'],
            opacity=0.7,
            hovertemplate='Current %{x}: %{y:.2f}<extra></extra>'
        ))
        
        # Projected performance
        fig.add_trace(go.Bar(
            name='Projected with Recommendations',
            x=metrics,
            y=projected,
            marker_color=self.colors['excellent'],
            opacity=0.8,
            hovertemplate='Projected %{x}: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="Performance Improvement Projections",
                font=dict(size=18, color=self.colors['text']),
                x=0.5
            ),
            xaxis=dict(
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            yaxis=dict(
                title="Value",
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text']),
                gridcolor=self.colors['grid']
            ),
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            barmode='group',
            legend=dict(
                font=dict(color=self.colors['text'])
            )
        )
        
        return fig
    
    def create_confidence_gauge(self, confidence_level, trade_count):
        """Create confidence level gauge"""
        
        confidence_mapping = {
            'insufficient': 20,
            'basic': 40,
            'reliable': 60,
            'high': 80,
            'professional': 95
        }
        
        confidence_value = confidence_mapping.get(confidence_level, 50)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = confidence_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Analysis Confidence<br><span style='font-size:14px'>Based on {trade_count} trades</span>"},
            delta = {'reference': 70, 'increasing': {'color': self.colors['excellent']}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': self.colors['text']},
                'bar': {'color': self.colors['excellent']},
                'steps': [
                    {'range': [0, 30], 'color': self.colors['poor']},
                    {'range': [30, 60], 'color': self.colors['average']},
                    {'range': [60, 80], 'color': self.colors['good']},
                    {'range': [80, 100], 'color': self.colors['excellent']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text'], 'size': 12},
            height=300
        )
        
        return fig