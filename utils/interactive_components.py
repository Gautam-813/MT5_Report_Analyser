"""
Interactive Components for Enhanced MT5 Dashboard
Professional UI components and interactive features
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_interactive_equity_curve(trades_df, theme='light'):
    """Create interactive equity curve with advanced features"""
    
    if trades_df.empty:
        return go.Figure()
    
    # Calculate equity curve
    df = trades_df.copy()
    df['cumulative'] = df['profit'].cumsum()
    # Removed fake drawdown calculation - we don't have tick data
    
    # Create subplot
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=('Equity Curve', 'Trade Distribution', 'Trade Profit/Loss'),
        vertical_spacing=0.05,
        row_heights=[0.5, 0.25, 0.25]
    )
    
    # Equity curve with hover information
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['cumulative'],
            mode='lines',
            name='Equity',
            line=dict(color='#3b82f6', width=2),
            hovertemplate='<b>%{x}</b><br>Equity: $%{y:,.2f}<extra></extra>',
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Add running maximum line
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['cumulative'],
            mode='lines',
            name='Cumulative Profit',
            line=dict(color='#10b981', width=1, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Peak: $%{y:,.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Trade distribution histogram
    fig.add_trace(
        go.Histogram(
            x=df['profit'],
            name='Trade Distribution',
            marker_color='rgba(59, 130, 246, 0.7)',
            hovertemplate='<b>Profit Range: $%{x}</b><br>Count: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Individual trade profits/losses
    colors = ['#10b981' if p > 0 else '#ef4444' for p in df['profit']]
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['profit'],
            mode='markers',
            name='Trades',
            marker=dict(
                color=colors,
                size=6,
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Interactive Equity Analysis",
        height=700,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Theme styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_performance_heatmap(daily_stats):
    """Create interactive performance heatmap"""
    
    if daily_stats.empty:
        return go.Figure()
    
    # Prepare data
    df = daily_stats.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.isocalendar().week
    
    # Create pivot table for heatmap
    pivot_data = df.pivot_table(
        values='profit_sum',
        index='weekday',
        columns='week',
        aggfunc='sum',
        fill_value=0
    )
    
    # Reorder weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(weekday_order)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn',
        zmid=0,
        hoverongaps=False,
        hovertemplate='<b>Week %{x}, %{y}</b><br>P&L: $%{z:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Daily Performance Heatmap",
        xaxis_title="Week of Year",
        yaxis_title="Day of Week",
        height=400
    )
    
    return fig

def create_risk_gauge_dashboard(risk_metrics):
    """Create interactive risk gauge dashboard"""
    
    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=('Profit Factor', 'Win Rate', 'Sharpe Ratio', 
                       'Recovery Factor', 'Risk Score', 'Consistency')
    )
    
    # Profit Factor Gauge
    pf = risk_metrics.get('profit_factor', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=pf,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Profit Factor"},
        delta={'reference': 1.5},
        gauge={
            'axis': {'range': [None, 3]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "lightgray"},
                {'range': [1, 1.5], 'color': "gray"},
                {'range': [1.5, 3], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 2
            }
        }
    ), row=1, col=1)
    
    # Win Rate Gauge
    wr = risk_metrics.get('win_rate', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=wr,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Win Rate (%)"},
        delta={'reference': 60},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "gray"},
                {'range': [60, 100], 'color': "lightgreen"}
            ]
        }
    ), row=1, col=2)
    
    # Sharpe Ratio Gauge
    sr = risk_metrics.get('sharpe_ratio', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=sr,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sharpe Ratio"},
        delta={'reference': 1.0},
        gauge={
            'axis': {'range': [-1, 3]},
            'bar': {'color': "purple"},
            'steps': [
                {'range': [-1, 0], 'color': "lightgray"},
                {'range': [0, 1], 'color': "gray"},
                {'range': [1, 3], 'color': "lightgreen"}
            ]
        }
    ), row=1, col=3)
    
    # Add more gauges...
    
    fig.update_layout(
        height=600,
        title="Risk Metrics Dashboard"
    )
    
    return fig

def create_trade_distribution_analysis(trades_df):
    """Create interactive trade distribution analysis"""
    
    if trades_df.empty:
        return go.Figure()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Profit Distribution', 'Trade Size Distribution',
                       'Hourly Trading Pattern', 'Monthly Performance'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Profit distribution
    fig.add_trace(
        go.Histogram(
            x=trades_df['profit'],
            nbinsx=50,
            name='Profit Distribution',
            marker_color='rgba(59, 130, 246, 0.7)',
            hovertemplate='Range: $%{x}<br>Count: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Trade size distribution (if volume available)
    if 'volume' in trades_df.columns:
        fig.add_trace(
            go.Histogram(
                x=trades_df['volume'],
                nbinsx=30,
                name='Volume Distribution',
                marker_color='rgba(16, 185, 129, 0.7)',
                hovertemplate='Volume: %{x}<br>Count: %{y}<extra></extra>'
            ),
            row=1, col=2
        )
    
    # Hourly pattern
    hourly_data = trades_df.groupby(trades_df['time'].dt.hour)['profit'].agg(['count', 'sum'])
    fig.add_trace(
        go.Bar(
            x=hourly_data.index,
            y=hourly_data['sum'],
            name='Hourly P&L',
            marker_color=['#10b981' if p > 0 else '#ef4444' for p in hourly_data['sum']],
            hovertemplate='Hour: %{x}<br>P&L: $%{y:,.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Monthly performance
    monthly_data = trades_df.groupby(trades_df['time'].dt.to_period('M'))['profit'].sum()
    fig.add_trace(
        go.Bar(
            x=[str(m) for m in monthly_data.index],
            y=monthly_data.values,
            name='Monthly P&L',
            marker_color=['#10b981' if p > 0 else '#ef4444' for p in monthly_data.values],
            hovertemplate='Month: %{x}<br>P&L: $%{y:,.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title="Trade Distribution Analysis",
        showlegend=False
    )
    
    return fig

def create_comparison_tool(current_metrics, benchmark_metrics=None):
    """Create strategy comparison tool"""
    
    if benchmark_metrics is None:
        # Use industry benchmarks
        benchmark_metrics = {
            'profit_factor': 1.5,
            'win_rate': 55.0,
            'sharpe_ratio': 1.0,
            'risk_reward_ratio': 2.0
        }
    
    metrics = ['Profit Factor', 'Win Rate (%)', 'Sharpe Ratio', 'Risk-Reward Ratio']
    current_values = [
        current_metrics.get('profit_factor', 0),
        current_metrics.get('win_rate', 0),
        current_metrics.get('sharpe_ratio', 0),
        current_metrics.get('risk_reward_ratio', 0)
    ]
    benchmark_values = [
        benchmark_metrics.get('profit_factor', 1.5),
        benchmark_metrics.get('win_rate', 55.0),
        benchmark_metrics.get('sharpe_ratio', 1.0),
        benchmark_metrics.get('risk_reward_ratio', 2.0)
    ]
    
    fig = go.Figure()
    
    # Current strategy
    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=metrics,
        fill='toself',
        name='Your Strategy',
        line_color='#3b82f6'
    ))
    
    # Benchmark
    fig.add_trace(go.Scatterpolar(
        r=benchmark_values,
        theta=metrics,
        fill='toself',
        name='Benchmark',
        line_color='#10b981',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(current_values), max(benchmark_values)) * 1.1]
            )
        ),
        title="Strategy vs Benchmark Comparison",
        height=500
    )
    
    return fig