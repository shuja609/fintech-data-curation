"""
Configuration management for FinTech Data Curator
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List

class Config:
    """Configuration class for managing application settings."""
    
    def __init__(self):
        self.setup_default_config()
    
    def setup_default_config(self):
        """Set up default configuration values."""
        
        # Data source URLs and settings
        self.data_sources = {
            'yahoo_finance': {
                'base_url': 'https://finance.yahoo.com',
                'news_url': 'https://finance.yahoo.com/news/',
                'timeout': 30,
                'retry_count': 3
            },
            'yahoo_api': {
                'enabled': True,
                'timeout': 30
            },
            'coindesk': {
                'base_url': 'https://www.coindesk.com',
                'rss_url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'timeout': 30
            }
        }
        
        # Technical indicators to calculate
        self.technical_indicators = {
            'moving_averages': [5, 10, 20],  # days
            'volatility_window': 10,  # days
            'rsi_period': 14,  # days
            'bollinger_period': 20,  # days
            'bollinger_std': 2  # standard deviations
        }
        
        # Feature selection settings
        self.features = {
            'structured': [
                'open', 'high', 'low', 'close', 'volume',
                'daily_return', 'volatility',
                'ma_5', 'ma_10', 'ma_20',
                'rsi', 'bollinger_upper', 'bollinger_lower'
            ],
            'unstructured': [
                'news_headline', 'news_summary', 'news_sentiment',
                'news_source', 'news_relevance'
            ]
        }
        
        # Output settings
        self.output = {
            'csv_separator': ',',
            'json_indent': 2,
            'date_format': '%Y-%m-%d',
            'timestamp_format': '%Y-%m-%d %H:%M:%S'
        }
        
        # Web scraping settings
        self.scraping = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'delay_between_requests': 1,  # seconds
            'max_retries': 3,
            'timeout': 30
        }
        
        # News filtering settings
        self.news_filters = {
            'max_articles_per_day': 10,
            'min_headline_length': 10,
            'relevant_keywords': [
                'stock', 'market', 'trading', 'price', 'earnings',
                'revenue', 'profit', 'loss', 'shares', 'investment',
                'crypto', 'bitcoin', 'cryptocurrency', 'blockchain'
            ]
        }
        
        # Exchange mappings
        self.exchanges = {
            'NYSE': {'suffix': '', 'market': 'US'},
            'NASDAQ': {'suffix': '', 'market': 'US'},
            'PSX': {'suffix': '.KHI', 'market': 'PK'},
            'CRYPTO': {'suffix': '', 'market': 'CRYPTO'}
        }
    
    def get_symbol_with_suffix(self, symbol: str, exchange: str) -> str:
        """Get symbol with appropriate suffix for the exchange."""
        if exchange in self.exchanges:
            suffix = self.exchanges[exchange]['suffix']
            return f"{symbol}{suffix}" if suffix else symbol
        return symbol
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for web scraping."""
        return {
            'User-Agent': self.scraping['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_date_range(self, days: int) -> tuple:
        """Get start and end dates for data collection."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date