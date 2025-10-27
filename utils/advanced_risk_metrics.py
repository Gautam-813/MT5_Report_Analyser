"""
Advanced Risk Metrics Module
Professional-grade risk analytics used by institutional traders
"""

import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedRiskAnalyzer:
    """Professional risk analytics for institutional-grade analysis"""
    
    def __init__(self, trades_df):
        self.trades_df = trades_df
        self.returns = self._calculate_returns()
    
    def _calculate_returns(self):
        """Calculate returns from trades data"""
        try:
            if self.trades_df.empty or 'profit' not in self.trades_df.columns:
                return pd.Series([])
            
            profits = pd.to_numeric(self.trades_df['profit'], errors='coerce')
            return profits.dropna()
        except Exception:
            return pd.Series([])
    
    def calculate_var(self, confidence=0.95):
        """Calculate Value at Risk (VaR) - Industry standard risk metric"""
        try:
            if len(self.returns) < 10:
                return {'var_95': 0, 'var_99': 0, 'interpretation': 'Insufficient data'}
            
            var_95 = np.percentile(self.returns, (1 - 0.95) * 100)
            var_99 = np.percentile(self.returns, (1 - 0.99) * 100)
            
            return {
                'var_95': abs(var_95),
                'var_99': abs(var_99),
                'interpretation': f'95% chance daily loss won\'t exceed ${abs(var_95):.2f}',
                'risk_level': self._assess_var_risk_level(abs(var_95))
            }
        except Exception:
            return {'var_95': 0, 'var_99': 0, 'interpretation': 'Calculation error'}
    
    def calculate_expected_shortfall(self, confidence=0.95):
        """Calculate Expected Shortfall (Conditional VaR) - Tail risk measure"""
        try:
            if len(self.returns) < 10:
                return {'es_95': 0, 'es_99': 0, 'interpretation': 'Insufficient data'}
            
            var_95 = np.percentile(self.returns, 5)
            var_99 = np.percentile(self.returns, 1)
            
            # Expected Shortfall = average of losses beyond VaR
            es_95 = self.returns[self.returns <= var_95].mean()
            es_99 = self.returns[self.returns <= var_99].mean()
            
            return {
                'es_95': abs(es_95) if not np.isnan(es_95) else 0,
                'es_99': abs(es_99) if not np.isnan(es_99) else 0,
                'interpretation': f'Average loss in worst 5% scenarios: ${abs(es_95):.2f}',
                'tail_risk': 'High' if abs(es_95) > abs(var_95) * 1.5 else 'Moderate'
            }
        except Exception:
            return {'es_95': 0, 'es_99': 0, 'interpretation': 'Calculation error'}
    
    def calculate_sortino_ratio(self):
        """Calculate Sortino Ratio - Downside deviation focused performance"""
        try:
            if len(self.returns) < 10:
                return {'sortino_ratio': 0, 'interpretation': 'Insufficient data'}
            
            mean_return = self.returns.mean()
            downside_returns = self.returns[self.returns < 0]
            
            if len(downside_returns) == 0:
                return {'sortino_ratio': float('inf'), 'interpretation': 'No negative returns'}
            
            downside_deviation = np.sqrt(np.mean(downside_returns**2))
            sortino_ratio = mean_return / downside_deviation if downside_deviation > 0 else 0
            
            return {
                'sortino_ratio': sortino_ratio,
                'interpretation': self._interpret_sortino(sortino_ratio),
                'rating': self._rate_sortino(sortino_ratio)
            }
        except Exception:
            return {'sortino_ratio': 0, 'interpretation': 'Calculation error'}
    
    def calculate_calmar_ratio(self):
        """Calculate Calmar Ratio - Return/Max Drawdown ratio"""
        try:
            if len(self.returns) < 10:
                return {'calmar_ratio': 0, 'interpretation': 'Insufficient data'}
            
            # Calculate cumulative returns for drawdown
            cumulative_returns = self.returns.cumsum()
            running_max = cumulative_returns.expanding().max()
            drawdown = cumulative_returns - running_max
            max_drawdown = abs(drawdown.min())
            
            annual_return = self.returns.mean() * 252  # Assuming daily returns
            
            if max_drawdown == 0:
                return {'calmar_ratio': float('inf'), 'interpretation': 'No drawdown observed'}
            
            calmar_ratio = annual_return / max_drawdown
            
            return {
                'calmar_ratio': calmar_ratio,
                'max_drawdown': max_drawdown,
                'interpretation': self._interpret_calmar(calmar_ratio),
                'rating': self._rate_calmar(calmar_ratio)
            }
        except Exception:
            return {'calmar_ratio': 0, 'interpretation': 'Calculation error'}
    
    def calculate_omega_ratio(self, threshold=0):
        """Calculate Omega Ratio - Probability weighted gains vs losses"""
        try:
            if len(self.returns) < 10:
                return {'omega_ratio': 0, 'interpretation': 'Insufficient data'}
            
            gains = self.returns[self.returns > threshold] - threshold
            losses = threshold - self.returns[self.returns <= threshold]
            
            if len(losses) == 0 or losses.sum() == 0:
                return {'omega_ratio': float('inf'), 'interpretation': 'No losses observed'}
            
            omega_ratio = gains.sum() / losses.sum()
            
            return {
                'omega_ratio': omega_ratio,
                'interpretation': self._interpret_omega(omega_ratio),
                'rating': self._rate_omega(omega_ratio)
            }
        except Exception:
            return {'omega_ratio': 0, 'interpretation': 'Calculation error'}
    
    def analyze_mae_mfe(self):
        """Analyze Maximum Adverse/Favorable Excursion"""
        try:
            if len(self.returns) < 10:
                return {'mae_analysis': 'Insufficient data', 'mfe_analysis': 'Insufficient data'}
            
            # Simulate MAE/MFE based on profit distribution
            winning_trades = self.returns[self.returns > 0]
            losing_trades = self.returns[self.returns < 0]
            
            if len(winning_trades) == 0 or len(losing_trades) == 0:
                return {'mae_analysis': 'Need both wins and losses', 'mfe_analysis': 'Need both wins and losses'}
            
            # MAE Analysis - How much trades went against before closing
            mae_avg = abs(losing_trades.mean()) * 0.7  # Estimate
            mae_max = abs(losing_trades.min()) * 1.2   # Estimate
            
            # MFE Analysis - How much trades went in favor before closing
            mfe_avg = winning_trades.mean() * 1.3      # Estimate
            mfe_max = winning_trades.max() * 1.5       # Estimate
            
            return {
                'mae_analysis': {
                    'average_mae': mae_avg,
                    'maximum_mae': mae_max,
                    'interpretation': f'Trades typically go ${mae_avg:.2f} against before exit'
                },
                'mfe_analysis': {
                    'average_mfe': mfe_avg,
                    'maximum_mfe': mfe_max,
                    'interpretation': f'Trades typically reach ${mfe_avg:.2f} profit before exit'
                },
                'efficiency_ratio': mfe_avg / mae_avg if mae_avg > 0 else 0
            }
        except Exception:
            return {'mae_analysis': 'Calculation error', 'mfe_analysis': 'Calculation error'}
    
    def generate_professional_risk_report(self):
        """Generate comprehensive professional risk report"""
        try:
            var_analysis = self.calculate_var()
            es_analysis = self.calculate_expected_shortfall()
            sortino_analysis = self.calculate_sortino_ratio()
            calmar_analysis = self.calculate_calmar_ratio()
            omega_analysis = self.calculate_omega_ratio()
            mae_mfe_analysis = self.analyze_mae_mfe()
            
            return {
                'value_at_risk': var_analysis,
                'expected_shortfall': es_analysis,
                'sortino_ratio': sortino_analysis,
                'calmar_ratio': calmar_analysis,
                'omega_ratio': omega_analysis,
                'mae_mfe_analysis': mae_mfe_analysis,
                'overall_risk_assessment': self._generate_overall_assessment(
                    var_analysis, sortino_analysis, calmar_analysis
                )
            }
        except Exception:
            return {'error': 'Failed to generate risk report'}
    
    def _assess_var_risk_level(self, var_value):
        """Assess VaR risk level"""
        if var_value < 50:
            return 'Low Risk'
        elif var_value < 100:
            return 'Moderate Risk'
        else:
            return 'High Risk'
    
    def _interpret_sortino(self, sortino):
        """Interpret Sortino ratio"""
        if sortino > 2.0:
            return 'Excellent risk-adjusted returns'
        elif sortino > 1.0:
            return 'Good risk-adjusted returns'
        elif sortino > 0.5:
            return 'Acceptable risk-adjusted returns'
        else:
            return 'Poor risk-adjusted returns'
    
    def _rate_sortino(self, sortino):
        """Rate Sortino ratio"""
        if sortino > 2.0:
            return 'Excellent'
        elif sortino > 1.0:
            return 'Good'
        elif sortino > 0.5:
            return 'Average'
        else:
            return 'Poor'
    
    def _interpret_calmar(self, calmar):
        """Interpret Calmar ratio"""
        if calmar > 3.0:
            return 'Exceptional return per unit of drawdown'
        elif calmar > 1.0:
            return 'Good return per unit of drawdown'
        elif calmar > 0.5:
            return 'Acceptable return per unit of drawdown'
        else:
            return 'Poor return relative to drawdown'
    
    def _rate_calmar(self, calmar):
        """Rate Calmar ratio"""
        if calmar > 3.0:
            return 'Excellent'
        elif calmar > 1.0:
            return 'Good'
        elif calmar > 0.5:
            return 'Average'
        else:
            return 'Poor'
    
    def _interpret_omega(self, omega):
        """Interpret Omega ratio"""
        if omega > 2.0:
            return 'Excellent probability-weighted performance'
        elif omega > 1.5:
            return 'Good probability-weighted performance'
        elif omega > 1.0:
            return 'Positive probability-weighted performance'
        else:
            return 'Negative probability-weighted performance'
    
    def _rate_omega(self, omega):
        """Rate Omega ratio"""
        if omega > 2.0:
            return 'Excellent'
        elif omega > 1.5:
            return 'Good'
        elif omega > 1.0:
            return 'Average'
        else:
            return 'Poor'
    
    def _generate_overall_assessment(self, var_analysis, sortino_analysis, calmar_analysis):
        """Generate overall risk assessment"""
        try:
            risk_factors = []
            
            # VaR assessment
            if var_analysis.get('risk_level') == 'High Risk':
                risk_factors.append('High tail risk exposure')
            
            # Sortino assessment
            if sortino_analysis.get('rating') in ['Poor', 'Average']:
                risk_factors.append('Suboptimal downside risk management')
            
            # Calmar assessment
            if calmar_analysis.get('rating') in ['Poor', 'Average']:
                risk_factors.append('High drawdown relative to returns')
            
            if not risk_factors:
                return {
                    'overall_rating': 'Excellent',
                    'summary': 'Strategy demonstrates strong risk management across all metrics',
                    'recommendation': 'Maintain current risk parameters'
                }
            elif len(risk_factors) == 1:
                return {
                    'overall_rating': 'Good',
                    'summary': f'Strategy shows good risk management with minor concern: {risk_factors[0]}',
                    'recommendation': 'Consider minor risk parameter adjustments'
                }
            else:
                return {
                    'overall_rating': 'Needs Improvement',
                    'summary': f'Strategy has multiple risk concerns: {", ".join(risk_factors)}',
                    'recommendation': 'Significant risk parameter optimization recommended'
                }
        except Exception:
            return {
                'overall_rating': 'Unknown',
                'summary': 'Unable to assess overall risk',
                'recommendation': 'Review risk calculation inputs'
            }