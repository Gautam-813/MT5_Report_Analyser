"""
Safe formatting utilities for MT5 data display
"""

def safe_format_currency(value, decimals=2):
    """Safely format currency values with consistent 2 decimal places"""
    try:
        if isinstance(value, (int, float)):
            return f"${value:,.{decimals}f}"
        elif isinstance(value, str):
            # Try to convert string to float first
            cleaned = value.replace('$', '').replace(',', '').strip()
            num_value = float(cleaned)
            return f"${num_value:,.{decimals}f}"
        else:
            return f"${0:.{decimals}f}"
    except:
        return str(value)

def safe_format_number(value, decimals=2):
    """Safely format numeric values with consistent 2 decimal places"""
    try:
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}"
        elif isinstance(value, str):
            # Try to convert string to float first
            cleaned = value.replace(',', '').strip()
            num_value = float(cleaned)
            return f"{num_value:.{decimals}f}"
        else:
            return f"{0:.{decimals}f}"
    except:
        return str(value)

def safe_format_integer(value):
    """Safely format integer values"""
    if isinstance(value, (int, float)):
        return f"{int(value):,}"
    else:
        return str(value)

def safe_format_percentage(value, decimals=2):
    """Safely format percentage values with consistent 2 decimal places"""
    try:
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}%"
        elif isinstance(value, str):
            # Try to convert string to float first
            cleaned = value.replace('%', '').replace(',', '').strip()
            num_value = float(cleaned)
            return f"{num_value:.{decimals}f}%"
        else:
            return f"{0:.{decimals}f}%"
    except:
        return str(value)

def safe_format_ratio(value, decimals=2):
    """Safely format ratio values with consistent 2 decimal places"""
    try:
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}"
        elif isinstance(value, str):
            # Try to convert string to float first
            cleaned = value.replace(',', '').strip()
            num_value = float(cleaned)
            return f"{num_value:.{decimals}f}"
        else:
            return f"{0:.{decimals}f}"
    except:
        return str(value)