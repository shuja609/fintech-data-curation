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
            },
            'additional_rss_feeds': {
                'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
                'reuters_business': 'https://feeds.reuters.com/reuters/businessNews',
                'reuters_markets': 'https://feeds.reuters.com/news/artsculture',
                'bloomberg_markets': 'https://feeds.bloomberg.com/markets/news.rss',
                'cnbc_finance': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664',
                'seeking_alpha': 'https://seekingalpha.com/feed.xml',
                'benzinga': 'https://www.benzinga.com/feed',
                'crypto_news': 'https://cointelegraph.com/rss',
                'fintech_news': 'https://www.fintechnews.org/feed/',
                'nasdaq_news': 'https://www.nasdaq.com/feed/rssoutbound',
                'financial_times': 'https://www.ft.com/rss/home',
                # Phase 1 Enhancement: Regulatory and Government RSS feeds
                'sec_press_releases': 'https://www.sec.gov/news/pressreleases.rss',
                'fed_press_releases': 'https://www.federalreserve.gov/feeds/press_all.xml',
                'treasury_press': 'https://home.treasury.gov/rss/press-releases',
                'cftc_press': 'https://www.cftc.gov/rss/PressReleases',
                'finra_news': 'https://www.finra.org/rss'
            }
        }
        
        # Technical indicators to calculate
        self.technical_indicators = {
            'moving_averages': [5, 10, 20],  # days
            'volatility_window': 10,  # days
            'rsi_period': 14,  # days
            'bollinger_period': 20,  # days
            'bollinger_std': 2,  # standard deviations
            # Phase 1 Enhancement: Advanced technical indicators
            'macd_fast': 12,  # MACD fast period
            'macd_slow': 26,  # MACD slow period 
            'macd_signal': 9,  # MACD signal period
            'stoch_k_period': 14,  # Stochastic %K period
            'stoch_d_period': 3,  # Stochastic %D period
            'williams_r_period': 14  # Williams %R period
        }
        
        # Feature selection settings
        self.features = {
            'structured': [
                'open', 'high', 'low', 'close', 'volume',
                'daily_return', 'volatility',
                'ma_5', 'ma_10', 'ma_20',
                'rsi', 'bollinger_upper', 'bollinger_lower',
                # Phase 1 Enhancement: Advanced technical indicators
                'macd', 'macd_signal', 'macd_histogram',
                'stoch_k', 'stoch_d', 'williams_r',
                # Phase 1 Enhancement: Market-wide indicators
                'vix', 'dxy', 'treasury_10y', 'sp500_correlation'
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
            'max_articles_per_day': 15,
            'min_headline_length': 10,
            'relevant_keywords': [
                'stock', 'market', 'trading', 'price', 'earnings',
                'revenue', 'profit', 'loss', 'shares', 'investment',
                'crypto', 'bitcoin', 'cryptocurrency', 'blockchain',
                'financial', 'finance', 'economy', 'economic',
                'nasdaq', 'nyse', 'exchange', 'securities',
                'dividend', 'acquisition', 'merger', 'ipo',
                'analyst', 'rating', 'upgrade', 'downgrade',
                'quarterly', 'annual', 'results', 'guidance',
                'federal reserve', 'fed', 'interest rate', 'inflation',
                # Phase 1 Enhancement: Regulatory keywords
                'sec', 'securities commission', 'regulatory', 'compliance',
                'treasury', 'cftc', 'finra', 'government', 'policy'
            ]
        }
        
        # Exchange mappings
        self.exchanges = {
            'NYSE': {'suffix': '', 'market': 'US'},
            'NASDAQ': {'suffix': '', 'market': 'US'},
            'PSX': {'suffix': '.KHI', 'market': 'PK'},
            'CRYPTO': {'suffix': '', 'market': 'CRYPTO'}
        }
        
        # Phase 1 Enhancement: Market-wide indicators configuration
        self.market_indicators = {
            'vix': '^VIX',  # CBOE Volatility Index
            'dxy': 'DX-Y.NYB',  # US Dollar Index
            'treasury_10y': '^TNX',  # 10-Year Treasury Note Yield
            'sp500': '^GSPC',  # S&P 500 Index
            'nasdaq': '^IXIC',  # NASDAQ Composite
            'dow_jones': '^DJI',  # Dow Jones Industrial Average
            'russell_2000': '^RUT'  # Russell 2000 Index
        }
        
        # Phase 1 Enhancement: Data validation settings
        self.data_validation = {
            'outlier_method': 'iqr',  # 'iqr' or 'zscore'
            'iqr_multiplier': 1.5,  # IQR multiplier for outlier detection
            'zscore_threshold': 3,  # Z-score threshold for outlier detection
            'min_data_points': 5,  # Minimum data points required
            'max_missing_percentage': 20  # Maximum percentage of missing data allowed
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