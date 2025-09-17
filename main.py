"""
FinTech Data Curator
===================

A Python program for collecting minimal feature sets necessary to predict 
next-day prices for stocks and cryptocurrencies.

Author: CS4063 Student
Date: September 17, 2025
Assignment: Data Curation for FinTech
"""

from src.data_collector import FinancialDataCollector
from src.config import Config
import argparse
import sys
import os

def main():
    """Main entry point for the FinTech Data Curator."""
    
    parser = argparse.ArgumentParser(
        description='Collect financial data for stock/crypto price prediction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --exchange NYSE --symbol AAPL --days 7
  python main.py --exchange CRYPTO --symbol BTC-USD --days 5
  python main.py --exchange NASDAQ --symbol GOOGL --days 10
        """
    )
    
    parser.add_argument(
        '--exchange', 
        required=True,
        choices=['NYSE', 'NASDAQ', 'PSX', 'CRYPTO'],
        help='Stock exchange name (NYSE, NASDAQ, PSX) or CRYPTO for cryptocurrencies'
    )
    
    parser.add_argument(
        '--symbol', 
        required=True,
        help='Stock symbol (e.g., AAPL, GOOGL) or crypto ticker (e.g., BTC-USD)'
    )
    
    parser.add_argument(
        '--days', 
        type=int, 
        default=7,
        help='Number of historical days to collect (default: 7)'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['csv', 'json', 'both'],
        default='both',
        help='Output format for the collected data (default: both)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Directory to save output files (default: ./output)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config = Config()
        
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Initialize data collector
        collector = FinancialDataCollector(config)
        
        print(f"🚀 Starting data collection for {args.symbol} on {args.exchange}")
        print(f"📅 Collecting {args.days} days of historical data")
        print(f"💾 Output format: {args.output_format}")
        print("-" * 50)
        
        # Collect the data
        dataset = collector.collect_data(
            exchange=args.exchange,
            symbol=args.symbol,
            days=args.days
        )
        
        # Export the data
        collector.export_data(
            dataset=dataset,
            symbol=args.symbol,
            output_dir=args.output_dir,
            format_type=args.output_format
        )
        
        print("✅ Data collection completed successfully!")
        print(f"📁 Output saved to: {args.output_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()