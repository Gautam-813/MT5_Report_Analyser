"""
Industry Benchmark Standards for Trading Performance
Based on professional trading research and industry standards
"""

class TradingBenchmarks:
    """Professional trading performance benchmarks"""
    
    # Performance Benchmarks (Research-based)
    PERFORMANCE_BENCHMARKS = {
        'win_rate': {
            'excellent': 70,
            'good': 60,
            'average': 50,
            'poor': 40
        },
        'profit_factor': {
            'excellent': 2.5,
            'good': 2.0,
            'average': 1.5,
            'poor': 1.2
        },
        'sharpe_ratio': {
            'excellent': 2.0,
            'good': 1.5,
            'average': 1.0,
            'poor': 0.5
        },
        'max_drawdown': {
            'excellent': 5,
            'good': 10,
            'average': 15,
            'poor': 20
        },
        'risk_reward_ratio': {
            'excellent': 3.0,
            'good': 2.0,
            'average': 1.5,
            'poor': 1.0
        }
    }
    
    # Statistical Confidence Levels
    CONFIDENCE_LEVELS = {
        'professional': {'min_trades': 500, 'confidence': 95},
        'high': {'min_trades': 300, 'confidence': 90},
        'reliable': {'min_trades': 100, 'confidence': 80},
        'basic': {'min_trades': 30, 'confidence': 70},
        'insufficient': {'min_trades': 0, 'confidence': 50}
    }
    
    # Risk Tolerance Profiles
    RISK_PROFILES = {
        'conservative': {
            'max_risk_per_trade': 0.02,  # 2%
            'min_risk_reward': 2.0,
            'max_drawdown': 10,
            'min_win_rate': 60
        },
        'moderate': {
            'max_risk_per_trade': 0.03,  # 3%
            'min_risk_reward': 1.5,
            'max_drawdown': 15,
            'min_win_rate': 50
        },
        'aggressive': {
            'max_risk_per_trade': 0.05,  # 5%
            'min_risk_reward': 1.0,
            'max_drawdown': 20,
            'min_win_rate': 40
        }
    }
    
    # Market Session Characteristics
    MARKET_SESSIONS = {
        'asian': {
            'hours': (0, 9),  # GMT
            'characteristics': 'Lower volatility, range-bound',
            'best_for': 'Range trading strategies'
        },
        'european': {
            'hours': (7, 16),  # GMT
            'characteristics': 'High volatility, trending',
            'best_for': 'Breakout and trend strategies'
        },
        'us': {
            'hours': (12, 21),  # GMT
            'characteristics': 'High volatility, news-driven',
            'best_for': 'News trading and momentum'
        },
        'overlap_eu_us': {
            'hours': (12, 16),  # GMT
            'characteristics': 'Maximum liquidity',
            'best_for': 'All strategies'
        }
    }
    
    @classmethod
    def get_performance_rating(cls, metric_name, value):
        """Get performance rating for a specific metric"""
        try:
            if metric_name not in cls.PERFORMANCE_BENCHMARKS:
                return 'unknown'
            
            if value is None or not isinstance(value, (int, float)):
                return 'unknown'
            
            benchmarks = cls.PERFORMANCE_BENCHMARKS[metric_name]
            
            if value >= benchmarks['excellent']:
                return 'excellent'
            elif value >= benchmarks['good']:
                return 'good'
            elif value >= benchmarks['average']:
                return 'average'
            else:
                return 'poor'
        except Exception:
            return 'unknown'
    
    @classmethod
    def get_confidence_level(cls, trade_count):
        """Get statistical confidence level based on trade count"""
        try:
            if not isinstance(trade_count, (int, float)) or trade_count < 0:
                return 'insufficient', 50
            
            for level, requirements in cls.CONFIDENCE_LEVELS.items():
                if trade_count >= requirements['min_trades']:
                    return level, requirements['confidence']
            return 'insufficient', 50
        except Exception:
            return 'insufficient', 50
    
    @classmethod
    def get_risk_profile_standards(cls, risk_tolerance):
        """Get standards for specific risk tolerance"""
        return cls.RISK_PROFILES.get(risk_tolerance.lower(), cls.RISK_PROFILES['moderate'])
    
    @classmethod
    def get_session_info(cls, hour_gmt):
        """Get market session info for specific GMT hour"""
        try:
            if not isinstance(hour_gmt, (int, float)) or hour_gmt < 0 or hour_gmt >= 24:
                return 'off_hours', {'characteristics': 'Invalid hour', 'best_for': 'Check time format'}
            
            for session, info in cls.MARKET_SESSIONS.items():
                start_hour, end_hour = info['hours']
                if start_hour <= hour_gmt < end_hour:
                    return session, info
            return 'off_hours', {'characteristics': 'Low activity', 'best_for': 'Avoid trading'}
        except Exception:
            return 'off_hours', {'characteristics': 'Error processing', 'best_for': 'Check data'}