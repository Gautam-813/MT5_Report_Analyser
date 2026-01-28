"""
Advanced Live Trade Charts
Additional visualization functions for comprehensive live trading analysis
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def create_daily_performance_calendar(positions_df, title="Daily Performance Calendar"):
    """Create calendar heatmap showing daily P&L performance"""
    
    if positions_df.empty:
        return go.Figure().add_annotation(text="No trading data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Prepare daily data
    positions_df['date'] = pd.to_datetime(positions_df['time']).dt.date
    daily_pnl = positions_df.groupby('date').agg({
        'profit': ['sum', 'count']
    }).round(2)
    
    # Flatten column names
    daily_pnl.columns = ['daily_profit', 'trade_count']
    daily_pnl = daily_pnl.reset_index()
    
    # Add weekday and week information
    daily_pnl['weekday'] = pd.to_datetime(daily_pnl['date']).dt.day_name()
    daily_pnl['week'] = pd.to_datetime(daily_pnl['date']).dt.isocalendar().week
    daily_pnl['day_of_week'] = pd.to_datetime(daily_pnl['date']).dt.dayofweek
    
    # Create calendar-style heatmap
    fig = go.Figure(data=go.Scatter(
        x=daily_pnl['week'],
        y=daily_pnl['day_of_week'],
        mode='markers+text',
        marker=dict(
            size=40,
            color=daily_pnl['daily_profit'],
            colorscale='RdYlGn',
            cmid=0,
            showscale=True,
            colorbar=dict(title="Daily P&L ($)")
        ),
        text=[f"{date.strftime('%m/%d')}<br>${profit:.1f}" 
              for date, profit in zip(daily_pnl['date'], daily_pnl['daily_profit'])],
        textposition="middle center",
        hovertemplate='<b>%{text}</b><br>' +
                     'Trades: %{customdata}<br>' +
                     '<extra></extra>',
        customdata=daily_pnl['trade_count']
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=400,
        xaxis_title="Week Number",
        yaxis_title="Day of Week",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        )
    )
    
    return fig

def create_cumulative_pnl_curve(positions_df, title="Cumulative P&L Progression"):
    """Create cumulative P&L curve showing trading progression over time"""
    
    if positions_df.empty:
        return go.Figure().add_annotation(text="No trading data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Sort by time and calculate cumulative P&L
    positions_sorted = positions_df.sort_values('time').copy()
    positions_sorted['cumulative_pnl'] = positions_sorted['profit'].cumsum()
    positions_sorted['trade_number'] = range(1, len(positions_sorted) + 1)
    
    # Calculate running maximum for drawdown
    positions_sorted['running_max'] = positions_sorted['cumulative_pnl'].expanding().max()
    positions_sorted['drawdown'] = positions_sorted['cumulative_pnl'] - positions_sorted['running_max']
    
    # Create subplot with cumulative P&L and drawdown
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Cumulative P&L Over Time', 'Drawdown'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Cumulative P&L line
    fig.add_trace(
        go.Scatter(
            x=positions_sorted['time'],
            y=positions_sorted['cumulative_pnl'],
            mode='lines',
            name='Cumulative P&L',
            line=dict(color='#00D4AA', width=3),
            hovertemplate='<b>Trade #%{customdata}</b><br>' +
                         'Time: %{x}<br>' +
                         'Cumulative P&L: $%{y:.2f}<extra></extra>',
            customdata=positions_sorted['trade_number']
        ),
        row=1, col=1
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=1)
    
    # Drawdown area chart
    fig.add_trace(
        go.Scatter(
            x=positions_sorted['time'],
            y=positions_sorted['drawdown'],
            mode='lines',
            name='Drawdown',
            fill='tonexty',
            line=dict(color='#FF6B6B', width=2),
            fillcolor='rgba(255, 107, 107, 0.3)',
            hovertemplate='<b>Drawdown</b><br>' +
                         'Time: %{x}<br>' +
                         'Drawdown: $%{y:.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative P&L ($)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown ($)", row=2, col=1)
    
    return fig

def create_trade_size_vs_profit_scatter(positions_df, title="Trade Size vs Profit Analysis"):
    """Create scatter plot showing relationship between trade size and profit"""
    
    if positions_df.empty or 'volume' not in positions_df.columns:
        return go.Figure().add_annotation(text="No volume data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Prepare data
    scatter_data = positions_df.copy()
    scatter_data['trade_type'] = scatter_data['type'].str.title()
    scatter_data['profit_category'] = scatter_data['profit'].apply(
        lambda x: 'Profit' if x > 0 else ('Loss' if x < 0 else 'Breakeven')
    )
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add traces for different profit categories
    for category in ['Profit', 'Loss', 'Breakeven']:
        category_data = scatter_data[scatter_data['profit_category'] == category]
        if not category_data.empty:
            color = '#00D4AA' if category == 'Profit' else ('#FF6B6B' if category == 'Loss' else '#FFA500')
            
            fig.add_trace(
                go.Scatter(
                    x=category_data['volume'],
                    y=category_data['profit'],
                    mode='markers',
                    name=f'{category} Trades',
                    marker=dict(
                        color=color,
                        size=8,
                        opacity=0.7
                    ),
                    hovertemplate='<b>%{fullData.name}</b><br>' +
                                 'Volume: %{x}<br>' +
                                 'Profit: $%{y:.2f}<br>' +
                                 'Type: %{customdata}<extra></extra>',
                    customdata=category_data['trade_type']
                )
            )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=500,
        xaxis_title="Trade Volume",
        yaxis_title="Profit/Loss ($)",
        showlegend=True
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig

def create_weekday_performance_analysis(positions_df, title="Weekday Performance Analysis"):
    """Create analysis of performance by day of the week"""
    
    if positions_df.empty:
        return go.Figure().add_annotation(text="No trading data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Prepare weekday data
    positions_df['weekday'] = pd.to_datetime(positions_df['time']).dt.day_name()
    weekday_stats = positions_df.groupby('weekday').agg({
        'profit': ['sum', 'count', 'mean'],
        'time': 'count'
    }).round(2)
    
    # Flatten column names
    weekday_stats.columns = ['total_profit', 'trade_count', 'avg_profit', 'total_trades']
    weekday_stats = weekday_stats.reset_index()
    
    # Reorder weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_stats['weekday'] = pd.Categorical(weekday_stats['weekday'], categories=weekday_order, ordered=True)
    weekday_stats = weekday_stats.sort_values('weekday').reset_index(drop=True)
    
    # Create subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total P&L by Weekday', 'Average P&L per Trade', 
                       'Trade Count by Weekday', 'Win Rate by Weekday'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    weekdays = weekday_stats['weekday'].astype(str)
    
    # Total P&L
    pnl_colors = ['#00D4AA' if x >= 0 else '#FF6B6B' for x in weekday_stats['total_profit']]
    fig.add_trace(
        go.Bar(
            x=weekdays,
            y=weekday_stats['total_profit'],
            name='Total P&L',
            marker_color=pnl_colors,
            text=[f"${x:.2f}" for x in weekday_stats['total_profit']],
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # Average P&L per trade
    avg_colors = ['#00D4AA' if x >= 0 else '#FF6B6B' for x in weekday_stats['avg_profit']]
    fig.add_trace(
        go.Bar(
            x=weekdays,
            y=weekday_stats['avg_profit'],
            name='Avg P&L',
            marker_color=avg_colors,
            text=[f"${x:.2f}" for x in weekday_stats['avg_profit']],
            textposition='auto'
        ),
        row=1, col=2
    )
    
    # Trade count
    fig.add_trace(
        go.Bar(
            x=weekdays,
            y=weekday_stats['trade_count'],
            name='Trade Count',
            marker_color='#4ECDC4',
            text=weekday_stats['trade_count'].astype(str),
            textposition='auto'
        ),
        row=2, col=1
    )
    
    # Calculate win rate by weekday
    win_rates = []
    for weekday in weekday_order:
        weekday_trades = positions_df[positions_df['weekday'] == weekday]
        if len(weekday_trades) > 0:
            win_rate = (len(weekday_trades[weekday_trades['profit'] > 0]) / len(weekday_trades)) * 100
            win_rates.append(win_rate)
        else:
            win_rates.append(0)
    
    # Filter out weekdays with no trades
    active_weekdays = [wd for wd, wr in zip(weekday_order, win_rates) if wr > 0]
    active_win_rates = [wr for wr in win_rates if wr > 0]
    
    if active_win_rates:
        fig.add_trace(
            go.Bar(
                x=active_weekdays,
                y=active_win_rates,
                name='Win Rate',
                marker_color='#45B7D1',
                text=[f"{x:.1f}%" for x in active_win_rates],
                textposition='auto'
            ),
            row=2, col=2
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=600,
        showlegend=False
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="P&L ($)", row=1, col=1)
    fig.update_yaxes(title_text="Avg P&L ($)", row=1, col=2)
    fig.update_yaxes(title_text="Trade Count", row=2, col=1)
    fig.update_yaxes(title_text="Win Rate (%)", row=2, col=2)
    
    return fig

def create_win_loss_streak_analysis(positions_df, title="Win/Loss Streak Analysis"):
    """Create analysis of consecutive wins and losses"""
    
    if positions_df.empty:
        return go.Figure().add_annotation(text="No trading data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Sort by time
    positions_sorted = positions_df.sort_values('time').copy()
    positions_sorted['is_win'] = positions_sorted['profit'] > 0
    positions_sorted['trade_number'] = range(1, len(positions_sorted) + 1)
    
    # Calculate streaks
    streaks = []
    current_streak = 0
    current_type = None
    current_profit = 0
    
    for idx, row in positions_sorted.iterrows():
        is_win = row['is_win']
        profit = row['profit']
        
        if current_type is None:
            current_type = 'win' if is_win else 'loss'
            current_streak = 1
            current_profit = profit
        elif (is_win and current_type == 'win') or (not is_win and current_type == 'loss'):
            current_streak += 1
            current_profit += profit
        else:
            # Streak ended, record it
            streaks.append({
                'type': current_type,
                'length': current_streak,
                'profit': current_profit,
                'end_trade': row['trade_number'] - 1
            })
            # Start new streak
            current_type = 'win' if is_win else 'loss'
            current_streak = 1
            current_profit = profit
    
    # Add final streak
    if current_streak > 0:
        streaks.append({
            'type': current_type,
            'length': current_streak,
            'profit': current_profit,
            'end_trade': len(positions_sorted)
        })
    
    # Create streak visualization
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Streak Lengths Over Time', 'Streak Profit Impact'),
        vertical_spacing=0.15
    )
    
    if streaks:
        streak_df = pd.DataFrame(streaks)
        
        # Streak lengths over time
        win_streaks = streak_df[streak_df['type'] == 'win']
        loss_streaks = streak_df[streak_df['type'] == 'loss']
        
        if not win_streaks.empty:
            fig.add_trace(
                go.Scatter(
                    x=win_streaks['end_trade'],
                    y=win_streaks['length'],
                    mode='markers',
                    name='Win Streaks',
                    marker=dict(color='#00D4AA', size=10),
                    hovertemplate='<b>Win Streak</b><br>' +
                                 'Length: %{y} trades<br>' +
                                 'Ended at trade: %{x}<br>' +
                                 'Total profit: $%{customdata:.2f}<extra></extra>',
                    customdata=win_streaks['profit']
                ),
                row=1, col=1
            )
        
        if not loss_streaks.empty:
            fig.add_trace(
                go.Scatter(
                    x=loss_streaks['end_trade'],
                    y=loss_streaks['length'],
                    mode='markers',
                    name='Loss Streaks',
                    marker=dict(color='#FF6B6B', size=10),
                    hovertemplate='<b>Loss Streak</b><br>' +
                                 'Length: %{y} trades<br>' +
                                 'Ended at trade: %{x}<br>' +
                                 'Total loss: $%{customdata:.2f}<extra></extra>',
                    customdata=loss_streaks['profit']
                ),
                row=1, col=1
            )
        
        # Streak profit impact
        fig.add_trace(
            go.Bar(
                x=[f"{row['type'].title()} #{i+1}" for i, row in streak_df.iterrows()],
                y=streak_df['profit'],
                name='Streak P&L',
                marker_color=['#00D4AA' if x > 0 else '#FF6B6B' for x in streak_df['profit']],
                text=[f"${x:.2f}" for x in streak_df['profit']],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>' +
                             'Length: %{customdata} trades<br>' +
                             'P&L: $%{y:.2f}<extra></extra>',
                customdata=streak_df['length']
            ),
            row=2, col=1
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_dark',
        height=600,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Trade Number", row=1, col=1)
    fig.update_xaxes(title_text="Streak", row=2, col=1)
    fig.update_yaxes(title_text="Streak Length", row=1, col=1)
    fig.update_yaxes(title_text="Streak P&L ($)", row=2, col=1)
    
    return fig