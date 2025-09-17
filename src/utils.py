"""
Utility functions for FinTech Data Curator
"""

import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_logging(level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('fintech_collector.log')
        ]
    )
    return logging.getLogger(__name__)

def create_robust_session(retries: int = 3, backoff_factor: float = 0.3) -> requests.Session:
    """Create a robust HTTP session with retry logic."""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],  # Updated method name
        backoff_factor=backoff_factor
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def safe_request(url: str, headers: Dict[str, str], timeout: int = 30, 
                max_retries: int = 3) -> Optional[requests.Response]:
    """Make a safe HTTP request with error handling and retries."""
    session = create_robust_session(retries=max_retries)
    
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"All {max_retries} attempts failed for {url}")
                
    return None

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = " ".join(text.split())
    
    # Remove special characters that might cause CSV issues
    text = text.replace('"', "'").replace('\n', ' ').replace('\r', ' ')
    
    return text.strip()

def validate_symbol(symbol: str) -> bool:
    """Validate stock/crypto symbol format."""
    if not symbol or len(symbol.strip()) == 0:
        return False
    
    # Basic validation - alphanumeric and common separators
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    return all(c in allowed_chars for c in symbol.upper())

def validate_exchange(exchange: str) -> bool:
    """Validate exchange name."""
    valid_exchanges = {'NYSE', 'NASDAQ', 'PSX', 'CRYPTO'}
    return exchange.upper() in valid_exchanges

def calculate_relevance_score(headline: str, symbol: str) -> float:
    """Calculate relevance score of news headline to symbol."""
    if not headline or not symbol:
        return 0.0
    
    headline_lower = headline.lower()
    symbol_lower = symbol.replace('-USD', '').lower()
    
    # Direct symbol mention
    if symbol_lower in headline_lower:
        return 0.9
    
    # Company name mapping (simplified)
    company_names = {
        'aapl': ['apple', 'iphone', 'ipad', 'mac', 'tim cook'],
        'googl': ['google', 'alphabet', 'android', 'youtube', 'chrome'],
        'msft': ['microsoft', 'windows', 'office', 'azure', 'teams'],
        'amzn': ['amazon', 'aws', 'prime', 'bezos'],
        'tsla': ['tesla', 'elon musk', 'electric vehicle', 'ev'],
        'meta': ['facebook', 'instagram', 'whatsapp', 'metaverse'],
        'nflx': ['netflix', 'streaming'],
        'nvda': ['nvidia', 'gpu', 'ai chip'],
        'btc': ['bitcoin', 'btc', 'cryptocurrency'],
        'eth': ['ethereum', 'eth', 'smart contract']
    }
    
    if symbol_lower in company_names:
        for term in company_names[symbol_lower]:
            if term in headline_lower:
                return 0.8
    
    # Sector-specific keywords for better relevance
    tech_keywords = ['technology', 'tech', 'software', 'digital', 'ai', 'artificial intelligence']
    finance_keywords = ['bank', 'financial', 'credit', 'loan', 'payment']
    market_keywords = ['stock', 'market', 'shares', 'trading', 'investment', 'earnings', 'revenue', 'profit']
    
    # Higher relevance for market-related news
    for keyword in market_keywords:
        if keyword in headline_lower:
            return 0.6
    
    # Medium relevance for sector news
    for keyword in tech_keywords + finance_keywords:
        if keyword in headline_lower:
            return 0.4
    
    # General financial news
    general_keywords = ['economy', 'economic', 'business', 'corporate', 'industry']
    for keyword in general_keywords:
        if keyword in headline_lower:
            return 0.3
    
    return 0.1  # Very low but not zero relevance for any news

def format_currency(value: float, currency: str = 'USD') -> str:
    """Format currency values consistently."""
    if currency == 'USD':
        return f"${value:.2f}"
    return f"{value:.2f} {currency}"

def get_trading_days_back(days: int) -> List[datetime]:
    """Get list of trading days going back from today."""
    from datetime import timedelta
    
    trading_days = []
    current_date = datetime.now()
    days_collected = 0
    
    while days_collected < days:
        # Skip weekends (0=Monday, 6=Sunday)
        if current_date.weekday() < 5:  # Monday to Friday
            trading_days.append(current_date)
            days_collected += 1
        current_date -= timedelta(days=1)
    
    return list(reversed(trading_days))

def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def rate_limit(delay: float = 1.0):
    """Simple rate limiting decorator."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator