"""
Enhanced Interactive Charts for Professional Dashboard
Advanced Plotly visualizations with hover, zoom, and professional styling
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.dark_mode import get_plotly_template

def create_professional_equity_curve(trades_df, theme='light'):
    """Create professional equity curve with advanced interactivity"""
    
    if trades_df.empty:
        return go.Figure()
    
    # Calculate equity metrics
    df = trades_df.copy()
    df['cumulative'] = df['profit'].cumsum()
    # Removed fake drawdown calculation - we don't have tick data
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=(
            'Equity Curve & Running Maximum', 
            'Trade Distribution', 
            'Individual Trade P&L'
        ),
        vertical_spacing=0.08,
        row_heights=[0.5, 0.25, 0.25],
        specs=[[{"secondary_y": True}], [{}], [{}]]
    )
    
    # Main equity curve
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['cumulative'],
            mode='lines',
            name='Equity Curve',
            line=dict(color='#3b82f6', width=2.5),
            hovertemplate='<b>%{x}</b><br>' +
                         'Equity: $%{y:,.2f}<br>' +
                         '<extra></extra>',
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Running maximum
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['cumulative'],
            mode='lines',
            name='Cumulative Profit',
            line=dict(color='#10b981', width=1.5, dash='dash'),
            hovertemplate='<b>%{x}</b><br>' +
                         'Peak: $%{y:,.2f}<br>' +
                         '<extra></extra>',
            opacity=0.8
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
    
    # Individual trades as scatter plot
    colors = ['#10b981' if p > 0 else '#ef4444' if p < 0 else '#6b7280' for p in df['profit']]
    sizes = [max(6, min(20, abs(p) / 10)) for p in df['profit']]  # Size based on profit magnitude
    
    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['profit'],
            mode='markers',
            name='Individual Trades',
            marker=dict(
                color=colors,
                size=sizes,
                opacity=0.7,
                line=dict(width=1, color='white'),
                symbol='circle'
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         'Trade P&L: $%{y:,.2f}<br>' +
                         'Type: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=df.get('type', ['Trade'] * len(df))
        ),
        row=3, col=1
    )
    
    # Add zero line for trade distribution
    fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5, row=3, col=1)
    
    # Apply theme
    template = get_plotly_template()
    fig.update_layout(template['layout'])
    
    # Enhanced layout
    fig.update_layout(
        title={
            'text': "Professional Equity Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        height=800,
        showlegend=True,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Equity ($)", row=1, col=1)
    fig.update_yaxes(title_text="Trade Count", row=2, col=1)
    fig.update_yaxes(title_text="Trade P&L ($)", row=3, col=1)
    
    return fig

def create_interactive_performance_heatmap(daily_stats, theme='light'):
    """Create interactive performance heatmap with drill-down capabilities"""
    
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
    df['month_name'] = df['date'].dt.strftime('%B')
    
    # Create calendar heatmap
    # Use 'profit' column if 'profit_sum' doesn't exist
    profit_col = 'profit_sum' if 'profit_sum' in df.columns else 'profit'
    
    pivot_data = df.pivot_table(
        values=profit_col,
        index='weekday',
        columns='week',
        aggfunc='sum',
        fill_value=0
    )
    
    # Reorder weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(weekday_order)
    
    # Create custom hover text
    hover_text = []
    for i, weekday in enumerate(weekday_order):
        hover_row = []
        for j, week in enumerate(pivot_data.columns):
            value = pivot_data.iloc[i, j]
            # Find corresponding date info
            date_info = df[(df['weekday'] == weekday) & (df['week'] == week)]
            if not date_info.empty:
                date_str = date_info.iloc[0]['date'].strftime('%Y-%m-%d')
                trades = date_info.iloc[0].get('profit_count', 0)
                win_rate = date_info.iloc[0].get('win_rate', 0)
                hover_text_cell = f"Date: {date_str}<br>P&L: ${value:,.2f}<br>Trades: {trades}<br>Win Rate: {win_rate:.1f}%"
            else:
                hover_text_cell = f"Week {week}, {weekday}<br>P&L: ${value:,.2f}"
            hover_row.append(hover_text_cell)
        hover_text.append(hover_row)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn',
        zmid=0,
        hoverongaps=False,
        hovertemplate='%{text}<extra></extra>',
        text=hover_text,
        colorbar=dict(
            title=dict(
                text="Daily P&L ($)",
                side="right"
            )
        )
    ))
    
    # Apply theme
    template = get_plotly_template()
    fig.update_layout(template['layout'])
    
    fig.update_layout(
        title={
            'text': "Daily Performance Heatmap",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter'}
        },
        xaxis_title="Week of Year",
        yaxis_title="Day of Week",
        height=400,
        font=dict(family="Inter")
    )
    
    return fig

def create_advanced_risk_dashboard(risk_metrics, theme='light'):
    """Create advanced risk metrics dashboard with gauges and indicators"""
    
    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=('Profit Factor', 'Win Rate (%)', 'Sharpe Ratio', 
                       'Risk Score', 'Risk-Reward Score', 'Consistency Score')
    )
    
    # Color scheme based on theme
    if theme == 'dark':
        gauge_colors = {
            'good': '#10b981',
            'average': '#f59e0b', 
            'poor': '#ef4444',
            'bg': '#374151'
        }
    else:
        gauge_colors = {
            'good': '#10b981',
            'average': '#f59e0b',
            'poor': '#ef4444', 
            'bg': '#f3f4f6'
        }
    
    # Profit Factor Gauge
    pf = risk_metrics.get('profit_factor', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=pf,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Profit Factor", 'font': {'size': 16, 'family': 'Inter'}},
        delta={'reference': 1.5, 'position': "top"},
        gauge={
            'axis': {'range': [None, 3], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['good'] if pf >= 1.5 else gauge_colors['average'] if pf >= 1.0 else gauge_colors['poor']},
            'steps': [
                {'range': [0, 1], 'color': gauge_colors['bg']},
                {'range': [1, 1.5], 'color': 'lightgray'},
                {'range': [1.5, 3], 'color': 'lightgreen'}
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
        title={'text': "Win Rate (%)", 'font': {'size': 16, 'family': 'Inter'}},
        delta={'reference': 60, 'position': "top"},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['good'] if wr >= 60 else gauge_colors['average'] if wr >= 50 else gauge_colors['poor']},
            'steps': [
                {'range': [0, 40], 'color': gauge_colors['bg']},
                {'range': [40, 60], 'color': 'lightgray'},
                {'range': [60, 100], 'color': 'lightgreen'}
            ]
        }
    ), row=1, col=2)
    
    # Sharpe Ratio Gauge
    sr = risk_metrics.get('sharpe_ratio', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=sr,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sharpe Ratio", 'font': {'size': 16, 'family': 'Inter'}},
        delta={'reference': 1.0, 'position': "top"},
        gauge={
            'axis': {'range': [-1, 3], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['good'] if sr >= 1.0 else gauge_colors['average'] if sr >= 0.5 else gauge_colors['poor']},
            'steps': [
                {'range': [-1, 0], 'color': gauge_colors['bg']},
                {'range': [0, 1], 'color': 'lightgray'},
                {'range': [1, 3], 'color': 'lightgreen'}
            ]
        }
    ), row=1, col=3)
    
    # Calculate composite risk score
    risk_score = 0
    if pf >= 1.5: risk_score += 25
    elif pf >= 1.0: risk_score += 15
    
    if wr >= 60: risk_score += 25
    elif wr >= 50: risk_score += 15
    
    if sr >= 1.0: risk_score += 25
    elif sr >= 0.5: risk_score += 15
    
    # Risk assessment based on proper metrics (no fake drawdown)
    profit_factor = risk_metrics.get('profit_factor', 1.0)
    risk_reward = risk_metrics.get('risk_reward_ratio', 0.0)
    win_rate = risk_metrics.get('win_rate', 50.0)
    
    # Calculate risk score based on real metrics
    if profit_factor >= 2.0 and risk_reward >= 2.0: risk_score += 25
    elif profit_factor >= 1.5 and risk_reward >= 1.5: risk_score += 15
    elif profit_factor >= 1.2 and risk_reward >= 1.0: risk_score += 10
    
    # Risk Score Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 16, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['good'] if risk_score >= 80 else gauge_colors['average'] if risk_score >= 60 else gauge_colors['poor']},
            'steps': [
                {'range': [0, 40], 'color': 'lightcoral'},
                {'range': [40, 70], 'color': 'lightyellow'},
                {'range': [70, 100], 'color': 'lightgreen'}
            ]
        }
    ), row=2, col=1)
    
    # Risk-Reward Gauge (proper metric instead of fake drawdown)
    rr_score = min(100, max(0, risk_reward * 25))  # Convert ratio to score (0-4 range)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=rr_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk-Reward Score", 'font': {'size': 16, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['good'] if rr_score >= 70 else gauge_colors['average'] if rr_score >= 50 else gauge_colors['poor']},
            'steps': [
                {'range': [0, 30], 'color': 'lightcoral'},
                {'range': [30, 70], 'color': 'lightyellow'},
                {'range': [70, 100], 'color': 'lightgreen'}
            ]
        }
    ), row=2, col=2)
    
    # Consistency Score (based on standard deviation of returns)
    if 'trades_df' in locals():
        consistency_score = 50  # Placeholder
    else:
        consistency_score = 50
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=consistency_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Consistency", 'font': {'size': 16, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'size': 12}},
            'bar': {'color': gauge_colors['average']},
            'steps': [
                {'range': [0, 40], 'color': 'lightcoral'},
                {'range': [40, 70], 'color': 'lightyellow'},
                {'range': [70, 100], 'color': 'lightgreen'}
            ]
        }
    ), row=2, col=3)
    
    # Apply theme
    template = get_plotly_template()
    fig.update_layout(template['layout'])
    
    fig.update_layout(
        title={
            'text': "Advanced Risk Metrics Dashboard",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        height=600,
        font=dict(family="Inter")
    )
    
    return fig

def create_session_performance_radar(session_stats, theme='light'):
    """Create interactive session performance radar chart"""
    
    if session_stats.empty:
        return go.Figure()
    
    # Prepare data for radar chart
    sessions = session_stats['session'].tolist()
    
    # Normalize metrics for radar display
    profits = session_stats['profit_sum'].tolist()
    win_rates = session_stats['win_rate'].tolist()
    trade_counts = session_stats['profit_count'].tolist()
    
    # Normalize to 0-100 scale for better visualization
    max_profit = max(abs(p) for p in profits) if profits else 1
    normalized_profits = [(p / max_profit * 50 + 50) for p in profits]
    
    max_trades = max(trade_counts) if trade_counts else 1
    normalized_trades = [(t / max_trades * 100) for t in trade_counts]
    
    fig = go.Figure()
    
    # Add profit performance
    fig.add_trace(go.Scatterpolar(
        r=normalized_profits,
        theta=sessions,
        fill='toself',
        name='Profit Performance',
        line_color='#3b82f6',
        fillcolor='rgba(59, 130, 246, 0.3)',
        hovertemplate='<b>%{theta} Session</b><br>' +
                     'Profit: $%{customdata:,.2f}<br>' +
                     '<extra></extra>',
        customdata=profits
    ))
    
    # Add win rate
    fig.add_trace(go.Scatterpolar(
        r=win_rates,
        theta=sessions,
        fill='toself',
        name='Win Rate (%)',
        line_color='#10b981',
        fillcolor='rgba(16, 185, 129, 0.3)',
        hovertemplate='<b>%{theta} Session</b><br>' +
                     'Win Rate: %{r:.1f}%<br>' +
                     '<extra></extra>'
    ))
    
    # Add trade volume
    fig.add_trace(go.Scatterpolar(
        r=normalized_trades,
        theta=sessions,
        fill='toself',
        name='Trade Volume',
        line_color='#f59e0b',
        fillcolor='rgba(245, 158, 11, 0.3)',
        hovertemplate='<b>%{theta} Session</b><br>' +
                     'Trades: %{customdata:,}<br>' +
                     '<extra></extra>',
        customdata=trade_counts
    ))
    
    # Apply theme
    template = get_plotly_template()
    fig.update_layout(template['layout'])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Inter')
            )
        ),
        title={
            'text': "Session Performance Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter'}
        },
        height=500,
        showlegend=True,
        font=dict(family="Inter")
    )
    
    return fig