"""
Safe formatting utilities for MT5 data display
"""

def safe_format_currency(value, decimals=2):
    """Safely format currency values"""
    if isinstance(value, (int, float)):
        return f"${value:,.{decimals}f}"
    else:
        return str(value)

def safe_format_number(value, decimals=2):
    """Safely format numeric values"""
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}"
    else:
        return str(value)

def safe_format_integer(value):
    """Safely format integer values"""
    if isinstance(value, (int, float)):
        return f"{int(value):,}"
    else:
        return str(value)

def safe_format_percentage(value, decimals=1):
    """Safely format percentage values"""
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}%"
    else:
        return str(value)

def safe_format_ratio(value, decimals=2):
    """Safely format ratio values"""
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}"
    else:
        return str(value)