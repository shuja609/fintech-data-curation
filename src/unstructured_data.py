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
            
            # Try RSS feeds first (more reliable)
            rss_news = self._get_rss_financial_news(symbol, days)
            news_articles.extend(rss_news)
            
            # Yahoo Finance News (with improved scraping)
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
            
            # Try multiple Yahoo Finance news URLs
            news_urls = [
                f"https://finance.yahoo.com/quote/{symbol}/news",
                f"https://finance.yahoo.com/news/",
                f"https://finance.yahoo.com/topic/stock-market-news"
            ]
            
            headers = self.config.get_headers()
            
            for search_url in news_urls:
                try:
                    response = safe_request(search_url, headers)
                    if not response:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try multiple selectors for Yahoo Finance
                    selectors = [
                        'h3[data-test-locator="headline"]',
                        'h3[class*="headline"]',
                        'h4[class*="headline"]',
                        'a[class*="story-title"]',
                        'div[class*="story"] h3',
                        'div[class*="news"] h3',
                        'li[class*="stream-item"] h3',
                        'div[data-module="stream"] h3',
                        '[data-test-locator="stream"] h3'
                    ]
                    
                    news_items = []
                    for selector in selectors:
                        items = soup.select(selector)
                        if items:
                            news_items.extend(items[:10])  # Limit items per selector
                    
                    # Also try generic headline selectors
                    if not news_items:
                        news_items = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=lambda text: text and len(text) > 20)[:20]
                    
                    for item in news_items[:15]:  # Limit total items
                        try:
                            if hasattr(item, 'get_text'):
                                headline = clean_text(item.get_text())
                            else:
                                headline = clean_text(str(item))
                            
                            if len(headline) >= self.config.news_filters['min_headline_length']:
                                # Check if headline contains financial keywords
                                financial_keywords = ['stock', 'market', 'price', 'trading', 'shares', 'earnings', 'revenue', 'profit', 'loss', 'investment']
                                if any(keyword in headline.lower() for keyword in financial_keywords):
                                    article = {
                                        'headline': headline,
                                        'summary': headline[:200] + '...' if len(headline) > 200 else headline,
                                        'source': 'Yahoo Finance',
                                        'date': datetime.now().date(),
                                        'url': search_url
                                    }
                                    articles.append(article)
                                    
                        except Exception as e:
                            self.logger.debug(f"Error parsing Yahoo news item: {e}")
                            continue
                    
                    if articles:  # If we found articles, break
                        break
                        
                except Exception as e:
                    self.logger.debug(f"Error with URL {search_url}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching Yahoo Finance news: {e}")
            return []
    
    def _get_rss_financial_news(self, symbol: str, days: int) -> List[Dict]:
        """Get financial news from RSS feeds."""
        try:
            articles = []
            
            # Get all RSS feeds from config
            rss_feeds = []
            
            # Add core feeds
            rss_feeds.append(('Yahoo Finance', 'https://feeds.finance.yahoo.com/rss/2.0/headline'))
            rss_feeds.append(('CoinDesk', self.config.data_sources['coindesk']['rss_url']))
            
            # Add additional feeds from config
            for name, url in self.config.data_sources['additional_rss_feeds'].items():
                rss_feeds.append((name.replace('_', ' ').title(), url))
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for feed_name, feed_url in rss_feeds:
                try:
                    self.logger.debug(f"Fetching RSS feed: {feed_name} - {feed_url}")
                    
                    # Add timeout for RSS parsing
                    import socket
                    socket.setdefaulttimeout(10)
                    
                    feed = feedparser.parse(feed_url)
                    
                    if not feed.entries:
                        self.logger.debug(f"No entries found in {feed_name}")
                        continue
                    
                    for entry in feed.entries[:15]:  # Limit entries per feed
                        try:
                            # Parse publication date
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                pub_date = datetime(*entry.published_parsed[:6])
                            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                                pub_date = datetime(*entry.updated_parsed[:6])
                            else:
                                pub_date = datetime.now()  # Use current time if no date
                            
                            if pub_date >= cutoff_date:
                                headline = clean_text(entry.title) if hasattr(entry, 'title') else ''
                                summary = clean_text(entry.summary) if hasattr(entry, 'summary') else headline
                                
                                # Check if headline contains any relevant keywords
                                if len(headline) >= self.config.news_filters['min_headline_length']:
                                    keywords = self.config.news_filters['relevant_keywords']
                                    headline_lower = headline.lower()
                                    
                                    # Check for keyword relevance
                                    has_keywords = any(keyword in headline_lower for keyword in keywords)
                                    
                                    if has_keywords or feed_name.lower() in ['coindesk', 'crypto', 'fintech']:
                                        article = {
                                            'headline': headline,
                                            'summary': summary[:300] + '...' if len(summary) > 300 else summary,
                                            'source': feed_name,
                                            'date': pub_date.date(),
                                            'url': entry.link if hasattr(entry, 'link') else feed_url
                                        }
                                        articles.append(article)
                                    
                        except Exception as e:
                            self.logger.debug(f"Error parsing RSS entry from {feed_name}: {e}")
                            continue
                            
                except Exception as e:
                    self.logger.debug(f"Error fetching RSS feed {feed_name}: {e}")
                    continue
            
            # Remove duplicates based on headline
            seen_headlines = set()
            unique_articles = []
            for article in articles:
                if article['headline'] not in seen_headlines:
                    seen_headlines.add(article['headline'])
                    unique_articles.append(article)
            
            self.logger.info(f"Collected {len(unique_articles)} unique articles from RSS feeds")
            return unique_articles
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS financial news: {e}")
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
                    
                    # Filter by relevance (lowered threshold to capture more news)
                    if relevance < 0.1:
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