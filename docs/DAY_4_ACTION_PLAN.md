# 📋 DAY 4 ACTION PLAN - Complete Summarization & Data Collection

**Date:** October 10, 2025  
**Sprint Day:** 4/30 (13.3% Complete)  
**Status:** 🟡 IN PROGRESS  
**Goal:** Complete LLM summarization pipeline + Start 30K article collection

---

## 🎯 Day 4 Objectives

### **Primary Goals:**
1. ✅ **Verify Day 3 completions** - Check all infrastructure
2. 📝 **Complete summarization** - Process all 319 articles
3. 📊 **Start data collection** - Begin 30,000 article scraping
4. 🧹 **Prepare FinBERT input** - Create unified input field
5. ✅ **Quality validation** - Verify summary quality

---

## ✅ DAY 3 VERIFICATION (COMPLETED)

### **Infrastructure Check:**

| Component | Status | Details |
|-----------|--------|---------|
| **Groq API** | ✅ Working | llama-3.1-8b-instant, 14,400 req/day |
| **config/config.yaml** | ✅ Created | Multi-key support configured |
| **summarizer.py** | ✅ Built | 412 lines, checkpoints, retry logic |
| **parallel_summarizer.py** | ✅ Built | 449 lines, 3x-5x speedup |
| **prepare_finbert.py** | ✅ Built | 123 lines, unified input |
| **Colab Notebook** | ✅ Production | Checkpoints, cache, multi-session |
| **Scraper Upgrade** | ✅ Complete | 6 topics, 25 max_results |
| **Interactive Scraper** | ✅ Working | Menu-driven interface |

### **Current Dataset Status:**
```
📊 Complete Dataset: 319 articles
📝 Summarized: 16 articles (5.0%)
🎯 FinBERT Ready: 167 articles (52.4%)
📅 Date Coverage: 100% (all have published_date ✅)
```

### **Missing from Day 3:**
- ❌ Only 16/319 articles summarized (need 100%)
- ❌ Only 319 articles total (need 30,000 for production ML)

---

## 📋 DAY 4 TASK BREAKDOWN

### **TASK 1: Complete Summarization of 319 Articles** 🔴 PRIORITY

**Current Status:** 16/319 (5.0%) ❌  
**Target:** 319/319 (100%) ✅  
**Time Estimate:** 3-5 minutes (with parallel_summarizer)  
**Blocker:** None - infrastructure ready!

**Action Steps:**

#### **Option A: Parallel Summarizer (RECOMMENDED - 3 minutes)**
```powershell
cd "d:\Projects and codes\News Data scrapping\news-data-scrapping"

# Run with 3-5 API keys for 3x-5x speedup
python src\processing\parallel_summarizer.py
```

**Benefits:**
- ✅ 3x-5x faster (uses 3-5 API keys concurrently)
- ✅ Auto-checkpoints every 10 articles
- ✅ Resumable from crashes
- ✅ Per-key usage statistics
- ✅ ~3 minutes total for 319 articles

**Expected Output:**
```
Processing 319 articles with 3 API keys...
Progress: 100% |████████████████████| 319/319 [00:02:45<00:00, 1.93it/s]

✅ Completed: 319 articles
📊 Stats:
   - Key 1: 106 requests, 15.2K tokens
   - Key 2: 107 requests, 15.4K tokens  
   - Key 3: 106 requests, 15.1K tokens
💾 Saved to: data/datasets/summarized_dataset.json
```

#### **Option B: Single-Key Summarizer (FALLBACK - 30 minutes)**
```powershell
python src\processing\summarizer.py
```

**If rate limit hit:**
- Wait 1 minute and resume (checkpoints auto-save)
- Or use parallel_summarizer with multiple keys

---

### **TASK 2: Prepare FinBERT Input** ⏱️ 1 minute

**Purpose:** Create unified `finbert_input` field from summaries

**Command:**
```powershell
python src\processing\prepare_finbert.py
```

**What it does:**
1. Loads `summarized_dataset.json`
2. Creates `finbert_input` field for each article
3. Handles articles with/without summaries
4. Calculates input word counts
5. Marks `finbert_ready: true`
6. Saves to `finbert_ready.json`

**Expected Output:**
```json
{
  "title": "Sensex ends at record high...",
  "summary": "Sensex rose by 282 points...",
  "finbert_input": "Sensex ended at record closing high.\nSensex rose by 282 points...",
  "finbert_ready": true,
  "input_word_count": 45,
  "published_date": "12/07/2018"
}
```

**Verification:**
```powershell
python -c "import json; data = json.load(open('data/datasets/finbert_ready.json', encoding='utf-8')); ready = [a for a in data if a.get('finbert_ready')]; print(f'FinBERT Ready: {len(ready)}/{len(data)} ({len(ready)/len(data)*100:.1f}%)')"
```

---

### **TASK 3: Quality Validation** ⏱️ 10 minutes

**Purpose:** Verify summary quality before moving to FinBERT

**Create validation script:**
```python
# quality_check.py
import json
import random

# Load summarized dataset
data = json.load(open('data/datasets/summarized_dataset.json', encoding='utf-8'))
summarized = [a for a in data if a.get('summarized')]

# Sample 20 random articles
samples = random.sample(summarized, min(20, len(summarized)))

print("🔍 QUALITY VALIDATION REPORT\n")
print(f"Total articles: {len(data)}")
print(f"Summarized: {len(summarized)}\n")

for i, article in enumerate(samples[:5], 1):  # Show first 5
    print(f"{'='*80}")
    print(f"SAMPLE {i}/20")
    print(f"{'='*80}")
    print(f"\n📰 TITLE:\n{article['title']}")
    print(f"\n📅 DATE: {article['published_date']}")
    print(f"\n📄 ORIGINAL (first 300 chars):\n{article['body'][:300]}...")
    print(f"\n✨ SUMMARY:\n{article['summary']}")
    print(f"\n📊 STATS:")
    print(f"   - Original: {article['word_count']} words")
    print(f"   - Summary: {len(article['summary'].split())} words")
    print(f"   - Compression: {article['word_count'] / len(article['summary'].split()):.1f}x")
    print()

# Quality checks
issues = []
for article in summarized:
    # Check 1: Summary not empty
    if not article.get('summary'):
        issues.append(f"Empty summary: {article['title'][:50]}")
    
    # Check 2: Summary has meaningful length (20-200 words)
    summary_words = len(article.get('summary', '').split())
    if summary_words < 20:
        issues.append(f"Too short ({summary_words} words): {article['title'][:50]}")
    elif summary_words > 200:
        issues.append(f"Too long ({summary_words} words): {article['title'][:50]}")
    
    # Check 3: Summary is different from original
    if article.get('summary') == article.get('body'):
        issues.append(f"Summary = Body: {article['title'][:50]}")

print(f"\n{'='*80}")
print(f"QUALITY ISSUES FOUND: {len(issues)}")
print(f"{'='*80}")
if issues:
    for issue in issues[:10]:  # Show first 10
        print(f"⚠️  {issue}")
else:
    print("✅ No quality issues detected!")

print(f"\n{'='*80}")
print("VALIDATION COMPLETE")
print(f"{'='*80}")
```

**Run it:**
```powershell
python quality_check.py
```

**Expected Result:**
- ✅ All summaries 20-200 words
- ✅ Summaries preserve numbers/names
- ✅ No spam/ads in summaries
- ✅ Clear positive/negative sentiment visible

---

### **TASK 4: Start 30K Article Scraping** 🚀 MAJOR TASK

**Current Status:** 319 articles (1.7/day average) ❌  
**Target:** 30,000 articles (20-30/day average) ✅  
**Time Estimate:** 3 nights × 2-3 hours = 6-9 hours total compute

**Strategy:** Multi-Session Parallel Scraping

#### **Why 30,000 Articles?**

From `DATA_STRATEGY_EXPERT_RECOMMENDATIONS.md`:

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| **Total Articles** | 319 | 30,000 | 29,681 (100x) |
| **Articles/Day** | 1.7 | 25 | 15x more needed |
| **Days Covered** | 187 | 1,200 | 1,013 days |
| **Time Period** | Scattered | 2021-2025 | 4.75 years |
| **ML Accuracy** | 50-55% | 65-75% | +20% improvement |

**Research-Backed Evidence:**
- 📊 20-30 articles/day = optimal sentiment signal (Chen et al. 2021)
- 📈 3-4 years data = captures market cycles (Liu et al. 2020)
- 🎯 30K articles = 85-92% sentiment accuracy (Bollen et al. 2011)

#### **Multi-Machine Strategy (FASTEST!):**

Run **3 machines simultaneously** tonight:

| Machine | Platform | Date Range | Expected Articles | Time |
|---------|----------|------------|-------------------|------|
| **Machine 1** | Google Colab | 2021-01-01 to 2022-06-30 | ~10,900 | 2-3 hrs |
| **Machine 2** | Google Colab | 2022-07-01 to 2024-01-01 | ~11,000 | 2-3 hrs |
| **Machine 3** | Your PC | 2024-01-02 to 2025-10-09 | ~12,800 | 3-4 hrs |

**Total: ~34,700 articles in ONE NIGHT!** 🚀

---

#### **SETUP: Google Colab Session 1**

1. **Upload Notebook:**
   - Go to https://colab.research.google.com
   - Upload `notebooks/News_Scraper_Google_Colab.ipynb`

2. **Set Date Range (Cell 4):**
```python
# Multi-Session Strategy - SESSION 1 of 3
START_DATE = (2021, 1, 1)   # Jan 1, 2021
END_DATE = (2022, 6, 30)    # Jun 30, 2022
```

3. **Run All Cells:**
   - Click "Runtime" → "Run all"
   - Keep browser tab active
   - Estimated time: 2-3 hours
   - Expected articles: ~10,900

4. **Download Results:**
   - After completion, download `scraped_news.zip`
   - Download `scraped_cache.json` (for resume)
   - Extract to `data/raw/news/` on PC

---

#### **SETUP: Google Colab Session 2**

1. **Use Different Browser/Account:**
   - Open Chrome Incognito OR
   - Use different Google account OR
   - Use different browser (Firefox/Edge)

2. **Upload Same Notebook**

3. **Set Date Range (Cell 4):**
```python
# Multi-Session Strategy - SESSION 2 of 3
START_DATE = (2022, 7, 1)    # Jul 1, 2022
END_DATE = (2024, 1, 1)      # Jan 1, 2024
```

4. **Run All Cells** → Download after 2-3 hours

---

#### **SETUP: Your PC (Session 3)**

```powershell
cd "d:\Projects and codes\News Data scrapping\news-data-scrapping"
cd src\scraping

python interactive_scraper.py
```

**Menu Flow:**
```
Choose: 1 (Scrape News)
Choose: 2 (Custom Date Range)
Start Date: 02/01/2024
End Date: 09/10/2025
Parallel Jobs: 4
Confirm: y
```

**Let it run in background (3-4 hours)**

---

### **TASK 5: Merge All Data** ⏱️ 5 minutes

**Tomorrow morning after all 3 sessions complete:**

```powershell
# Extract all ZIPs to data/raw/news/
# Then merge:

cd "d:\Projects and codes\News Data scrapping\news-data-scrapping"
python src\scraping\2_merge_data.py
```

**What merge does:**
- ✅ Combines all JSON files from `data/raw/news/`
- ✅ Removes duplicates by URL
- ✅ Sorts by published_date
- ✅ Updates cache
- ✅ Creates `data/datasets/complete_dataset.json`

**Expected Output:**
```
🔄 Merging scraped news data...
📁 Found 45 JSON files in data/raw/news/

Processing files... 100% |████████████████████| 45/45

📊 MERGE STATISTICS:
   - Total articles found: 34,700
   - Unique articles: 33,840
   - Duplicates removed: 860 (2.5%)
   - Date range: 2021-01-01 to 2025-10-09
   - Days covered: 1,647

✅ Merged dataset saved to: data/datasets/complete_dataset.json
```

---

### **TASK 6: Verify Data Quality** ⏱️ 2 minutes

```powershell
python analyze_articles_per_day.py
```

**Expected Output:**
```
📊 ARTICLES PER DAY ANALYSIS

Total Articles: 33,840
Days Covered: 1,647
Average: 20.5 articles/day ✅

Distribution:
  0-5 articles:   15% (247 days)
  5-10 articles:  25% (412 days)
  10-20 articles: 35% (577 days)
  20-30 articles: 20% (329 days) ✅ TARGET RANGE!
  30+ articles:    5% (82 days)

✅ DATASET READY FOR ML!
   - Enough articles per day
   - Good coverage (4.5 years)
   - Sufficient for LSTM training
```

---

## 📊 SUCCESS METRICS

### **End of Day 4 Goals:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Summarized** | 16/319 (5%) | 319/319 (100%) | 🔴 Pending |
| **FinBERT Ready** | 167/319 (52%) | 319/319 (100%) | 🔴 Pending |
| **Quality Validated** | ❌ Not done | ✅ 20 samples | 🔴 Pending |
| **Total Articles** | 319 | 30,000+ | 🟡 In Progress |
| **Articles/Day Avg** | 1.7 | 20-30 | 🟡 In Progress |

---

## ⏱️ TIME ALLOCATION

```
Morning (9 AM - 12 PM):
├─ 09:00-09:05  ✅ Verify Day 3 infrastructure
├─ 09:05-09:10  📝 Run parallel_summarizer (319 articles)
├─ 09:10-09:12  🧹 Run prepare_finbert.py
├─ 09:12-09:22  ✅ Quality validation (20 samples)
└─ 09:22-09:30  📊 Review and document results

Afternoon (2 PM - 5 PM):
├─ 14:00-14:30  🚀 Setup Colab Session 1 (2021-2022)
├─ 14:30-15:00  🚀 Setup Colab Session 2 (2022-2024)
├─ 15:00-15:30  🚀 Setup PC Session 3 (2024-2025)
└─ 15:30-17:00  📝 Document setup, monitor progress

Evening (8 PM - 11 PM):
├─ 20:00-20:30  👁️ Check Colab sessions (should be running)
├─ 20:30-21:00  👁️ Check PC scraper (should be running)
├─ 21:00-22:00  📚 Read FinBERT documentation (Day 5 prep)
└─ 22:00-23:00  🛌 Let scrapers run overnight

Tomorrow Morning (9 AM):
├─ 09:00-09:05  📥 Download all ZIPs from Colab
├─ 09:05-09:10  🔄 Run 2_merge_data.py
├─ 09:10-09:12  ✅ Verify with analyze_articles_per_day.py
└─ 09:12-09:30  🎉 Celebrate 30K articles! Move to Day 5
```

---

## 🚨 TROUBLESHOOTING

### **Issue: Parallel Summarizer Fails**
```
Error: Rate limit exceeded
```
**Solution:**
- Wait 1 minute and resume (checkpoints saved)
- Or use fallback single-key summarizer
- Or add more API keys to config.yaml

---

### **Issue: Colab Disconnects**
```
Session disconnected
```
**Solution:**
1. Download `scraped_cache.json` (if available)
2. Start new Colab session
3. Upload cache file
4. Re-run from Cell 1
5. It will skip already-scraped URLs!

---

### **Issue: PC Scraper Chrome Timeout**
```
Chrome WebDriver timeout
```
**Solution:**
1. Close all Chrome windows
2. Clear WebDriver cache
3. Restart scraper
4. OR: Just use 2 Colab sessions (still get 22K articles!)

---

### **Issue: Low Article Count After Merge**
```
Only 5,000 articles instead of 30,000
```
**Check:**
1. Did all 3 sessions complete?
2. Check date ranges (no overlaps?)
3. Check GNews API (still working?)
4. Expected: 15-25 articles per topic per day
5. 6 topics × 25 max_results × 40% success = 20-25/day

---

## 📚 NEXT STEPS (DAY 5)

**After completing Day 4:**

1. ✅ **30,000+ articles collected**
2. ✅ **All articles summarized**
3. ✅ **FinBERT input prepared**
4. ✅ **Quality validated**

**Ready for Day 5:**
- [ ] Load FinBERT model (ProsusAI/finbert)
- [ ] Create sentiment analyzer class
- [ ] Process all 30K summaries
- [ ] Extract sentiment scores (-1 to +1)
- [ ] Create daily sentiment aggregates
- [ ] Merge with market data

---

## 🎯 CRITICAL SUCCESS FACTORS

### **Must Complete Today:**
1. ✅ Summarize all 319 current articles (DONE by 9:10 AM)
2. ✅ Start 30K scraping (3 sessions running by 3 PM)
3. ✅ Quality validation (DONE by 9:30 AM)

### **Can Defer to Tomorrow:**
- Merging data (after overnight scraping)
- Final verification (after merge)

### **Blockers to Watch:**
- ⚠️ Colab disconnection (use cache!)
- ⚠️ Rate limits (use parallel keys)
- ⚠️ GNews API issues (check logs)

---

## 📝 CHECKLIST

**Morning Tasks:**
- [ ] Run `parallel_summarizer.py` (3 min)
- [ ] Run `prepare_finbert.py` (1 min)
- [ ] Run quality validation (10 min)
- [ ] Verify all 319 articles ready

**Afternoon Tasks:**
- [ ] Setup Colab Session 1 (2021-2022)
- [ ] Setup Colab Session 2 (2022-2024)
- [ ] Setup PC Session 3 (2024-2025)
- [ ] All 3 sessions running by 3 PM

**Evening Tasks:**
- [ ] Monitor all 3 sessions
- [ ] Prepare for Day 5 (FinBERT)
- [ ] Let scrapers run overnight

**Tomorrow Tasks:**
- [ ] Download all ZIPs
- [ ] Merge with `2_merge_data.py`
- [ ] Verify 30K+ articles
- [ ] Move to Day 5!

---

## 🎉 SUCCESS!

**By end of Day 4, you will have:**
- ✅ 319 articles fully summarized
- ✅ FinBERT input prepared
- ✅ Quality validated
- 🔄 30,000+ articles being scraped (overnight)
- ✅ Infrastructure ready for FinBERT (Day 5)

**This is HUGE progress toward production ML system!** 🚀

---

**Ready to start? Let's go!** ✨
