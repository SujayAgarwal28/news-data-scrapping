# 🎨 StockBus - Trade Pulse Dashboard Specification

> **Dashboard Name:** StockBus Trade Pulse Analytics  
> **Framework:** Streamlit (Python)  
> **Theme:** Professional financial dashboard with dark mode support  
> **Target Users:** Traders, analysts, project stakeholders

---

## 🌟 Dashboard Features Overview

### Core Capabilities:
- ✅ **Real-time Market Analysis:** Live Nifty 50 data and predictions
- ✅ **Historical Data Exploration:** Browse 2018-2025 news and sentiment
- ✅ **Interactive Visualizations:** Zoom, filter, export charts
- ✅ **AI-Powered Insights:** LLM-generated market explanations
- ✅ **Performance Tracking:** Backtesting results and live trading metrics
- ✅ **News Intelligence:** View original articles, summaries, and sentiment scores
- ✅ **Trading Integration:** Monitor StockPass bot activity

---

## 📄 Page-by-Page Specifications

### Page 1: 🏠 Overview Dashboard

**Purpose:** High-level snapshot of current market status and system performance

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  STOCKBUS - TRADE PULSE ANALYTICS          [Dark Mode Toggle]│
│  Last Updated: Oct 8, 2025, 10:35 AM IST     [Refresh Button]│
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Nifty 50 │  │Sentiment │  │Prediction│  │Bot Status│   │
│  │  24,850  │  │   +72    │  │  ↑ +1.2%│  │  ACTIVE  │   │
│  │  +0.8%   │  │ Positive │  │ 5 Days   │  │ Running  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  NIFTY 50 PRICE & PREDICTION (Last 30 Days)            ││
│  │  [Interactive Plotly Chart]                             ││
│  │  • Blue line: Actual Nifty price                        ││
│  │  • Green overlay: Sentiment score (right axis)          ││
│  │  • Orange dashed: 5-day prediction forecast             ││
│  │  • Shaded area: Confidence interval                     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Quick Stats                        System Health            │
│  ─────────────────────────────────  ──────────────────────  │
│  📰 Articles Today: 24               ✅ Scraper: Online      │
│  📊 Accuracy (30d): 64%              ✅ Model: Loaded        │
│  💰 Backtest Return: +28.5%          ✅ Database: Connected  │
│  📈 Active Position: Long 50 units   ✅ Pipeline: Running    │
│                                                               │
│  Latest News Headlines (Top 5)                               │
│  ───────────────────────────────────────────────────────────│
│  1. [+0.85] FII inflows surge to ₹5,200cr...  [View]       │
│  2. [+0.62] IT sector earnings beat estimates... [View]     │
│  3. [-0.45] RBI maintains hawkish stance...     [View]      │
│  4. [+0.51] Infrastructure spending up 15%...   [View]      │
│  5. [+0.38] Global markets rally on Fed data... [View]      │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Metric Cards (Top Row):**
   - Nifty 50: Current value, % change, color-coded (green/red)
   - Sentiment: Score (0-100), label (Positive/Neutral/Negative)
   - Prediction: Direction arrow, magnitude, timeframe
   - Bot Status: Active/Paused with colored indicator

2. **Main Chart:**
   - Dual-axis Plotly chart (price + sentiment)
   - Tooltips showing exact values on hover
   - Zoom and pan controls
   - Date range selector

3. **Quick Stats Grid:**
   - Key metrics in compact format
   - Auto-updating values
   - Links to detailed pages

4. **System Health:**
   - Component status indicators
   - Last update times
   - Error alerts if any

5. **Top News Headlines:**
   - Sentiment score prefix [+0.85]
   - Truncated headline with "View" link
   - Sorted by relevance/sentiment strength

---

### Page 2: 📰 News Analysis

**Purpose:** Deep dive into news articles, summaries, and sentiment analysis

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  📰 NEWS ANALYSIS                                            │
├─────────────────────────────────────────────────────────────┤
│  Filter Options:                                             │
│  Date Range: [Oct 1, 2025] to [Oct 8, 2025]                │
│  Sentiment: [All ▼] [Positive/Neutral/Negative]            │
│  Source: [All ▼] [Economic Times/Moneycontrol/...]         │
│  Search: [________________________]  [Search Button]        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 News Statistics (This Period)                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │Articles/Day│  │Source Dist.│  │Sentiment   │            │
│  │[Line Chart]│  │[Pie Chart] │  │[Bar Chart] │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                               │
│  📋 News Articles Table                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │Date    │Headline               │Source  │Sentiment│...│  │
│  ├───────────────────────────────────────────────────────┤  │
│  │Oct 8   │FII inflows surge...   │ET      │+0.85    │[▼]│  │
│  │  └─ Summary: • Point 1: FII investments increased...   │  │
│  │            • Point 2: Market sentiment positive...     │  │
│  │            • Point 3: Banking sector leading...        │  │
│  │            [View Full Article] [View Original Body]    │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │Oct 8   │IT sector earnings...  │MC      │+0.62    │[▼]│  │
│  │Oct 7   │RBI policy unchanged...│BS      │-0.45    │[▼]│  │
│  │...     │...                    │...     │...      │...│  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  Pagination: [< Previous]  Page 1 of 12  [Next >]          │
│  Export: [Download as CSV] [Download as Excel]              │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Filters:**
   - Date range picker (calendar widget)
   - Dropdown for sentiment filter
   - Dropdown for source filter
   - Search box (searches headlines and summaries)

2. **Statistics Charts:**
   - Articles per day: Line chart showing volume trends
   - Source distribution: Pie chart of news sources
   - Sentiment distribution: Stacked bar chart (positive/neutral/negative over time)

3. **Articles Table:**
   - Sortable columns (date, sentiment, source)
   - Expandable rows (click to show summary)
   - Summary: LLM-generated 5-10 bullet points
   - Links to view full article body
   - Color-coded sentiment scores

4. **Pagination & Export:**
   - Handle thousands of articles
   - Export filtered results to CSV/Excel

---

### Page 3: 📈 Sentiment Trends

**Purpose:** Visualize sentiment evolution and correlation with market movements

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  📈 SENTIMENT TRENDS ANALYSIS                                │
├─────────────────────────────────────────────────────────────┤
│  Time Period: [Last 30 Days ▼] [Custom Range]              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Sentiment & Price Over Time                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Interactive dual-axis chart]                           ││
│  │ • Left axis: Nifty 50 price (line)                      ││
│  │ • Right axis: Daily sentiment score (area chart)        ││
│  │ • Hover for exact values                                ││
│  │ • Click to highlight major events                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  🔗 Correlation Analysis                                     │
│  ┌─────────────┐  ┌──────────────────────────────────────┐ │
│  │Correlation  │  │ Sentiment vs Returns (Scatter Plot)  │ │
│  │Heatmap      │  │ • X-axis: Sentiment score            │ │
│  │             │  │ • Y-axis: Next-day return %          │ │
│  │Sentiment vs:│  │ • Color: Density of points           │ │
│  │• Same Day   │  │ • Regression line overlay            │ │
│  │• +1 Day     │  │                                       │ │
│  │• +3 Days    │  └──────────────────────────────────────┘ │
│  │• +5 Days    │                                            │
│  │• +7 Days    │  📊 Sentiment Breakdown                   │
│  └─────────────┘  ┌──────────────────────────────────────┐ │
│                    │ Positive: 58% ██████████████▓▓▓▓▓▓  │ │
│  Correlation      │ Neutral:  28% ███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │
│  Metrics:          │ Negative: 14% ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │
│  ─────────────    └──────────────────────────────────────┘ │
│  Best Lag: 1 day                                            │
│  Correlation: 0.38  📈 Sentiment Strength Distribution     │
│  P-value: 0.002    ┌──────────────────────────────────────┐ │
│  (Significant!)    │ [Histogram of sentiment scores]      │ │
│                    │ Shows distribution shape              │ │
│                    └──────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Time Series Chart:**
   - Dual-axis: Price (left) + Sentiment (right)
   - Interactive zoom and pan
   - Highlight significant events (earnings, policy decisions)
   - Customizable date ranges

2. **Correlation Heatmap:**
   - Shows correlation between sentiment and future returns
   - Different time lags (0, 1, 3, 5, 7 days)
   - Color-coded strength (dark = strong correlation)

3. **Scatter Plot:**
   - Sentiment score vs. next-day return
   - Regression line to show relationship
   - Density coloring for overlapping points

4. **Sentiment Breakdown:**
   - Horizontal bar chart showing distribution
   - Percentage of positive/neutral/negative articles
   - Updated based on selected time period

5. **Sentiment Strength:**
   - Histogram showing distribution of sentiment scores
   - Helps understand data quality and extremes

---

### Page 4: 🔮 Predictions

**Purpose:** Display current predictions, historical accuracy, and AI reasoning

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  🔮 NIFTY 50 PREDICTIONS                                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📍 CURRENT PREDICTION                                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Prediction for: Next 5 Trading Days                    ││
│  │  Generated: Oct 8, 2025, 8:15 AM IST                    ││
│  │                                                           ││
│  │         ┌────────────────────────────────┐              ││
│  │         │     ↑  BULLISH                 │              ││
│  │         │                                 │              ││
│  │         │  Expected Change: +1.2% to +1.8%│             ││
│  │         │  Target: 25,150 - 25,300        │              ││
│  │         │                                 │              ││
│  │         │  Confidence: ████████░░  82%    │              ││
│  │         └────────────────────────────────┘              ││
│  │                                                           ││
│  │  🤖 AI REASONING:                                        ││
│  │  The model predicts a bullish move based on:            ││
│  │  • Strong positive sentiment (72/100) from recent news  ││
│  │  • FII inflows surged by ₹5,200 crores this week       ││
│  │  • IT sector earnings beat estimates by 8%              ││
│  │  • Technical indicators show RSI at 58 (neutral-bull)   ││
│  │  • Global markets rallied on positive Fed data          ││
│  │                                                           ││
│  │  Key Risks:                                              ││
│  │  • RBI policy meeting next week (uncertainty)           ││
│  │  • Global crude oil prices remain volatile              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📊 PREDICTION VISUALIZATION                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Candlestick chart with forecast]                       ││
│  │ • Historical prices (last 30 days)                      ││
│  │ • Predicted range (shaded cone)                         ││
│  │ • Multiple timeframes (1/3/5/7 days)                    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📜 PREDICTION HISTORY                                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │Date     │Predicted│Actual  │Accuracy│Confidence│Status │││
│  ├─────────────────────────────────────────────────────────┤││
│  │Oct 7    │+0.8%    │+0.9%   │✓ Correct│85%      │Closed│││
│  │Oct 6    │+1.2%    │-0.3%   │✗ Wrong  │72%      │Closed│││
│  │Oct 5    │-0.5%    │-0.7%   │✓ Correct│90%      │Closed│││
│  │Oct 4    │+0.6%    │+0.4%   │✓ Correct│68%      │Closed│││
│  │...      │...      │...     │...      │...      │...   │││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📈 Accuracy Metrics (Last 30 Days)                          │
│  • Directional Accuracy: 64% (19/30 correct)                │
│  • Mean Absolute Error: 0.45%                               │
│  • Correlation: 0.42 (moderate positive)                    │
│                                                               │
│  [Download Predictions CSV] [View Model Details]            │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Current Prediction Card:**
   - Large, prominent display
   - Direction indicator (↑ Bullish / ↓ Bearish)
   - Expected change range
   - Confidence score with visual bar
   - Generation timestamp

2. **AI Reasoning:**
   - LLM-generated natural language explanation
   - Bullet points for key factors
   - Risk section
   - Easy to read and understand

3. **Forecast Visualization:**
   - Candlestick chart of recent price action
   - Prediction cone showing expected range
   - Multiple timeframe overlays
   - Interactive (zoom, hover)

4. **Prediction History Table:**
   - Date, predicted value, actual value
   - Accuracy indicator (✓/✗)
   - Confidence scores
   - Sortable and filterable

5. **Accuracy Metrics:**
   - Overall success rate
   - MAE (Mean Absolute Error)
   - Correlation coefficient
   - Time-series chart of accuracy over time

---

### Page 5: 🔬 Backtesting Results

**Purpose:** Demonstrate historical performance and validate strategy

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  🔬 BACKTESTING RESULTS                                      │
├─────────────────────────────────────────────────────────────┤
│  Backtest Period: Jan 1, 2018 - Dec 31, 2024 (7 years)     │
│  Strategy: Sentiment-Based Directional Trading              │
│  Initial Capital: ₹10,00,000                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🏆 PERFORMANCE SUMMARY                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │Final Value   │ │Total Return  │ │Annual Return │        │
│  │₹15,45,000    │ │+54.5%        │ │+7.8%         │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │Sharpe Ratio  │ │Max Drawdown  │ │Win Rate      │        │
│  │1.45          │ │-12.3%        │ │62%           │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
│  📈 EQUITY CURVE                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Line chart]                                             ││
│  │ • Blue: Strategy portfolio value                        ││
│  │ • Gray: Buy-and-hold Nifty 50                           ││
│  │ • Shaded: Drawdown periods                              ││
│  │ • Annotations: Major market events                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📊 COMPARISON: Strategy vs. Benchmark                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Metric              │ Strategy │ Buy & Hold │ Difference│││
│  ├─────────────────────────────────────────────────────────┤││
│  │ Total Return        │ +54.5%   │ +48.2%     │ +6.3%    │││
│  │ Annualized Return   │ +7.8%    │ +7.0%      │ +0.8%    │││
│  │ Sharpe Ratio        │ 1.45     │ 1.15       │ +0.30    │││
│  │ Max Drawdown        │ -12.3%   │ -18.5%     │ +6.2%    │││
│  │ Volatility          │ 14.2%    │ 16.8%      │ -2.6%    │││
│  │ Number of Trades    │ 145      │ 0          │ -        │││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📅 MONTHLY RETURNS HEATMAP                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │       Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct...│││
│  │ 2018  +2.1 -0.5 +1.8 +0.9 -1.2 +3.4 +1.5 -0.8 +2.3 +1.1..│││
│  │ 2019  +1.5 +2.8 -0.3 +1.2 +0.8 +2.1 -1.5 +1.9 +0.5 +2.7..│││
│  │ 2020  -2.1 -1.8 -8.5 +4.2 +3.8 +5.1 +2.4 +3.6 +1.2 +2.8..│││
│  │ ...                                                       ││
│  │ (Color-coded: green = positive, red = negative)          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📊 TRADE ANALYSIS                                           │
│  ┌──────────────┐  ┌──────────────────────────────────────┐ │
│  │Win/Loss Dist.│  │ Trade Details                        │ │
│  │[Pie Chart]   │  │ • Total Trades: 145                  │ │
│  │ Wins: 62%    │  │ • Average Win: +2.3%                 │ │
│  │ Losses: 38%  │  │ • Average Loss: -1.1%                │ │
│  └──────────────┘  │ • Profit Factor: 1.95                │ │
│                    │ • Avg Hold Time: 4.8 days            │ │
│                    └──────────────────────────────────────┘ │
│                                                               │
│  [Download Backtest Report] [View Trade Log] [Run New Test] │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Performance Summary Cards:**
   - Key metrics in large, easy-to-read format
   - Color-coded (green for good, red for bad)
   - Comparison indicators vs. benchmark

2. **Equity Curve:**
   - Shows portfolio value over time
   - Overlays buy-and-hold benchmark
   - Highlights drawdown periods (shaded)
   - Annotations for major events (COVID crash, etc.)

3. **Comparison Table:**
   - Strategy vs. buy-and-hold side-by-side
   - All important metrics
   - Difference column to show alpha

4. **Monthly Returns Heatmap:**
   - Grid layout (year × month)
   - Color intensity shows magnitude
   - Easy to spot patterns and seasonality

5. **Trade Analysis:**
   - Win/loss distribution pie chart
   - Trade statistics table
   - Profit factor and average hold time

6. **Export Options:**
   - Download full backtest report as PDF
   - Export trade log as CSV
   - Re-run backtest with different parameters

---

### Page 6: 🤖 Live Trading (StockPass Integration)

**Purpose:** Monitor live trading bot performance and control settings

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 LIVE TRADING - STOCKPASS INTEGRATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🚦 BOT STATUS                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Status: ● ACTIVE                     [⏸ Pause Bot]    ││
│  │  Last Update: Oct 8, 2025, 10:32 AM IST                ││
│  │  Uptime: 45 days, 12 hours                             ││
│  │  Next Action: 9:00 AM tomorrow (pre-market)            ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  💼 CURRENT POSITIONS                                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │Symbol  │Qty│Entry Price│Current│P&L    │P&L%   │Action │││
│  ├─────────────────────────────────────────────────────────┤││
│  │NIFTY50 │50 │24,680     │24,850 │+₹8,500│+0.69% │[Close]│││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📊 PERFORMANCE METRICS                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │Today's P&L   │ │Week's P&L    │ │Month's P&L   │        │
│  │+₹8,500       │ │+₹12,300      │ │+₹45,600      │        │
│  │(+0.85%)      │ │(+1.23%)      │ │(+4.56%)      │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │Total Return  │ │Win Rate      │ │Sharpe Ratio  │        │
│  │+₹1,25,000    │ │61%           │ │1.38          │        │
│  │(+12.5%)      │ │(14/23 trades)│ │              │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
│  📈 EQUITY CURVE (Live Trading Period)                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Line chart showing portfolio value since bot start]    ││
│  │ Started: Aug 25, 2025 with ₹10,00,000                   ││
│  │ Current: ₹11,25,000                                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📜 RECENT TRADES (Last 10)                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │Date  │Action│Price │Qty│P&L     │Reason                │││
│  ├─────────────────────────────────────────────────────────┤││
│  │Oct 7 │SELL  │24,680│50 │+₹3,200 │Target reached        │││
│  │Oct 5 │BUY   │24,616│50 │-       │Bullish sentiment     │││
│  │Oct 3 │SELL  │24,520│50 │+₹1,850 │Prediction reversed   │││
│  │Oct 2 │BUY   │24,483│50 │-       │Strong positive news  │││
│  │Sep 30│SELL  │24,350│50 │-₹850   │Stop loss triggered   │││
│  │...   │...   │...   │.. │...     │...                   │││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ⚙️ RISK MANAGEMENT                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ • Current Position Size: 50 units (5% of capital)       ││
│  │ • Available Capital: ₹10,75,000                         ││
│  │ • Daily Loss Limit: ₹20,000 (Used: ₹0 / 0%)            ││
│  │ • Weekly Loss Limit: ₹50,000 (Used: ₹0 / 0%)           ││
│  │ • Max Position Size: 30% of capital                     ││
│  │ • Stop Loss: 2% per trade                               ││
│  │ • Take Profit: 5% per trade                             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  🎛️ BOT CONTROLS                                             │
│  [⏸ Pause Bot] [▶ Resume Bot] [🔄 Manual Refresh]          │
│  [⚙️ Adjust Settings] [📊 View Full Trade Log]              │
│                                                               │
│  🔔 ALERTS & NOTIFICATIONS                                   │
│  • Oct 8, 10:30 AM: Position opened - Bought 50 @ 24,680   │
│  • Oct 7, 3:15 PM: Position closed - Profit of ₹3,200      │
│  • Oct 6, 9:00 AM: High confidence prediction (85%)         │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Bot Status Card:**
   - Active/paused indicator with colored dot
   - Last update timestamp
   - Uptime counter
   - Next scheduled action
   - Pause/resume button

2. **Current Positions Table:**
   - Symbol, quantity, entry price
   - Current price and unrealized P&L
   - Quick close button for manual intervention

3. **Performance Metrics:**
   - Today/week/month P&L in rupees and percentage
   - Total return since bot started
   - Win rate and Sharpe ratio
   - Large, color-coded cards

4. **Live Equity Curve:**
   - Portfolio value over time (since bot activation)
   - Shows growth trajectory
   - Annotations for major trades

5. **Recent Trades Table:**
   - Last 10 trades with details
   - Date, action, price, quantity, P&L
   - Reason for trade (from AI logic)

6. **Risk Management Panel:**
   - Current position size
   - Available capital
   - Loss limits and usage
   - Stop-loss and take-profit levels
   - Visual progress bars for limits

7. **Bot Controls:**
   - Pause/resume buttons
   - Manual refresh
   - Settings adjustment link
   - Full trade log viewer

8. **Alerts Feed:**
   - Real-time notifications
   - Trade executions
   - Important events
   - System messages

---

## 🎨 Design Specifications

### Color Scheme:
```css
/* Light Mode */
Primary: #1E3A8A (Deep Blue)
Secondary: #10B981 (Green - Bullish)
Accent: #EF4444 (Red - Bearish)
Background: #F9FAFB (Light Gray)
Text: #111827 (Dark Gray)

/* Dark Mode */
Primary: #3B82F6 (Bright Blue)
Secondary: #34D399 (Light Green)
Accent: #F87171 (Light Red)
Background: #111827 (Dark Gray)
Text: #F9FAFB (Light Gray)
```

### Typography:
- **Headers:** Inter, 24-32px, Bold
- **Body:** Inter, 14-16px, Regular
- **Numbers:** JetBrains Mono, 16-20px, Medium (for metrics)
- **Tables:** Inter, 13-14px, Regular

### Component Library:
- **Charts:** Plotly (interactive, professional)
- **Tables:** Streamlit AgGrid (sortable, filterable)
- **Cards:** Custom Streamlit components with shadows
- **Buttons:** Streamlit native with custom CSS

---

## 🚀 Technical Implementation

### Streamlit Structure:
```python
# src/dashboard/app.py
import streamlit as st

st.set_page_config(
    page_title="StockBus - Trade Pulse Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview", "📰 News Analysis", "📈 Sentiment Trends",
     "🔮 Predictions", "🔬 Backtesting", "🤖 Live Trading"]
)

# Load page
if page == "🏠 Overview":
    from pages import overview
    overview.render()
elif page == "📰 News Analysis":
    from pages import news_analysis
    news_analysis.render()
# ... etc
```

### Data Loading:
- **Cache data** using `@st.cache_data` to avoid reloading
- **Lazy loading** for large datasets
- **Incremental updates** for real-time data
- **Background workers** for heavy computations

### Interactivity:
- **Filters persist** across sessions (using `st.session_state`)
- **Real-time updates** every 5 minutes during market hours
- **Responsive design** works on tablets and phones
- **Export functionality** for all tables and charts

---

## 📱 Mobile Responsiveness

### Optimizations:
- Single-column layout on mobile
- Collapsible sections for long content
- Touch-friendly buttons and controls
- Simplified charts for small screens
- Hamburger menu for navigation

---

## 🔒 Security & Access Control

### Features:
- **Password protection** for dashboard access
- **API key management** stored in `.env` file
- **Read-only mode** for stakeholders (no trading controls)
- **Admin mode** for full access (trading + settings)

---

## 📊 Performance Targets

### Load Times:
- Initial page load: <3 seconds
- Chart rendering: <1 second
- Data refresh: <2 seconds
- Filter application: <500ms

### Data Handling:
- Support 10,000+ news articles
- Handle 2,000+ predictions
- Display 500+ trades
- Real-time updates without lag

---

## 🎯 Success Metrics

### User Experience:
- **Intuitive navigation:** Find any info in <3 clicks
- **Visual clarity:** All charts labeled and easy to read
- **Actionable insights:** Clear what to do based on data
- **Professional appearance:** Suitable for stakeholder presentations

### Technical:
- **99%+ uptime**
- **<3 second load times**
- **Mobile responsive**
- **Cross-browser compatible** (Chrome, Firefox, Safari, Edge)

---

## 🛠️ Development Roadmap

### Phase 1 (Day 28): Core Dashboard
- Set up Streamlit
- Create 6 basic pages with placeholders
- Implement navigation
- Add basic styling

### Phase 2 (Day 28 continued): Data Integration
- Connect to data sources
- Load news, sentiment, predictions
- Display in tables and charts
- Test with real data

### Phase 3 (Day 28-29): Visualizations
- Build all Plotly charts
- Add interactivity (filters, zoom)
- Implement export functionality
- Optimize performance

### Phase 4 (Day 29): Polish & Testing
- Refine UI/UX
- Add dark mode
- Mobile responsiveness
- Bug fixes

---

**This dashboard will be the centerpiece of your project presentation, showcasing all the hard work in an intuitive, professional interface! 🎨📊🚀**
