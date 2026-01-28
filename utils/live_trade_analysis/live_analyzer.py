"""
Live Trade Analyzer
Analyzes live trading data to generate insights and metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, time

class LiveTradeAnalyzer:
    def __init__(self, positions_df, deals_df=None, account_info=None):
        self.positions_df = positions_df.copy() if not positions_df.empty else pd.DataFrame()
        self.deals_df = deals_df.copy() if deals_df is not None and not deals_df.empty else pd.DataFrame()
        self.account_info = account_info or {}
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis"""
        if self.positions_df.empty:
            return
        
        try:
            # Add date and time components
            self.positions_df['date'] = self.positions_df['time'].dt.date
            self.positions_df['hour'] = self.positions_df['time'].dt.hour
            self.positions_df['day_of_week'] = self.positions_df['time'].dt.day_name()
            
            # Add trading session
            self.positions_df['session'] = self.positions_df['hour'].apply(self._get_trading_session)
            
            # Add cumulative profit
            self.positions_df['cumulative_profit'] = self.positions_df['profit'].cumsum()
            
            # Mark winning/losing trades
            self.positions_df['is_loss'] = self.positions_df['profit'] < 0
            self.positions_df['is_win'] = self.positions_df['profit'] > 0
            
            # Add real balance curve if deals data is available
            if not self.deals_df.empty:
                self._prepare_balance_curve()
                
        except Exception as e:
            print(f"Error preparing data: {e}")
            # Create minimal required columns if there's an error
            if 'session' not in self.positions_df.columns:
                self.positions_df['session'] = 'Unknown'
            if 'is_loss' not in self.positions_df.columns:
                self.positions_df['is_loss'] = False
            if 'is_win' not in self.positions_df.columns:
                self.positions_df['is_win'] = False
    
    def _prepare_balance_curve(self):
        """Prepare real balance curve from deals data"""
        if self.deals_df.empty:
            return
        
        try:
            # Filter balance entries and trades
            balance_entries = self.deals_df[self.deals_df.get('is_balance_entry', False) == True].copy()
            trade_entries = self.deals_df[self.deals_df.get('is_balance_entry', False) == False].copy()
            
            # Create balance curve from deals
            if not balance_entries.empty:
                balance_entries = balance_entries.sort_values('time')
                self.balance_curve = balance_entries[['time', 'balance']].copy()
            else:
                # If no balance entries, create from cumulative profits
                if not trade_entries.empty:
                    trade_entries = trade_entries.sort_values('time')
                    trade_entries['cumulative_balance'] = trade_entries['profit'].cumsum()
                    # Assume starting balance (could be extracted from account info)
                    starting_balance = 100000.0  # Default, should be from account info
                    trade_entries['balance'] = starting_balance + trade_entries['cumulative_balance']
                    self.balance_curve = trade_entries[['time', 'balance']].copy()
                else:
                    self.balance_curve = pd.DataFrame()
        except Exception as e:
            print(f"Error preparing balance curve: {e}")
            self.balance_curve = pd.DataFrame()
    
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
    
    def get_live_summary_stats(self):
        """Calculate comprehensive live trading statistics"""
        if self.positions_df.empty:
            return {}
        
        try:
            stats = {}
            
            # Basic trade statistics
            total_trades = len(self.positions_df)
            winning_trades = len(self.positions_df[self.positions_df['profit'] > 0])
            losing_trades = len(self.positions_df[self.positions_df['profit'] < 0])
            
            stats['total_trades'] = total_trades
            stats['winning_trades'] = winning_trades
            stats['losing_trades'] = losing_trades
            stats['win_rate'] = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            # Profit statistics
            total_profit = self.positions_df['profit'].sum()
            gross_profit = self.positions_df[self.positions_df['profit'] > 0]['profit'].sum()
            gross_loss = abs(self.positions_df[self.positions_df['profit'] < 0]['profit'].sum())
            
            stats['total_net_profit'] = total_profit
            stats['gross_profit'] = gross_profit
            stats['gross_loss'] = gross_loss
            stats['profit_factor'] = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            # Average trade statistics
            if winning_trades > 0:
                stats['avg_winning_trade'] = self.positions_df[self.positions_df['profit'] > 0]['profit'].mean()
                stats['largest_winning_trade'] = self.positions_df[self.positions_df['profit'] > 0]['profit'].max()
            else:
                stats['avg_winning_trade'] = 0
                stats['largest_winning_trade'] = 0
                
            if losing_trades > 0:
                stats['avg_losing_trade'] = self.positions_df[self.positions_df['profit'] < 0]['profit'].mean()
                stats['largest_losing_trade'] = self.positions_df[self.positions_df['profit'] < 0]['profit'].min()
            else:
                stats['avg_losing_trade'] = 0
                stats['largest_losing_trade'] = 0
            
            # Expected payoff
            stats['expected_payoff'] = total_profit / total_trades if total_trades > 0 else 0
            
            # Drawdown analysis (from balance curve if available)
            if hasattr(self, 'balance_curve') and not self.balance_curve.empty:
                balance_values = self.balance_curve['balance']
                running_max = balance_values.expanding().max()
                drawdown = balance_values - running_max
                
                stats['max_drawdown_absolute'] = abs(drawdown.min())
                stats['max_drawdown_percent'] = abs(drawdown.min() / running_max.max() * 100) if running_max.max() > 0 else 0
                stats['current_drawdown'] = abs(drawdown.iloc[-1]) if len(drawdown) > 0 else 0
            else:
                # Fallback: calculate from cumulative profit
                cumulative = self.positions_df['profit'].cumsum()
                running_max = cumulative.expanding().max()
                drawdown = cumulative - running_max
                
                stats['max_drawdown_absolute'] = abs(drawdown.min())
                stats['max_drawdown_percent'] = abs(drawdown.min() / running_max.max() * 100) if running_max.max() > 0 else 0
                stats['current_drawdown'] = abs(drawdown.iloc[-1]) if len(drawdown) > 0 else 0
            
            # Consecutive wins/losses
            consecutive_stats = self._calculate_consecutive_stats()
            stats.update(consecutive_stats)
            
            # Trading frequency
            if total_trades > 0:
                date_range = (self.positions_df['time'].max() - self.positions_df['time'].min()).days
                stats['trades_per_day'] = total_trades / max(date_range, 1)
            else:
                stats['trades_per_day'] = 0
            
            return stats
            
        except Exception as e:
            print(f"Error calculating live summary stats: {e}")
            return {}
    
    def _calculate_consecutive_stats(self):
        """Calculate consecutive wins and losses statistics"""
        try:
            if self.positions_df.empty:
                return {}
            
            # Create win/loss sequence
            wins_losses = (self.positions_df['profit'] > 0).astype(int)
            
            # Find consecutive sequences
            consecutive_wins = []
            consecutive_losses = []
            consecutive_win_profits = []
            consecutive_loss_profits = []
            
            current_streak = 0
            current_profit = 0
            current_type = None
            
            for i, (is_win, profit) in enumerate(zip(wins_losses, self.positions_df['profit'])):
                if is_win == 1:  # Win
                    if current_type == 'win':
                        current_streak += 1
                        current_profit += profit
                    else:
                        if current_type == 'loss' and current_streak > 0:
                            consecutive_losses.append(current_streak)
                            consecutive_loss_profits.append(current_profit)
                        current_streak = 1
                        current_profit = profit
                        current_type = 'win'
                else:  # Loss
                    if current_type == 'loss':
                        current_streak += 1
                        current_profit += profit
                    else:
                        if current_type == 'win' and current_streak > 0:
                            consecutive_wins.append(current_streak)
                            consecutive_win_profits.append(current_profit)
                        current_streak = 1
                        current_profit = profit
                        current_type = 'loss'
            
            # Handle last streak
            if current_type == 'win' and current_streak > 0:
                consecutive_wins.append(current_streak)
                consecutive_win_profits.append(current_profit)
            elif current_type == 'loss' and current_streak > 0:
                consecutive_losses.append(current_streak)
                consecutive_loss_profits.append(current_profit)
            
            stats = {}
            
            # Consecutive wins
            if consecutive_wins:
                stats['max_consecutive_wins'] = max(consecutive_wins)
                stats['avg_consecutive_wins'] = sum(consecutive_wins) / len(consecutive_wins)
                max_win_idx = consecutive_wins.index(max(consecutive_wins))
                stats['max_consecutive_win_profit'] = consecutive_win_profits[max_win_idx]
            else:
                stats['max_consecutive_wins'] = 0
                stats['avg_consecutive_wins'] = 0
                stats['max_consecutive_win_profit'] = 0
            
            # Consecutive losses
            if consecutive_losses:
                stats['max_consecutive_losses'] = max(consecutive_losses)
                stats['avg_consecutive_losses'] = sum(consecutive_losses) / len(consecutive_losses)
                max_loss_idx = consecutive_losses.index(max(consecutive_losses))
                stats['max_consecutive_loss_profit'] = consecutive_loss_profits[max_loss_idx]
            else:
                stats['max_consecutive_losses'] = 0
                stats['avg_consecutive_losses'] = 0
                stats['max_consecutive_loss_profit'] = 0
            
            # Maximum consecutive profit/loss (regardless of win/loss count)
            if consecutive_win_profits:
                stats['maximal_consecutive_profit'] = max(consecutive_win_profits)
            else:
                stats['maximal_consecutive_profit'] = 0
                
            if consecutive_loss_profits:
                stats['maximal_consecutive_loss'] = min(consecutive_loss_profits)
            else:
                stats['maximal_consecutive_loss'] = 0
            
            return stats
            
        except Exception as e:
            print(f"Error calculating consecutive stats: {e}")
            return {}
    
    def get_session_performance(self):
        """Analyze performance by trading session"""
        if self.positions_df.empty:
            return pd.DataFrame()
        
        try:
            session_stats = self.positions_df.groupby('session').agg({
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
            
            # Calculate average win/loss per session
            for session in session_stats.index:
                session_data = self.positions_df[self.positions_df['session'] == session]
                wins = session_data[session_data['profit'] > 0]['profit']
                losses = session_data[session_data['profit'] < 0]['profit']
                
                session_stats.loc[session, 'avg_win'] = wins.mean() if len(wins) > 0 else 0
                session_stats.loc[session, 'avg_loss'] = losses.mean() if len(losses) > 0 else 0
                session_stats.loc[session, 'profit_factor'] = (wins.sum() / abs(losses.sum())) if losses.sum() < 0 else float('inf')
            
            return session_stats.reset_index()
            
        except Exception as e:
            print(f"Error calculating session performance: {e}")
            return pd.DataFrame()
    
    def get_daily_performance(self):
        """Analyze daily performance"""
        if self.positions_df.empty:
            return pd.DataFrame()
        
        try:
            daily_stats = self.positions_df.groupby('date').agg({
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
            
            # Calculate daily profit factor
            for date in daily_stats.index:
                date_data = self.positions_df[self.positions_df['date'] == date]
                wins = date_data[date_data['profit'] > 0]['profit'].sum()
                losses = abs(date_data[date_data['profit'] < 0]['profit'].sum())
                daily_stats.loc[date, 'profit_factor'] = wins / losses if losses > 0 else float('inf')
            
            return daily_stats.reset_index()
            
        except Exception as e:
            print(f"Error calculating daily performance: {e}")
            return pd.DataFrame()
    
    def get_hourly_performance(self):
        """Analyze hourly performance patterns"""
        if self.positions_df.empty:
            return pd.DataFrame()
        
        try:
            hourly_stats = self.positions_df.groupby('hour').agg({
                'profit': ['sum', 'count', 'mean'],
                'is_win': 'sum'
            }).round(2)
            
            # Flatten column names
            hourly_stats.columns = ['_'.join(col).strip() for col in hourly_stats.columns]
            
            # Add win rate
            hourly_stats['win_rate'] = (hourly_stats['is_win_sum'] / hourly_stats['profit_count'] * 100).round(2)
            
            # Reset index to get hour as a column
            hourly_stats = hourly_stats.reset_index()
            
            # Convert hour to time range format (e.g., "7 to 8", "15 to 16")
            hourly_stats['hour_range'] = hourly_stats['hour'].apply(
                lambda x: f"{x} to {x+1}" if x < 23 else f"{x} to 0"
            )
            
            # Reorder columns to put hour_range first
            cols = ['hour_range'] + [col for col in hourly_stats.columns if col not in ['hour', 'hour_range']]
            hourly_stats = hourly_stats[cols]
            
            return hourly_stats
            
        except Exception as e:
            print(f"Error calculating hourly performance: {e}")
            return pd.DataFrame()
    
    def get_symbol_performance(self):
        """Analyze performance by symbol"""
        if self.positions_df.empty or 'symbol' not in self.positions_df.columns:
            return pd.DataFrame()
        
        try:
            symbol_stats = self.positions_df.groupby('symbol').agg({
                'profit': ['sum', 'count', 'mean', 'std'],
                'is_win': 'sum',
                'volume': 'sum'
            }).round(2)
            
            # Flatten column names
            symbol_stats.columns = ['_'.join(col).strip() for col in symbol_stats.columns]
            
            # Add win rate and profit factor
            symbol_stats['win_rate'] = (symbol_stats['is_win_sum'] / symbol_stats['profit_count'] * 100).round(2)
            
            for symbol in symbol_stats.index:
                symbol_data = self.positions_df[self.positions_df['symbol'] == symbol]
                wins = symbol_data[symbol_data['profit'] > 0]['profit'].sum()
                losses = abs(symbol_data[symbol_data['profit'] < 0]['profit'].sum())
                symbol_stats.loc[symbol, 'profit_factor'] = wins / losses if losses > 0 else float('inf')
            
            return symbol_stats.reset_index()
            
        except Exception as e:
            print(f"Error calculating symbol performance: {e}")
            return pd.DataFrame()
    
    def get_risk_metrics(self):
        """Calculate advanced risk metrics for live trading"""
        if self.positions_df.empty:
            return {}
        
        try:
            metrics = {}
            profits = self.positions_df['profit']
            
            # Basic risk metrics
            metrics['total_return'] = profits.sum()
            metrics['volatility'] = profits.std()
            metrics['sharpe_ratio'] = (profits.mean() / profits.std()) if profits.std() > 0 else 0
            
            # Sortino ratio (downside deviation)
            negative_returns = profits[profits < 0]
            if len(negative_returns) > 0:
                downside_deviation = negative_returns.std()
                metrics['sortino_ratio'] = profits.mean() / downside_deviation if downside_deviation > 0 else 0
            else:
                metrics['sortino_ratio'] = float('inf')
            
            # Calmar ratio (return / max drawdown)
            if hasattr(self, 'balance_curve') and not self.balance_curve.empty:
                balance_values = self.balance_curve['balance']
                running_max = balance_values.expanding().max()
                drawdown = balance_values - running_max
                max_drawdown = abs(drawdown.min())
                
                annual_return = profits.sum()  # Simplified - should be annualized
                metrics['calmar_ratio'] = annual_return / max_drawdown if max_drawdown > 0 else float('inf')
                metrics['max_drawdown'] = max_drawdown
            else:
                metrics['calmar_ratio'] = 0
                metrics['max_drawdown'] = 0
            
            # Value at Risk (95% confidence)
            if len(profits) >= 20:
                metrics['var_95'] = abs(np.percentile(profits, 5))
                metrics['var_99'] = abs(np.percentile(profits, 1))
            else:
                metrics['var_95'] = 0
                metrics['var_99'] = 0
            
            # Maximum Adverse Excursion (simplified)
            if 'open_price' in self.positions_df.columns and 'close_price' in self.positions_df.columns:
                # This would require tick data for proper MAE calculation
                # For now, we'll use a simplified version
                metrics['mae_avg'] = 0  # Placeholder
                metrics['mfe_avg'] = 0  # Placeholder
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating risk metrics: {e}")
            return {}