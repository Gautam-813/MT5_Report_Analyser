"""
Trade Account History Parser
Parses real MT5 account trading history reports (not backtester reports)
"""

import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np

class TradeHistoryParser:
    def __init__(self):
        self.trades_data = None
        self.summary_data = None
        
    def parse_trade_history_report(self, file_path_or_content):
        """Parse MT5 trade history report and extract trade data"""
        try:
            # Handle both file path and uploaded file content
            if hasattr(file_path_or_content, 'getvalue'):
                # It's an uploaded file
                content = file_path_or_content.getvalue().decode('utf-8', errors='ignore')
            else:
                # It's a file path
                encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path_or_content, 'r', encoding=encoding) as file:
                            content = file.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    raise Exception("Could not decode file with any supported encoding")
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract trades from Positions section (completed trades)
            trades_df = self._extract_positions_table(soup)
            
            # Extract summary statistics
            summary_dict = self._extract_summary_stats(soup)
            
            return trades_df, summary_dict
            
        except Exception as e:
            raise Exception(f"Error parsing trade history report: {str(e)}")
    
    def _extract_positions_table(self, soup):
        """Extract completed trades from the Positions section"""
        trades = []
        
        # Look for the "Positions" section specifically
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
                if len(header_cells) >= 12:  # Expected number of columns for positions
                    # Process subsequent data rows
                    for j in range(i + 1, len(all_rows)):
                        data_row = all_rows[j]
                        
                        # Stop if we hit another section (like "Deals")
                        if data_row.find('th') or data_row.get('colspan'):
                            break
                            
                        cells = data_row.find_all('td')
                        if len(cells) >= 12:  # Minimum expected columns
                            trade_data = self._parse_position_row(cells)
                            if trade_data:
                                trades.append(trade_data)
                break
        
        if trades:
            df = pd.DataFrame(trades)
            df = self._clean_trades_dataframe(df)
            return df
        else:
            return pd.DataFrame()
    
    def _parse_position_row(self, cells):
        """Parse individual position row from trade history"""
        try:
            # Trade History Position structure (accounting for hidden columns and colspan):
            # Time, Position, Symbol, Type, [hidden columns], Volume, Price, S/L, T/P, Time, Price, Commission, Swap, Profit
            
            # Filter out hidden cells and handle colspan
            visible_cells = []
            for cell in cells:
                if not cell.get('class') or 'hidden' not in cell.get('class', []):
                    visible_cells.append(cell)
            
            if len(visible_cells) < 10:  # Minimum expected visible columns
                return None
            
            trade = {}
            
            # Extract entry time (column 0)
            entry_time_text = visible_cells[0].get_text().strip()
            trade['time'] = self._parse_datetime(entry_time_text)
            
            if not trade['time']:
                return None
            
            # Extract position ID (column 1)
            trade['position_id'] = visible_cells[1].get_text().strip()
            
            # Extract symbol (column 2)
            trade['symbol'] = visible_cells[2].get_text().strip()
            
            # Extract type (column 3)
            trade['type'] = visible_cells[3].get_text().strip().lower()
            
            # Extract volume (column 4)
            volume_text = visible_cells[4].get_text().strip()
            if volume_text:
                try:
                    trade['volume'] = float(volume_text)
                except:
                    trade['volume'] = 0.0
            
            # Extract entry price (column 5)
            entry_price_text = visible_cells[5].get_text().strip()
            if entry_price_text:
                try:
                    trade['entry_price'] = float(entry_price_text)
                except:
                    trade['entry_price'] = 0.0
            
            # Skip S/L and T/P columns (6, 7)
            
            # Extract exit time (column 8)
            if len(visible_cells) > 8:
                exit_time_text = visible_cells[8].get_text().strip()
                if exit_time_text:
                    trade['exit_time'] = self._parse_datetime(exit_time_text)
            
            # Extract exit price (column 9)
            if len(visible_cells) > 9:
                exit_price_text = visible_cells[9].get_text().strip()
                if exit_price_text:
                    try:
                        trade['exit_price'] = float(exit_price_text)
                    except:
                        trade['exit_price'] = 0.0
            
            # Extract commission (column 10)
            if len(visible_cells) > 10:
                commission_text = visible_cells[10].get_text().strip()
                if commission_text:
                    try:
                        trade['commission'] = float(commission_text)
                    except:
                        trade['commission'] = 0.0
            
            # Extract swap (column 11)
            if len(visible_cells) > 11:
                swap_text = visible_cells[11].get_text().strip()
                if swap_text:
                    try:
                        trade['swap'] = float(swap_text)
                    except:
                        trade['swap'] = 0.0
            
            # Extract profit (last column, may have colspan)
            profit_text = ""
            if len(visible_cells) > 12:
                profit_text = visible_cells[12].get_text().strip()
            elif len(visible_cells) > 11:
                # Check if the last cell contains profit data
                last_cell_text = visible_cells[-1].get_text().strip()
                if self._is_numeric_value(last_cell_text):
                    profit_text = last_cell_text
            
            trade['profit'] = self._parse_profit(profit_text)
            
            # Only return trades with actual profit/loss data or complete entry/exit info
            if trade['profit'] != 0.0 or (trade.get('exit_time') and trade.get('exit_price')):
                return trade
            
            return None
            
        except Exception as e:
            print(f"Error parsing position row: {e}")
            return None
    
    def _extract_summary_stats(self, soup):
        """Extract summary statistics from the Results section"""
        summary = {}
        
        try:
            # Look for the "Results" section
            all_rows = soup.find_all('tr')
            
            for row in all_rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # Extract key-value pairs from the results section
                    for i in range(0, len(cells) - 1, 2):
                        key_cell = cells[i]
                        value_cell = cells[i + 1]
                        
                        if key_cell and value_cell:
                            key = key_cell.get_text().strip().lower().replace(':', '')
                            value = value_cell.get_text().strip()
                            
                            # Map common statistics
                            if 'total net profit' in key:
                                summary['total_net_profit'] = self._parse_numeric_value(value)
                            elif 'gross profit' in key:
                                summary['gross_profit'] = self._parse_numeric_value(value)
                            elif 'gross loss' in key:
                                summary['gross_loss'] = self._parse_numeric_value(value)
                            elif 'profit factor' in key:
                                summary['profit_factor'] = self._parse_numeric_value(value)
                            elif 'expected payoff' in key:
                                summary['expected_payoff'] = self._parse_numeric_value(value)
                            elif 'recovery factor' in key:
                                summary['recovery_factor'] = self._parse_numeric_value(value)
                            elif 'sharpe ratio' in key:
                                summary['sharpe_ratio'] = self._parse_numeric_value(value)
                            elif 'total trades' in key:
                                summary['total_trades'] = self._parse_integer_value(value)
                            elif 'profit trades' in key and 'total' in key:
                                # Extract both count and percentage
                                match = re.search(r'(\d+)\s*\(([0-9.]+)%\)', value)
                                if match:
                                    summary['profit_trades'] = int(match.group(1))
                                    summary['win_rate'] = float(match.group(2))
                            elif 'loss trades' in key and 'total' in key:
                                match = re.search(r'(\d+)\s*\(([0-9.]+)%\)', value)
                                if match:
                                    summary['loss_trades'] = int(match.group(1))
                            elif 'largest profit trade' in key:
                                summary['largest_profit'] = self._parse_numeric_value(value)
                            elif 'largest loss trade' in key:
                                summary['largest_loss'] = self._parse_numeric_value(value)
                            elif 'average profit trade' in key:
                                summary['average_profit'] = self._parse_numeric_value(value)
                            elif 'average loss trade' in key:
                                summary['average_loss'] = self._parse_numeric_value(value)
                            elif 'maximum consecutive wins' in key:
                                # Extract count and amount
                                match = re.search(r'(\d+)\s*\(([0-9.-]+)\)', value)
                                if match:
                                    summary['max_consecutive_wins'] = int(match.group(1))
                                    summary['max_consecutive_wins_amount'] = float(match.group(2))
                            elif 'maximum consecutive losses' in key:
                                match = re.search(r'(\d+)\s*\(([0-9.-]+)\)', value)
                                if match:
                                    summary['max_consecutive_losses'] = int(match.group(1))
                                    summary['max_consecutive_losses_amount'] = float(match.group(2))
                            elif 'balance drawdown maximal' in key:
                                # Extract both absolute and percentage
                                match = re.search(r'([0-9.-]+)\s*\(([0-9.]+)%\)', value)
                                if match:
                                    summary['max_drawdown_absolute'] = float(match.group(1))
                                    summary['max_drawdown_percent'] = float(match.group(2))
            
            return summary
            
        except Exception as e:
            print(f"Error extracting summary stats: {e}")
            return {}
    
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
    
    def _parse_profit(self, profit_str):
        """Parse profit/loss value from text"""
        if not profit_str:
            return 0.0
        
        # Remove currency symbols and spaces
        profit_str = re.sub(r'[^\d.-]', '', profit_str.strip())
        
        try:
            return float(profit_str)
        except ValueError:
            return 0.0
    
    def _parse_numeric_value(self, value_str):
        """Parse numeric value from text"""
        if not value_str:
            return 0.0
        
        # Remove currency symbols, spaces, and extract numeric value
        value_str = re.sub(r'[^\d.-]', '', value_str.strip())
        
        try:
            return float(value_str)
        except ValueError:
            return 0.0
    
    def _parse_integer_value(self, value_str):
        """Parse integer value from text"""
        if not value_str:
            return 0
        
        # Extract first number found
        match = re.search(r'\d+', value_str)
        if match:
            return int(match.group())
        
        return 0
    
    def _is_numeric_value(self, value_str):
        """Check if a string contains a numeric value"""
        if not value_str:
            return False
        
        # Remove currency symbols and spaces
        cleaned = re.sub(r'[^\d.-]', '', value_str.strip())
        
        try:
            float(cleaned)
            return True
        except ValueError:
            return False
    
    def _clean_trades_dataframe(self, df):
        """Clean and standardize the trades dataframe"""
        if df.empty:
            return df
        
        try:
            # Ensure required columns exist
            required_columns = ['time', 'type', 'profit', 'volume', 'symbol']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'time':
                        df[col] = pd.NaT
                    elif col in ['profit', 'volume']:
                        df[col] = 0.0
                    else:
                        df[col] = ''
            
            # Convert data types
            df['time'] = pd.to_datetime(df['time'], errors='coerce')
            df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0.0)
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna(0.0)
            
            # Remove rows with invalid timestamps
            df = df.dropna(subset=['time'])
            
            # Sort by time
            df = df.sort_values('time').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"Error cleaning trades dataframe: {e}")
            return df

# Convenience function for easy import
def parse_trade_history_report(uploaded_file, progress_callback=None):
    """Parse trade history report with progress callback"""
    try:
        if progress_callback:
            progress_callback("Parsing trade history report...", 10)
        
        parser = TradeHistoryParser()
        
        if progress_callback:
            progress_callback("Extracting trade data...", 50)
        
        trades_df, summary_dict = parser.parse_trade_history_report(uploaded_file)
        
        if progress_callback:
            progress_callback("Cleaning and validating data...", 90)
        
        return trades_df, summary_dict
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", 100)
        raise e
        return 0