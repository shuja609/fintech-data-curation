"""
Main data collector for FinTech Data Curator
Coordinates structured and unstructured data collection
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any
import logging
import pandas as pd

from .config import Config
from .structured_data import StructuredDataCollector
from .unstructured_data import UnstructuredDataCollector
from .utils import setup_logging, validate_symbol, validate_exchange

class FinancialDataCollector:
    """Main coordinator for financial data collection."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.logger = setup_logging()
        
        # Initialize sub-collectors
        self.structured_collector = StructuredDataCollector(self.config)
        self.unstructured_collector = UnstructuredDataCollector(self.config)
    
    def collect_data(self, exchange: str, symbol: str, days: int) -> Dict[str, Any]:
        """Main method to collect all data for a given symbol."""
        try:
            # Validate inputs
            if not validate_exchange(exchange):
                raise ValueError(f"Invalid exchange: {exchange}")
            
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if days <= 0:
                raise ValueError(f"Days must be positive: {days}")
            
            self.logger.info(f"Starting data collection for {symbol} on {exchange}")
            
            # Collect structured data
            self.logger.info("Collecting structured data...")
            structured_data = self.structured_collector.get_latest_data(symbol, exchange, days)
            
            # Collect unstructured data
            self.logger.info("Collecting unstructured data...")
            news_data = self.unstructured_collector.collect_news_data(symbol, exchange, days)
            
            # Merge data
            self.logger.info("Merging structured and unstructured data...")
            merged_data = self._merge_data(structured_data, news_data, days)
            
            # Create dataset
            dataset = {
                'metadata': {
                    'symbol': symbol,
                    'exchange': exchange,
                    'collection_date': datetime.now().isoformat(),
                    'days_requested': days,
                    'days_collected': len(merged_data),
                    'data_quality': self._assess_data_quality(merged_data)
                },
                'data': merged_data
            }
            
            self.logger.info(f"Data collection completed. Collected {len(merged_data)} days of data")
            return dataset
            
        except Exception as e:
            self.logger.error(f"Error in data collection: {e}")
            raise
    
    def _merge_data(self, structured_data: pd.DataFrame, 
                   news_data: List[Dict], days: int) -> List[Dict]:
        """Merge structured and unstructured data by date."""
        try:
            merged_records = []
            
            # Create date range from structured data
            date_range = [datetime.strptime(str(date), '%Y-%m-%d') 
                         for date in structured_data['date'].values]
            
            # Align news with dates
            aligned_news = self.unstructured_collector.align_news_with_dates(news_data, date_range)
            
            # Merge each day's data
            for _, row in structured_data.iterrows():
                date_str = str(row['date'])
                
                # Get structured data for this date
                structured_record = row.to_dict()
                
                # Convert date to string for consistency
                structured_record['date'] = date_str
                
                # Get news for this date
                date_news = aligned_news.get(date_str, [])
                representative_news = self.unstructured_collector.get_representative_news(date_news)
                
                # Create merged record
                merged_record = {
                    'date': date_str,
                    'structured': {k: v for k, v in structured_record.items() if k != 'date'},
                    'unstructured': representative_news,
                    'all_news': date_news  # Keep all news for reference
                }
                
                merged_records.append(merged_record)
            
            return merged_records
            
        except Exception as e:
            self.logger.error(f"Error merging data: {e}")
            raise
    
    def _assess_data_quality(self, data: List[Dict]) -> Dict[str, Any]:
        """Assess the quality of the collected dataset."""
        try:
            if not data:
                return {'quality_score': 0, 'issues': ['No data collected']}
            
            issues = []
            total_records = len(data)
            complete_records = 0
            
            for record in data:
                structured = record.get('structured', {})
                unstructured = record.get('unstructured', {})
                
                # Check structured data completeness
                required_fields = ['open', 'high', 'low', 'close', 'volume']
                if all(field in structured and structured[field] not in [None, 0] 
                       for field in required_fields):
                    complete_records += 1
                
                # Check for news availability
                if not unstructured.get('headline') or unstructured.get('headline') == 'No relevant news found':
                    issues.append(f"No news found for {record['date']}")
            
            quality_score = (complete_records / total_records) * 100 if total_records > 0 else 0
            
            return {
                'quality_score': round(quality_score, 2),
                'total_records': total_records,
                'complete_records': complete_records,
                'issues': issues[:5]  # Limit to first 5 issues
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing data quality: {e}")
            return {'quality_score': 0, 'issues': ['Error assessing quality']}
    
    def export_data(self, dataset: Dict[str, Any], symbol: str, 
                   output_dir: str, format_type: str = 'both'):
        """Export dataset to specified format(s)."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"{symbol}_{timestamp}"
            
            if format_type in ['csv', 'both']:
                csv_path = os.path.join(output_dir, f"{base_filename}.csv")
                self._export_to_csv(dataset, csv_path)
                self.logger.info(f"CSV exported to: {csv_path}")
            
            if format_type in ['json', 'both']:
                json_path = os.path.join(output_dir, f"{base_filename}.json")
                self._export_to_json(dataset, json_path)
                self.logger.info(f"JSON exported to: {json_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            raise
    
    def _export_to_csv(self, dataset: Dict[str, Any], filepath: str):
        """Export dataset to CSV format."""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                # Define CSV headers
                headers = ['date']
                
                # Add structured data headers
                if dataset['data']:
                    structured_sample = dataset['data'][0]['structured']
                    headers.extend(structured_sample.keys())
                
                # Add unstructured data headers
                headers.extend(['news_headline', 'news_summary', 'news_sentiment', 
                               'news_source', 'news_relevance'])
                
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                # Write data rows
                for record in dataset['data']:
                    row = {'date': record['date']}
                    
                    # Add structured data
                    row.update(record['structured'])
                    
                    # Add unstructured data
                    unstructured = record['unstructured']
                    row.update({
                        'news_headline': unstructured.get('headline', ''),
                        'news_summary': unstructured.get('summary', ''),
                        'news_sentiment': unstructured.get('sentiment', 0.5),
                        'news_source': unstructured.get('source', ''),
                        'news_relevance': unstructured.get('relevance', 0.0)
                    })
                    
                    writer.writerow(row)
                    
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def _export_to_json(self, dataset: Dict[str, Any], filepath: str):
        """Export dataset to JSON format."""
        try:
            # Clean dataset for JSON serialization
            clean_dataset = self._clean_for_json(dataset)
            
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(clean_dataset, jsonfile, indent=self.config.output['json_indent'], 
                         ensure_ascii=False, default=str)
                
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def _clean_for_json(self, obj):
        """Clean data structure for JSON serialization."""
        if isinstance(obj, dict):
            return {k: self._clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json(item) for item in obj]
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        elif isinstance(obj, (float, int)) and str(obj) in ['nan', 'inf', '-inf']:
            return None
        else:
            return obj