"""
Debug parser to analyze MT5 HTML structure
"""

from bs4 import BeautifulSoup
import re

def debug_html_structure(uploaded_file):
    """
    Debug function to analyze the structure of the uploaded HTML file
    """
    try:
        # Read the HTML content
        content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html.parser')
        
        print("🔍 DEBUG: Analyzing HTML structure...")
        
        # Find all tables
        tables = soup.find_all('table')
        print(f"📊 Found {len(tables)} tables")
        
        # Find all rows
        all_rows = soup.find_all('tr')
        print(f"📋 Found {len(all_rows)} table rows")
        
        # Look for text patterns that might indicate trades
        text_content = soup.get_text().lower()
        
        # Check for common MT5 keywords
        keywords = ['deals', 'trades', 'orders', 'profit', 'balance', 'buy', 'sell']
        found_keywords = []
        for keyword in keywords:
            if keyword in text_content:
                found_keywords.append(keyword)
        
        print(f"🔍 Found keywords: {found_keywords}")
        
        # Look for table headers
        headers = soup.find_all('th')
        print(f"📑 Found {len(headers)} table headers")
        
        for i, header in enumerate(headers[:10]):  # Show first 10 headers
            print(f"  Header {i}: {header.get_text().strip()}")
        
        # Look for rows with bgcolor (common in MT5 reports)
        colored_rows = soup.find_all('tr', {'bgcolor': True})
        print(f"🎨 Found {len(colored_rows)} colored rows")
        
        # Check for specific bgcolor values
        bgcolor_values = set()
        for row in colored_rows:
            bgcolor = row.get('bgcolor')
            if bgcolor:
                bgcolor_values.add(bgcolor)
        
        print(f"🎨 Background colors found: {list(bgcolor_values)}")
        
        # Look for rows that might contain trade data
        potential_trade_rows = []
        for i, row in enumerate(all_rows[:50]):  # Check first 50 rows
            cells = row.find_all('td')
            if len(cells) >= 5:  # Minimum cells for trade data
                cell_texts = [cell.get_text().strip() for cell in cells[:5]]
                # Check if first cell looks like a date/time
                if cells and re.match(r'\d{4}[.-]\d{2}[.-]\d{2}', cell_texts[0]):
                    potential_trade_rows.append((i, cell_texts))
        
        print(f"📈 Found {len(potential_trade_rows)} potential trade rows")
        
        # Show sample of potential trade rows
        for i, (row_idx, cell_texts) in enumerate(potential_trade_rows[:5]):
            print(f"  Row {row_idx}: {cell_texts}")
        
        # Look for summary statistics
        summary_patterns = [
            r'total.*profit',
            r'profit.*factor',
            r'total.*trades',
            r'win.*rate',
            r'gross.*profit',
            r'gross.*loss'
        ]
        
        found_summaries = []
        for pattern in summary_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                found_summaries.extend(matches)
        
        print(f"📊 Found summary patterns: {found_summaries[:10]}")
        
        return {
            'tables': len(tables),
            'rows': len(all_rows),
            'headers': len(headers),
            'keywords': found_keywords,
            'colored_rows': len(colored_rows),
            'bgcolor_values': list(bgcolor_values),
            'potential_trades': len(potential_trade_rows),
            'sample_trades': potential_trade_rows[:3]
        }
        
    except Exception as e:
        print(f"❌ DEBUG: Error analyzing HTML: {str(e)}")
        return None

def create_flexible_parser(debug_info):
    """
    Create a parser based on the debug information
    """
    print("🔧 Creating flexible parser based on HTML structure...")
    
    # This would contain logic to adapt parsing based on what we found
    # For now, return a basic structure
    return {
        'strategy': 'flexible',
        'target_bgcolor': debug_info.get('bgcolor_values', [None])[0] if debug_info else None,
        'expected_columns': 10  # Default MT5 structure
    }