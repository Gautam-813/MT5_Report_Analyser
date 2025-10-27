"""
Statistical Analysis Module for Trading Performance
Provides confidence levels and statistical significance testing
"""

import pandas as pd
import numpy as np
from scipy import stats
from .benchmark_standards import TradingBenchmarks

class StatisticalAnalyzer:
    """Statistical analysis for trading performance"""
    
    def __init__(self, trades_df):
        try:
            if trades_df is None or trades_df.empty:
                raise ValueError("Empty or None trades dataframe provided")
            
            self.trades_df = trades_df
            self.trade_count = len(trades_df)
            self.confidence_level, self.confidence_percentage = TradingBenchmarks.get_confidence_level(self.trade_count)
        except Exception as e:
            # Fallback for error cases
            self.trades_df = pd.DataFrame()
            self.trade_count = 0
            self.confidence_level, self.confidence_percentage = 'insufficient', 50
    
    def get_sample_adequacy(self):
        """Assess if sample size is adequate for analysis"""
        return {
            'trade_count': self.trade_count,
            'confidence_level': self.confidence_level,
            'confidence_percentage': self.confidence_percentage,
            'is_adequate': self.trade_count >= 30,
            'recommendation': self._get_sample_recommendation()
        }
    
    def _get_sample_recommendation(self):
        """Get recommendation based on sample size"""
        if self.trade_count >= 500:
            return "Excellent sample size for professional-grade analysis"
        elif self.trade_count >= 300:
            return "Very good sample size for high-confidence analysis"
        elif self.trade_count >= 100:
            return "Good sample size for reliable analysis"
        elif self.trade_count >= 30:
            return "Minimum sample size for basic analysis"
        else:
            return f"Need {30 - self.trade_count} more trades for reliable analysis"
    
    def analyze_time_patterns(self):
        """Analyze time-based trading patterns with statistical significance"""
        try:
            if self.trades_df.empty or 'time' not in self.trades_df.columns:
                return {}
            
            # Add time components with error handling
            df = self.trades_df.copy()
            
            # Ensure time column is datetime
            if not pd.api.types.is_datetime64_any_dtype(df['time']):
                df['time'] = pd.to_datetime(df['time'], errors='coerce')
            
            # Remove rows with invalid dates
            df = df.dropna(subset=['time'])
            
            if df.empty:
                return {}
            
            df['hour'] = df['time'].dt.hour
            df['weekday'] = df['time'].dt.day_name()
            df['month'] = df['time'].dt.month_name()
        except Exception as e:
            return {'error': f'Time analysis failed: {str(e)}'}
        
        analysis = {}
        
        # Hourly analysis
        if self.trade_count >= 30:
            hourly_stats = self._analyze_hourly_performance(df)
            analysis['hourly'] = hourly_stats
        
        # Daily analysis
        if self.trade_count >= 50:
            daily_stats = self._analyze_daily_performance(df)
            analysis['daily'] = daily_stats
        
        # Monthly analysis (only if enough data)
        if self.trade_count >= 100:
            monthly_stats = self._analyze_monthly_performance(df)
            analysis['monthly'] = monthly_stats
        
        return analysis
    
    def _analyze_hourly_performance(self, df):
        """Analyze performance by hour with statistical tests"""
        hourly_group = df.groupby('hour').agg({
            'profit': ['count', 'sum', 'mean'],
            'profit': lambda x: (x > 0).sum() / len(x) * 100  # win rate
        }).round(2)
        
        # Find best and worst hours
        hourly_profits = df.groupby('hour')['profit'].sum()
        best_hour = hourly_profits.idxmax()
        worst_hour = hourly_profits.idxmin()
        
        # Statistical significance test
        best_hour_trades = df[df['hour'] == best_hour]['profit']
        worst_hour_trades = df[df['hour'] == worst_hour]['profit']
        
        significance = self._test_significance(best_hour_trades, worst_hour_trades)
        
        return {
            'best_hour': best_hour,
            'worst_hour': worst_hour,
            'best_hour_profit': hourly_profits[best_hour],
            'worst_hour_profit': hourly_profits[worst_hour],
            'statistical_significance': significance,
            'hourly_data': hourly_group.to_dict()
        }
    
    def _analyze_daily_performance(self, df):
        """Analyze performance by day of week"""
        daily_group = df.groupby('weekday').agg({
            'profit': ['count', 'sum', 'mean']
        }).round(2)
        
        # Calculate win rates
        daily_win_rates = df.groupby('weekday').apply(
            lambda x: (x['profit'] > 0).sum() / len(x) * 100
        ).round(1)
        
        daily_profits = df.groupby('weekday')['profit'].sum()
        best_day = daily_profits.idxmax()
        worst_day = daily_profits.idxmin()
        
        return {
            'best_day': best_day,
            'worst_day': worst_day,
            'best_day_profit': daily_profits[best_day],
            'worst_day_profit': daily_profits[worst_day],
            'daily_win_rates': daily_win_rates.to_dict(),
            'daily_data': daily_group.to_dict()
        }
    
    def _analyze_monthly_performance(self, df):
        """Analyze performance by month (seasonal patterns)"""
        monthly_group = df.groupby('month').agg({
            'profit': ['count', 'sum', 'mean']
        }).round(2)
        
        monthly_profits = df.groupby('month')['profit'].sum()
        best_month = monthly_profits.idxmax()
        worst_month = monthly_profits.idxmin()
        
        return {
            'best_month': best_month,
            'worst_month': worst_month,
            'best_month_profit': monthly_profits[best_month],
            'worst_month_profit': monthly_profits[worst_month],
            'monthly_data': monthly_group.to_dict()
        }
    
    def _test_significance(self, sample1, sample2, alpha=0.05):
        """Test statistical significance between two samples"""
        if len(sample1) < 5 or len(sample2) < 5:
            return {'significant': False, 'reason': 'Insufficient sample size'}
        
        try:
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(sample1, sample2)
            
            return {
                'significant': p_value < alpha,
                'p_value': p_value,
                't_statistic': t_stat,
                'confidence': (1 - p_value) * 100
            }
        except:
            return {'significant': False, 'reason': 'Statistical test failed'}
    
    def analyze_risk_parameters(self):
        """Analyze current risk parameters and suggest optimizations"""
        try:
            if self.trades_df.empty or 'profit' not in self.trades_df.columns:
                return {}
            
            profits = self.trades_df['profit']
            
            # Handle non-numeric profit values
            profits = pd.to_numeric(profits, errors='coerce')
            profits = profits.dropna()
            
            if len(profits) == 0:
                return {'error': 'No valid profit data found'}
            
            winning_trades = profits[profits > 0]
            losing_trades = profits[profits < 0]
            
            if len(winning_trades) == 0 or len(losing_trades) == 0:
                return {'error': 'Need both winning and losing trades for analysis'}
            
            avg_win = winning_trades.mean()
            avg_loss = abs(losing_trades.mean())
            current_rr = avg_win / avg_loss if avg_loss > 0 else 0
            
            # Analyze stop loss efficiency
            sl_analysis = self._analyze_stop_loss_efficiency()
            
            # Analyze take profit optimization
            tp_analysis = self._analyze_take_profit_optimization()
            
            return {
                'current_risk_reward': current_rr,
                'average_win': avg_win,
                'average_loss': avg_loss,
                'stop_loss_analysis': sl_analysis,
                'take_profit_analysis': tp_analysis
            }
        except Exception as e:
            return {'error': f'Risk analysis failed: {str(e)}'}
    
    def _analyze_stop_loss_efficiency(self):
        """Analyze if stop losses are too tight or too wide"""
        # This would need more detailed trade data (entry, exit, high, low)
        # For now, provide basic analysis based on loss distribution
        
        losses = self.trades_df[self.trades_df['profit'] < 0]['profit']
        if len(losses) == 0:
            return {'recommendation': 'No losing trades to analyze'}
        
        loss_std = losses.std()
        loss_mean = losses.mean()
        
        # Basic heuristic: if losses are very consistent, SL might be too tight
        coefficient_of_variation = abs(loss_std / loss_mean) if loss_mean != 0 else 0
        
        if coefficient_of_variation < 0.3:
            return {
                'recommendation': 'Consider widening stop loss',
                'reason': 'Losses are very consistent, suggesting premature exits',
                'confidence': 'medium'
            }
        elif coefficient_of_variation > 0.8:
            return {
                'recommendation': 'Consider tightening stop loss',
                'reason': 'High variation in losses suggests inconsistent risk management',
                'confidence': 'medium'
            }
        else:
            return {
                'recommendation': 'Stop loss appears appropriate',
                'reason': 'Loss distribution shows reasonable consistency',
                'confidence': 'low'
            }
    
    def _analyze_take_profit_optimization(self):
        """Analyze take profit optimization opportunities"""
        wins = self.trades_df[self.trades_df['profit'] > 0]['profit']
        if len(wins) == 0:
            return {'recommendation': 'No winning trades to analyze'}
        
        win_std = wins.std()
        win_mean = wins.mean()
        
        # Basic heuristic for TP optimization
        coefficient_of_variation = win_std / win_mean if win_mean != 0 else 0
        
        if coefficient_of_variation > 0.6:
            return {
                'recommendation': 'Consider multiple take profit levels',
                'reason': 'High variation in wins suggests missed opportunities',
                'confidence': 'medium'
            }
        else:
            return {
                'recommendation': 'Take profit strategy appears consistent',
                'reason': 'Win distribution shows good consistency',
                'confidence': 'low'
            }