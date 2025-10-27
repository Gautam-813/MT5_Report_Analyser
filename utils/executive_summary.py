"""
Executive Summary Generator
Creates C-suite ready professional reports
"""

import pandas as pd
import numpy as np
from datetime import datetime

class ExecutiveSummaryGenerator:
    """Generate executive-level trading strategy summaries"""
    
    def __init__(self, trades_df, risk_metrics, feedback_report):
        self.trades_df = trades_df
        self.risk_metrics = risk_metrics
        self.feedback_report = feedback_report
        
    def generate_executive_summary(self):
        """Generate comprehensive executive summary"""
        try:
            summary = {
                'executive_overview': self._create_executive_overview(),
                'key_performance_indicators': self._create_kpi_dashboard(),
                'risk_assessment': self._create_risk_assessment(),
                'strategic_recommendations': self._create_strategic_recommendations(),
                'financial_impact': self._calculate_financial_impact(),
                'implementation_roadmap': self._create_implementation_roadmap()
            }
            
            return summary
        except Exception as e:
            return {'error': f'Failed to generate executive summary: {str(e)}'}
    
    def _create_executive_overview(self):
        """Create high-level executive overview"""
        try:
            total_trades = len(self.trades_df)
            total_profit = self.risk_metrics.get('total_profit', 0)
            win_rate = self.risk_metrics.get('win_rate', 0)
            overall_score = self.feedback_report.get('overall_score', 0)
            
            # Determine performance category
            if overall_score >= 80:
                performance_category = "EXCEPTIONAL"
                performance_color = "#10b981"
            elif overall_score >= 60:
                performance_category = "STRONG"
                performance_color = "#3b82f6"
            elif overall_score >= 40:
                performance_category = "MODERATE"
                performance_color = "#f59e0b"
            else:
                performance_category = "UNDERPERFORMING"
                performance_color = "#ef4444"
            
            # Calculate time period
            if not self.trades_df.empty and 'time' in self.trades_df.columns:
                start_date = self.trades_df['time'].min()
                end_date = self.trades_df['time'].max()
                period_days = (end_date - start_date).days
            else:
                period_days = 0
            
            return {
                'performance_category': performance_category,
                'performance_color': performance_color,
                'overall_score': overall_score,
                'total_trades': total_trades,
                'analysis_period_days': period_days,
                'total_profit': total_profit,
                'win_rate': win_rate,
                'executive_summary_text': self._generate_executive_text(
                    performance_category, total_profit, win_rate, total_trades
                )
            }
        except Exception:
            return {'error': 'Failed to create executive overview'}
    
    def _generate_executive_text(self, category, profit, win_rate, trades):
        """Generate executive summary text"""
        if category == "EXCEPTIONAL":
            return f"Strategy demonstrates exceptional performance with ${profit:,.2f} profit across {trades} trades. Win rate of {win_rate:.1f}% significantly exceeds industry benchmarks. Recommend scaling and optimization."
        elif category == "STRONG":
            return f"Strategy shows strong performance generating ${profit:,.2f} with {win_rate:.1f}% win rate over {trades} trades. Performance above market average with identified optimization opportunities."
        elif category == "MODERATE":
            return f"Strategy exhibits moderate performance with ${profit:,.2f} profit and {win_rate:.1f}% win rate. Significant improvement potential identified through strategic adjustments."
        else:
            return f"Strategy requires immediate attention. Current performance of ${profit:,.2f} with {win_rate:.1f}% win rate below acceptable thresholds. Comprehensive optimization recommended."
    
    def _create_kpi_dashboard(self):
        """Create key performance indicators dashboard"""
        try:
            kpis = []
            
            # Profitability KPIs
            total_profit = self.risk_metrics.get('total_profit', 0)
            profit_factor = self.risk_metrics.get('profit_factor', 0)
            
            kpis.append({
                'category': 'Profitability',
                'metrics': [
                    {'name': 'Total Profit', 'value': f"${total_profit:,.2f}", 'status': self._get_profit_status(total_profit)},
                    {'name': 'Profit Factor', 'value': f"{profit_factor:.2f}", 'status': self._get_pf_status(profit_factor)},
                    {'name': 'ROI', 'value': f"{self._calculate_roi():.1f}%", 'status': self._get_roi_status()}
                ]
            })
            
            # Risk Management KPIs
            win_rate = self.risk_metrics.get('win_rate', 0)
            sharpe_ratio = self.risk_metrics.get('sharpe_ratio', 0)
            
            kpis.append({
                'category': 'Risk Management',
                'metrics': [
                    {'name': 'Win Rate', 'value': f"{win_rate:.1f}%", 'status': self._get_wr_status(win_rate)},
                    {'name': 'Sharpe Ratio', 'value': f"{sharpe_ratio:.2f}", 'status': self._get_sharpe_status(sharpe_ratio)},
                    {'name': 'Risk Level', 'value': self._assess_overall_risk(), 'status': self._get_risk_status()}
                ]
            })
            
            # Operational KPIs
            total_trades = len(self.trades_df)
            confidence_level = self.feedback_report.get('confidence_level', 'unknown')
            
            kpis.append({
                'category': 'Operational',
                'metrics': [
                    {'name': 'Total Trades', 'value': f"{total_trades:,}", 'status': self._get_trade_count_status(total_trades)},
                    {'name': 'Data Quality', 'value': confidence_level.title(), 'status': self._get_confidence_status(confidence_level)},
                    {'name': 'Consistency', 'value': self._assess_consistency(), 'status': 'good'}
                ]
            })
            
            return kpis
        except Exception:
            return [{'category': 'Error', 'metrics': [{'name': 'KPI Error', 'value': 'N/A', 'status': 'error'}]}]
    
    def _create_risk_assessment(self):
        """Create executive risk assessment"""
        try:
            risk_factors = []
            
            # Analyze key risk factors
            profit_factor = self.risk_metrics.get('profit_factor', 0)
            win_rate = self.risk_metrics.get('win_rate', 0)
            total_profit = self.risk_metrics.get('total_profit', 0)
            
            # Risk factor analysis
            if profit_factor < 1.2:
                risk_factors.append({
                    'factor': 'Low Profitability',
                    'severity': 'HIGH',
                    'description': f'Profit factor of {profit_factor:.2f} indicates minimal edge',
                    'impact': 'Strategy may not be sustainable long-term'
                })
            
            if win_rate < 45:
                risk_factors.append({
                    'factor': 'Low Win Rate',
                    'severity': 'MEDIUM',
                    'description': f'Win rate of {win_rate:.1f}% below industry average',
                    'impact': 'Higher psychological pressure and drawdown risk'
                })
            
            if total_profit < 0:
                risk_factors.append({
                    'factor': 'Negative Returns',
                    'severity': 'CRITICAL',
                    'description': f'Strategy showing net loss of ${abs(total_profit):,.2f}',
                    'impact': 'Immediate strategy revision required'
                })
            
            # Overall risk rating
            if not risk_factors:
                overall_risk = 'LOW'
            elif any(rf['severity'] == 'CRITICAL' for rf in risk_factors):
                overall_risk = 'CRITICAL'
            elif any(rf['severity'] == 'HIGH' for rf in risk_factors):
                overall_risk = 'HIGH'
            else:
                overall_risk = 'MEDIUM'
            
            return {
                'overall_risk_rating': overall_risk,
                'risk_factors': risk_factors,
                'risk_mitigation_priority': len([rf for rf in risk_factors if rf['severity'] in ['CRITICAL', 'HIGH']])
            }
        except Exception:
            return {'overall_risk_rating': 'UNKNOWN', 'risk_factors': [], 'risk_mitigation_priority': 0}
    
    def _create_strategic_recommendations(self):
        """Create strategic recommendations for executives"""
        try:
            recommendations = self.feedback_report.get('recommendations', [])
            
            # Group recommendations by impact level
            strategic_recs = {
                'immediate_actions': [],
                'short_term_optimizations': [],
                'long_term_improvements': []
            }
            
            for rec in recommendations[:10]:  # Top 10 recommendations
                if rec.get('priority') == 'CRITICAL':
                    strategic_recs['immediate_actions'].append({
                        'action': rec.get('title', 'Unknown'),
                        'impact': rec.get('potential_impact', 'Unknown'),
                        'timeline': 'Immediate (1-7 days)'
                    })
                elif rec.get('priority') == 'HIGH':
                    strategic_recs['short_term_optimizations'].append({
                        'action': rec.get('title', 'Unknown'),
                        'impact': rec.get('potential_impact', 'Unknown'),
                        'timeline': 'Short-term (1-4 weeks)'
                    })
                else:
                    strategic_recs['long_term_improvements'].append({
                        'action': rec.get('title', 'Unknown'),
                        'impact': rec.get('potential_impact', 'Unknown'),
                        'timeline': 'Long-term (1-3 months)'
                    })
            
            return strategic_recs
        except Exception:
            return {'immediate_actions': [], 'short_term_optimizations': [], 'long_term_improvements': []}
    
    def _calculate_financial_impact(self):
        """Calculate projected financial impact of recommendations"""
        try:
            current_profit = self.risk_metrics.get('total_profit', 0)
            current_win_rate = self.risk_metrics.get('win_rate', 50)
            current_pf = self.risk_metrics.get('profit_factor', 1.0)
            
            # Conservative improvement estimates based on recommendations
            projected_win_rate = min(85, current_win_rate * 1.15)  # 15% improvement cap at 85%
            projected_pf = min(3.0, current_pf * 1.25)  # 25% improvement cap at 3.0
            
            # Calculate projected profit improvement
            improvement_factor = (projected_win_rate / current_win_rate) * (projected_pf / current_pf) if current_win_rate > 0 and current_pf > 0 else 1.1
            projected_profit = current_profit * improvement_factor
            
            profit_increase = projected_profit - current_profit
            percentage_increase = ((projected_profit / current_profit) - 1) * 100 if current_profit != 0 else 0
            
            return {
                'current_monthly_profit': current_profit,
                'projected_monthly_profit': projected_profit,
                'absolute_improvement': profit_increase,
                'percentage_improvement': percentage_increase,
                'annual_impact': profit_increase * 12,
                'roi_timeline': '3-6 months for full implementation'
            }
        except Exception:
            return {
                'current_monthly_profit': 0,
                'projected_monthly_profit': 0,
                'absolute_improvement': 0,
                'percentage_improvement': 0,
                'annual_impact': 0,
                'roi_timeline': 'Unable to calculate'
            }
    
    def _create_implementation_roadmap(self):
        """Create implementation roadmap for executives"""
        try:
            roadmap = [
                {
                    'phase': 'Phase 1: Immediate Risk Mitigation',
                    'timeline': '1-7 days',
                    'actions': ['Stop unprofitable trading sessions', 'Adjust risk parameters', 'Implement critical recommendations'],
                    'success_metrics': ['Reduced daily losses', 'Improved risk metrics'],
                    'resources_required': 'Minimal - Configuration changes only'
                },
                {
                    'phase': 'Phase 2: Strategy Optimization',
                    'timeline': '1-4 weeks',
                    'actions': ['Implement high-impact recommendations', 'Optimize trading schedule', 'Fine-tune parameters'],
                    'success_metrics': ['Improved win rate', 'Better profit factor'],
                    'resources_required': 'Moderate - Testing and validation'
                },
                {
                    'phase': 'Phase 3: Performance Enhancement',
                    'timeline': '1-3 months',
                    'actions': ['Advanced optimization', 'Long-term improvements', 'Scaling considerations'],
                    'success_metrics': ['Sustained profitability', 'Consistent performance'],
                    'resources_required': 'Significant - Ongoing monitoring and adjustment'
                }
            ]
            
            return roadmap
        except Exception:
            return []
    
    # Helper methods for status assessment
    def _get_profit_status(self, profit):
        return 'excellent' if profit > 1000 else 'good' if profit > 0 else 'poor'
    
    def _get_pf_status(self, pf):
        return 'excellent' if pf > 2.0 else 'good' if pf > 1.5 else 'average' if pf > 1.2 else 'poor'
    
    def _get_wr_status(self, wr):
        return 'excellent' if wr > 70 else 'good' if wr > 60 else 'average' if wr > 50 else 'poor'
    
    def _get_sharpe_status(self, sharpe):
        return 'excellent' if sharpe > 1.5 else 'good' if sharpe > 1.0 else 'average' if sharpe > 0.5 else 'poor'
    
    def _get_trade_count_status(self, count):
        return 'excellent' if count > 300 else 'good' if count > 100 else 'average' if count > 30 else 'poor'
    
    def _get_confidence_status(self, level):
        return 'excellent' if level == 'professional' else 'good' if level == 'high' else 'average' if level == 'reliable' else 'poor'
    
    def _calculate_roi(self):
        # Simplified ROI calculation
        profit = self.risk_metrics.get('total_profit', 0)
        return max(0, profit / 1000 * 100)  # Assuming $1000 base capital
    
    def _get_roi_status(self):
        roi = self._calculate_roi()
        return 'excellent' if roi > 20 else 'good' if roi > 10 else 'average' if roi > 5 else 'poor'
    
    def _assess_overall_risk(self):
        pf = self.risk_metrics.get('profit_factor', 1.0)
        wr = self.risk_metrics.get('win_rate', 50)
        
        if pf > 1.5 and wr > 60:
            return 'Low'
        elif pf > 1.2 and wr > 50:
            return 'Medium'
        else:
            return 'High'
    
    def _get_risk_status(self):
        risk = self._assess_overall_risk()
        return 'excellent' if risk == 'Low' else 'average' if risk == 'Medium' else 'poor'
    
    def _assess_consistency(self):
        # Simplified consistency assessment
        pf = self.risk_metrics.get('profit_factor', 1.0)
        return 'High' if pf > 1.3 else 'Medium' if pf > 1.1 else 'Low'