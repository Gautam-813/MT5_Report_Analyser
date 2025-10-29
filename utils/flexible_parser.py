"""
Flexible MT5 Parser that can handle different report formats
"""

import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np

def parse_mt5_flexible(uploaded_file, progress_callback=None):
    """
    Flexible parser that tries multiple strategies to extract trade data
    """
    try:
        if progress_callback:
            progress_callback("Reading HTML content...", 10)
        
        # Read content
        content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html.parser')
        
        if progress_callback:
            progress_callback("Analyzing HTML structure...", 20)
        
        # Try multiple parsing strategies
        strategies = [
            parse_strategy_deals_section,
            parse_strategy_orders_section,
            parse_strategy_generic_table,
            parse_strategy_text_extraction
        ]
        
        trades_df = pd.DataFrame()
        summary_dict = {}
        
        for i, strategy in enumerate(strategies):
            if progress_callback:
                progress_callback(f"Trying parsing strategy {i+1}/4...", 30 + i*15)
            
            try:
                trades_df, summary_dict = strategy(soup, progress_callback)
                if not trades_df.empty:
                    print(f"✅ Success with strategy {i+1}: Found {len(trades_df)} trades")
                    break
            except Exception as e:
                print(f"⚠️ Strategy {i+1} failed: {str(e)}")
                continue
        
        if progress_callback:
            progress_callback("Extracting summary statistics...", 85)
        
        # Always try to extract summary even if no trades found
        if not summary_dict:
            summary_dict = extract_summary_flexible(soup)
        
        if progress_callback:
            progress_callback("Processing complete", 100)
        
        return trades_df, summary_dict
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", 0)
        raise e

def parse_strategy_deals_section(soup, progress_callback=None):
    """Strategy 1: Look for 'Deals' section (original approach)"""
    trades = []
    
    # Look for the "Deals" section
    deals_found = False
    all_rows = soup.find_all('tr')
    
    for i, row in enumerate(all_rows):
        # Check if this row contains "Deals" header
        if row.find('th') and 'deals' in row.get_text().lower():
            deals_found = True
            continue
        
        # If we found deals section, look for data rows
        if deals_found and row.get('bgcolor') == '#E5F0FC':
            # Process subsequent data rows
            for j in range(i + 1, len(all_rows)):
                data_row = all_rows[j]
                
                if data_row.find('th') or data_row.get('colspan'):
                    break
                    
                cells = data_row.find_all('td')
                if len(cells) >= 10:
                    trade_data = parse_deal_row(cells)
                    if trade_data:
                        trades.append(trade_data)
            break
    
    df = pd.DataFrame(trades) if trades else pd.DataFrame()
    return clean_dataframe(df), {}

def parse_strategy_orders_section(soup, progress_callback=None):
    """Strategy 2: Look for 'Orders' section"""
    trades = []
    
    # Look for "Orders" section
    orders_found = False
    all_rows = soup.find_all('tr')
    
    for i, row in enumerate(all_rows):
        if row.find('th') and 'orders' in row.get_text().lower():
            orders_found = True
            continue
        
        if orders_found and len(row.find_all('td')) >= 8:
            cells = row.find_all('td')
            trade_data = parse_order_row(cells)
            if trade_data:
                trades.append(trade_data)
    
    df = pd.DataFrame(trades) if trades else pd.DataFrame()
    return clean_dataframe(df), {}

def parse_strategy_generic_table(soup, progress_callback=None):
    """Strategy 3: Look for any table with date/time and profit columns"""
    trades = []
    
    # Find all tables
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        
        # Look for header row to identify columns
        header_row = None
        for row in rows:
            if row.find('th'):
                header_row = row
                break
        
        if not header_row:
            continue
        
        # Get column headers
        headers = [th.get_text().strip().lower() for th in header_row.find_all('th')]
        
        # Check if this looks like a trades table
        has_time = any('time' in h or 'date' in h for h in headers)
        has_profit = any('profit' in h or 'p&l' in h or 'result' in h for h in headers)
        
        if has_time and has_profit:
            # Process data rows
            for row in rows:
                if row == header_row:
                    continue
                
                cells = row.find_all('td')
                if len(cells) >= len(headers):
                    trade_data = parse_generic_row(cells, headers)
                    if trade_data:
                        trades.append(trade_data)
    
    df = pd.DataFrame(trades) if trades else pd.DataFrame()
    return clean_dataframe(df), {}

def parse_strategy_text_extraction(soup, progress_callback=None):
    """Strategy 4: Extract data from text patterns"""
    trades = []
    
    # Get all text and look for patterns
    text = soup.get_text()
    lines = text.split('\n')
    
    # Look for lines that match trade patterns
    trade_pattern = r'(\d{4}[.-]\d{2}[.-]\d{2}\s+\d{2}:\d{2}:\d{2}).*?([+-]?\d+\.?\d*)'
    
    for line in lines:
        match = re.search(trade_pattern, line)
        if match:
            try:
                time_str = match.group(1)
                profit_str = match.group(2)
                
                trade_time = parse_datetime_flexible(time_str)
                profit = float(profit_str)
                
                if trade_time and profit != 0:
                    trades.append({
                        'time': trade_time,
                        'profit': profit,
                        'type': 'unknown'
                    })
            except:
                continue
    
    df = pd.DataFrame(trades) if trades else pd.DataFrame()
    return clean_dataframe(df), {}

def parse_deal_row(cells):
    """Parse MT5 deal row"""
    try:
        if len(cells) < 11:
            return None
        
        # Extract time (column 0)
        time_text = cells[0].get_text().strip()
        trade_time = parse_datetime_flexible(time_text)
        
        if not trade_time:
            return None
        
        # Extract profit (column 10)
        profit_text = cells[10].get_text().strip()
        profit = parse_profit_flexible(profit_text)
        
        # Only return trades with actual profit/loss
        if profit != 0.0:
            return {
                'time': trade_time,
                'profit': profit,
                'type': cells[3].get_text().strip() if len(cells) > 3 else 'unknown'
            }
        
        return None
    except:
        return None

def parse_order_row(cells):
    """Parse order row format"""
    try:
        # Look for time in first few columns
        trade_time = None
        for i in range(min(3, len(cells))):
            time_text = cells[i].get_text().strip()
            trade_time = parse_datetime_flexible(time_text)
            if trade_time:
                break
        
        if not trade_time:
            return None
        
        # Look for profit in last few columns
        profit = 0.0
        for i in range(max(0, len(cells)-5), len(cells)):
            profit_text = cells[i].get_text().strip()
            try:
                profit = parse_profit_flexible(profit_text)
                if profit != 0.0:
                    break
            except:
                continue
        
        if profit != 0.0:
            return {
                'time': trade_time,
                'profit': profit,
                'type': 'order'
            }
        
        return None
    except:
        return None

def parse_generic_row(cells, headers):
    """Parse generic table row based on headers"""
    try:
        # Find time column
        time_idx = None
        for i, header in enumerate(headers):
            if 'time' in header or 'date' in header:
                time_idx = i
                break
        
        # Find profit column
        profit_idx = None
        for i, header in enumerate(headers):
            if 'profit' in header or 'p&l' in header or 'result' in header:
                profit_idx = i
                break
        
        if time_idx is None or profit_idx is None:
            return None
        
        if len(cells) <= max(time_idx, profit_idx):
            return None
        
        # Extract data
        time_text = cells[time_idx].get_text().strip()
        profit_text = cells[profit_idx].get_text().strip()
        
        trade_time = parse_datetime_flexible(time_text)
        profit = parse_profit_flexible(profit_text)
        
        if trade_time and profit != 0.0:
            return {
                'time': trade_time,
                'profit': profit,
                'type': 'generic'
            }
        
        return None
    except:
        return None

def parse_datetime_flexible(time_str):
    """Flexible datetime parsing"""
    time_str = time_str.strip()
    
    formats = [
        '%Y.%m.%d %H:%M:%S',
        '%Y.%m.%d %H:%M',
        '%d.%m.%Y %H:%M:%S',
        '%d.%m.%Y %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    
    return None

def parse_profit_flexible(profit_str):
    """Flexible profit parsing"""
    try:
        # Clean the string
        cleaned = profit_str.replace(' ', '').replace(',', '')
        cleaned = re.sub(r'[^\d.+-]', '', cleaned)
        
        if cleaned and cleaned not in ['+', '-', '.']:
            return float(cleaned)
        return 0.0
    except:
        return 0.0

def extract_summary_flexible(soup):
    """Extract summary statistics flexibly"""
    summary = {}
    text = soup.get_text()
    
    # Common patterns
    patterns = {
        'total_net_profit': r'total.*net.*profit.*?([+-]?[\d\s,]+\.?\d*)',
        'profit_factor': r'profit.*factor.*?([+-]?[\d.]+)',
        'total_trades': r'total.*trades.*?(\d+)',
        'win_rate': r'win.*rate.*?(\d+\.?\d*)%?',
        'gross_profit': r'gross.*profit.*?([+-]?[\d\s,]+\.?\d*)',
        'gross_loss': r'gross.*loss.*?([+-]?[\d\s,]+\.?\d*)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            try:
                if key in ['total_trades']:
                    summary[key] = int(re.sub(r'[\s,]', '', value))
                elif key in ['win_rate']:
                    summary[key] = float(value)
                else:
                    summary[key] = float(re.sub(r'[\s,]', '', value))
            except:
                summary[key] = value
    
    return summary

def clean_dataframe(df):
    """Clean the resulting dataframe"""
    if df.empty:
        return df
    
    # Ensure required columns
    if 'time' not in df.columns or 'profit' not in df.columns:
        return pd.DataFrame()
    
    # Remove invalid rows
    df = df.dropna(subset=['time', 'profit'])
    
    # Convert types
    df['time'] = pd.to_datetime(df['time'])
    df['profit'] = pd.to_numeric(df['profit'], errors='coerce')
    
    # Remove zero profit rows
    df = df[df['profit'] != 0]
    
    # Sort by time
    df = df.sort_values('time').reset_index(drop=True)
    
    return df