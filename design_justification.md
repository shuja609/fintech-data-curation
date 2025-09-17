# FinTech Data Curator - Design Justification Document

**CS4063 - Natural Language Processing Assignment 1**  
**Author:** M Shuja Uddin 22i2553 
**Date:** September 18, 2025  

---

## Executive Summary

This document justifies the design decisions made in developing the FinTech Data Curator, a Python system that collects minimal feature sets for predicting next-day stock and cryptocurrency prices. The system successfully combines structured numerical data with unstructured textual information to create comprehensive datasets suitable for financial prediction models.

---

## Feature Selection Rationale

### Structured Data Features

**1. Core Price Data (OHLCV)**
- **Open, High, Low, Close, Volume**: Essential baseline features representing market activity and price movements
- **Rationale**: These form the foundation of technical analysis and are universally available across all financial instruments
- **Predictive Value**: Price patterns and volume trends are fundamental indicators of market sentiment and momentum

**2. Technical Indicators**
- **Moving Averages (5, 10, 20 days)**: Capture short, medium, and longer-term price trends
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions indicating potential reversals
- **Bollinger Bands**: Measure volatility and price extremes relative to historical norms
- **Daily Returns & Volatility**: Quantify price change magnitude and market uncertainty

**Justification**: These indicators are:
- Computationally efficient and widely used in quantitative finance
- Complementary in capturing different aspects of price behavior (trend, momentum, volatility)
- Proven effective in academic literature for short-term price prediction

### Unstructured Data Features

**1. News Headlines & Summaries**
- **Source Selection**: 11+ comprehensive RSS feeds including Yahoo Finance, MarketWatch, Reuters, Bloomberg, CNBC, Seeking Alpha, Benzinga, Financial Times, TheStreet, Fool, CoinDesk, and CoinTelegraph
- **Rationale**: News events significantly impact short-term price movements, especially earnings announcements, regulatory changes, and market sentiment shifts. Multiple sources ensure diverse coverage and reduced bias.

**2. Sentiment Analysis**
- **Implementation**: TextBlob-based sentiment scoring (0-1 scale) with enhanced relevance filtering
- **Justification**: Market psychology drives price movements; sentiment provides emotional context missing from pure technical analysis. Improved filtering ensures higher quality sentiment signals.

**3. Relevance Scoring**
- **Algorithm**: Multi-tier relevance scoring with symbol mentions (0.9), company names (0.8), financial keywords (0.6), sector terms (0.4), and general business (0.3)
- **Purpose**: Filter noise and focus on news directly impacting the target asset while maintaining contextual market information

---

## Minimality Argument

### Why This Feature Set is Sufficient

**1. Comprehensive Market Aspects**
- **Price Action**: OHLCV data captures all transaction information
- **Technical Context**: Moving averages and RSI provide trend and momentum context
- **Volatility Measurement**: Bollinger Bands and volatility metrics capture market uncertainty
- **External Factors**: News sentiment incorporates fundamental and event-driven influences

**2. Computational Efficiency**
- Limited to 13 numerical features + enhanced textual features from 11+ sources
- Avoids redundant indicators that increase noise without adding predictive value
- Balances information richness with model complexity while maximizing news coverage

**3. Data Availability**
- All features are reliably obtainable from free, public RSS feeds and APIs
- Consistent format across different assets (stocks, crypto) with specialized crypto sources
- Minimal dependencies on proprietary data feeds with robust fallback mechanisms

---

## Technical Design Decisions

### Architecture Rationale

**1. Modular Design**
- **Structured Data Collector**: Isolated technical indicator calculations for easy modification
- **Unstructured Data Collector**: Separate news processing pipeline for maintainability
- **Main Coordinator**: Centralized orchestration with error handling

**2. Data Integration Strategy**
- **Date Alignment**: Ensures temporal consistency between price and news data
- **Quality Assessment**: Validates data completeness and identifies gaps
- **Dual Export Format**: CSV for spreadsheet analysis, JSON for programmatic use

### Error Handling & Robustness

**1. Network Resilience**
- Enhanced RSS feed processing with 10-second timeouts per source
- HTTP retry logic with exponential backoff for API calls
- Graceful degradation when individual news sources are unavailable
- Comprehensive fallback mechanisms across 11+ RSS feeds

**2. Data Validation**
- Input parameter validation (exchange, symbol format)
- Price data completeness checks with technical indicator validation
- Enhanced news relevance filtering with duplicate removal
- Financial keyword matching to reduce noise and improve signal quality

---

## Validation Results

### Testing Summary
- **AAPL (NYSE)**: Successfully collected complete price data with technical indicators and enhanced news coverage
- **GOOGL (NASDAQ)**: Verified cross-exchange compatibility with improved RSS integration
- **TSLA (NYSE)**: Validated high-profile stock news collection from multiple sources
- **BTC-USD (CRYPTO)**: Confirmed cryptocurrency support with specialized CoinDesk and CoinTelegraph coverage
- **Multiple Assets**: Tested news collection across 11+ RSS feeds with improved relevance scoring

### Data Quality Metrics
- **Structured Data**: 100% completeness for all tested symbols with robust technical indicators
- **Technical Indicators**: Successfully calculated RSI, Bollinger Bands, and moving averages for all periods
- **News Integration**: Enhanced coverage from 11+ RSS feeds with improved relevance filtering
- **Recent News Coverage**: Good availability for 1-3 day periods from diverse financial sources
- **Export Functionality**: Both CSV and JSON formats with comprehensive data alignment

---

## Conclusion

The FinTech Data Curator implements a minimal yet comprehensive feature set that captures the essential elements needed for next-day price prediction:

✅ **Technical Analysis Foundation**: Core price data and proven indicators (RSI, Bollinger Bands, MA)  
✅ **Enhanced Market Sentiment**: News-based sentiment from 11+ diverse financial RSS sources  
✅ **Scalable Architecture**: Modular design supporting stocks, crypto, and multiple exchanges  
✅ **Robust Implementation**: Enhanced error handling, timeout protection, and data validation  
✅ **Practical Utility**: Standard output formats with comprehensive news integration  
✅ **Production Ready**: Thoroughly tested with real market data and news coverage  

This minimal feature set strikes an optimal balance between predictive power and computational efficiency, providing a solid foundation for financial machine learning applications while remaining maintainable and extensible for future enhancements.

---

**References:**
- Bollinger, J. (2001). Bollinger on Bollinger Bands. McGraw-Hill
- Murphy, J. J. (1999). Technical Analysis of the Financial Markets. New York Institute of Finance
- Wilder, J. W. (1978). New Concepts in Technical Trading Systems. Trend Research