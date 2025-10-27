"""
Intelligent Feedback Engine for Trading Strategy Analysis
Generates actionable recommendations based on performance data
"""

import pandas as pd
import numpy as np
from .benchmark_standards import TradingBenchmarks
from .statistical_analyzer import StatisticalAnalyzer

class IntelligentFeedbackEngine:
    """Core engine for generating intelligent trading feedback"""
    
    def __init__(self, trades_df, risk_tolerance='moderate', feedback_level='intermediate'):
        try:
            if trades_df is None or trades_df.empty:
                raise ValueError("Empty or None trades dataframe provided")
            
            self.trades_df = trades_df
            self.risk_tolerance = str(risk_tolerance).lower() if risk_tolerance else 'moderate'
            self.feedback_level = str(feedback_level).lower() if feedback_level else 'intermediate'
            self.analyzer = StatisticalAnalyzer(trades_df)
            self.risk_profile = TradingBenchmarks.get_risk_profile_standards(self.risk_tolerance)
        except Exception as e:
            # Fallback initialization
            self.trades_df = pd.DataFrame()
            self.risk_tolerance = 'moderate'
            self.feedback_level = 'intermediate'
            self.analyzer = StatisticalAnalyzer(pd.DataFrame())
            self.risk_profile = TradingBenchmarks.get_risk_profile_standards('moderate')
        
    def generate_comprehensive_feedback(self, risk_metrics):
        """Generate complete feedback report"""
        try:
            # Validate risk_metrics
            if not risk_metrics or not isinstance(risk_metrics, dict):
                risk_metrics = {}
            
            # Get sample adequacy
            sample_info = self.analyzer.get_sample_adequacy()
            
            # Generate all analysis components with error handling
            benchmark_analysis = self._analyze_benchmark_performance(risk_metrics)
            time_analysis = self.analyzer.analyze_time_patterns()
            risk_analysis = self.analyzer.analyze_risk_parameters()
            recommendations = self._generate_ranked_recommendations(
                benchmark_analysis, time_analysis, risk_analysis, risk_metrics
            )
            
            return {
                'sample_adequacy': sample_info,
                'benchmark_analysis': benchmark_analysis,
                'time_analysis': time_analysis,
                'risk_analysis': risk_analysis,
                'recommendations': recommendations,
                'overall_score': self._calculate_overall_score(risk_metrics),
                'confidence_level': sample_info['confidence_level']
            }
        except Exception as e:
            # Return safe fallback
            return {
                'sample_adequacy': {'trade_count': 0, 'confidence_level': 'insufficient', 'confidence_percentage': 50, 'is_adequate': False, 'recommendation': 'Error in analysis'},
                'benchmark_analysis': {},
                'time_analysis': {},
                'risk_analysis': {},
                'recommendations': [],
                'overall_score': 0,
                'confidence_level': 'insufficient',
                'error': f'Feedback generation failed: {str(e)}'
            }
    
    def _analyze_benchmark_performance(self, risk_metrics):
        """Compare performance against industry benchmarks"""
        
        analysis = {}
        
        # Analyze each key metric
        key_metrics = ['win_rate', 'profit_factor', 'sharpe_ratio']
        
        for metric in key_metrics:
            if metric in risk_metrics:
                value = risk_metrics[metric]
                rating = TradingBenchmarks.get_performance_rating(metric, value)
                benchmarks = TradingBenchmarks.PERFORMANCE_BENCHMARKS[metric]
                
                analysis[metric] = {
                    'value': value,
                    'rating': rating,
                    'benchmarks': benchmarks,
                    'percentile': self._calculate_percentile(metric, value),
                    'improvement_needed': self._calculate_improvement_needed(metric, value)
                }
        
        return analysis
    
    def _calculate_percentile(self, metric, value):
        """Calculate approximate percentile based on industry data"""
        benchmarks = TradingBenchmarks.PERFORMANCE_BENCHMARKS[metric]
        
        if value >= benchmarks['excellent']:
            return 90 + min(10, (value - benchmarks['excellent']) / benchmarks['excellent'] * 10)
        elif value >= benchmarks['good']:
            return 70 + (value - benchmarks['good']) / (benchmarks['excellent'] - benchmarks['good']) * 20
        elif value >= benchmarks['average']:
            return 40 + (value - benchmarks['average']) / (benchmarks['good'] - benchmarks['average']) * 30
        elif value >= benchmarks['poor']:
            return 20 + (value - benchmarks['poor']) / (benchmarks['average'] - benchmarks['poor']) * 20
        else:
            return max(0, 20 * (value / benchmarks['poor']))
    
    def _calculate_improvement_needed(self, metric, value):
        """Calculate how much improvement is needed to reach next level"""
        benchmarks = TradingBenchmarks.PERFORMANCE_BENCHMARKS[metric]
        
        if value >= benchmarks['excellent']:
            return {'target': 'maintain', 'improvement': 0}
        elif value >= benchmarks['good']:
            return {'target': 'excellent', 'improvement': benchmarks['excellent'] - value}
        elif value >= benchmarks['average']:
            return {'target': 'good', 'improvement': benchmarks['good'] - value}
        else:
            return {'target': 'average', 'improvement': benchmarks['average'] - value}
    
    def _generate_ranked_recommendations(self, benchmark_analysis, time_analysis, risk_analysis, risk_metrics):
        """Generate and rank recommendations by potential impact"""
        
        recommendations = []
        
        # Benchmark-based recommendations
        recommendations.extend(self._get_benchmark_recommendations(benchmark_analysis))
        
        # Time-based recommendations
        recommendations.extend(self._get_time_recommendations(time_analysis))
        
        # Risk management recommendations
        recommendations.extend(self._get_risk_recommendations(risk_analysis, risk_metrics))
        
        # Risk tolerance specific recommendations
        recommendations.extend(self._get_risk_tolerance_recommendations(risk_metrics))
        
        # Sort by priority and potential impact
        recommendations.sort(key=lambda x: (x['priority_score'], x['impact_score']), reverse=True)
        
        return recommendations
    
    def _get_benchmark_recommendations(self, benchmark_analysis):
        """Generate recommendations based on benchmark comparison"""
        recommendations = []
        
        for metric, analysis in benchmark_analysis.items():
            if analysis['rating'] in ['poor', 'average']:
                improvement = analysis['improvement_needed']
                
                if metric == 'win_rate':
                    recommendations.append({
                        'category': 'Performance',
                        'priority': 'HIGH' if analysis['rating'] == 'poor' else 'MEDIUM',
                        'priority_score': 90 if analysis['rating'] == 'poor' else 70,
                        'impact_score': 85,
                        'title': f'Improve Win Rate from {analysis["value"]:.1f}%',
                        'description': f'Target: {improvement["target"].title()} level ({improvement["improvement"]:.1f}% improvement needed)',
                        'action': 'Focus on trade selection quality and entry timing',
                        'potential_impact': f'Could improve overall performance by 15-25%',
                        'confidence': self.analyzer.confidence_level
                    })
                
                elif metric == 'profit_factor':
                    recommendations.append({
                        'category': 'Profitability',
                        'priority': 'CRITICAL' if analysis['rating'] == 'poor' else 'HIGH',
                        'priority_score': 95 if analysis['rating'] == 'poor' else 85,
                        'impact_score': 90,
                        'title': f'Improve Profit Factor from {analysis["value"]:.2f}',
                        'description': f'Target: {improvement["target"].title()} level ({improvement["improvement"]:.2f} improvement needed)',
                        'action': 'Optimize risk/reward ratio and reduce losing trade sizes',
                        'potential_impact': f'Could increase profitability by 20-40%',
                        'confidence': self.analyzer.confidence_level
                    })
                
                elif metric == 'sharpe_ratio':
                    recommendations.append({
                        'category': 'Risk-Adjusted Returns',
                        'priority': 'MEDIUM',
                        'priority_score': 75,
                        'impact_score': 70,
                        'title': f'Improve Sharpe Ratio from {analysis["value"]:.2f}',
                        'description': f'Target: {improvement["target"].title()} level ({improvement["improvement"]:.2f} improvement needed)',
                        'action': 'Reduce volatility while maintaining returns',
                        'potential_impact': f'Better risk-adjusted performance',
                        'confidence': self.analyzer.confidence_level
                    })
        
        return recommendations
    
    def _get_time_recommendations(self, time_analysis):
        """Generate time-based trading recommendations"""
        recommendations = []
        
        if 'hourly' in time_analysis:
            hourly = time_analysis['hourly']
            
            # Best hour recommendation
            recommendations.append({
                'category': 'Timing Optimization',
                'priority': 'HIGH',
                'priority_score': 80,
                'impact_score': 75,
                'title': f'Focus Trading on Hour {hourly["best_hour"]}:00 GMT',
                'description': f'Your best performing hour with {hourly["best_hour_profit"]:.2f} total profit',
                'action': f'Concentrate trading activities around {hourly["best_hour"]}:00 GMT',
                'potential_impact': 'Could improve profits by 15-30%',
                'confidence': self.analyzer.confidence_level
            })
            
            # Worst hour avoidance
            if hourly["worst_hour_profit"] < 0:
                recommendations.append({
                    'category': 'Risk Avoidance',
                    'priority': 'MEDIUM',
                    'priority_score': 70,
                    'impact_score': 60,
                    'title': f'Avoid Trading at Hour {hourly["worst_hour"]}:00 GMT',
                    'description': f'Consistent losses of {hourly["worst_hour_profit"]:.2f} during this hour',
                    'action': f'Avoid opening new positions at {hourly["worst_hour"]}:00 GMT',
                    'potential_impact': 'Could reduce losses by 10-20%',
                    'confidence': self.analyzer.confidence_level
                })
        
        if 'daily' in time_analysis:
            daily = time_analysis['daily']
            
            # Best day recommendation
            recommendations.append({
                'category': 'Weekly Optimization',
                'priority': 'MEDIUM',
                'priority_score': 75,
                'impact_score': 70,
                'title': f'Increase Trading on {daily["best_day"]}',
                'description': f'Best performing day with {daily["best_day_profit"]:.2f} total profit',
                'action': f'Allocate more trading capital to {daily["best_day"]}',
                'potential_impact': 'Could improve weekly performance by 10-25%',
                'confidence': self.analyzer.confidence_level
            })
            
            # Worst day avoidance
            if daily["worst_day_profit"] < 0:
                recommendations.append({
                    'category': 'Weekly Risk Management',
                    'priority': 'MEDIUM',
                    'priority_score': 65,
                    'impact_score': 55,
                    'title': f'Reduce Trading on {daily["worst_day"]}',
                    'description': f'Consistent losses of {daily["worst_day_profit"]:.2f} on this day',
                    'action': f'Limit or avoid trading on {daily["worst_day"]}',
                    'potential_impact': 'Could reduce weekly losses by 15%',
                    'confidence': self.analyzer.confidence_level
                })
        
        return recommendations
    
    def _get_risk_recommendations(self, risk_analysis, risk_metrics):
        """Generate risk management recommendations"""
        recommendations = []
        
        if 'stop_loss_analysis' in risk_analysis:
            sl_analysis = risk_analysis['stop_loss_analysis']
            
            if 'recommendation' in sl_analysis and sl_analysis['recommendation'] != 'Stop loss appears appropriate':
                recommendations.append({
                    'category': 'Risk Management',
                    'priority': 'HIGH',
                    'priority_score': 85,
                    'impact_score': 80,
                    'title': 'Optimize Stop Loss Strategy',
                    'description': sl_analysis['recommendation'],
                    'action': sl_analysis['reason'],
                    'potential_impact': 'Could improve win rate by 10-20%',
                    'confidence': sl_analysis.get('confidence', 'medium')
                })
        
        if 'take_profit_analysis' in risk_analysis:
            tp_analysis = risk_analysis['take_profit_analysis']
            
            if 'recommendation' in tp_analysis and tp_analysis['recommendation'] != 'Take profit strategy appears consistent':
                recommendations.append({
                    'category': 'Profit Optimization',
                    'priority': 'MEDIUM',
                    'priority_score': 70,
                    'impact_score': 65,
                    'title': 'Optimize Take Profit Strategy',
                    'description': tp_analysis['recommendation'],
                    'action': tp_analysis['reason'],
                    'potential_impact': 'Could increase average profits by 15%',
                    'confidence': tp_analysis.get('confidence', 'medium')
                })
        
        return recommendations
    
    def _get_risk_tolerance_recommendations(self, risk_metrics):
        """Generate recommendations based on user's risk tolerance"""
        recommendations = []
        
        current_rr = risk_metrics.get('risk_reward_ratio', 0)
        min_rr = self.risk_profile['min_risk_reward']
        
        if current_rr < min_rr:
            recommendations.append({
                'category': 'Risk Profile Alignment',
                'priority': 'HIGH',
                'priority_score': 80,
                'impact_score': 75,
                'title': f'Improve Risk/Reward Ratio for {self.risk_tolerance.title()} Profile',
                'description': f'Current R:R {current_rr:.2f} below {self.risk_tolerance} minimum of {min_rr:.1f}',
                'action': f'Adjust stop loss and take profit to achieve minimum {min_rr:.1f}:1 ratio',
                'potential_impact': f'Align strategy with {self.risk_tolerance} risk tolerance',
                'confidence': 'high'
            })
        
        return recommendations
    
    def _calculate_overall_score(self, risk_metrics):
        """Calculate overall strategy performance score (0-100)"""
        try:
            # Weighted scoring based on key metrics
            win_rate = risk_metrics.get('win_rate', 50)
            profit_factor = risk_metrics.get('profit_factor', 1.0)
            sharpe_ratio = risk_metrics.get('sharpe_ratio', 0.0)
            
            # Score components (0-25 each)
            wr_score = min(25, max(0, (win_rate - 30) / 2.8))  # 30-100% range
            pf_score = min(25, max(0, (profit_factor - 0.8) * 11.36))  # 0.8-3.0 range
            sr_score = min(25, max(0, (sharpe_ratio + 1) * 12.5))  # -1 to 1 range
            
            # Consistency bonus based on trade count
            consistency_score = min(25, self.analyzer.trade_count / 20)  # Up to 500 trades
            
            total_score = wr_score + pf_score + sr_score + consistency_score
            return round(min(100, max(0, total_score)), 1)
            
        except Exception:
            return 50.0