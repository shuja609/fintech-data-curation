# FinTech Data Curator - Design Justification Document

**CS4063 - Natural Language Processing Assignment 1**  
**Author:** CS4063 Student  
**Date:** September 17, 2025  

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
- **Source Selection**: Yahoo Finance (broad coverage), CoinDesk (crypto-specific expertise)
- **Rationale**: News events significantly impact short-term price movements, especially earnings announcements, regulatory changes, and market sentiment shifts

**2. Sentiment Analysis**
- **Implementation**: TextBlob-based sentiment scoring (0-1 scale)
- **Justification**: Market psychology drives price movements; sentiment provides emotional context missing from pure technical analysis

**3. Relevance Scoring**
- **Algorithm**: Symbol-specific keyword matching with company name recognition
- **Purpose**: Filter noise and focus on news directly impacting the target asset

---

## Minimality Argument

### Why This Feature Set is Sufficient

**1. Comprehensive Market Aspects**
- **Price Action**: OHLCV data captures all transaction information
- **Technical Context**: Moving averages and RSI provide trend and momentum context
- **Volatility Measurement**: Bollinger Bands and volatility metrics capture market uncertainty
- **External Factors**: News sentiment incorporates fundamental and event-driven influences

**2. Computational Efficiency**
- Limited to 13 numerical features + 5 textual features
- Avoids redundant indicators that increase noise without adding predictive value
- Balances information richness with model complexity

**3. Data Availability**
- All features are reliably obtainable from free, public sources
- Consistent format across different assets (stocks, crypto)
- Minimal dependencies on proprietary data feeds

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
- HTTP retry logic with exponential backoff
- Graceful degradation when news sources are unavailable
- Fallback mechanisms for missing data

**2. Data Validation**
- Input parameter validation (exchange, symbol format)
- Price data completeness checks
- News relevance filtering to reduce noise

---

## Validation Results

### Testing Summary
- **AAPL (NYSE)**: Successfully collected 5 days of complete price data with technical indicators
- **GOOGL (NASDAQ)**: Verified cross-exchange compatibility
- **BTC-USD (CRYPTO)**: Confirmed cryptocurrency support with news integration

### Data Quality Metrics
- **Structured Data**: 100% completeness for all tested symbols
- **Technical Indicators**: Successfully calculated for all requested periods
- **News Integration**: CoinDesk RSS feed provided relevant cryptocurrency news
- **Export Functionality**: Both CSV and JSON formats generated successfully

---

## Conclusion

The FinTech Data Curator implements a minimal yet comprehensive feature set that captures the essential elements needed for next-day price prediction:

✅ **Technical Analysis Foundation**: Core price data and proven indicators  
✅ **Market Sentiment Integration**: News-based sentiment analysis  
✅ **Scalable Architecture**: Modular design supporting multiple asset types  
✅ **Robust Implementation**: Error handling and data validation  
✅ **Practical Utility**: Standard output formats for immediate use  

This minimal feature set strikes an optimal balance between predictive power and computational efficiency, providing a solid foundation for financial machine learning applications while remaining maintainable and extensible for future enhancements.

---

**References:**
- Bollinger, J. (2001). Bollinger on Bollinger Bands. McGraw-Hill
- Murphy, J. J. (1999). Technical Analysis of the Financial Markets. New York Institute of Finance
- Wilder, J. W. (1978). New Concepts in Technical Trading Systems. Trend Research