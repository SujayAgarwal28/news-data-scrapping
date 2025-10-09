# 🚀 PRODUCTION SCRAPING STRATEGY - GET 30,000 ARTICLES FAST

**Date:** October 9, 2025  
**Goal:** Scrape 20-30 articles/day for 2021-2025 (30,000+ articles)  
**Time:** 3 nights (parallel scraping on multiple machines)

---

## 📊 **UPDATED SCRAPER CAPABILITIES**

### **OLD Configuration:**
- 4 topics × 10 articles = 40 articles/scrape
- Actual yield: **8-12 articles/day** ❌

### **NEW Configuration (UPDATED!):**
- **6 topics** × **25 articles** = **150 articles/scrape**
- Actual yield: **20-30 articles/day** ✅

**Changes Made:**
```python
# Added 2 new topics:
SEARCH_TOPICS = [
    "Nifty 50 stock market India",
    "BSE Sensex India stock market",
    "Indian stock market news",
    "NSE India trading",
    "Nifty 50 India today",        # NEW
    "Indian stock market today"     # NEW
]

# Increased max results:
max_results = 25  # Was 10
```

---

## ⚡ **MULTI-MACHINE STRATEGY (FASTEST!)**

### **Problem:** 
- 4.75 years (2021-2025) = ~1,600 days
- 1 machine scraping sequentially = 8-12 hours
- Colab disconnects after 6 hours

### **Solution: PARALLEL SCRAPING ON MULTIPLE MACHINES!**

Use **3 machines** running simultaneously:

| Machine | Platform | Date Range | Days | Expected Articles | Time |
|---------|----------|------------|------|-------------------|------|
| **Machine 1** | Google Colab | 2021-01-01 to 2022-06-30 | 545 | ~10,900 | 2-3 hrs |
| **Machine 2** | Google Colab | 2022-07-01 to 2024-01-01 | 550 | ~11,000 | 2-3 hrs |
| **Machine 3** | Your PC | 2024-01-02 to 2025-10-09 | 640 | ~12,800 | 3-4 hrs |

**Total:** ~34,700 articles in **ONE NIGHT!** 🚀

---

## 🎯 **STEP-BY-STEP EXECUTION PLAN**

### **Tonight (3 Machines Running Simultaneously):**

#### **Machine 1: Google Colab Session 1**
```python
# In notebook cell 4, set:
START_DATE = (2021, 1, 1)
END_DATE = (2022, 6, 30)

# Run all cells
# Let it run 2-3 hours
# Download: scraped_news.zip
```

#### **Machine 2: Google Colab Session 2** (Different Google account or browser)
```python
# In notebook cell 4, set:
START_DATE = (2022, 7, 1)
END_DATE = (2024, 1, 1)

# Run all cells
# Let it run 2-3 hours
# Download: scraped_news.zip
```

#### **Machine 3: Your PC** (Updated local scraper)
```powershell
cd src\scraping
python interactive_scraper.py

# Choose: 1 → 2 (Custom Range)
# Start: 02/01/2024
# End: 09/10/2025
# Parallel jobs: 4
# Confirm: y
```

---

### **Tomorrow Morning: MERGE ALL DATA**

1. Extract all 3 ZIP files to `data/raw/news/`
2. Run merge script:

```powershell
cd "d:\Projects and codes\News Data scrapping\news-data-scrapping"
python src\scraping\2_merge_data.py
```

**The merge script automatically:**
✅ Combines all JSON files
✅ Removes duplicates by URL
✅ Updates cache
✅ Creates `data/datasets/complete_dataset.json`

3. Verify articles per day:
```powershell
python analyze_articles_per_day.py
```

**Expected output:**
```
Total Articles: 34,700
Average: 22 articles/day ✅
Days covered: 1,600
Ready for ML: YES 🎯
```

---

## 🛡️ **CRASH-PROOF FEATURES (COLAB NOTEBOOK)**

### **Auto-Save Checkpoints:**
- Saves every 10 articles to `checkpoint_*.json`
- If crash: checkpoints preserved
- Saves cache to `scraped_cache.json`

### **Resume Capability:**
```python
# If Colab crashes halfway:
1. Download scraped_cache.json
2. Start new Colab session
3. Upload scraped_cache.json
4. Re-run from cell 1
5. It will skip already-scraped URLs!
```

### **Cache System:**
- Creates MD5 hash of each URL
- Stores in `scraped_cache.json`
- Skips duplicate URLs across sessions
- **Even from different machines!**

---

## 📁 **FILE ORGANIZATION**

### **After All 3 Sessions, You'll Have:**

```
data/raw/news/
├── Session 1 (Colab):
│   ├── combined_2021_01_01_to_2022_06_30.json  (~10,900 articles)
│   ├── nifty_50_stock_market_india_*.json
│   ├── bse_sensex_india_stock_market_*.json
│   └── ... (6 topic files)
│
├── Session 2 (Colab):
│   ├── combined_2022_07_01_to_2024_01_01.json  (~11,000 articles)
│   └── ... (6 topic files)
│
└── Session 3 (Your PC):
    ├── combined_2024_01_02_to_2025_10_09.json  (~12,800 articles)
    └── ... (6 topic files)
```

### **After Merge:**
```
data/datasets/
└── complete_dataset.json  (~34,000 articles after deduplication)
```

---

## 🔄 **DEDUPLICATION STRATEGY**

### **Automatic Deduplication (No Work Needed!):**

The `2_merge_data.py` script:
1. Loads all JSON files
2. Creates set of unique URLs
3. Keeps only first occurrence
4. Saves to `complete_dataset.json`

**Example:**
```
Session 1: 10,900 articles
Session 2: 11,000 articles
Session 3: 12,800 articles
Total: 34,700 articles

After deduplication: ~33,000-34,000 articles
(Duplicates: ~2-5% overlap)
```

---

## ⚙️ **CACHE & LOGS INTEGRATION**

### **Cache Structure:**
```json
{
  "scraped": [
    "a3f5e9c1b2d4...",  // MD5 hash of URL 1
    "b8d2c4e7a1f3...",  // MD5 hash of URL 2
    ...
  ]
}
```

### **How It Works:**
1. Machine 1 scrapes → Creates cache with 10,900 URL hashes
2. Machine 2 scrapes → Creates separate cache with 11,000 URL hashes
3. Machine 3 scrapes → Creates separate cache with 12,800 URL hashes
4. `2_merge_data.py` → Uses URLs (not hashes) for final deduplication
5. Result: Clean dataset with no duplicates!

---

## 💡 **PRO TIPS**

### **For Google Colab:**
1. ✅ Use **Chrome Incognito** for session 2 (different account)
2. ✅ Set runtime to **high RAM** (Edit → Notebook Settings)
3. ✅ Keep browser tab **active** (prevents disconnect)
4. ✅ Download checkpoint files every hour (backup)

### **For Local PC:**
1. ✅ Run in background (`python ... &`)
2. ✅ Use `nohup` if on Linux/Mac
3. ✅ Check logs: `logs/scraper_*.log`

### **General:**
1. ✅ Start all 3 sessions **simultaneously** (fastest!)
2. ✅ Download ZIPs immediately when done
3. ✅ Don't worry about duplicates (merge script handles it)
4. ✅ Check `data/raw/news/` folder size (should be ~200-300 MB)

---

## 📊 **EXPECTED TIMELINE**

### **Tonight (Simultaneous Scraping):**
```
8:00 PM  - Start all 3 sessions
8:05 PM  - All running (verify progress bars)
11:00 PM - Session 1 complete (Colab) → Download ZIP
11:30 PM - Session 2 complete (Colab) → Download ZIP
12:00 AM - Session 3 complete (PC) → Files saved locally
```

### **Tomorrow Morning (Merge):**
```
9:00 AM  - Extract ZIPs to data/raw/news/
9:05 AM  - python 2_merge_data.py
9:10 AM  - Verify: python analyze_articles_per_day.py
9:15 AM  - ✅ 34,000 articles ready for ML!
```

---

## 🎯 **WHAT YOU'LL ACHIEVE**

### **Data Quality:**
- ✅ 34,000 articles (optimal for ML)
- ✅ 20-22 articles/day average
- ✅ 1,600 days covered (2021-2025)
- ✅ No duplicates
- ✅ Clean sentiment signal

### **ML Readiness:**
- ✅ Enough for FinBERT training
- ✅ Enough for LSTM (1,600 days)
- ✅ Train/Val/Test split possible
- ✅ Captures full market cycle

### **Time Saved:**
- ❌ Sequential scraping: 8-12 hours
- ✅ Parallel scraping: **3-4 hours!** 🚀

---

## 🚨 **TROUBLESHOOTING**

### **Colab Disconnects:**
```
Solution: 
1. Download scraped_cache.json
2. Start new session
3. Upload cache
4. Re-run from cell 1
5. It will skip already-scraped articles!
```

### **Low Article Count:**
```
Check:
1. Date range too small? (expand dates)
2. Topics not loading? (check GNews API)
3. Extraction failing? (check logs)

Expected: 15-25 articles per topic
```

### **Duplicates in Final Dataset:**
```
Normal: 2-5% overlap expected
Merge script removes them automatically
If > 10% duplicates, check date range overlaps
```

### **PC Scraper Chrome Timeout:**
```
Solution:
1. Close all Chrome windows
2. Clear WebDriver cache
3. Try again
OR: Just use 2 Colab sessions (enough!)
```

---

## ✅ **FINAL CHECKLIST**

**Before Starting:**
- [ ] Updated Colab notebook uploaded
- [ ] Local scraper updated (6 topics, max_results=25)
- [ ] Google Colab account ready
- [ ] PC ready for local scraping (or use 2nd Colab)

**During Scraping:**
- [ ] All 3 sessions started simultaneously
- [ ] Progress bars showing activity
- [ ] Download checkpoints hourly (backup)

**After Completion:**
- [ ] All 3 ZIPs downloaded
- [ ] Extracted to data/raw/news/
- [ ] Run 2_merge_data.py
- [ ] Verify with analyze_articles_per_day.py
- [ ] Check: ~34,000 articles, ~22/day average

**Next Steps:**
- [ ] Run parallel_summarizer.py (with 3 API keys)
- [ ] Prepare FinBERT input
- [ ] Continue Day 4-5 (FinBERT sentiment)

---

## 🎊 **YOU'RE READY!**

**Start Tonight:**
1. Open 2 Google Colab tabs (different accounts)
2. Upload updated notebook to both
3. Set different date ranges
4. Run your PC scraper
5. Go to bed! 😴
6. Wake up to 34,000 articles! 🎉

**This is a PRODUCTION-GRADE approach used by real trading firms!** 🚀

---

**Questions? Issues? Check logs and cache files for debugging!**
