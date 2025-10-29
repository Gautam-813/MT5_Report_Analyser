"""
Non-blocking MT5 Parser that processes files in small chunks
Prevents browser from becoming unresponsive
"""

import pandas as pd
import re
from datetime import datetime
import time
import streamlit as st

def parse_mt5_non_blocking(uploaded_file, progress_callback=None):
    """
    Parse MT5 file in small chunks to prevent UI blocking
    """
    try:
        if progress_callback:
            progress_callback("Reading file in chunks...", 5)
        
        # Read file content
        content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        
        if progress_callback:
            progress_callback("Analyzing file structure...", 10)
        
        # Process in chunks to prevent blocking
        chunk_size = 50000  # 50KB chunks
        total_chunks = len(content) // chunk_size + 1
        
        trades = []
        summary_data = {}
        
        # Look for trade data patterns in chunks
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            chunk_num = i // chunk_size + 1
            
            if progress_callback:
                progress = 10 + (chunk_num / total_chunks) * 70
                progress_callback(f"Processing chunk {chunk_num}/{total_chunks}...", progress)
            
            # Extract trades from this chunk
            chunk_trades = extract_trades_from_chunk(chunk, i > 0)
            trades.extend(chunk_trades)
            
            # Small delay to keep UI responsive
            time.sleep(0.01)
        
        if progress_callback:
            progress_callback("Extracting summary statistics...", 85)
        
        # Extract summary from full content (faster patterns)
        summary_data = extract_summary_fast(content)
        
        if progress_callback:
            progress_callback("Creating DataFrame...", 90)
        
        # Create DataFrame
        if trades:
            df = pd.DataFrame(trades)
            df = clean_trades_fast(df)
        else:
            df = pd.DataFrame()
        
        if progress_callback:
            progress_callback("Processing complete!", 100)
        
        return df, summary_data
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", 0)
        raise e

def extract_trades_from_chunk(chunk, is_continuation=False):
    """
    Extract trade data from a text chunk using regex patterns
    """
    trades = []
    
    # Pattern for MT5 deal lines (common format)
    # Matches: 2024.01.15 10:30:00  123456  EURUSD  buy  in  0.10  1.0850  ...  +15.50
    deal_pattern = r'(\d{4}[.\-/]\d{2}[.\-/]\d{2}\s+\d{2}:\d{2}:\d{2})\s+\d+\s+\w+\s+\w+\s+\w+\s+[\d.]+\s+[\d.]+.*?([+-]?\d+\.?\d*)\s*$'
    
    # Pattern for simpler formats
    # Matches: 2024.01.15 10:30:00 ... +15.50
    simple_pattern = r'(\d{4}[.\-/]\d{2}[.\-/]\d{2}\s+\d{2}:\d{2}:\d{2}).*?([+-]\d+\.?\d+)'
    
    # Pattern for CSV-like formats
    csv_pattern = r'(\d{4}[.\-/]\d{2}[.\-/]\d{2}[,\s]+\d{2}:\d{2}:\d{2})[,\s]+.*?[,\s]+([+-]?\d+\.?\d*)'
    
    patterns = [deal_pattern, simple_pattern, csv_pattern]
    
    lines = chunk.split('\n')
    
    for line in lines:
        line = line.strip()
        if len(line) < 20:  # Skip short lines
            continue
        
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                try:
                    time_str = match[0]
                    profit_str = match[1]
                    
                    # Parse datetime
                    trade_time = parse_datetime_fast(time_str)
                    if not trade_time:
                        continue
                    
                    # Parse profit
                    profit = parse_profit_fast(profit_str)
                    if profit == 0.0:
                        continue
                    
                    trades.append({
                        'time': trade_time,
                        'profit': profit,
                        'type': 'trade'
                    })
                    
                except Exception:
                    continue
    
    return trades

def parse_datetime_fast(time_str):
    """Fast datetime parsing with common formats"""
    time_str = time_str.strip()
    
    # Try most common MT5 format first
    try:
        return datetime.strptime(time_str, '%Y.%m.%d %H:%M:%S')
    except:
        pass
    
    # Try other common formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d.%m.%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except:
            continue
    
    return None

def parse_profit_fast(profit_str):
    """Fast profit parsing"""
    try:
        # Remove common characters
        cleaned = profit_str.replace(' ', '').replace(',', '')
        
        # Extract number with sign
        match = re.search(r'([+-]?\d+\.?\d*)', cleaned)
        if match:
            return float(match.group(1))
        return 0.0
    except:
        return 0.0

def extract_summary_fast(content):
    """Fast summary extraction using simple regex"""
    summary = {}
    
    # Use case-insensitive search
    content_lower = content.lower()
    
    # Simple patterns for key metrics
    patterns = {
        'total_net_profit': r'total.*net.*profit.*?([+-]?\d+\.?\d*)',
        'profit_factor': r'profit.*factor.*?(\d+\.?\d*)',
        'total_trades': r'total.*trades.*?(\d+)',
        'win_rate': r'win.*rate.*?(\d+\.?\d*)%?'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content_lower)
        if match:
            try:
                value = match.group(1)
                if key == 'total_trades':
                    summary[key] = int(value)
                else:
                    summary[key] = float(value)
            except:
                summary[key] = value
    
    return summary

def clean_trades_fast(df):
    """Fast DataFrame cleaning"""
    if df.empty:
        return df
    
    # Basic cleaning
    df = df.dropna(subset=['time', 'profit'])
    df['time'] = pd.to_datetime(df['time'])
    df['profit'] = pd.to_numeric(df['profit'], errors='coerce')
    df = df[df['profit'] != 0]
    df = df.sort_values('time').reset_index(drop=True)
    
    return df

def parse_mt5_ultra_fast(uploaded_file, progress_callback=None):
    """
    Ultra-fast parser that only looks for essential data
    """
    try:
        if progress_callback:
            progress_callback("Ultra-fast parsing mode...", 10)
        
        # Read content
        content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        
        if progress_callback:
            progress_callback("Extracting trade patterns...", 30)
        
        # Use single regex to find all trades at once
        # This is much faster than line-by-line processing
        trade_pattern = r'(\d{4}[.\-/]\d{2}[.\-/]\d{2}\s+\d{2}:\d{2}:\d{2}).*?([+-]\d+\.?\d+)'
        
        matches = re.findall(trade_pattern, content)
        
        if progress_callback:
            progress_callback(f"Found {len(matches)} potential trades...", 60)
        
        trades = []
        for i, (time_str, profit_str) in enumerate(matches):
            if i % 100 == 0 and progress_callback:
                progress = 60 + (i / len(matches)) * 20
                progress_callback(f"Processing trade {i}/{len(matches)}...", progress)
            
            try:
                trade_time = datetime.strptime(time_str, '%Y.%m.%d %H:%M:%S')
                profit = float(profit_str)
                
                if profit != 0:
                    trades.append({
                        'time': trade_time,
                        'profit': profit,
                        'type': 'trade'
                    })
            except:
                continue
        
        if progress_callback:
            progress_callback("Creating final dataset...", 85)
        
        # Create DataFrame
        if trades:
            df = pd.DataFrame(trades)
            df = df.sort_values('time').reset_index(drop=True)
        else:
            df = pd.DataFrame()
        
        # Quick summary
        summary = {
            'total_trades': len(trades),
            'total_net_profit': sum(t['profit'] for t in trades) if trades else 0
        }
        
        if progress_callback:
            progress_callback("Ultra-fast parsing complete!", 100)
        
        return df, summary
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", 0)
        raise e