# 🚀 INTERACTIVE NEWS SCRAPER - USER GUIDE

**Simple menu-driven scraping with NO complex commands!**

---

## 🎯 **Quick Start (30 Seconds)**

### Windows:
1. Double-click: `START_SCRAPER.bat`
2. Choose option from menu
3. Done! 🎉

### Command Line:
```powershell
cd src/scraping
python interactive_scraper.py
```

---

## 📋 **MAIN MENU OPTIONS**

### **1. 📰 Scrape News**
Start a new scraping session with guided options:

#### **Option 1: Quick Scrape (Last 30 Days)**
- Perfect for testing or recent news only
- Fast: ~5-10 minutes
- ~300-500 articles

#### **Option 2: Custom Date Range**
- Enter dates in simple format: `DD/MM/YYYY`
- Example: `01/01/2024` to `31/12/2024`
- Automatically suggests parallel jobs for large ranges

#### **Option 3: Full Dataset (2018 to Today) ⭐ RECOMMENDED**
- **Best for accuracy!** More data = Better predictions
- ~7 years of historical news
- ~15,000-25,000 articles
- Parallel processing options:
  - **Conservative** (4 jobs): ~3-4 hours
  - **Balanced** (8 jobs): ~2 hours  ⭐ Recommended
  - **Fast** (12 jobs): ~1.5 hours
  - **Maximum** (16 jobs): ~1 hour

---

### **2. 🔄 Merge All Scraped Data**
- Combines all JSON files into one dataset
- Removes duplicates automatically
- Creates: `data/datasets/complete_dataset.json`
- **Run this after scraping completes!**

---

### **3. 📊 Generate Quality Report**
- Analyzes dataset quality (0-100 score)
- Shows metrics: completeness, duplicates, errors
- Helps validate data before training

---

### **4. 📂 View Scraping Status**
- See how many articles scraped
- Check file locations
- Monitor progress

---

### **5. ⚙️ Advanced Options**
- View/clear cache
- Check logs
- Configure settings

---

## 🎬 **TYPICAL WORKFLOW**

### **Scenario 1: Maximum Accuracy (Recommended)**
```
1. Choose Option 1: Scrape News
   → Option 3: Full Dataset (2018 to Today)
   → Select mode 2: Balanced (8 parallel jobs)
   → Confirm and start

2. Wait ~2 hours for scraping to complete
   (You can close terminal, jobs run in background)

3. Choose Option 2: Merge All Scraped Data
   → Confirm

4. Choose Option 3: Generate Quality Report
   → Review quality score

✅ Done! You now have ~20,000 articles ready for FinBERT!
```

---

### **Scenario 2: Quick Test**
```
1. Choose Option 1: Scrape News
   → Option 1: Quick Scrape (Last 30 Days)
   → Confirm

2. Wait ~10 minutes

3. Choose Option 2: Merge All Scraped Data

✅ Done! ~500 articles for testing
```

---

### **Scenario 3: Custom Range (e.g., 2024 only)**
```
1. Choose Option 1: Scrape News
   → Option 2: Custom Date Range
   → Start: 01/01/2024
   → End: 31/12/2024
   → Parallel jobs: 4
   → Confirm

2. Wait ~1 hour

3. Choose Option 2: Merge All Scraped Data

✅ Done! ~3,000 articles from 2024
```

---

## 📅 **DATE FORMAT EXAMPLES**

**Always use: DD/MM/YYYY**

✅ Correct:
- `01/01/2018`
- `15/06/2024`
- `31/12/2025`

❌ Wrong:
- `2024-01-01` (use DD/MM/YYYY)
- `1/1/2024` (need leading zeros)
- `01-01-2024` (use slashes)

---

## ⚡ **PARALLEL PROCESSING EXPLAINED**

When scraping large date ranges (>90 days), the script offers parallel jobs:

### **How It Works:**
```
Single Job (1):
  2018-2025 → [==================] 4 hours

4 Parallel Jobs:
  2018-2020 → [=====] 1 hour
  2020-2022 → [=====] 1 hour
  2022-2024 → [=====] 1 hour
  2024-2025 → [=====] 1 hour
  Total: ~1 hour (4x faster!)
```

### **Recommendations:**
- **1-90 days:** 1 job (simple)
- **90-365 days:** 4 jobs
- **1-3 years:** 8 jobs ⭐
- **3-7 years:** 12-16 jobs

---

## 🛡️ **SMART FEATURES**

### **Automatic Caching**
- Remembers scraped URLs
- Won't re-scrape duplicates
- Saves time and API calls

### **Resume on Failure**
- If scraping stops, just run again
- Cache prevents duplicate work
- Picks up where it left off

### **Quality Validation**
- Filters clickbait automatically
- Removes spam/ads
- Extracts clean article text

### **Progress Tracking**
- Real-time progress bars
- Shows articles scraped
- Estimates time remaining

---

## 📂 **WHERE DATA IS SAVED**

```
data/
├── raw/
│   └── news/
│       ├── indian_stock_market_news_20180101_to_20181209.json
│       ├── bse_sensex_india_stock_market_20180101_to_20181209.json
│       └── ... (many files)
│
└── datasets/
    └── complete_dataset.json  ← Merged final dataset
```

---

## ❓ **COMMON QUESTIONS**

### **Q: How long does full scraping take?**
**A:** With 8 parallel jobs: ~2 hours for 2018-2025

### **Q: Can I close the terminal?**
**A:** Yes! If you run parallel jobs, they open in separate windows. You can close the main terminal.

### **Q: What if scraping fails?**
**A:** Just run again! Cache prevents re-scraping. Pick option 2 to merge whatever was scraped.

### **Q: How many articles will I get?**
**A:** 
- Last 30 days: ~300-500
- 2024 only: ~3,000
- 2018-2025: ~15,000-25,000

### **Q: Why scrape from 2018?**
**A:** More data = Better FinBERT accuracy! Captures different market cycles.

### **Q: Can I scrape specific topics?**
**A:** Currently scrapes 4 main topics automatically:
- Nifty 50 stock market
- BSE Sensex
- Indian stock market news
- NSE India trading

### **Q: How much disk space needed?**
**A:** ~500MB for full dataset (2018-2025)

---

## 🎯 **NEXT STEPS AFTER SCRAPING**

1. ✅ Scrape news (option 1)
2. ✅ Merge data (option 2)
3. ✅ Generate quality report (option 3)
4. ➡️ Run LLM summarization:
   ```powershell
   python src/processing/parallel_summarizer.py
   ```
5. ➡️ Prepare FinBERT input:
   ```powershell
   python src/processing/prepare_finbert.py
   ```
6. ➡️ Continue to Day 4: FinBERT sentiment analysis

---

## 🆘 **TROUBLESHOOTING**

### **Error: "No module named selenium"**
```powershell
pip install selenium webdriver-manager gnews newspaper3k
```

### **Error: "ChromeDriver not found"**
The script auto-downloads ChromeDriver. If it fails:
```powershell
pip install --upgrade webdriver-manager
```

### **Scraping is very slow**
- Use more parallel jobs (8-16)
- Check internet connection
- Some news sites may be rate-limiting

### **Getting 0 articles**
- Check date range (not in future)
- Verify internet connection
- Try different date range

---

## 📞 **SUPPORT**

- Check logs: `src/scraping/logs/`
- View cache: Option 5 → Option 2
- Clear cache if issues: Option 5 → Option 3

---

**Ready to scrape?** Run `START_SCRAPER.bat` or `python interactive_scraper.py` 🚀

**Recommended first run:** Option 1 → Option 3 (Full Dataset, 8 jobs, ~2 hours)

This gives you maximum accuracy for your trading system! 📈
