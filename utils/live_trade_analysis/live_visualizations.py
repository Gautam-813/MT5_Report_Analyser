"""
Live Trade Visualizations
Creates charts and visualizations specific to live trading analysis
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_buy_sell_analysis(positions_df, title="Buy vs Sell Trade Analysis"):
    """Create analysis of buy vs sell trades with profit/loss breakdown"""
    
    if positions_df.empty:
        return go.Figure().add_annotation(text="No trading data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Analyze buy trades
    buy_trades = positions_df[positions_df['type'].str.lower() == 'buy']
    buy_profit = buy_trades[buy_trades['profit'] > 0]
    buy_loss = buy_trades[buy_trades['profit'] < 0]
    
    # Analyze sell trades
    sell_trades = positions_df[positions_df['type'].str.lower() == 'sell']
    sell_profit = sell_trades[sell_trades['profit'] > 0]
    sell_loss = sell_trades[sell_trades['profit'] < 0]
    
    # Create subplot with 2 charts side by side
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Buy Trades Analysis', 'Sell Trades Analysis'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Buy trades chart
    buy_categories = ['Total Buy', 'Buy Profit', 'Buy Loss']
    buy_values = [len(buy_trades), len(buy_profit), len(buy_loss)]
    buy_colors = ['#4ECDC4', '#00D4AA', '#FF6B6B']
    
    fig.add_trace(
        go.Bar(
            x=buy_categories,
            y=buy_values,
            name='Buy Trades',
            marker_color=buy_colors,
            text=buy_values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Sell trades chart
    sell_categories = ['Total Sell', 'Sell Profit', 'Sell Loss']
    sell_values = [len(sell_trades), len(sell_profit), len(sell_loss)]
    sell_colors = ['#45B7D1', '#00D4AA', '#FF6B6B']
    
    fig.add_trace(
        go.Bar(
            x=sell_categories,
            y=sell_values,
            name='Sell Trades',
            marker_color=sell_colors,
            text=sell_values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=500,
        showlegend=False
    )
    
    # Update axes
    fig.update_yaxes(title_text="Number of Trades", row=1, col=1)
    fig.update_yaxes(title_text="Number of Trades", row=1, col=2)
    
    return fig

def create_session_wise_analysis(session_stats, title="Session-wise Profit & Loss Analysis"):
    """Create session-wise profit and loss analysis chart"""
    
    if session_stats.empty:
        return go.Figure().add_annotation(text="No session data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Create subplot with profit/loss analysis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total P&L by Session', 'Win Rate by Session', 
                       'Average Trade by Session', 'Trade Count by Session'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    sessions = session_stats['session']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue for Asian, European, US
    
    # Total P&L by session
    pnl_colors = ['#00D4AA' if x >= 0 else '#FF6B6B' for x in session_stats['profit_sum']]
    fig.add_trace(
        go.Bar(
            x=sessions,
            y=session_stats['profit_sum'],
            name='Total P&L',
            marker_color=pnl_colors,
            text=[f"${x:.2f}" for x in session_stats['profit_sum']],
            textposition='auto',
            hovertemplate='<b>%{x} Session</b><br>Total P&L: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Win Rate by session
    fig.add_trace(
        go.Bar(
            x=sessions,
            y=session_stats['win_rate'],
            name='Win Rate',
            marker_color=colors,
            text=[f"{x:.1f}%" for x in session_stats['win_rate']],
            textposition='auto',
            hovertemplate='<b>%{x} Session</b><br>Win Rate: %{y:.1f}%<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Average trade by session
    avg_colors = ['#00D4AA' if x >= 0 else '#FF6B6B' for x in session_stats['profit_mean']]
    fig.add_trace(
        go.Bar(
            x=sessions,
            y=session_stats['profit_mean'],
            name='Avg Trade',
            marker_color=avg_colors,
            text=[f"${x:.2f}" for x in session_stats['profit_mean']],
            textposition='auto',
            hovertemplate='<b>%{x} Session</b><br>Avg Trade: $%{y:.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Trade count by session
    fig.add_trace(
        go.Bar(
            x=sessions,
            y=session_stats['profit_count'],
            name='Trade Count',
            marker_color=colors,
            text=session_stats['profit_count'].astype(str),
            textposition='auto',
            hovertemplate='<b>%{x} Session</b><br>Trades: %{y}<extra></extra>'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=600,
        showlegend=False
    )
    
    # Update y-axes titles
    fig.update_yaxes(title_text="P&L ($)", row=1, col=1)
    fig.update_yaxes(title_text="Win Rate (%)", row=1, col=2)
    fig.update_yaxes(title_text="Avg P&L ($)", row=2, col=1)
    fig.update_yaxes(title_text="Trade Count", row=2, col=2)
    
    return fig
def create_hourly_performance_chart(hourly_stats, title="Hourly Performance Analysis"):
    """Create hourly performance bar chart with time ranges"""
    
    if hourly_stats.empty:
        return go.Figure().add_annotation(text="No hourly data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Create subplot with 2 charts
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Hourly P&L Distribution', 'Hourly Trade Count'),
        vertical_spacing=0.15,
        row_heights=[0.6, 0.4]
    )
    
    # Get hour ranges and data
    hour_ranges = hourly_stats['hour_range']
    profit_sums = hourly_stats['profit_sum']
    trade_counts = hourly_stats['profit_count']
    
    # Color coding for P&L bars
    pnl_colors = ['#00D4AA' if x >= 0 else '#FF6B6B' for x in profit_sums]
    
    # Hourly P&L Bar Chart
    fig.add_trace(
        go.Bar(
            x=hour_ranges,
            y=profit_sums,
            name='Hourly P&L',
            marker_color=pnl_colors,
            text=[f"${x:.2f}" for x in profit_sums],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>' +
                         'P&L: $%{y:.2f}<br>' +
                         '<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Hourly Trade Count Bar Chart
    fig.add_trace(
        go.Bar(
            x=hour_ranges,
            y=trade_counts,
            name='Trade Count',
            marker_color='#4ECDC4',
            text=[str(x) for x in trade_counts],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>' +
                         'Trades: %{y}<br>' +
                         '<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=700,
        showlegend=False
    )
    
    # Update axes
    fig.update_xaxes(title_text="Hour Range", row=2, col=1)
    fig.update_yaxes(title_text="P&L ($)", row=1, col=1)
    fig.update_yaxes(title_text="Number of Trades", row=2, col=1)
    
    # Add zero line for P&L chart
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=1)
    
    return fig