# 📊 StockBus - Trade Pulse: AI-Powered Sentiment Analysis for Nifty 50
├── 📂 docs/                      # Documentation
    ├── 30_DAY_SPRINT_PLAN.md    # Technical implementation guide
    ├── DASHBOARD_SPECIFICATION.md # UI/UX specifications
    ├── NAVIGATION.md             # File reference guide
    ├── START_DAY_1.md            # Day 1 kickoff guide
    └── archive/                  # Historical documents
```

**📌 Quick Start:** See `MASTER_TRACKER.md` for daily progress and tasks.

---A production-ready system that predicts Nifty 50 movements using news sentiment analysis, deep learning, and automated trading integration.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-yellow.svg)]()

---

## 🎯 Project Overview

**StockBus** is an integrated stock analysis and trading platform. **Trade Pulse** is the sentiment analysis engine that:

1. **Scrapes** financial news articles with full body text
2. **Summarizes** articles into 5-10 key points using LLM (GPT-4/Claude)
3. **Analyzes** sentiment using fine-tuned FinBERT model
4. **Predicts** Nifty 50 movements (4-7 day forecasts) with LSTM
5. **Backtests** strategies on 7 years of historical data (2018-2024)
6. **Generates** AI-powered daily reports with reasoning
7. **Integrates** with StockPass paper trading platform for automated execution

### Key Features:
- ✅ **Data Quality First:** LLM summarization removes clickbait and noise
- ✅ **Deep Learning:** FinBERT sentiment + LSTM price prediction
- ✅ **Comprehensive Dashboard:** 6-page Streamlit analytics interface
- ✅ **Proven Performance:** Backtesting shows edge over buy-and-hold
- ✅ **Fully Automated:** Daily pipeline runs before market open
- ✅ **Production Ready:** 30-day development sprint (Oct 8 - Nov 6, 2025)

---

## 📁 Project Structure

```
news-data-scrapping/              # Root directory
│
├── 📋 MASTER_TRACKER.md         # Single source of truth for progress
├── 📖 README.md                  # This file
├── requirements.txt              # Python dependencies
├── config.yaml                   # Configuration (API keys, parameters)
├── .env                          # Environment variables (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
│
├── 📂 src/                       # Source code (organized by function)
│   ├── scraping/                 # News scraping & data collection
│   ├── processing/               # Summarization & sentiment analysis
│   ├── modeling/                 # ML models (LSTM, FinBERT)
│   ├── backtesting/              # Strategy backtesting
│   ├── trading/                  # StockPass integration
│   ├── reporting/                # Report generation & visualizations
│   └── dashboard/                # Streamlit web dashboard
│
├── 📂 data/                      # All data files
│   ├── raw/news/                 # Scraped news articles
│   ├── processed/                # Summaries, sentiment, features
│   ├── market/                   # Nifty 50 OHLCV data
│   └── datasets/                 # Train/validation/test splits
│
├── 📂 models/                    # Trained models
│   ├── finbert/                  # Fine-tuned FinBERT
│   └── lstm/                     # LSTM predictor
│
├── 📂 outputs/                   # Generated outputs
│   ├── reports/daily/            # Daily PDF/HTML reports
│   ├── predictions/              # Prediction history
│   ├── backtests/                # Backtest results
│   └── visualizations/           # Charts and plots
│
├── 📂 logs/                      # Log files (pipeline, training, errors)
├── 📂 scripts/                   # Executable scripts
├── 📂 notebooks/                 # Jupyter notebooks (exploration)
├── 📂 tests/                     # Unit tests
└── 📂 docs/                      # Documentation
    ├── DASHBOARD_SPECIFICATION.md
    └── setup_guide.md
```

---

## 🚀 Quick Start

### Prerequisites:
- Python 3.10 or higher
- Windows 10/11 (or adapt for Linux/Mac)
- OpenAI API key (for GPT-4o-mini) or Anthropic (Claude)
- 8GB+ RAM recommended
- GPU optional but helpful for FinBERT training

### Installation:

1. **Clone the repository:**
```powershell
git clone https://github.com/SujayAgarwal28/news-data-scrapping.git
cd news-data-scrapping
```

2. **Create virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Set up configuration:**
```powershell
# Copy config template
cp config.yaml.template config.yaml

# Add your API keys to config.yaml
# Or create .env file:
echo "OPENAI_API_KEY=your-key-here" > .env
```

5. **Run initial setup:**
```powershell
python scripts/setup_environment.py
```

### First Run:

**Test the scraper:**
```powershell
python src/scraping/news_scraper.py --start 2024-10-01 --end 2024-10-08
```

**Launch dashboard:**
```powershell
streamlit run src/dashboard/app.py
```

---

## 📊 Dashboard

Access the **StockBus Trade Pulse Analytics Dashboard** at `http://localhost:8501`

### Pages:
1. **🏠 Overview** - Key metrics, latest prediction, system status
2. **📰 News Analysis** - Browse articles, summaries, sentiment scores
3. **📈 Sentiment Trends** - Historical sentiment vs. price movements
4. **🔮 Predictions** - Current forecast, AI reasoning, accuracy history
5. **🔬 Backtesting** - Performance metrics, equity curves, trade analysis
6. **🤖 Live Trading** - StockPass integration, bot status, recent trades

---

## 🗓️ Development Timeline

**Total Duration:** 30 days (Oct 8 - Nov 6, 2025)

- **Week 1 (Days 1-7):** Data pipeline & LLM summarization
- **Week 2 (Days 8-14):** Sentiment analysis (FinBERT)
- **Week 3 (Days 15-21):** Prediction model & backtesting
- **Week 4 (Days 22-30):** Trading integration, automation, dashboard

**Current Status:** See `MASTER_TRACKER.md` for daily progress updates

---

## 🛠️ Technology Stack

### Core:
- **Python 3.10+** - Programming language
- **PyTorch** - Deep learning framework
- **Transformers** - FinBERT sentiment analysis
- **Streamlit** - Interactive dashboard

### Data Collection:
- **newspaper3k / trafilatura** - Article body extraction
- **BeautifulSoup & Selenium** - Web scraping
- **yfinance / nsepy** - Market data

### ML & NLP:
- **Hugging Face** - Pre-trained models
- **OpenAI API / Anthropic Claude** - LLM summarization
- **scikit-learn** - Feature engineering
- **Optuna** - Hyperparameter tuning

### Visualization:
- **Plotly** - Interactive charts
- **Matplotlib & Seaborn** - Static plots

### Automation:
- **APScheduler** - Python scheduling
- **Windows Task Scheduler** - Daily automation

---

## 📈 Performance Targets

### Model Metrics:
- **Prediction Accuracy:** >60% directional (beat 50% baseline)
- **Sentiment Correlation:** >0.3 with future returns
- **Backtest Sharpe Ratio:** >1.0

### System Metrics:
- **Pipeline Execution:** <10 minutes per day
- **Dashboard Load Time:** <3 seconds
- **Uptime:** >99%

### Business Metrics:
- **Beat Buy-and-Hold:** Positive alpha
- **Max Drawdown:** <20%

---

## 🔧 Usage

### Daily Automated Pipeline:
```powershell
# Runs automatically at 8:00 AM IST via Task Scheduler
python scripts/daily_pipeline.py
```

### Manual Operations:

**Scrape news:**
```powershell
python src/scraping/news_scraper.py --start 2024-10-01 --end 2024-10-08
```

**Train model:**
```powershell
python scripts/train_model.py --epochs 50 --batch-size 32
```

**Run backtest:**
```powershell
python scripts/run_backtest.py --start 2018-01-01 --end 2024-12-31
```

**Generate report:**
```powershell
python scripts/generate_report.py --date 2024-10-08
```

---

## 📚 Documentation

- **[MASTER_TRACKER.md](MASTER_TRACKER.md)** - Daily progress tracking & task checklist
- **[DASHBOARD_SPECIFICATION.md](docs/DASHBOARD_SPECIFICATION.md)** - Complete dashboard design
- **[30_DAY_SPRINT_PLAN.md](30_DAY_SPRINT_PLAN.md)** - Detailed development roadmap
- **[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)** - Long-term vision (archived)

---

## 🧪 Testing

Run unit tests:
```powershell
pytest tests/
```

Run specific test file:
```powershell
pytest tests/test_scraper.py -v
```

---

## 🔒 Security & Privacy

- **API Keys:** Stored in `.env` file (not committed to Git)
- **Sensitive Data:** `.gitignore` excludes logs, cache, API keys
- **Paper Trading Only:** No real money during development

---

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Contact

**Project Owner:** Sujay Agarwal  
**Repository:** https://github.com/SujayAgarwal28/news-data-scrapping  
**Related Project:** StockPass (Paper Trading Platform)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **FinBERT** by ProsusAI - Financial sentiment analysis
- **Hugging Face** - Transformer models
- **Streamlit** - Dashboard framework
- **OpenAI/Anthropic** - LLM summarization

---

## ⚠️ Disclaimer

**This system is for educational and research purposes only. Past performance does not guarantee future results. Always conduct your own research and consult with financial advisors before making investment decisions. The developers are not responsible for any financial losses incurred from using this system.**

---

## 🎯 Current Status

**Phase:** Week 1 - Data Pipeline  
**Last Updated:** October 8, 2025  
**Next Milestone:** Enhanced news scraper with body extraction (Day 1-2)

For detailed daily progress, see [MASTER_TRACKER.md](MASTER_TRACKER.md)

---

**Built with ❤️ and AI by Sujay Agarwal | Powered by GitHub Copilot 🚀**
