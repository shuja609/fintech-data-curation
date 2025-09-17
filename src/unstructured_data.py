"""
Unstructured data collection for FinTech Data Curator
Handles news data and sentiment analysis
"""

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import time
import re
from textblob import TextBlob
from .utils import safe_request, clean_text, calculate_relevance_score, setup_logging

class UnstructuredDataCollector:
    """Collector for unstructured financial data (news, sentiment)."""
    
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging()
    
    def collect_news_data(self, symbol: str, exchange: str, days: int) -> List[Dict]:
        """Collect news data for a symbol from multiple sources."""
        try:
            news_articles = []
            
            # Yahoo Finance News
            yahoo_news = self._get_yahoo_finance_news(symbol, days)
            news_articles.extend(yahoo_news)
            
            # CoinDesk for crypto
            if exchange == 'CRYPTO':
                coindesk_news = self._get_coindesk_news(symbol, days)
                news_articles.extend(coindesk_news)
            
            # Filter and process news
            processed_news = self._process_news_articles(news_articles, symbol, days)
            
            self.logger.info(f"Collected {len(processed_news)} relevant news articles")
            return processed_news
            
        except Exception as e:
            self.logger.error(f"Error collecting news data: {e}")
            return []
    
    def _get_yahoo_finance_news(self, symbol: str, days: int) -> List[Dict]:
        """Get news from Yahoo Finance."""
        try:
            articles = []
            base_url = self.config.data_sources['yahoo_finance']['news_url']
            
            # Search for symbol-related news
            search_url = f"https://finance.yahoo.com/quote/{symbol}/news"
            
            headers = self.config.get_headers()
            response = safe_request(search_url, headers)
            
            if not response:
                return articles
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find news articles (simplified selector - may need adjustment)
            news_items = soup.find_all('div', class_=re.compile('.*news.*|.*article.*'))
            
            for item in news_items[:20]:  # Limit to first 20 items
                try:
                    headline_elem = item.find(['h3', 'h4', 'a'])
                    if headline_elem:
                        headline = clean_text(headline_elem.get_text())
                        
                        if len(headline) >= self.config.news_filters['min_headline_length']:
                            article = {
                                'headline': headline,
                                'summary': headline,  # Use headline as summary for now
                                'source': 'Yahoo Finance',
                                'date': datetime.now().date(),
                                'url': search_url
                            }
                            articles.append(article)
                            
                except Exception as e:
                    self.logger.debug(f"Error parsing Yahoo news item: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching Yahoo Finance news: {e}")
            return []
    
    def _get_coindesk_news(self, symbol: str, days: int) -> List[Dict]:
        """Get cryptocurrency news from CoinDesk RSS feed."""
        try:
            articles = []
            rss_url = self.config.data_sources['coindesk']['rss_url']
            
            # Fetch RSS feed
            feed = feedparser.parse(rss_url)
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for entry in feed.entries[:50]:  # Limit to recent entries
                try:
                    # Parse publication date
                    pub_date = datetime(*entry.published_parsed[:6])
                    
                    if pub_date >= cutoff_date:
                        headline = clean_text(entry.title)
                        summary = clean_text(entry.summary) if hasattr(entry, 'summary') else headline
                        
                        article = {
                            'headline': headline,
                            'summary': summary,
                            'source': 'CoinDesk',
                            'date': pub_date.date(),
                            'url': entry.link if hasattr(entry, 'link') else ''
                        }
                        articles.append(article)
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing CoinDesk RSS entry: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching CoinDesk news: {e}")
            return []
    
    def _process_news_articles(self, articles: List[Dict], symbol: str, days: int) -> List[Dict]:
        """Process and filter news articles."""
        try:
            processed_articles = []
            cutoff_date = datetime.now().date() - timedelta(days=days)
            
            for article in articles:
                try:
                    # Filter by date
                    if article['date'] < cutoff_date:
                        continue
                    
                    # Calculate relevance score
                    relevance = calculate_relevance_score(article['headline'], symbol)
                    
                    # Filter by relevance (keep only relevant articles)
                    if relevance < 0.3:
                        continue
                    
                    # Add sentiment analysis
                    sentiment = self._analyze_sentiment(article['headline'])
                    
                    # Create processed article
                    processed_article = {
                        'headline': article['headline'],
                        'summary': article['summary'],
                        'sentiment': sentiment,
                        'source': article['source'],
                        'relevance': relevance,
                        'date': article['date'],
                        'url': article.get('url', '')
                    }
                    
                    processed_articles.append(processed_article)
                    
                except Exception as e:
                    self.logger.debug(f"Error processing article: {e}")
                    continue
            
            # Sort by date (most recent first) and limit
            processed_articles.sort(key=lambda x: x['date'], reverse=True)
            max_articles = self.config.news_filters['max_articles_per_day'] * days
            
            return processed_articles[:max_articles]
            
        except Exception as e:
            self.logger.error(f"Error processing news articles: {e}")
            return []
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text using TextBlob."""
        try:
            if not text:
                return 0.0
            
            blob = TextBlob(text)
            sentiment_polarity = blob.sentiment.polarity
            
            # Convert from [-1, 1] to [0, 1] scale
            normalized_sentiment = (sentiment_polarity + 1) / 2
            
            return round(normalized_sentiment, 3)
            
        except Exception as e:
            self.logger.debug(f"Error analyzing sentiment: {e}")
            return 0.5  # Neutral sentiment as fallback
    
    def align_news_with_dates(self, news_data: List[Dict], 
                            date_range: List[datetime]) -> Dict[str, List[Dict]]:
        """Align news articles with specific dates."""
        try:
            aligned_news = {}
            
            # Initialize empty lists for each date
            for date in date_range:
                date_str = date.strftime(self.config.output['date_format'])
                aligned_news[date_str] = []
            
            # Group news by date
            for article in news_data:
                article_date = article['date']
                date_str = article_date.strftime(self.config.output['date_format'])
                
                if date_str in aligned_news:
                    aligned_news[date_str].append(article)
            
            return aligned_news
            
        except Exception as e:
            self.logger.error(f"Error aligning news with dates: {e}")
            return {}
    
    def get_representative_news(self, date_news: List[Dict]) -> Dict:
        """Get the most representative news for a given date."""
        try:
            if not date_news:
                return {
                    'headline': 'No relevant news found',
                    'summary': '',
                    'sentiment': 0.5,
                    'source': 'N/A',
                    'relevance': 0.0
                }
            
            # Sort by relevance and pick the best one
            date_news.sort(key=lambda x: x['relevance'], reverse=True)
            best_article = date_news[0]
            
            return {
                'headline': best_article['headline'],
                'summary': best_article['summary'][:200] + '...' if len(best_article['summary']) > 200 else best_article['summary'],
                'sentiment': best_article['sentiment'],
                'source': best_article['source'],
                'relevance': best_article['relevance']
            }
            
        except Exception as e:
            self.logger.error(f"Error getting representative news: {e}")
            return {
                'headline': 'Error processing news',
                'summary': '',
                'sentiment': 0.5,
                'source': 'Error',
                'relevance': 0.0
            }