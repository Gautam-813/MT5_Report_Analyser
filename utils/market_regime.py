"""
Market Regime Analyzer
Advanced market condition analysis for institutional trading
Based on quantitative finance research and hedge fund methodologies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

class MarketRegimeAnalyzer:
    """
    Professional market regime detection and analysis
    Used by hedge funds and institutional traders for strategy optimization
    """
    
    def __init__(self, trades_df):
        """Initialize with trading data"""
        try:
            self.trades_df = trades_df.copy() if trades_df is not None and not trades_df.empty else pd.DataFrame()
            self.prepared_data = self._prepare_market_data() if not self.trades_df.empty else pd.DataFrame()
        except Exception:
            self.trades_df = pd.DataFrame()
            self.prepared_data = pd.DataFrame()
    
    def _prepare_market_data(self):
        """Prepare and clean market data for analysis"""
        try:
            if self.trades_df.empty or 'time' not in self.trades_df.columns:
                return pd.DataFrame()
            
            df = self.trades_df.copy()
            df['time'] = pd.to_datetime(df['time'], errors='coerce')
            df = df.dropna(subset=['time']).sort_values('time')
            
            if len(df) < 10:
                return pd.DataFrame()
            
            # Add time components
            df['hour'] = df['time'].dt.hour
            df['weekday'] = df['time'].dt.weekday
            df['month'] = df['time'].dt.month
            df['date'] = df['time'].dt.date
            
            # Calculate returns and volatility
            df['cumulative_pnl'] = df['profit'].cumsum()
            df['returns'] = df['profit'] / d