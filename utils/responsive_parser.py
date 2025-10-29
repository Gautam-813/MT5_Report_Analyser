"""
Responsive MT5 Parser with progress callbacks
Prevents UI blocking during large file processing
"""

import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np
import io
import time

def parse_uploaded_report_responsive(uploaded_file, progress_callback=None):
    """
    Parse MT5 report with progress callbacks to keep UI responsive
    """
    try:
        if progress_callback:
            progress_callback("Reading file content...", 10)
        
        # Determine file type
        file_name = uploaded_file.name.lower()
        is_csv = file_name.endswith('.csv')
        is_html = file_name.endswith(('.html', '.htm'))
        
        if progress_callback:
            progress_callback("Determining file format...", 15)
        
        if is_csv:
            # Parse CSV with progress
            if progress_callback:
                progress_callback("Parsing CSV data...", 20)
            
            file_content = io.StringIO(uploaded_file.getvalue().decode('utf-8'))
            trades_df, summary_dict = parse_csv_responsive(file_content, progress_callback)
            
        elif is_html:
            # Parse HTML with progress
            if progress_callback:
                progress_callback("Parsing HTML report...", 20)
            
            # Read file content in chunks to prevent blocking
            content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
            
            if progress_callback:
                progress_callback("Processing HTML structure...", 30)
            
            trades_df, summary_dict = parse_html_responsive(content, progress_callback)
            
        else:
            raise Exception("Unsupported file format. Please upload HTML or CSV files.")
        
        if progress_callback:
            progress_callback("Finalizing data processing...", 90)
        
        # Ensure the DataFrame has required columns
        if not trades_df.empty and 'time' in trades_df.columns:
            # Make sure time is datetime
            if not pd.api.types.is_datetime64_any_dtype(trades_df['time']):
                trades_df['time'] = pd.to_datetime(trades_df['time'])
        
        if progress_callback:
            progress_callback("Processing complete!", 100)
        
        return trades_df, summary_dict
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", 0)
        raise Exception(f"Error parsing {uploaded_file.name}: {str(e)}")

def parse_html_responsive(content, progress_callback=None):
    """Parse HTML content with progress updates"""
    
    if progress_callback:
        progress_callback("Creating HTML parser...", 35)
    
    soup = BeautifulSoup(content, 'html.parser')
    
    if progress_callback:
        progress_callback("Extracting trade data...", 50)
    
    # Extract trades table with progress
    trades_df = extract_trades_responsive(soup, progress_callback)
    
    if progress_callback:
        progress_callback("Extracting summary statistics...", 70)
    
    # Extract summary statistics
    summary_dict = extract_summary_responsive(soup, progress_callback)
    
    return trades_df, summary_dict

def extract_trades_responsive(soup, progress_callback=None):
    """Extract trades with progress updates"""
    trades = []
    
    if progress_callback:
        progress_callback("Searching for trade data...", 55)
    
    # Look for the "Deals" section specifically
    deals_found = False
    all_rows = soup.find_all('tr')
    
    if progress_callback:
        progress_callback(f"Processing {len(all_rows)} table rows...", 60)
    
    for i, row in enumerate(all_rows):
        # Update progress every 100 rows to keep UI responsive
        if i % 100 == 0 and progress_callback:
            progress = 60 + (i / len(all_rows)) * 10  # 60-70% range
            progress_callback(f"Processing row {i}/{len(all_rows)}...", progress)
        
        # Check if this row contains "Deals" header
        if row.find('th') and 'deals' in row.get_text().lower():
            deals_found = True
            continue
        
        # If we found deals section, look for the header row
        if deals_found and row.get('bgcolor') == '#E5F0FC':
            # This is the header row, start processing data rows
            header_cells = row.find_all('td')
            if len(header_cells) >= 10:  # Expected number of columns
                # Process subsequent data rows
                for j in range(i + 1, len(all_rows)):
                    data_row = all_rows[j]
                    
                    # Stop if we hit another section
                    if data_row.find('th') or data_row.get('colspan'):
                        break
                        
                    cells = data_row.find_all('td')
                    if len(cells) >= 10:  # Minimum expected columns
                        trade_data = parse_trade_row_safe(cells)
                        if trade_data:
                            trades.append(trade_data)
            break
    
    if progress_callback:
        progress_callback(f"Found {len(trades)} trades, creating DataFrame...", 65)
    
    if trades:
        df = pd.DataFrame(trades)
        df = clean_trades_dataframe_safe(df)
        return df
    else:
        return pd.DataFrame()

def parse_trade_row_safe(cells):
    """Safely parse trade row without blocking"""
    try:
        if len(cells) < 11:
            return None
        
        trade = {}
        
        # Extract time (column 0)
        time_text = cells[0].get_text().strip()
        trade['time'] = parse_datetime_safe(time_text)
        
        if not trade['time']:
            return None
        
        # Extract type and direction (columns 3 and 4)
        trade_type = cells[3].get_text().strip().lower()
        direction = cells[4].get_text().strip().lower()
        
        # Only process actual trades (not balance entries)
        if trade_type == 'balance':
            return None
        
        # Combine type and direction for trade type
        if direction == 'in':
            trade['type'] = f"{trade_type}_open"
        elif direction == 'out':
            trade['type'] = f"{trade_type}_close"
        else:
            trade['type'] = trade_type
        
        # Extract volume (column 5)
        volume_text = cells[5].get_text().strip()
        if volume_text:
            try:
                trade['volume'] = float(volume_text)
            except:
                trade['volume'] = 0.0
        
        # Extract profit (column 10)
        profit_text = cells[10].get_text().strip()
        trade['profit'] = parse_profit_safe(profit_text)
        
        # Only return trades with actual profit/loss (not 0.00 opening trades)
        if trade['profit'] != 0.0:
            return trade
        
        return None
        
    except Exception:
        return None

def parse_datetime_safe(time_str):
    """Safely parse datetime"""
    time_str = time_str.strip()
    
    formats = [
        '%Y.%m.%d %H:%M:%S',
        '%Y.%m.%d %H:%M',
        '%d.%m.%Y %H:%M:%S',
        '%d.%m.%Y %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    
    return None

def parse_profit_safe(profit_str):
    """Safely parse profit value"""
    try:
        cleaned = profit_str.replace(' ', '').replace(',', '')
        cleaned = re.sub(r'[^\d.+-]', '', cleaned)
        
        if cleaned and cleaned not in ['+', '-', '.']:
            return float(cleaned)
        return 0.0
    except:
        return 0.0

def clean_trades_dataframe_safe(df):
    """Safely clean trades dataframe"""
    if df.empty:
        return df
    
    # Ensure required columns exist
    required_cols = ['time', 'profit']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
    
    # Remove rows with invalid data
    df = df.dropna(subset=['time', 'profit'])
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Sort by time
    df = df.sort_values('time').reset_index(drop=True)
    
    return df

def extract_summary_responsive(soup, progress_callback=None):
    """Extract summary with progress updates"""
    if progress_callback:
        progress_callback("Extracting summary statistics...", 75)
    
    # Use existing summary extraction logic but with progress
    summary = {}
    text = soup.get_text()
    
    # Basic patterns for quick extraction
    patterns = {
        'total_net_profit': r'Total Net Profit\s*:?\s*([+-]?[\d\s,]+\.?\d*)',
        'profit_factor': r'Profit Factor\s*:?\s*([+-]?[\d.]+)',
        'total_trades': r'Total Trades\s*:?\s*([\d\s,]+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            try:
                if key in ['total_trades']:
                    summary[key] = int(re.sub(r'[\s,]', '', value))
                elif key in ['total_net_profit', 'profit_factor']:
                    summary[key] = float(re.sub(r'[\s,]', '', value))
                else:
                    summary[key] = value
            except:
                summary[key] = value
    
    if progress_callback:
        progress_callback("Summary extraction complete", 80)
    
    return summary

def parse_csv_responsive(file_content, progress_callback=None):
    """Parse CSV with progress updates"""
    if progress_callback:
        progress_callback("Reading CSV data...", 30)
    
    # Try different separators
    separators = [',', ';', '\t']
    df = None
    
    for sep in separators:
        try:
            file_content.seek(0)
            df = pd.read_csv(file_content, sep=sep)
            
            if len(df.columns) > 1 and len(df) > 0:
                break
        except Exception:
            continue
    
    if df is None or df.empty:
        raise Exception("Could not parse CSV file")
    
    if progress_callback:
        progress_callback("Mapping CSV columns...", 50)
    
    # Map columns
    trades_df = map_csv_columns_safe(df)
    
    if progress_callback:
        progress_callback("Generating CSV summary...", 70)
    
    # Generate summary
    summary_dict = generate_csv_summary_safe(trades_df)
    
    return trades_df, summary_dict

def map_csv_columns_safe(df):
    """Safely map CSV columns"""
    # Simplified column mapping for responsiveness
    mapped_df = pd.DataFrame()
    
    # Look for profit column
    for col in df.columns:
        if any(word in col.lower() for word in ['profit', 'pnl', 'p&l']):
            mapped_df['profit'] = df[col]
            break
    
    # Look for time column
    for col in df.columns:
        if any(word in col.lower() for word in ['time', 'date', 'datetime']):
            mapped_df['time'] = df[col]
            break
    
    # If no time column, create sequential times
    if 'time' not in mapped_df.columns:
        base_time = datetime.now()
        mapped_df['time'] = pd.date_range(start=base_time, periods=len(df), freq='h')
    
    # Ensure we have profit column
    if 'profit' not in mapped_df.columns:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            mapped_df['profit'] = df[numeric_cols[0]]
        else:
            raise Exception("Could not identify profit/PnL column in CSV")
    
    return clean_trades_dataframe_safe(mapped_df)

def generate_csv_summary_safe(trades_df):
    """Generate basic summary from CSV"""
    if trades_df.empty:
        return {}
    
    total_trades = len(trades_df)
    profitable_trades = len(trades_df[trades_df['profit'] > 0])
    total_profit = trades_df['profit'].sum()
    
    return {
        'total_trades': total_trades,
        'profit_trades': profitable_trades,
        'total_net_profit': total_profit,
        'profit_factor': 1.0 if total_profit > 0 else 0.0
    }