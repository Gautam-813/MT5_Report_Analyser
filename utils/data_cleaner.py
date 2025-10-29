"""
Data cleaning utilities to fix Arrow serialization issues
"""

import pandas as pd
import numpy as np
import re

def safe_float(value, default=0.0):
    """Safely convert value to float, handling strings and other types"""
    if value is None:
        return default
    
    try:
        # If it's already a number, return it
        if isinstance(value, (int, float)):
            return float(value)
        
        # If it's a string, try to convert
        if isinstance(value, str):
            # Remove common formatting characters
            cleaned = value.replace(',', '').replace(' ', '').replace('$', '').replace('%', '')
            return float(cleaned)
        
        # Try direct conversion
        return float(value)
    except (ValueError, TypeError):
        return default

def clean_dataframe_for_display(df):
    """
    Clean dataframe to prevent Arrow serialization errors
    Converts mixed types to consistent string format for display
    """
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(clean_value_for_display)
    
    return df_clean

def clean_value_for_display(value):
    """
    Clean individual values for safe display
    """
    if pd.isna(value):
        return ""
    
    # Convert to string and clean
    str_value = str(value)
    
    # Handle numeric strings with spaces/commas
    if is_numeric_string(str_value):
        try:
            # Remove spaces and commas, convert to float, then format
            cleaned = re.sub(r'[\s,]', '', str_value)
            num_value = float(cleaned)
            
            # Format based on value type
            if abs(num_value) >= 1000:
                return f"{num_value:,.2f}"
            else:
                return f"{num_value:.2f}"
        except:
            return str_value
    
    # Handle percentage strings
    if str_value.endswith('%'):
        try:
            num_part = str_value[:-1].strip()
            num_value = float(num_part)
            return f"{num_value:.1f}%"
        except:
            return str_value
    
    return str_value

def is_numeric_string(s):
    """
    Check if string represents a numeric value
    """
    # Remove common formatting characters
    cleaned = re.sub(r'[\s,]', '', s)
    
    # Check if it's a number (with optional +/- and decimal)
    pattern = r'^[+-]?\d*\.?\d+$'
    return bool(re.match(pattern, cleaned))

def convert_summary_dict_for_display(summary_dict):
    """
    Convert summary dictionary values to display-safe format
    """
    if not summary_dict:
        return {}
    
    cleaned_dict = {}
    
    for key, value in summary_dict.items():
        if pd.isna(value):
            cleaned_dict[key] = ""
        elif isinstance(value, (int, float)):
            # Format numbers appropriately
            if abs(value) >= 1000:
                cleaned_dict[key] = f"{value:,.2f}"
            else:
                cleaned_dict[key] = f"{value:.2f}"
        else:
            # Clean string values
            cleaned_dict[key] = clean_value_for_display(value)
    
    return cleaned_dict

def create_display_metrics_dataframe(metrics_dict):
    """
    Create a clean dataframe from metrics dictionary for display
    """
    if not metrics_dict:
        return pd.DataFrame()
    
    # Convert to list of dictionaries for DataFrame
    data = []
    for key, value in metrics_dict.items():
        # Format the key (make it more readable)
        display_key = format_metric_name(key)
        
        # Clean the value
        display_value = clean_value_for_display(value)
        
        data.append({
            'Metric': display_key,
            'Value': display_value
        })
    
    return pd.DataFrame(data)

def format_metric_name(key):
    """
    Format metric names for better display
    """
    # Replace underscores with spaces and title case
    formatted = key.replace('_', ' ').title()
    
    # Handle special cases
    replacements = {
        'Pnl': 'P&L',
        'Pf': 'Profit Factor',
        'Wr': 'Win Rate',
        'Rr': 'Risk Reward',
        'Avg': 'Average',
        'Max': 'Maximum',
        'Min': 'Minimum',
        'Std': 'Standard Deviation'
    }
    
    for old, new in replacements.items():
        formatted = formatted.replace(old, new)
    
    return formatted

def ensure_numeric_columns(df, numeric_columns):
    """
    Ensure specified columns are properly numeric
    """
    df_clean = df.copy()
    
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean

def clean_trades_dataframe(trades_df):
    """
    Clean trades dataframe for analysis and display
    """
    if trades_df.empty:
        return trades_df
    
    df_clean = trades_df.copy()
    
    # Ensure profit column is numeric
    if 'profit' in df_clean.columns:
        df_clean['profit'] = pd.to_numeric(df_clean['profit'], errors='coerce')
        df_clean['profit'] = df_clean['profit'].fillna(0)
    
    # Ensure time column is datetime
    if 'time' in df_clean.columns:
        df_clean['time'] = pd.to_datetime(df_clean['time'], errors='coerce')
    
    # Ensure volume column is numeric if it exists
    if 'volume' in df_clean.columns:
        df_clean['volume'] = pd.to_numeric(df_clean['volume'], errors='coerce')
        df_clean['volume'] = df_clean['volume'].fillna(0)
    
    # Remove rows with invalid data
    df_clean = df_clean.dropna(subset=['time', 'profit'])
    
    return df_clean