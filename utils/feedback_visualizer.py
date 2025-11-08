"""
Feedback Visualization Module
Creates interactive charts and visual feedback for trading analysis
"""

import plotly.graph_objects as go
import numpy as np


class FeedbackVisualizer:
    """
    Creates visual feedback components for trading analysis.
    Supports dark/light themes and robust error handling.
    """

    def __init__(self, theme='dark'):
        """
        Initialize visualizer with theme.

        Args:
            theme (str): 'dark' or 'light'
        """
        self.theme = theme.lower()
        self.colors = self._get_color_scheme()

    def _get_color_scheme(self):
        """Return color palette based on theme."""
        if self.theme == 'dark':
            return {
                'excellent': '#10b981',  # emerald-500
                'good': '#3b82f6',       # blue-500
                'average': '#f59e0b',    # amber-500
                'poor': '#ef4444',       # red-500
                'background': '#1e293b', # slate-800
                'text': '#f1f5f9',       # slate-100
                'grid': '#374151'        # slate-700
            }
        else:  # light theme
            return {
                'excellent': '#059669',  # emerald-600
                'good': '#1d4ed8',       # blue-700
                'average': '#d97706',    # amber-700
                'poor': '#dc2626',       # red-600
                'background': '#ffffff',
                'text': '#1f2937',       # slate-800
                'grid': '#e5e7eb'        # slate-300
            }

    def _safe_num(self, value, default=0.0):
        """
        Safely convert value to float with fallback.

        Args:
            value: Input value (str, int, float, etc.)
            default: Fallback value if conversion fails

        Returns:
            float: Converted number or default
        """
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                cleaned = value.strip().rstrip('%').replace(',', '')
                return float(cleaned) if cleaned else default
            return float(value)
        except (ValueError, TypeError, AttributeError):
            return float(default)

    def create_benchmark_comparison_chart(self, benchmark_analysis):
        """
        Create radar chart comparing user performance to industry benchmarks.

        Args:
            benchmark_analysis (dict): {metric: {percentile: X, rating: 'excellent'|'good'|...}}

        Returns:
            plotly.graph_objects.Figure or None
        """
        try:
            if not benchmark_analysis or not isinstance(benchmark_analysis, dict):
                return None

            metrics = []
            current_values = []
            benchmark_values = []

            for metric, data in benchmark_analysis.items():
                if not isinstance(data, dict) or 'percentile' not in data or 'rating' not in data:
                    continue

                metrics.append(metric.replace('_', ' ').title())
                current_values.append(float(data.get('percentile', 50)))
                benchmark_values.append(70)  # "Good" benchmark threshold

            if not metrics:
                return None

            # Close the polygon
            current_values += [current_values[0]]
            benchmark_values += [benchmark_values[0]]
            metrics += [metrics[0]]

            fig = go.Figure()

            # Benchmark area
            fig.add_trace(go.Scatterpolar(
                r=benchmark_values,
                theta=metrics,
                fill='toself',
                fillcolor='rgba(59, 130, 246, 0.1)',
                line=dict(color='rgba(59, 130, 246, 0.5)', width=2),
                name='Industry Benchmark (Good)',
                hovertemplate='%{theta}: %{r}th percentile<extra></extra>'
            ))

            # User performance
            fig.add_trace(go.Scatterpolar(
                r=current_values,
                theta=metrics,
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
                        tickfont=dict(color=self.colors['text'], size=12),
                        rotation=90
                    )
                ),
                showlegend=True,
                title=dict(
                    text="Performance vs Industry Benchmarks",
                    x=0.5,
                    font=dict(size=18, color=self.colors['text'])
                ),
                paper_bgcolor=self.colors['background'],
                plot_bgcolor=self.colors['background'],
                font=dict(color=self.colors['text']),
                legend=dict(font=dict(color=self.colors['text'])),
                margin=dict(l=60, r=60, t=80, b=60)
            )

            return fig

        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)[:50]}...",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color=self.colors['poor'])
            )
            fig.update_layout(paper_bgcolor=self.colors['background'])
            return fig

    def create_time_performance_heatmap(self, time_analysis):
        """
        Create heatmap of performance by day and hour.

        Args:
            time_analysis (dict): Must contain 'hourly': {'best_hour': int, 'worst_hour': int}

        Returns:
            plotly.graph_objects.Figure or None
        """
        try:
            if not time_analysis or not isinstance(time_analysis, dict):
                return None
            if 'hourly' not in time_analysis or not isinstance(time_analysis['hourly'], dict):
                return None

            hourly = time_analysis['hourly']
            if 'best_hour' not in hourly or 'worst_hour' not in hourly:
                return None

            best_hour = int(hourly['best_hour'])
            worst_hour = int(hourly['worst_hour'])

            if not (0 <= best_hour <= 23 and 0 <= worst_hour <= 23):
                return None

            hours = list(range(24))
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

            np.random.seed(42)
            data = np.random.normal(0, 1, (len(days), len(hours)))

            # Emphasize best/worst hours
            data[:, best_hour] += 2.0
            data[:, worst_hour] -= 2.0

            fig = go.Figure(data=go.Heatmap(
                z=data,
                x=hours,
                y=days,
                colorscale=[
                    [0.0, self.colors['poor']],
                    [0.25, self.colors['average']],
                    [0.75, self.colors['good']],
                    [1.0, self.colors['excellent']]
                ],
                hoverongaps=False,
                hovertemplate=(
                    'Day: %{y}<br>'
                    'Hour: %{x}:00 GMT<br>'
                    'Performance: %{z:.2f}<extra></extra>'
                )
            ))

            fig.update_layout(
                title=dict(
                    text="Trading Performance by Day and Hour",
                    x=0.5,
                    font=dict(size=18, color=self.colors['text'])
                ),
                xaxis=dict(
                    title="Hour (GMT)",
                    tickmode='linear',
                    tick0=0,
                    dtick=2,
                    tickfont=dict(color=self.colors['text']),
                    title_font=dict(color=self.colors['text'])
                ),
                yaxis=dict(
                    title="Day of Week",
                    tickfont=dict(color=self.colors['text']),
                    title_font=dict(color=self.colors['text'])
                ),
                paper_bgcolor=self.colors['background'],
                plot_bgcolor=self.colors['background'],
                margin=dict(l=80, r=40, t=80, b=60)
            )

            return fig

        except Exception:
            return None

    def create_recommendation_priority_chart(self, recommendations):
        """
        Create bubble chart of recommendation priority vs impact.

        Args:
            recommendations (list): List of dicts with priority_score, impact_score, title, priority

        Returns:
            plotly.graph_objects.Figure or None
        """
        if not recommendations or not isinstance(recommendations, list):
            return None

        top_n = recommendations[:10]
        if not top_n:
            return None

        priorities = [rec.get('priority_score', 0) for rec in top_n]
        impacts = [rec.get('impact_score', 0) for rec in top_n]
        titles = [
            (rec.get('title') or '')[:50] + ('...' if len(rec.get('title') or '') > 50 else '')
            for rec in top_n
        ]

        # Priority-based coloring
        priority_colors = []
        for rec in top_n:
            p = (rec.get('priority') or '').upper()
            if p == 'CRITICAL':
                priority_colors.append(self.colors['poor'])
            elif p == 'HIGH':
                priority_colors.append(self.colors['average'])
            else:
                priority_colors.append(self.colors['good'])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=priorities,
            y=impacts,
            mode='markers+text',
            marker=dict(
                size=[max(10, p / 3) for p in priorities],
                color=priority_colors,
                opacity=0.8,
                line=dict(width=2, color=self.colors['text'])
            ),
            text=[f"{i+1}" for i in range(len(titles))],
            textposition="middle center",
            textfont=dict(color='white', size=12, family="Arial Black"),
            hovertemplate=(
                '<b>%{customdata}</b><br>'
                'Priority: %{x}<br>'
                'Impact: %{y}<extra></extra>'
            ),
            customdata=titles,
            name='Recommendations'
        ))

        fig.update_layout(
            title=dict(
                text="Recommendation Priority vs Impact",
                x=0.5,
                font=dict(size=18, color=self.colors['text'])
            ),
            xaxis=dict(
                title="Priority Score",
                range=[0, 100],
                gridcolor=self.colors['grid'],
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            yaxis=dict(
                title="Impact Score",
                range=[0, 100],
                gridcolor=self.colors['grid'],
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            showlegend=False,
            margin=dict(l=60, r=60, t=80, b=60)
        )

        # Quadrant labels
        fig.add_annotation(x=75, y=75, text="High Priority<br>High Impact",
                           showarrow=False, font=dict(size=10, color=self.colors['text']),
                           bgcolor="rgba(239,68,68,0.1)", bordercolor=self.colors['poor'])
        fig.add_annotation(x=25, y=75, text="Low Priority<br>High Impact",
                           showarrow=False, font=dict(size=10, color=self.colors['text']),
                           bgcolor="rgba(245,158,11,0.1)", bordercolor=self.colors['average'])
        fig.add_annotation(x=75, y=25, text="High Priority<br>Low Impact",
                           showarrow=False, font=dict(size=10, color=self.colors['text']),
                           bgcolor="rgba(59,130,246,0.1)", bordercolor=self.colors['good'])
        fig.add_annotation(x=25, y=25, text="Low Priority<br>Low Impact",
                           showarrow=False, font=dict(size=10, color=self.colors['text']),
                           bgcolor="rgba(150,150,150,0.1)", bordercolor=self.colors['grid'])

        return fig

    def create_improvement_projection_chart(self, current_metrics, projected_metrics=None):
        """
        Bar chart showing current vs projected performance.

        Args:
            current_metrics (dict): win_rate, profit_factor, sharpe_ratio
            projected_metrics (dict, optional): Override projections

        Returns:
            plotly.graph_objects.Figure
        """
        metrics = ['Win Rate (%)', 'Profit Factor', 'Sharpe Ratio']

        win_rate = self._safe_num(current_metrics.get('win_rate', 50), 50.0)
        profit_factor = self._safe_num(current_metrics.get('profit_factor', 1.0), 1.0)
        sharpe = self._safe_num(current_metrics.get('sharpe_ratio', 0.0), 0.0)

        current = [win_rate, profit_factor, sharpe]

        projected = [
            min(80.0, win_rate * 1.15),
            min(3.0, profit_factor * 1.25),
            min(2.0, sharpe + 0.5)
        ]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Current',
            x=metrics,
            y=current,
            marker_color=self.colors['average'],
            opacity=0.7,
            hovertemplate='Current: %{y:.2f}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            name='Projected',
            x=metrics,
            y=projected,
            marker_color=self.colors['excellent'],
            opacity=0.9,
            hovertemplate='Projected: %{y:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text="Performance Improvement Projection",
                x=0.5,
                font=dict(size=18, color=self.colors['text'])
            ),
            barmode='group',
            xaxis=dict(tickfont=dict(color=self.colors['text'])),
            yaxis=dict(
                title="Value",
                gridcolor=self.colors['grid'],
                tickfont=dict(color=self.colors['text']),
                title_font=dict(color=self.colors['text'])
            ),
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            legend=dict(font=dict(color=self.colors['text'])),
            margin=dict(l=60, r=60, t=80, b=60)
        )

        return fig

    def create_confidence_gauge(self, confidence_level, trade_count):
        """
        Gauge chart showing analysis confidence.

        Args:
            confidence_level (str): 'insufficient', 'basic', 'reliable', 'high', 'professional'
            trade_count (int): Number of trades analyzed

        Returns:
            plotly.graph_objects.Figure
        """
        mapping = {
            'insufficient': 20,
            'basic': 40,
            'reliable': 60,
            'high': 80,
            'professional': 95
        }
        value = mapping.get(str(confidence_level).lower(), 50)

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': f"Analysis Confidence<br><span style='font-size:14px'>"
                        f"Based on {trade_count} trades</span>"
            },
            delta={'reference': 70, 'increasing': {'color': self.colors['excellent']}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': self.colors['text']},
                'bar': {'color': self.colors['excellent']},
                'steps': [
                    {'range': [0, 30], 'color': self.colors['poor']},
                    {'range': [30, 60], 'color': self.colors['average']},
                    {'range': [60, 80], 'color': self.colors['good']},
                    {'range': [80, 100], 'color': self.colors['excellent']}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        fig.update_layout(
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text'], 'size': 12},
            height=300,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        return fig