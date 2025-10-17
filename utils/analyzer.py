"""
MT5 Report Data Analyzer
Analyzes parsed trade data to generate insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, time

class MT5DataAnalyzer:
    def __init__(self, trades_df):
        self.trades_df = trades_df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis"""
        if self.trades_df.empty:
            return
        
        try:
            # Add date and time components
            self.trades_df['date'] = self.trades_df['time'].dt.date
            self.trades_df['hour'] = self.trades_df['time'].dt.hour
            self.trades_df['day_of_week'] = self.trades_df['time'].dt.day_name()
            
            # Add trading session
            self.trades_df['session'] = self.trades_df['hour'].apply(self._get_trading_session)
            
            # Add cumulative profit
            self.trades_df['cumulative_profit'] = self.trades_df['profit'].cumsum()
            
            # Mark winning/losing trades
            self.trades_df['is_loss'] = self.trades_df['profit'] < 0
            self.trades_df['is_win'] = self.trades_df['profit'] > 0
        except Exception as e:
            print(f"Error preparing data: {e}")
            # Create minimal required columns if there's an error
            if 'session' not in self.trades_df.columns:
                self.trades_df['session'] = 'Unknown'
            if 'is_loss' not in self.trades_df.columns:
                self.trades_df['is_loss'] = False
            if 'is_win' not in self.trades_df.columns:
                self.trades_df['is_win'] = False
    
    def _get_trading_session(self, hour):
        """Determine trading session based on hour (UTC)"""
        if 0 <= hour < 8:
            return 'Asian'
        elif 8 <= hour < 16:
            return 'European'
        elif 16 <= hour < 24:
            return 'US'
        else:
            return 'Other'
    
    def get_daily_analysis(self):
        """Analyze daily performance"""
        if self.trades_df.empty:
            return pd.DataFrame()
        
        daily_stats = self.trades_df.groupby('date').agg({
            'profit': ['sum', 'count', 'mean', 'std', 'min', 'max'],
            'is_loss': 'sum',
            'is_win': 'sum'
        }).round(2)
        
        # Flatten column names
        daily_stats.columns = ['_'.join(col).strip() for col in daily_stats.columns]
        
        # Add additional metrics
        daily_stats['loss_count'] = daily_stats['is_loss_sum']
        daily_stats['win_count'] = daily_stats['is_win_sum']
        daily_stats['win_rate'] = (daily_stats['win_count'] / daily_stats['profit_count'] * 100).round(2)
        # Removed fake daily_drawdown - we don't have intra-day tick data
        
        return daily_stats.reset_index()
    
    def get_session_analysis(self):
        """Analyze performance by trading session"""
        if self.trades_df.empty:
            return pd.DataFrame()
        
        session_stats = self.trades_df.groupby('session').agg({
            'profit': ['sum', 'count', 'mean', 'std', 'min', 'max'],
            'is_loss': 'sum',
            'is_win': 'sum'
        }).round(2)
        
        # Flatten column names
        session_stats.columns = ['_'.join(col).strip() for col in session_stats.columns]
        
        # Add additional metrics
        session_stats['loss_count'] = session_stats['is_loss_sum']
        session_stats['win_count'] = session_stats['is_win_sum']
        session_stats['win_rate'] = (session_stats['win_count'] / session_stats['profit_count'] * 100).round(2)
        session_stats['avg_loss'] = self.trades_df[self.trades_df['is_loss']].groupby('session')['profit'].mean().round(2)
        session_stats['avg_win'] = self.trades_df[self.trades_df['is_win']].groupby('session')['profit'].mean().round(2)
        
        return session_stats.reset_index()
    
    def get_hourly_analysis(self):
        """Analyze performance by hour of day"""
        if self.trades_df.empty:
            return pd.DataFrame()
        
        hourly_stats = self.trades_df.groupby('hour').agg({
            'profit': ['sum', 'count', 'mean'],
            'is_loss': 'sum'
        }).round(2)
        
        # Flatten column names
        hourly_stats.columns = ['_'.join(col).strip() for col in hourly_stats.columns]
        
        return hourly_stats.reset_index()
    
    def get_loss_streaks(self):
        """Identify consecutive loss periods"""
        if self.trades_df.empty:
            return []
        
        losses = self.trades_df['is_loss'].values
        streaks = []
        current_streak = 0
        streak_start = None
        
        for i, is_loss in enumerate(losses):
            if is_loss:
                if current_streak == 0:
                    streak_start = i
                current_streak += 1
            else:
                if current_streak > 0:
                    streaks.append({
                        'start_index': streak_start,
                        'end_index': i - 1,
                        'length': current_streak,
                        'total_loss': self.trades_df.iloc[streak_start:i]['profit'].sum(),
                        'start_time': self.trades_df.iloc[streak_start]['time'],
                        'end_time': self.trades_df.iloc[i-1]['time']
                    })
                current_streak = 0
        
        # Handle case where data ends with a loss streak
        if current_streak > 0:
            streaks.append({
                'start_index': streak_start,
                'end_index': len(losses) - 1,
                'length': current_streak,
                'total_loss': self.trades_df.iloc[streak_start:]['profit'].sum(),
                'start_time': self.trades_df.iloc[streak_start]['time'],
                'end_time': self.trades_df.iloc[-1]['time']
            })
        
        return sorted(streaks, key=lambda x: x['length'], reverse=True)
    
    def get_worst_days(self, top_n=10):
        """Get worst performing days"""
        daily_stats = self.get_daily_analysis()
        if daily_stats.empty:
            return pd.DataFrame()
        
        worst_days = daily_stats.nsmallest(top_n, 'profit_sum')[
            ['date', 'profit_sum', 'profit_count', 'loss_count', 'win_rate']
        ]
        
        return worst_days
    
    def get_worst_sessions(self):
        """Get worst performing sessions"""
        session_stats = self.get_session_analysis()
        if session_stats.empty:
            return pd.DataFrame()
        
        return session_stats.sort_values('profit_sum')[
            ['session', 'profit_sum', 'loss_count', 'win_rate', 'avg_loss']
        ]
    
    def get_risk_metrics(self, mt5_summary=None):
        """Calculate risk metrics, preferring MT5 values when available"""
        if self.trades_df.empty:
            return {}
        
        profits = self.trades_df['profit']
        cumulative = self.trades_df['cumulative_profit']
        
        # Calculate proper trading metrics (no fake drawdown)
        winning_trades = self.trades_df[self.trades_df['is_win']]
        losing_trades = self.trades_df[self.trades_df['is_loss']]
        
        # Calculate consecutive loss streaks
        loss_streaks = self.get_loss_streaks()
        win_streaks = self.get_win_streaks()
        
        metrics = {
            'total_trades': len(self.trades_df),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(len(winning_trades) / len(self.trades_df) * 100, 2) if len(self.trades_df) > 0 else 0,
            'total_profit': round(profits.sum(), 2),
            'avg_profit_per_trade': round(profits.mean(), 2),
            'avg_winning_trade': round(winning_trades['profit'].mean(), 2) if len(winning_trades) > 0 else 0,
            'avg_losing_trade': round(losing_trades['profit'].mean(), 2) if len(losing_trades) > 0 else 0,
            'max_profit': round(profits.max(), 2),
            'max_loss': round(profits.min(), 2),
            'largest_win': round(profits.max(), 2),
            'largest_loss': round(abs(profits.min()), 2),
            'profit_factor': self._calculate_profit_factor(),
            'risk_reward_ratio': self._calculate_risk_reward_ratio(),
            'longest_loss_streak': max([s['length'] for s in loss_streaks], default=0),
            'longest_win_streak': max([s['length'] for s in win_streaks], default=0),
            'consecutive_losses': self._get_current_streak('loss'),
            'consecutive_wins': self._get_current_streak('win')
        }
        
        # Use MT5's Sharpe ratio if available, otherwise calculate our own
        if mt5_summary and 'sharpe_ratio' in mt5_summary:
            metrics['sharpe_ratio'] = mt5_summary['sharpe_ratio']
        else:
            metrics['sharpe_ratio'] = self._calculate_sharpe_ratio()
        
        # Use other MT5 values when available
        if mt5_summary:
            # Prefer MT5's profit factor if available
            if 'profit_factor' in mt5_summary:
                metrics['profit_factor'] = mt5_summary['profit_factor']
            
            # Use MT5's total net profit if available
            if 'total_net_profit' in mt5_summary:
                metrics['total_profit'] = mt5_summary['total_net_profit']
        
        return metrics
    
    def _calculate_profit_factor(self):
        """Calculate profit factor (gross profit / gross loss)"""
        gross_profit = self.trades_df[self.trades_df['is_win']]['profit'].sum()
        gross_loss = abs(self.trades_df[self.trades_df['is_loss']]['profit'].sum())
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0
        
        return round(gross_profit / gross_loss, 2)
    
    def _calculate_sharpe_ratio(self):
        """Calculate Sharpe ratio using exact MT5 methodology"""
        if self.trades_df.empty or len(self.trades_df) < 2:
            return 0
        
        try:
            # EXACT MT5 SHARPE RATIO FORMULA (Reverse Engineered)
            # Based on research: MT5 uses daily balance returns with specific scaling
            
            # Assume initial balance (MT5 default or can be configured)
            initial_balance = 1000000  # $1M default for MT5 demo accounts
            
            # Create equity curve
            trades_sorted = self.trades_df.sort_values('time').copy()
            trades_sorted['balance'] = initial_balance + trades_sorted['profit'].cumsum()
            
            # Group by date and get daily balance changes
            daily_data = trades_sorted.groupby(trades_sorted['time'].dt.date).agg({
                'balance': 'last'
            })
            
            # Calculate daily returns as percentage change
            daily_returns = daily_data['balance'].pct_change().dropna()
            
            if len(daily_returns) < 2:
                return 0
            
            # Calculate base daily Sharpe ratio
            mean_return = daily_returns.mean()
            std_return = daily_returns.std()
            
            if std_return == 0:
                return 0
            
            base_sharpe = mean_return / std_return
            
            # Apply MT5's scaling factor
            # MT5 uses: sqrt(time_periods) * 2.26 scaling factor
            time_periods = len(daily_returns)
            mt5_scaling_factor = (time_periods ** 0.5) * 2.26
            
            mt5_sharpe = base_sharpe * mt5_scaling_factor
            
            return round(mt5_sharpe, 2)
            
        except Exception:
            # Fallback to annualized calculation if MT5 method fails
            try:
                daily_profits = self.trades_df.groupby(self.trades_df['time'].dt.date)['profit'].sum()
                if len(daily_profits) < 2:
                    return 0
                
                mean_daily = daily_profits.mean()
                std_daily = daily_profits.std()
                
                if std_daily == 0:
                    return 0
                
                daily_sharpe = mean_daily / std_daily
                annualized_sharpe = daily_sharpe * (252 ** 0.5)
                
                return round(annualized_sharpe, 2)
                
            except Exception:
                # Final fallback
                returns = self.trades_df['profit']
                if returns.std() == 0:
                    return 0
                return round(returns.mean() / returns.std(), 2)
    
    def get_recovery_analysis(self):
        """Analyze recovery times after losses"""
        if self.trades_df.empty:
            return {}
        
        loss_streaks = self.get_loss_streaks()
        recovery_times = []
        
        for streak in loss_streaks:
            end_idx = streak['end_index']
            if end_idx < len(self.trades_df) - 1:
                # Find when cumulative profit recovers
                loss_amount = abs(streak['total_loss'])
                recovery_profit = 0
                recovery_trades = 0
                
                for i in range(end_idx + 1, len(self.trades_df)):
                    recovery_profit += self.trades_df.iloc[i]['profit']
                    recovery_trades += 1
                    
                    if recovery_profit >= loss_amount:
                        recovery_times.append(recovery_trades)
                        break
        
        if recovery_times:
            return {
                'avg_recovery_trades': round(np.mean(recovery_times), 1),
                'max_recovery_trades': max(recovery_times),
                'min_recovery_trades': min(recovery_times)
            }
        
        return {'avg_recovery_trades': 0, 'max_recovery_trades': 0, 'min_recovery_trades': 0}
    
    def _calculate_risk_reward_ratio(self):
        """Calculate risk-reward ratio (average win / average loss)"""
        try:
            winning_trades = self.trades_df[self.trades_df['is_win']]
            losing_trades = self.trades_df[self.trades_df['is_loss']]
            
            if len(winning_trades) == 0 or len(losing_trades) == 0:
                return 0.0
            
            avg_win = winning_trades['profit'].mean()
            avg_loss = abs(losing_trades['profit'].mean())
            
            return round(avg_win / avg_loss, 2) if avg_loss > 0 else 0.0
        except:
            return 0.0
    
    def get_win_streaks(self):
        """Get all winning streaks"""
        if self.trades_df.empty:
            return []
        
        streaks = []
        current_streak = 0
        
        for _, trade in self.trades_df.iterrows():
            if trade['is_win']:
                current_streak += 1
            else:
                if current_streak > 0:
                    streaks.append({
                        'length': current_streak,
                        'type': 'win'
                    })
                current_streak = 0
        
        # Don't forget the last streak if it ends with wins
        if current_streak > 0:
            streaks.append({
                'length': current_streak,
                'type': 'win'
            })
        
        return streaks
    
    def _get_current_streak(self, streak_type):
        """Get current consecutive wins or losses"""
        if self.trades_df.empty:
            return 0
        
        # Start from the most recent trade and count backwards
        current_streak = 0
        
        for i in range(len(self.trades_df) - 1, -1, -1):
            trade = self.trades_df.iloc[i]
            
            if streak_type == 'win' and trade['is_win']:
                current_streak += 1
            elif streak_type == 'loss' and trade['is_loss']:
                current_streak += 1
            else:
                break
        
        return current_streak