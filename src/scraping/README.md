# 📰 NEWS SCRAPING - SIMPLE START

## 🚀 **ONE-CLICK START**

### **Windows Users:**
```
Double-click: START_SCRAPER.bat
```

### **Command Line:**
```powershell
python interactive_scraper.py
```

---

## 🎯 **What You'll See**

```
======================================================================
🚀 INTERACTIVE NEWS SCRAPER - STOCKBUS TRADE PULSE
======================================================================

MAIN MENU:

1. 📰 Scrape News (New Scraping Session)
2. 🔄 Merge All Scraped Data
3. 📊 Generate Quality Report
4. 📂 View Scraping Status
5. ⚙️  Advanced Options
6. ❌ Exit

Enter your choice (1-6):
```

---

## ⭐ **RECOMMENDED FIRST RUN**

For maximum accuracy, scrape from 2018:

1. Choose **1** (Scrape News)
2. Choose **3** (Full Dataset: 2018 to Today)
3. Choose **2** (Balanced: 8 parallel jobs)
4. Confirm **y**

⏱️ **Time:** ~2 hours
📊 **Result:** ~20,000 articles ready for sentiment analysis

---

## 📖 **FULL GUIDE**

See: **INTERACTIVE_SCRAPER_GUIDE.md**

---

## 🛠️ **OLD SCRIPTS (Still Work)**

If you prefer command-line:

### **Single scraping job:**
```powershell
python news_scraper.py --start 2024-01-01 --end 2024-12-31
```

### **Parallel jobs (faster):**
```powershell
# Step 1: Generate jobs
python 1_generate_jobs.py --start 2018-01-01 --end 2025-10-09 --splits 8

# Step 2: Run all (opens 8 windows)
run_all.bat

# Step 3: Merge data
python 2_merge_data.py
```

---

## 💡 **WHY USE INTERACTIVE MODE?**

✅ **No complex commands** - Just follow menus
✅ **Simple date format** - DD/MM/YYYY (e.g., 01/01/2024)
✅ **Guided options** - Script recommends best settings
✅ **Automatic merging** - One click to combine all data
✅ **Built-in validation** - Quality reports included

---

## 📁 **FILE STRUCTURE**

```
src/scraping/
├── START_SCRAPER.bat           ← Double-click this! 🎯
├── interactive_scraper.py       ← New menu-driven interface
├── INTERACTIVE_SCRAPER_GUIDE.md ← Full documentation
├── news_scraper.py              ← Core scraper (don't run directly)
├── 1_generate_jobs.py           ← Old parallel job generator
├── 2_merge_data.py              ← Old merge script
└── run_all.bat                  ← Auto-generated parallel launcher
```

---

## 🎬 **QUICK EXAMPLES**

### **Test Run (5 minutes):**
```
1 → 1 → y
(Option 1: Scrape News → Option 1: Quick 30 days)
```

### **2024 Only (1 hour):**
```
1 → 2 → 01/01/2024 → 31/12/2024 → 4 → y
(Custom range, 4 parallel jobs)
```

### **Full Dataset (2 hours) ⭐:**
```
1 → 3 → 2 → y
(Full dataset, 8 parallel jobs - RECOMMENDED)
```

---

**Start now:** `START_SCRAPER.bat` or `python interactive_scraper.py` 🚀
