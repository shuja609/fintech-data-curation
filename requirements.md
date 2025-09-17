# CS4063 - Natural Language Processing Assignment 1
## Data Curation for FinTech

**Due Date:** Thursday, September 18th by 10:00am  
**Assignment Type:** Individual work  
**Late Policy:** No late assignments accepted

---

## 📋 Assignment Overview

### Motivation
Financial Technolo## 🚀 Getting Started Checklist

- [x] Set up Python development environment
- [x] Research available financial data APIs
- [x] Identify target stocks and cryptocurrencies for testing
- [x] Plan feature selection strategy
- [x] Design data collection architecture
- [x] Implement basic scraping functionality
- [x] Add error handling and robustness
- [x] Test with multiple assets
- [x] Generate sample datasets
- [x] Write design justification document

---

## 🎉 Implementation Complete!

### ✅ All Assignment Requirements Met

**Input Parameters**: ✅ Stock exchange name and symbol via command line  
**Live Data Sources**: ✅ Yahoo Finance API, CoinDesk RSS feeds  
**Structured Data**: ✅ OHLCV + comprehensive technical indicators  
**Unstructured Data**: ✅ Financial news with sentiment analysis  
**Output Formats**: ✅ CSV and JSON with perfect date alignment  
**Modularity**: ✅ Easy parameter changes for different assets  
**Error Handling**: ✅ Robust network error management and retries  

### 📊 Testing Results

**Successfully tested with:**
- **AAPL (NYSE)**: 5 days of complete structured data
- **GOOGL (NASDAQ)**: Cross-exchange compatibility verified  
- **BTC-USD (CRYPTO)**: Full crypto support with news integration

### 📁 Project Deliverables

1. **Complete Python Implementation** (`src/` package)
2. **Sample Output Data** (CSV/JSON in `output/` directory)
3. **Design Justification Document** (`design_justification.md`)
4. **Comprehensive Documentation** (`README.md`, `requirements.md`)

### 🔄 How to Use

```bash
# Setup
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run examples
python main.py --exchange NYSE --symbol AAPL --days 7
python main.py --exchange CRYPTO --symbol BTC-USD --days 5
python main.py --exchange NASDAQ --symbol GOOGL --days 10
```

---epresents one of the most impactful applications of Artificial Intelligence today. This assignment focuses on data curation for financial prediction tasks, specifically:
- Stock price prediction
- Cryptocurrency value forecasting  
- Market movement analysis

The core challenge is to generate high-quality datasets from live financial sources, combining both structured numerical data and unstructured textual information to enable accurate next-day price predictions.

---

## 🎯 Primary Objective

**Implement a Python program that collects the minimal set of features necessary to predict the next day's price for any given stock or cryptocurrency.**

---

## 📝 Functional Requirements

### Core Inputs
The program must accept:
1. **Stock Exchange Name** (e.g., NYSE, NASDAQ, PSX)
2. **Stock Symbol or Cryptocurrency Ticker** (e.g., AAPL, BTC-USD)

### Data Collection Requirements

#### Structured Data (Numerical)
- **Historical Prices:** Open, High, Low, Close, Volume
- **Market Indicators:** 
  - Returns
  - Volatility measures
  - Moving averages
  - Other relevant technical indicators

#### Unstructured Data (Textual)
- **Financial News Headlines**
- **News Summaries**
- **Sentiment-bearing text** from trusted sources
- **Recommended Sources:**
  - Yahoo Finance News
  - Reuters
  - CoinDesk
  - Official exchange websites

### Data Sources
- Yahoo Finance
- Investing.com
- CoinMarketCap
- Official exchange websites
- Other open financial data sources

### Output Requirements
- **Format:** CSV or JSON
- **Structure:** Unstructured text fields aligned by date with structured numerical fields
- **Time Coverage:** Minimum 5 days of historical data
- **Modularity:** Easy parameter changes for different stocks/cryptocurrencies

---

## 🛠️ Technical Requirements

### Programming Language
- **Python** (required)

### Recommended Libraries
- `requests` - HTTP requests
- `BeautifulSoup` - HTML parsing
- `Selenium` - Dynamic content scraping
- `yfinance` - Yahoo Finance API
- `newspaper3k` - News extraction
- RSS feed libraries
- Other relevant financial APIs

### Code Quality Standards
- **Clean, reproducible code**
- **Proper documentation**
- **Exception handling** for network reliability
- **Modular design** for easy parameter changes

---

## 🔍 Feature Selection Criteria

### Critical Considerations
- **Minimality:** Focus on essential features, not comprehensive data collection
- **Predictive Power:** Select features with clear relevance to next-day price movements
- **Balance:** Combine numerical indicators with textual sentiment data
- **Temporal Alignment:** Ensure news and price data are properly synchronized by date

### Evidence Requirements
Demonstrate functionality with:
- **2+ different stocks** (sample runs)
- **1+ cryptocurrency** (sample run)
- **5+ days of historical data** per test case
- **Generated dataset snapshots**

---

## 📦 Deliverables

### 1. Python Code
- Complete web scraping implementation
- Well-documented and commented
- Includes error handling
- Modular design for different assets

### 2. Sample Output Data
- CSV/JSON files for test cases
- At least 2 stocks + 1 cryptocurrency
- Minimum 5 days of data per asset

### 3. Design Documentation
**One-page report including:**
- **Feature Selection Rationale:** Why these specific structured and unstructured features?
- **Sufficiency Justification:** Why is this minimal set adequate for next-day prediction?
- **References:** Sources and methodologies used

---

## 📊 Grading Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Code Correctness** | 25% | Program runs successfully and pulls both structured and unstructured data |
| **Feature Quality** | 25% | Optimal balance and minimality of chosen features |
| **Documentation** | 20% | Code clarity, comments, and organization |
| **Working Evidence** | 20% | Successful sample runs and stored outputs |
| **Design Justification** | 10% | Quality of reasoning in the written report |

---

## 🔒 Academic Integrity

### Allowed Collaboration
- Verbal discussions with classmates
- Email discussions with instructor and peers
- Internet research for methodology

### Prohibited Activities
- Copying or plagiarizing code
- Sharing written reports
- Using others' implementations without proper attribution

**Penalty:** Plagiarized work receives zero points

---

## � Product Backlog

### Epic 1: Core Data Collection Infrastructure
**Priority:** High | **Effort:** Large

#### User Stories:
- **As a developer**, I want to set up a Python environment with required libraries so that I can build the scraping system
- **As a user**, I want to input a stock exchange and symbol so that the system knows what data to collect
- **As a developer**, I want to create a modular architecture so that adding new stocks/cryptos is simple
- **As a user**, I want the system to handle network errors gracefully so that temporary failures don't crash the program

#### Tasks:
- [ ] Set up Python project structure with virtual environment
- [ ] Install and configure required libraries (requests, BeautifulSoup, yfinance, etc.)
- [ ] Create input validation for stock exchange and symbol parameters
- [ ] Design modular class structure for different data sources
- [ ] Implement basic error handling and retry mechanisms
- [ ] Create configuration management for API keys and settings

### Epic 2: Structured Data Collection
**Priority:** High | **Effort:** Medium

#### User Stories:
- **As a financial analyst**, I want historical price data (OHLCV) so that I can analyze price trends
- **As a data scientist**, I want calculated technical indicators so that I can build predictive models
- **As a user**, I want data from multiple exchanges so that I can compare different markets

#### Tasks:
- [ ] Implement Yahoo Finance API integration using yfinance
- [ ] Create price data scraper for OHLCV (Open, High, Low, Close, Volume)
- [ ] Calculate technical indicators (moving averages, volatility, returns)
- [ ] Add support for different stock exchanges (NYSE, NASDAQ, PSX)
- [ ] Implement cryptocurrency data collection (BTC-USD, etc.)
- [ ] Create data validation and quality checks
- [ ] Add date range handling for historical data

### Epic 3: Unstructured Data Collection  
**Priority:** High | **Effort:** Large

#### User Stories:
- **As a trader**, I want relevant news headlines so that I can understand market sentiment
- **As a researcher**, I want news aligned with price data by date so that I can study correlations
- **As a user**, I want news from trusted sources so that the information is reliable

#### Tasks:
- [ ] Implement news scraping from Yahoo Finance News
- [ ] Add Reuters news feed integration
- [ ] Create CoinDesk scraper for cryptocurrency news
- [ ] Implement date-based news filtering and alignment
- [ ] Add sentiment analysis preprocessing for news text
- [ ] Create news deduplication and relevance filtering
- [ ] Handle RSS feeds and news APIs

### Epic 4: Data Processing and Storage
**Priority:** Medium | **Effort:** Medium

#### User Stories:
- **As a data scientist**, I want data in CSV/JSON format so that I can easily import it into analysis tools
- **As a user**, I want structured output with aligned dates so that price and news data correspond correctly
- **As a developer**, I want clean data schemas so that the output is consistent and reliable

#### Tasks:
- [ ] Design CSV/JSON output schema with date alignment
- [ ] Implement data merging logic for price and news data
- [ ] Create data cleaning and preprocessing functions
- [ ] Add data export functionality (CSV and JSON formats)
- [ ] Implement data validation and completeness checks
- [ ] Create sample data generation for testing

### Epic 5: Feature Selection and Optimization
**Priority:** Medium | **Effort:** Small

#### User Stories:
- **As a researcher**, I want a minimal but effective feature set so that models are efficient and accurate
- **As a user**, I want documented feature selection rationale so that I understand why features were chosen

#### Tasks:
- [ ] Research and define minimal feature set for price prediction
- [ ] Implement feature importance analysis
- [ ] Create feature selection documentation
- [ ] Add configurable feature selection options
- [ ] Optimize data collection for selected features only

### Epic 6: Testing and Validation
**Priority:** Medium | **Effort:** Medium

#### User Stories:
- **As a user**, I want to see working examples so that I know the system functions correctly
- **As a developer**, I want comprehensive testing so that the system is reliable
- **As an evaluator**, I want sample outputs so that I can verify the system works

#### Tasks:
- [ ] Test with 2+ different stocks (e.g., AAPL, GOOGL)
- [ ] Test with 1+ cryptocurrency (e.g., BTC-USD)
- [ ] Generate 5+ days of sample data for each test case
- [ ] Create automated testing suite
- [ ] Validate data quality and completeness
- [ ] Document test cases and results

### Epic 7: Documentation and Reporting
**Priority:** Low | **Effort:** Small

#### User Stories:
- **As a user**, I want clear documentation so that I can understand and modify the code
- **As an evaluator**, I want design justification so that I can assess the technical decisions
- **As a developer**, I want maintainable code so that future enhancements are possible

#### Tasks:
- [ ] Write comprehensive code documentation and comments
- [ ] Create one-page design justification document
- [ ] Document feature selection rationale
- [ ] Add usage examples and tutorials
- [ ] Create README with setup and execution instructions
- [ ] Document API limitations and considerations

---

## 📊 Sprint Planning Recommendations

### Sprint 1 (Days 1-2): Foundation Setup
- Epic 1: Core Infrastructure
- Epic 2: Basic structured data collection

### Sprint 2 (Days 3-4): Data Collection Implementation  
- Epic 2: Complete structured data features
- Epic 3: Unstructured data collection
- Epic 4: Data processing basics

### Sprint 3 (Days 5-6): Integration and Testing
- Epic 4: Complete data storage
- Epic 5: Feature optimization
- Epic 6: Testing and validation

### Sprint 4 (Day 7): Documentation and Polish
- Epic 7: Documentation
- Final testing and refinement
- Submission preparation

---

## �🚀 Getting Started Checklist

- [ ] Set up Python development environment
- [ ] Research available financial data APIs
- [ ] Identify target stocks and cryptocurrencies for testing
- [ ] Plan feature selection strategy
- [ ] Design data collection architecture
- [ ] Implement basic scraping functionality
- [ ] Add error handling and robustness
- [ ] Test with multiple assets
- [ ] Generate sample datasets
- [ ] Write design justification document

---

## 💡 Success Tips

1. **Start Early:** Web scraping can be unpredictable due to website changes
2. **Test Frequently:** Verify data quality and completeness regularly
3. **Handle Errors:** Implement robust exception handling for network issues
4. **Document Decisions:** Keep notes on why you chose specific features
5. **Validate Data:** Ensure temporal alignment between price and news data

---

## 📞 Support

For questions or clarification:
- Contact course instructor
- Discuss concepts with classmates (following honor policy)
- Refer to course materials and recommended resources

---

*This requirements document serves as a comprehensive guide for completing Assignment 1. Ensure all requirements are met before submission.*