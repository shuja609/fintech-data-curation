"""
Structured data collection for FinTech Data Curator
Handles OHLCV data and technical indicators
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from .utils import safe_float, setup_logging

class StructuredDataCollector:
    """Collector for structured financial data (OHLCV + technical indicators)."""
    
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging()
    
    def collect_price_data(self, symbol: str, exchange: str, days: int) -> pd.DataFrame:
        """Collect historical price data for a symbol."""
        try:
            # Format symbol for yfinance
            formatted_symbol = self.config.get_symbol_with_suffix(symbol, exchange)
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)  # Extra buffer for MA calculations
            
            self.logger.info(f"Fetching price data for {formatted_symbol}")
            
            # Fetch data using yfinance
            ticker = yf.Ticker(formatted_symbol)
            price_data = ticker.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval='1d'
            )
            
            if price_data.empty:
                raise ValueError(f"No price data found for {formatted_symbol}")
            
            # Rename columns to lowercase
            price_data.columns = [col.lower() for col in price_data.columns]
            
            # Reset index to make date a column
            price_data.reset_index(inplace=True)
            
            # Ensure the date column is properly named
            if 'Date' in price_data.columns:
                price_data.rename(columns={'Date': 'date'}, inplace=True)
            elif price_data.index.name == 'Date':
                price_data.reset_index(inplace=True)
                price_data.rename(columns={'Date': 'date'}, inplace=True)
            
            # Convert date to proper format
            if 'date' in price_data.columns:
                price_data['date'] = pd.to_datetime(price_data['date']).dt.date
            else:
                # If no date column exists, use the index
                price_data['date'] = pd.to_datetime(price_data.index).date
            
            self.logger.info(f"Collected {len(price_data)} days of price data")
            return price_data
            
        except Exception as e:
            self.logger.error(f"Error collecting price data for {symbol}: {e}")
            raise
    
    def calculate_technical_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for the price data."""
        try:
            df = price_data.copy()
            
            # Daily returns
            df['daily_return'] = df['close'].pct_change()
            
            # Volatility (10-day rolling standard deviation of returns)
            volatility_window = self.config.technical_indicators['volatility_window']
            df['volatility'] = df['daily_return'].rolling(window=volatility_window).std()
            
            # Moving averages
            for ma_period in self.config.technical_indicators['moving_averages']:
                df[f'ma_{ma_period}'] = df['close'].rolling(window=ma_period).mean()
            
            # RSI (Relative Strength Index)
            rsi_period = self.config.technical_indicators['rsi_period']
            df['rsi'] = self._calculate_rsi(df['close'], rsi_period)
            
            # Bollinger Bands
            bb_period = self.config.technical_indicators['bollinger_period']
            bb_std = self.config.technical_indicators['bollinger_std']
            df['bollinger_upper'], df['bollinger_lower'] = self._calculate_bollinger_bands(
                df['close'], bb_period, bb_std
            )
            
            self.logger.info("Technical indicators calculated successfully")
            return df
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {e}")
            raise
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception:
            # Return series of NaN if calculation fails
            return pd.Series([np.nan] * len(prices), index=prices.index)
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, 
                                 std_dev: float = 2) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands."""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return upper_band, lower_band
            
        except Exception:
            # Return series of NaN if calculation fails
            nan_series = pd.Series([np.nan] * len(prices), index=prices.index)
            return nan_series, nan_series
    
    def get_latest_data(self, symbol: str, exchange: str, days: int) -> pd.DataFrame:
        """Get the latest structured data with specified number of days."""
        try:
            # Collect raw price data
            price_data = self.collect_price_data(symbol, exchange, days)
            
            # Calculate technical indicators
            enhanced_data = self.calculate_technical_indicators(price_data)
            
            # Get only the most recent 'days' worth of data
            latest_data = enhanced_data.tail(days).copy()
            
            # Select only the configured features
            feature_columns = ['date'] + self.config.features['structured']
            available_columns = [col for col in feature_columns if col in latest_data.columns]
            
            result = latest_data[available_columns].copy()
            
            # Round numerical values for cleaner output
            numeric_columns = result.select_dtypes(include=[np.number]).columns
            result[numeric_columns] = result[numeric_columns].round(4)
            
            # Fill NaN values with appropriate defaults
            result = result.fillna(0)
            
            self.logger.info(f"Prepared {len(result)} days of structured data")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting latest structured data: {e}")
            raise
    
    def validate_data_quality(self, data: pd.DataFrame) -> Dict[str, any]:
        """Validate the quality of collected structured data."""
        quality_report = {
            'total_records': len(data),
            'missing_values': data.isnull().sum().to_dict(),
            'date_range': {
                'start': data['date'].min() if not data.empty else None,
                'end': data['date'].max() if not data.empty else None
            },
            'price_range': {
                'min_close': safe_float(data['close'].min()) if 'close' in data.columns else None,
                'max_close': safe_float(data['close'].max()) if 'close' in data.columns else None
            },
            'data_completeness': (1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
        }
        
        return quality_report