"""
Monte Carlo Risk Simulation for Professional Trading Analysis
Industry-standard risk assessment and scenario modeling
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import streamlit as st

class MonteCarloSimulator:
    """Professional Monte Carlo simulation for trading strategy analysis"""
    
    def __init__(self, trades_df, num_simulations=1000):
        self.trades_df = trades_df
        self.num_simulations = num_simulations
        self.results = None
        
    def run_simulation(self):
        """Run Monte Carlo simulation on trading strategy"""
        
        if self.trades_df.empty:
            return None
            
        # For very large datasets, sample to improve performance
        max_trades = 1000
        if len(self.trades_df) > max_trades:
            trades_sample = self.trades_df.sample(n=max_trades, random_state=42).reset_index(drop=True)
        else:
            trades_sample = self.trades_df
            
        # Calculate trade statistics
        returns = trades_sample['profit'].values
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        num_trades = len(returns)
        
        # Generate random scenarios using vectorized operations for better performance
        # Generate all random returns at once
        random_returns = np.random.normal(mean_return, std_return, (self.num_simulations, num_trades))
        
        # Calculate cumulative performance for all simulations at once using vectorized operations
        cumulative = np.cumsum(random_returns, axis=1)
        
        # Calculate key metrics for all simulations
        final_profits = cumulative[:, -1]
        max_profits = np.max(cumulative, axis=1)
        min_profits = np.min(cumulative, axis=1)
        
        # Create results DataFrame more efficiently
        simulations_data = {
            'simulation': range(self.num_simulations),
            'final_profit': final_profits,
            'max_profit': max_profits,
            'min_profit': min_profits
        }
        
        # Only store cumulative paths for a sample of simulations to save memory
        sample_paths = {}
        sample_size = min(50, self.num_simulations)
        sample_indices = np.random.choice(self.num_simulations, sample_size, replace=False)
        
        for i in sample_indices:
            sample_paths[i] = cumulative[i]
            
        self.results = pd.DataFrame(simulations_data)
        self.sample_paths = sample_paths
        
        return self.results
    
    # Removed _calculate_max_drawdown - we don't have tick data for real drawdown
    
    def get_risk_statistics(self):
        """Calculate risk statistics from simulation results"""
        
        if self.results is None:
            return {}
        
        # Value at Risk (VaR) calculations
        var_95 = np.percentile(self.results['final_profit'], 5)
        var_99 = np.percentile(self.results['final_profit'], 1)
        
        # Expected Shortfall (Conditional VaR)
        es_95 = np.mean(self.results['final_profit'][self.results['final_profit'] <= var_95])
        es_99 = np.mean(self.results['final_profit'][self.results['final_profit'] <= var_99])
        
        # Minimum profit statistics (instead of fake drawdown)
        min_95 = np.percentile(self.results['min_profit'], 5)
        min_99 = np.percentile(self.results['min_profit'], 1)
        
        # Probability of loss
        prob_loss = (self.results['final_profit'] < 0).mean() * 100
        
        # Probability of large loss (>$1000)
        large_loss_threshold = -1000  # Adjust based on account size
        prob_large_loss = (self.results['min_profit'] < large_loss_threshold).mean() * 100
        
        return {
            'var_95': var_95,
            'var_99': var_99,
            'expected_shortfall_95': es_95,
            'expected_shortfall_99': es_99,
            'min_profit_95': min_95,
            'min_profit_99': min_99,
            'probability_of_loss': prob_loss,
            'probability_large_loss': prob_large_loss,
            'mean_final_profit': self.results['final_profit'].mean(),
            'std_final_profit': self.results['final_profit'].std()
        }
    
    def create_simulation_chart(self, theme='light'):
        """Create Monte Carlo simulation visualization"""
        
        if self.results is None:
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Profit Distribution', 'Minimum Profit Distribution',
                'Simulation Paths (Sample)', 'Probability of Loss'
            ),
            specs=[[{"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "scatter"}, {"type": "indicator"}]]
        )
        
        # Profit distribution histogram
        fig.add_trace(
            go.Histogram(
                x=self.results['final_profit'],
                nbinsx=50,
                name='Final Profit',
                marker_color='rgba(59, 130, 246, 0.7)',
                hovertemplate='Profit Range: $%{x}<br>Frequency: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Minimum profit distribution histogram
        fig.add_trace(
            go.Histogram(
                x=self.results['min_profit'],
                nbinsx=50,
                name='Minimum Profit',
                marker_color='rgba(239, 68, 68, 0.7)',
                hovertemplate='Minimum Profit Range: $%{x}<br>Frequency: %{y}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Sample simulation paths (using pre-calculated paths)
        if hasattr(self, 'sample_paths'):
            for sim_id, path in self.sample_paths.items():
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(path))),
                        y=path,
                        mode='lines',
                        name=f'Sim {sim_id}',
                        line=dict(width=1, color='rgba(100, 100, 100, 0.3)'),
                        showlegend=False,
                        hovertemplate='Trade: %{x}<br>Cumulative: $%{y:,.2f}<extra></extra>'
                    ),
                    row=2, col=1
                )
        
        # Add actual strategy path
        actual_cumulative = self.trades_df['profit'].cumsum()
        fig.add_trace(
            go.Scatter(
                x=list(range(len(actual_cumulative))),
                y=actual_cumulative,
                mode='lines',
                name='Actual Strategy',
                line=dict(color='#10b981', width=3),
                hovertemplate='Trade: %{x}<br>Actual Cumulative: $%{y:,.2f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Probability of loss gauge
        risk_stats = self.get_risk_statistics()
        prob_loss = risk_stats.get('probability_of_loss', 0)
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=prob_loss,
                title={'text': "Probability of Loss (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkred"},
                    'steps': [
                        {'range': [0, 20], 'color': "lightgreen"},
                        {'range': [20, 40], 'color': "yellow"},
                        {'range': [40, 100], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ),
            row=2, col=2
        )
        
        # Theme styling
        if theme == 'dark':
            fig.update_layout(
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font_color='white'
            )
        
        fig.update_layout(
            title="Monte Carlo Risk Analysis",
            height=800,
            showlegend=True
        )
        
        return fig
    
    def get_scenario_analysis(self):
        """Generate scenario analysis results"""
        
        if self.results is None:
            return {}
        
        # Define scenarios
        scenarios = {
            'Best Case (95th percentile)': np.percentile(self.results['final_profit'], 95),
            'Good Case (75th percentile)': np.percentile(self.results['final_profit'], 75),
            'Expected Case (50th percentile)': np.percentile(self.results['final_profit'], 50),
            'Poor Case (25th percentile)': np.percentile(self.results['final_profit'], 25),
            'Worst Case (5th percentile)': np.percentile(self.results['final_profit'], 5)
        }
        
        return scenarios

def create_monte_carlo_dashboard(trades_df, num_simulations=1000):
    """Create Monte Carlo analysis dashboard"""
    
    # Limit simulations for better performance
    max_simulations = 1000
    if num_simulations > max_simulations:
        num_simulations = max_simulations
        st.warning(f"Limiting simulations to {max_simulations} for performance. Increase for more accuracy.")
    
    st.markdown("### 🎲 **Monte Carlo Risk Simulation**")
    st.markdown("*Professional risk analysis using scenario simulations*")
    
    # Create simulator
    simulator = MonteCarloSimulator(trades_df, num_simulations)
    
    # Run simulation with progress bar
    with st.spinner(f"Running {num_simulations:,} Monte Carlo simulations..."):
        results = simulator.run_simulation()
    
    if results is None:
        st.error("Unable to run simulation - insufficient data")
        return
    
    # Display results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Simulation chart
        chart = simulator.create_simulation_chart()
        st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        # Risk statistics
        risk_stats = simulator.get_risk_statistics()
        
        st.markdown("#### 📊 **Risk Statistics**")
        
        # Value at Risk
        st.metric(
            "Value at Risk (95%)",
            f"${risk_stats['var_95']:,.2f}",
            help="Maximum expected loss in 95% of scenarios"
        )
        
        st.metric(
            "Value at Risk (99%)",
            f"${risk_stats['var_99']:,.2f}",
            help="Maximum expected loss in 99% of scenarios"
        )
        
        # Expected Shortfall
        st.metric(
            "Expected Shortfall (95%)",
            f"${risk_stats['expected_shortfall_95']:,.2f}",
            help="Average loss in worst 5% of scenarios"
        )
        
        # Probability metrics
        st.metric(
            "Probability of Loss",
            f"{risk_stats['probability_of_loss']:.1f}%",
            help="Chance of losing money"
        )
    
    # Scenario analysis
    st.markdown("#### 🎯 **Scenario Analysis**")
    scenarios = simulator.get_scenario_analysis()
    
    scenario_df = pd.DataFrame([
        {"Scenario": scenario, "Expected Profit": f"${profit:,.2f}"}
        for scenario, profit in scenarios.items()
    ])
    
    st.dataframe(scenario_df, use_container_width=True)
    
    return risk_stats