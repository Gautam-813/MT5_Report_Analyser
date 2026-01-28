"""
Live Trade Parser
Parses HTML reports from live MT5 trading accounts
"""

import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np
import io

class LiveTradeParser:
    def __init__(self):
        self.trades_data = None
        self.summary_data = None
        self.account_info = None
        
    def parse_live_html_report(self, file_path):
        """Parse live MT5 HTML report and extract trade data"""
        try:
            # Try different encodings - UTF-16 first for MT5 reports
            encodings = ['utf-16', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("Could not decode file with any supported encoding")
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract account information
            account_info = self._extract_account_info(soup)
            
            # Extract positions (completed trades)
            positions_df = self._extract_positions_table(soup)
            
            # Extract deals (individual transactions)
            deals_df = self._extract_deals_table(soup)
            
            # Extract summary statistics
            summary_dict = self._extract_live_summary_stats(soup)
            
            return positions_df, deals_df, summary_dict, account_info
            
        except Exception as e:
            raise Exception(f"Error parsing live MT5 report: {str(e)}")
    
    def _extract_account_info(self, soup):
        """Extract account information from the report header"""
        account_info = {}
        
        try:
            # Extract account details from the header
            text = soup.get_text()
            
            # Account name
            name_match = re.search(r'Name:\s*([^\n]+)', text)
            if name_match:
                account_info['name'] = name_match.group(1).strip()
            
            # Account number and details
            account_match = re.search(r'Account:\s*([^\n]+)', text)
            if account_match:
                account_details = account_match.group(1).strip()
                account_info['account_details'] = account_details
                
                # Extract account number
                acc_num_match = re.search(r'(\d+)', account_details)
                if acc_num_match:
                    account_info['account_number'] = acc_num_match.group(1)
                
                # Extract currency
                currency_match = re.search(r'\(([A-Z]{3})', account_details)
                if currency_match:
                    account_info['currency'] = currency_match.group(1)
            
            # Company
            company_match = re.search(r'Company:\s*([^\n]+)', text)
            if company_match:
                account_info['company'] = company_match.group(1).strip()
            
            # Report date
            date_match = re.search(r'Date:\s*([^\n]+)', text)
            if date_match:
                account_info['report_date'] = date_match.group(1).strip()
                
        except Exception as e:
            print(f"Warning: Could not extract account info: {e}")
        
        return account_info
    
    def _extract_positions_table(self, soup):
        """Extract completed positions from the Positions section"""
        positions = []
        
        try:
            # Find the Positions section
            positions_found = False
            all_rows = soup.find_all('tr')
            
            for i, row in enumerate(all_rows):
                # Check if this row contains "Positions" header
                if row.find('th') and 'positions' in row.get_text().lower():
                    positions_found = True
                    continue
                
                # If we found positions section, look for the header row
                if positions_found and row.get('bgcolor') == '#E5F0FC':
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
                                position_data = self._parse_live_position_row(cells)
                                if position_data:
                                    positions.append(position_data)
                    break
            
            if positions:
                df = pd.DataFrame(positions)
                df = self._clean_positions_dataframe(df)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error extracting positions: {e}")
            return pd.DataFrame()
    
    def _parse_live_position_row(self, cells):
        """Parse individual position row from live trading report"""
        try:
            # Live position structure: Time, Position, Symbol, Type, Volume, Price, S/L, T/P, Time, Price, Commission, Swap, Profit
            if len(cells) < 13:
                return None
            
            position = {}
            
            # Extract open time (column 0)
            open_time_text = cells[0].get_text().strip()
            position['open_time'] = self._parse_datetime(open_time_text)
            
            if not position['open_time']:
                return None
            
            # Extract position ID (column 1)
            position['position_id'] = cells[1].get_text().strip()
            
            # Extract symbol (column 2)
            position['symbol'] = cells[2].get_text().strip()
            
            # Extract type (column 3)
            position['type'] = cells[3].get_text().strip().lower()
            
            # Extract volume (column 4)
            volume_text = cells[4].get_text().strip()
            if volume_text:
                try:
                    position['volume'] = float(volume_text)
                except:
                    position['volume'] = 0.0
            
            # Extract open price (column 5)
            open_price_text = cells[5].get_text().strip()
            if open_price_text:
                try:
                    position['open_price'] = float(open_price_text)
                except:
                    position['open_price'] = 0.0
            
            # Extract close time (column 8)
            close_time_text = cells[8].get_text().strip()
            position['close_time'] = self._parse_datetime(close_time_text)
            
            # Extract close price (column 9)
            close_price_text = cells[9].get_text().strip()
            if close_price_text:
                try:
                    position['close_price'] = float(close_price_text)
                except:
                    position['close_price'] = 0.0
            
            # Extract commission (column 10)
            commission_text = cells[10].get_text().strip()
            position['commission'] = self._parse_numeric_value(commission_text)
            
            # Extract swap (column 11)
            swap_text = cells[11].get_text().strip()
            position['swap'] = self._parse_numeric_value(swap_text)
            
            # Extract profit (last column, often has colspan="2")
            # In live reports, profit is typically the last column and spans 2 columns
            profit_text = ""
            
            # Try to find the profit in the last few columns
            for i in range(len(cells) - 1, max(len(cells) - 4, 11), -1):
                if i < len(cells):
                    cell_text = cells[i].get_text().strip()
                    # Check if this looks like a profit value (has numbers and possibly negative)
                    if cell_text and (cell_text.replace('.', '').replace('-', '').replace(' ', '').isdigit() or 
                                    any(char.isdigit() for char in cell_text)):
                        profit_text = cell_text
                        break
            
            position['profit'] = self._parse_numeric_value(profit_text)
            
            # Calculate trade duration
            if position['open_time'] and position['close_time']:
                duration = position['close_time'] - position['open_time']
                position['duration_minutes'] = duration.total_seconds() / 60
            
            # Use close time as the main time for analysis
            position['time'] = position['close_time'] if position['close_time'] else position['open_time']
            
            return position
            
        except Exception as e:
            print(f"Error parsing position row: {e}")
            return None
    
    def _extract_deals_table(self, soup):
        """Extract individual deals from the Deals section"""
        deals = []
        
        try:
            # Find the Deals section
            deals_found = False
            all_rows = soup.find_all('tr')
            
            for i, row in enumerate(all_rows):
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
                            
                            # Stop if we hit another section or summary
                            if data_row.find('th') or 'Balance:' in data_row.get_text():
                                break
                                
                            cells = data_row.find_all('td')
                            if len(cells) >= 10:  # Minimum expected columns
                                deal_data = self._parse_live_deal_row(cells)
                                if deal_data:
                                    deals.append(deal_data)
                    break
            
            if deals:
                df = pd.DataFrame(deals)
                df = self._clean_deals_dataframe(df)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error extracting deals: {e}")
            return pd.DataFrame()
    
    def _parse_live_deal_row(self, cells):
        """Parse individual deal row from live trading report"""
        try:
            # Deal structure: Time, Deal, Symbol, Type, Direction, Volume, Price, Order, Commission, Fee, Swap, Profit, Balance, Comment
            if len(cells) < 12:
                return None
            
            deal = {}
            
            # Extract time (column 0)
            time_text = cells[0].get_text().strip()
            deal['time'] = self._parse_datetime(time_text)
            
            if not deal['time']:
                return None
            
            # Extract deal ID (column 1)
            deal['deal_id'] = cells[1].get_text().strip()
            
            # Extract symbol (column 2)
            deal['symbol'] = cells[2].get_text().strip()
            
            # Extract type (column 3)
            deal['type'] = cells[3].get_text().strip().lower()
            
            # Skip balance entries
            if deal['type'] == 'balance':
                # Extract balance amount for balance tracking
                balance_text = cells[-2].get_text().strip()  # Balance is usually second to last
                deal['balance'] = self._parse_numeric_value(balance_text)
                deal['is_balance_entry'] = True
                return deal
            
            # Extract direction (column 4)
            deal['direction'] = cells[4].get_text().strip().lower()
            
            # Extract volume (column 5)
            volume_text = cells[5].get_text().strip()
            if volume_text:
                try:
                    deal['volume'] = float(volume_text)
                except:
                    deal['volume'] = 0.0
            
            # Extract price (column 6)
            price_text = cells[6].get_text().strip()
            if price_text:
                try:
                    deal['price'] = float(price_text)
                except:
                    deal['price'] = 0.0
            
            # Extract order ID (column 7)
            deal['order_id'] = cells[7].get_text().strip()
            
            # Extract commission (column 9)
            commission_text = cells[9].get_text().strip()
            deal['commission'] = self._parse_numeric_value(commission_text)
            
            # Extract fee (column 10)
            fee_text = cells[10].get_text().strip()
            deal['fee'] = self._parse_numeric_value(fee_text)
            
            # Extract swap (column 11)
            swap_text = cells[11].get_text().strip()
            deal['swap'] = self._parse_numeric_value(swap_text)
            
            # Extract profit (column 12)
            profit_text = cells[12].get_text().strip()
            deal['profit'] = self._parse_numeric_value(profit_text)
            
            # Extract balance (column 13)
            balance_text = cells[13].get_text().strip()
            deal['balance'] = self._parse_numeric_value(balance_text)
            
            # Extract comment (column 14)
            if len(cells) > 14:
                deal['comment'] = cells[14].get_text().strip()
            
            deal['is_balance_entry'] = False
            
            return deal
            
        except Exception as e:
            print(f"Error parsing deal row: {e}")
            return None
    
    def _extract_live_summary_stats(self, soup):
        """Extract summary statistics from live trading report"""
        summary = {}
        
        try:
            # Get all text content
            text = soup.get_text()
            
            # Also get the raw HTML for patterns that need HTML tags
            html_content = str(soup)
            
            # Live trading specific patterns
            patterns = {
                # Account Balance Info
                'final_balance': r'Balance:\s*([0-9\s,]+\.?\d*)',
                
                # Profit/Loss Metrics
                'total_net_profit': r'Total Net Profit:\s*([+-]?[0-9\s,]+\.?\d*)',
                'gross_profit': r'Gross Profit:\s*([+-]?[0-9\s,]+\.?\d*)',
                'gross_loss': r'Gross Loss:\s*([+-]?[0-9\s,]+\.?\d*)',
                
                # Performance Ratios
                'profit_factor': r'Profit Factor:\s*([+-]?[\d.]+)',
                'expected_payoff': r'Expected Payoff:\s*([+-]?[\d.]+)',
                'recovery_factor': r'Recovery Factor:\s*([+-]?[\d.]+)',
                'sharpe_ratio': r'Sharpe Ratio:\s*([+-]?[\d.]+)',
                
                # Trade Statistics
                'total_trades': r'Total Trades:\s*([\d\s,]+)',
                'short_trades': r'Short Trades.*?(\d+)',
                'long_trades': r'Long Trades.*?(\d+)',
                'profit_trades': r'Profit Trades.*?(\d+)',
                'loss_trades': r'Loss Trades.*?(\d+)',
                'profit_trades_pct': r'Profit Trades.*?\(([0-9.]+)%\)',
                'loss_trades_pct': r'Loss Trades.*?\(([0-9.]+)%\)',
                
                # Individual Trade Metrics
                'largest_profit_trade': r'Largest profit trade:\s*([+-]?[\d.]+)',
                'largest_loss_trade': r'Largest loss trade:\s*([+-]?[\d.]+)',
                'average_profit_trade': r'Average profit trade:\s*([+-]?[\d.]+)',
                'average_loss_trade': r'Average loss trade:\s*([+-]?[\d.]+)',
                
                # Consecutive Trades
                'max_consecutive_wins': r'Maximum consecutive wins.*?(\d+)',
                'max_consecutive_losses': r'Maximum consecutive losses.*?(\d+)',
                'max_consecutive_wins_profit': r'Maximum consecutive wins.*?\(([+-]?[\d.]+)\)',
                'max_consecutive_losses_loss': r'Maximum consecutive losses.*?\(([+-]?[\d.]+)\)',
                'maximal_consecutive_profit': r'Maximal consecutive profit.*?([+-]?[\d.]+)',
                'maximal_consecutive_loss': r'Maximal consecutive loss.*?([+-]?[\d.]+)',
                'average_consecutive_wins': r'Average consecutive wins:\s*(\d+)',
                'average_consecutive_losses': r'Average consecutive losses:\s*(\d+)',
            }
            
            # HTML-specific patterns that need HTML tags
            html_patterns = {
                'balance_drawdown_maximal': r'Balance Drawdown Maximal:</td>.*?<b>([+-]?[\d\s,.]+\s*\([^)]+\))</b>',
            }
            
            # Extract all metrics from text
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    value = match.group(1).strip()
                    
                    # Clean and convert values
                    if key in ['final_balance', 'total_net_profit', 'gross_profit', 'gross_loss',
                              'balance_drawdown_absolute', 'largest_profit_trade', 'largest_loss_trade',
                              'average_profit_trade', 'average_loss_trade', 'maximal_consecutive_profit',
                              'maximal_consecutive_loss']:
                        # Remove spaces and commas from numbers
                        cleaned_value = re.sub(r'[\s,]', '', value)
                        try:
                            summary[key] = float(cleaned_value)
                        except:
                            summary[key] = value
                    
                    elif key in ['profit_factor', 'expected_payoff', 'recovery_factor', 'sharpe_ratio']:
                        try:
                            summary[key] = float(value)
                        except:
                            summary[key] = value
                    
                    elif key in ['total_trades', 'short_trades', 'long_trades', 'profit_trades', 
                               'loss_trades', 'max_consecutive_wins', 'max_consecutive_losses',
                               'average_consecutive_wins', 'average_consecutive_losses']:
                        try:
                            summary[key] = int(value)
                        except:
                            summary[key] = value
                    
                    elif key in ['profit_trades_pct', 'loss_trades_pct']:
                        try:
                            summary[key] = float(value)
                        except:
                            summary[key] = value
                    
                    else:
                        # Keep as string for other values
                        summary[key] = value
            
            # Extract HTML-specific patterns
            for key, pattern in html_patterns.items():
                match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
                if match:
                    value = match.group(1).strip()
                    
                    if key == 'balance_drawdown_maximal':
                        # Extract just the dollar amount from "1 604.73 (5.98%)"
                        dollar_match = re.search(r'([+-]?[\d\s,.]+)', value)
                        if dollar_match:
                            cleaned_value = re.sub(r'[\s,]', '', dollar_match.group(1))
                            try:
                                summary[key] = f"${float(cleaned_value):,.2f}"
                            except:
                                summary[key] = value
                        else:
                            summary[key] = value
            
        except Exception as e:
            print(f"Error extracting summary stats: {e}")
        
        return summary
    
    def _parse_datetime(self, time_str):
        """Parse datetime from various MT5 formats"""
        time_str = time_str.strip()
        
        # Common MT5 datetime formats
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
    
    def _parse_numeric_value(self, value_str):
        """Parse numeric value from string, handling various formats"""
        try:
            if not value_str or value_str.strip() == '':
                return 0.0
            
            # Handle different formats like "999 999 999.00", "-20.83", etc.
            cleaned = value_str.replace(' ', '').replace(',', '')
            
            # Remove currency symbols but keep +/- signs and decimals
            cleaned = re.sub(r'[^\d.+-]', '', cleaned)
            
            if cleaned and cleaned not in ['+', '-', '.']:
                return float(cleaned)
            return 0.0
        except:
            return 0.0
    
    def _clean_positions_dataframe(self, df):
        """Clean and prepare positions dataframe"""
        if df.empty:
            return df
        
        # Ensure required columns exist
        required_cols = ['time', 'profit', 'type', 'symbol']
        for col in required_cols:
            if col not in df.columns:
                if col == 'time':
                    df[col] = pd.NaT
                else:
                    df[col] = None
        
        # Remove rows with invalid data
        df = df.dropna(subset=['time', 'profit'])
        
        # Convert time to datetime
        df['time'] = pd.to_datetime(df['time'])
        
        # Sort by time
        df = df.sort_values('time').reset_index(drop=True)
        
        return df
    
    def _clean_deals_dataframe(self, df):
        """Clean and prepare deals dataframe"""
        if df.empty:
            return df
        
        # Ensure required columns exist
        required_cols = ['time', 'balance']
        for col in required_cols:
            if col not in df.columns:
                if col == 'time':
                    df[col] = pd.NaT
                else:
                    df[col] = 0.0
        
        # Remove rows with invalid data
        df = df.dropna(subset=['time'])
        
        # Convert time to datetime
        df['time'] = pd.to_datetime(df['time'])
        
        # Sort by time
        df = df.sort_values('time').reset_index(drop=True)
        
        return df


def parse_live_report(uploaded_file):
    """Helper function to parse uploaded live trading report"""
    parser = LiveTradeParser()
    
    # Determine file type from name
    file_name = uploaded_file.name.lower()
    is_html = file_name.endswith(('.html', '.htm'))
    
    try:
        if is_html:
            # Parse HTML file
            temp_file = "temp_live_report.html"
            try:
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                positions_df, deals_df, summary_dict, account_info = parser.parse_live_html_report(temp_file)
                
            finally:
                # Clean up temp file
                import os
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        else:
            raise Exception("Unsupported file format. Please upload HTML files from live MT5 account.")
        
        # Ensure the DataFrames have required columns
        if not positions_df.empty and 'time' in positions_df.columns:
            # Make sure time is datetime
            if not pd.api.types.is_datetime64_any_dtype(positions_df['time']):
                positions_df['time'] = pd.to_datetime(positions_df['time'])
        
        if not deals_df.empty and 'time' in deals_df.columns:
            # Make sure time is datetime
            if not pd.api.types.is_datetime64_any_dtype(deals_df['time']):
                deals_df['time'] = pd.to_datetime(deals_df['time'])
        
        return positions_df, deals_df, summary_dict, account_info
        
    except Exception as e:
        raise Exception(f"Error parsing live report {file_name}: {str(e)}")