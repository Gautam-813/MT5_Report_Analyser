"""
Visualization functions for MT5 Report Analyzer
Creates interactive charts using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_daily_pnl_heatmap(daily_stats, theme='light'):
    """Create daily P&L heatmap calendar with theme support"""
    if daily_stats.empty:
        return go.Figure()
    
    # Prepare data for heatmap
    df = daily_stats.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.dayofweek
    df['week'] = df['date'].dt.isocalendar().week
    
    # Create heatmap
    fig = px.density_heatmap(
        df, 
        x='week', 
        y='weekday',
        z='profit_sum',
        color_continuous_scale='RdYlGn',
        title='Daily P&L Heatmap',
        labels={'profit_sum': 'Daily Profit', 'week': 'Week of Year', 'weekday': 'Day of Week'}
    )
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white',
            title_font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black'
        )
    
    # Customize layout
    fig.update_layout(
        height=400,
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        )
    )
    
    return fig

def create_session_performance_chart(session_stats, theme='light'):
    """Create session performance radar chart with theme support"""
    if session_stats.empty:
        return go.Figure()
    
    # Prepare data for radar chart
    sessions = session_stats['session'].tolist()
    profits = session_stats['profit_sum'].tolist()
    win_rates = session_stats['win_rate'].tolist()
    
    fig = go.Figure()
    
    # Add profit trace
    fig.add_trace(go.Scatterpolar(
        r=profits,
        theta=sessions,
        fill='toself',
        name='Total Profit',
        line_color='blue'
    ))
    
    # Normalize win rates for better visualization
    normalized_win_rates = [wr * max(profits) / 100 for wr in win_rates]
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_win_rates,
        theta=sessions,
        fill='toself',
        name='Win Rate (Normalized)',
        line_color='green'
    ))
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white',
            title_font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black'
        )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        title="Session Performance Comparison",
        height=500
    )
    
    return fig

def create_equity_curve(trades_df, theme='light'):
    """Create equity curve (no fake drawdown - we don't have tick data)"""
    if trades_df.empty:
        return go.Figure()
    
    # Calculate cumulative profit only
    df = trades_df.copy()
    df['cumulative'] = df['profit'].cumsum()
    
    # Create single plot (no drawdown)
    fig = go.Figure()
    
    # Add equity curve only
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['cumulative'],
            mode='lines+markers',
            name='Cumulative Profit',
            line=dict(color='blue', width=3),
            marker=dict(size=4)
        )
    )
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white',
            title_font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black'
        )
    
    fig.update_layout(
        title="Equity Curve - Cumulative Profit Over Time",
        xaxis_title="Time",
        yaxis_title="Cumulative Profit ($)",
        height=400,
        showlegend=True
    )
    
    return fig

def create_hourly_performance_chart(hourly_stats, theme='light'):
    """Create hourly performance bar chart with theme support"""
    if hourly_stats.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Add profit bars
    colors = ['red' if profit < 0 else 'green' for profit in hourly_stats['profit_sum']]
    
    fig.add_trace(go.Bar(
        x=hourly_stats['hour'],
        y=hourly_stats['profit_sum'],
        name='Hourly Profit',
        marker_color=colors,
        text=hourly_stats['profit_sum'].round(2),
        textposition='outside'
    ))
    
    # Add session backgrounds
    fig.add_vrect(x0=-0.5, x1=7.5, fillcolor="lightblue", opacity=0.2, 
                  annotation_text="Asian Session", annotation_position="top left")
    fig.add_vrect(x0=7.5, x1=15.5, fillcolor="lightgreen", opacity=0.2,
                  annotation_text="European Session", annotation_position="top")
    fig.add_vrect(x0=15.5, x1=23.5, fillcolor="lightyellow", opacity=0.2,
                  annotation_text="US Session", annotation_position="top right")
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white',
            title_font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black'
        )
    
    fig.update_layout(
        title="Hourly Performance Analysis",
        xaxis_title="Hour of Day (UTC)",
        yaxis_title="Profit",
        height=400,
        showlegend=False
    )
    
    return fig

def create_loss_distribution_chart(trades_df, theme='light'):
    """Create loss distribution histogram with theme support"""
    if trades_df.empty:
        return go.Figure()
    
    losses = trades_df[trades_df['profit'] < 0]['profit']
    
    if losses.empty:
        return go.Figure().add_annotation(
            text="No losses found in the data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=losses,
        nbinsx=20,
        name='Loss Distribution',
        marker_color='red',
        opacity=0.7
    ))
    
    # Add mean line
    mean_loss = losses.mean()
    fig.add_vline(
        x=mean_loss,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Mean Loss: {mean_loss:.2f}"
    )
    
    fig.update_layout(
        title="Loss Distribution Analysis",
        xaxis_title="Loss Amount",
        yaxis_title="Frequency",
        height=400
    )
    
    return fig

def create_session_comparison_chart(session_stats, theme='light'):
    """Create session comparison bar chart with theme support"""
    if session_stats.empty:
        return go.Figure()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Total Profit by Session', 'Win Rate by Session'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Profit bars
    fig.add_trace(
        go.Bar(
            x=session_stats['session'],
            y=session_stats['profit_sum'],
            name='Total Profit',
            marker_color=['red' if p < 0 else 'green' for p in session_stats['profit_sum']]
        ),
        row=1, col=1
    )
    
    # Win rate bars
    fig.add_trace(
        go.Bar(
            x=session_stats['session'],
            y=session_stats['win_rate'],
            name='Win Rate (%)',
            marker_color='blue'
        ),
        row=1, col=2
    )
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white',
            title_font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black'
        )
    
    fig.update_layout(
        title="Session Performance Comparison",
        height=400,
        showlegend=False
    )
    
    return fig

def create_worst_days_chart(worst_days, theme='light'):
    """Create worst days analysis chart with theme support"""
    if worst_days.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=worst_days['date'].astype(str),
        y=worst_days['profit_sum'],
        name='Daily Loss',
        marker_color='red',
        text=worst_days['profit_sum'].round(2),
        textposition='outside'
    ))
    
    # Theme-based styling
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    else:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black'
        )
    
    fig.update_layout(
        title="Worst Performing Days",
        xaxis_title="Date",
        yaxis_title="Loss Amount",
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

def create_metrics_gauge_chart(risk_metrics, theme='light'):
    """Create gauge charts for key metrics with theme support"""
    if not risk_metrics:
        return go.Figure()
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=('Win Rate', 'Profit Factor', 'Sharpe Ratio', 'Risk-Reward Ratio')
    )
    
    # Win Rate Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_metrics.get('win_rate', 0),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Win Rate (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkgreen"},
               'steps': [{'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4},
                           'thickness': 0.75, 'value': 90}}
    ), row=1, col=1)
    
    # Profit Factor Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_metrics.get('profit_factor', 0),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Profit Factor"},
        gauge={'axis': {'range': [0, 3]},
               'bar': {'color': "darkblue"},
               'steps': [{'range': [0, 1], 'color': "lightgray"},
                        {'range': [1, 2], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4},
                           'thickness': 0.75, 'value': 2}}
    ), row=1, col=2)
    
    # Sharpe Ratio Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_metrics.get('sharpe_ratio', 0),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sharpe Ratio"},
        gauge={'axis': {'range': [-2, 3]},
               'bar': {'color': "purple"},
               'steps': [{'range': [-2, 0], 'color': "lightgray"},
                        {'range': [0, 1], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4},
                           'thickness': 0.75, 'value': 2}}
    ), row=2, col=1)
    
    # Risk-Reward Ratio (proper trading metric)
    rr_ratio = risk_metrics.get('risk_reward_ratio', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=rr_ratio,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk-Reward Ratio"},
        gauge={'axis': {'range': [0, 5]},
               'bar': {'color': "blue"},
               'steps': [{'range': [0, 1], 'color': "red"},
                        {'range': [1, 2], 'color': "yellow"},
                        {'range': [2, 5], 'color': "lightgreen"}]}
    ), row=2, col=2)
    
    fig.update_layout(height=600, title="Key Performance Metrics")
    
    return fig

def create_entries_by_hours_chart(trades_df, theme='light'):
    """Create bar chart showing number of entries by hour"""
    if trades_df.empty or 'time' not in trades_df.columns:
        return go.Figure()
    
    # Extract hour from time
    df = trades_df.copy()
    df['hour'] = df['time'].dt.hour
    
    # Count entries by hour
    hourly_entries = df.groupby('hour').size().reset_index(name='entries')
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=hourly_entries['hour'],
            y=hourly_entries['entries'],
            name='Entries',
            marker_color='#3b82f6',
            text=hourly_entries['entries'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Trading Entries by Hour of Day',
        xaxis_title='Hour (0-23)',
        yaxis_title='Number of Entries',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        showlegend=False
    )
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_entries_by_weekdays_chart(trades_df, theme='light'):
    """Create bar chart showing number of entries by weekday"""
    if trades_df.empty or 'time' not in trades_df.columns:
        return go.Figure()
    
    # Extract weekday from time
    df = trades_df.copy()
    df['weekday'] = df['time'].dt.day_name()
    
    # Define weekday order
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count entries by weekday
    weekday_entries = df.groupby('weekday').size().reset_index(name='entries')
    weekday_entries['weekday'] = pd.Categorical(weekday_entries['weekday'], categories=weekday_order, ordered=True)
    weekday_entries = weekday_entries.sort_values('weekday')
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=weekday_entries['weekday'],
            y=weekday_entries['entries'],
            name='Entries',
            marker_color='#10b981',
            text=weekday_entries['entries'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Trading Entries by Weekday',
        xaxis_title='Day of Week',
        yaxis_title='Number of Entries',
        showlegend=False
    )
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_entries_by_months_chart(trades_df, theme='light'):
    """Create bar chart showing number of entries by month"""
    if trades_df.empty or 'time' not in trades_df.columns:
        return go.Figure()
    
    # Extract month from time
    df = trades_df.copy()
    df['month'] = df['time'].dt.month_name()
    
    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    # Count entries by month
    monthly_entries = df.groupby('month').size().reset_index(name='entries')
    monthly_entries['month'] = pd.Categorical(monthly_entries['month'], categories=month_order, ordered=True)
    monthly_entries = monthly_entries.sort_values('month')
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=monthly_entries['month'],
            y=monthly_entries['entries'],
            name='Entries',
            marker_color='#f59e0b',
            text=monthly_entries['entries'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Trading Entries by Month',
        xaxis_title='Month',
        yaxis_title='Number of Entries',
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_pnl_by_hours_chart(trades_df, theme='light'):
    """Create bar chart showing profit/loss by hour"""
    if trades_df.empty or 'time' not in trades_df.columns or 'profit' not in trades_df.columns:
        return go.Figure()
    
    # Extract hour from time
    df = trades_df.copy()
    df['hour'] = df['time'].dt.hour
    
    # Sum profit/loss by hour
    hourly_pnl = df.groupby('hour')['profit'].sum().reset_index()
    
    # Color bars based on profit/loss
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in hourly_pnl['profit']]
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=hourly_pnl['hour'],
            y=hourly_pnl['profit'],
            name='P&L',
            marker_color=colors,
            text=[f'${x:.2f}' for x in hourly_pnl['profit']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Profit & Loss by Hour of Day',
        xaxis_title='Hour (0-23)',
        yaxis_title='Profit & Loss ($)',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        showlegend=False
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_pnl_by_weekdays_chart(trades_df, theme='light'):
    """Create bar chart showing profit/loss by weekday"""
    if trades_df.empty or 'time' not in trades_df.columns or 'profit' not in trades_df.columns:
        return go.Figure()
    
    # Extract weekday from time
    df = trades_df.copy()
    df['weekday'] = df['time'].dt.day_name()
    
    # Define weekday order
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Sum profit/loss by weekday
    weekday_pnl = df.groupby('weekday')['profit'].sum().reset_index()
    weekday_pnl['weekday'] = pd.Categorical(weekday_pnl['weekday'], categories=weekday_order, ordered=True)
    weekday_pnl = weekday_pnl.sort_values('weekday')
    
    # Color bars based on profit/loss
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in weekday_pnl['profit']]
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=weekday_pnl['weekday'],
            y=weekday_pnl['profit'],
            name='P&L',
            marker_color=colors,
            text=[f'${x:.2f}' for x in weekday_pnl['profit']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Profit & Loss by Weekday',
        xaxis_title='Day of Week',
        yaxis_title='Profit & Loss ($)',
        showlegend=False
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig

def create_pnl_by_months_chart(trades_df, theme='light'):
    """Create bar chart showing profit/loss by month"""
    if trades_df.empty or 'time' not in trades_df.columns or 'profit' not in trades_df.columns:
        return go.Figure()
    
    # Extract month from time
    df = trades_df.copy()
    df['month'] = df['time'].dt.month_name()
    
    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    # Sum profit/loss by month
    monthly_pnl = df.groupby('month')['profit'].sum().reset_index()
    monthly_pnl['month'] = pd.Categorical(monthly_pnl['month'], categories=month_order, ordered=True)
    monthly_pnl = monthly_pnl.sort_values('month')
    
    # Color bars based on profit/loss
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in monthly_pnl['profit']]
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=monthly_pnl['month'],
            y=monthly_pnl['profit'],
            name='P&L',
            marker_color=colors,
            text=[f'${x:.2f}' for x in monthly_pnl['profit']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Profit & Loss by Month',
        xaxis_title='Month',
        yaxis_title='Profit & Loss ($)',
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    # Apply theme
    if theme == 'dark':
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
    
    return fig