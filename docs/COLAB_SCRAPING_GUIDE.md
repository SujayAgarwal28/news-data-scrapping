# 🚀 Google Colab Scraping Setup Guide

**Created:** October 9, 2025  
**Purpose:** Run news scraper on free Google Colab (save money!)

---

## ✅ Why Use Google Colab for Scraping?

| Feature | Your PC | Google Colab |
|---------|---------|--------------|
| **Cost** | Electricity bill 💸 | FREE ✅ |
| **Runtime** | Drains battery | Runs in cloud |
| **Speed** | Your internet | Google's fast internet |
| **Can close laptop?** | ❌ No | ✅ Yes! |
| **Use while scraping?** | Limited | Full access |

**Verdict:** Use Colab for scraping, process locally! 🎯

---

## 📋 How to Use the Colab Notebook

### **Step 1: Upload to Google Colab**

1. Go to: **https://colab.research.google.com**
2. Click: **File → Upload notebook**
3. Upload: `notebooks/News_Scraper_Google_Colab.ipynb`
4. Click: **Open**

### **Step 2: Run All Cells**

1. Click: **Runtime → Run all**
2. Wait ~30-60 minutes (depends on how many articles)
3. Colab will:
   - ✅ Install all packages
   - ✅ Setup Chrome WebDriver
   - ✅ Scrape 5 topics × 10 articles = ~50 articles
   - ✅ Save to JSON files
   - ✅ Create ZIP file

### **Step 3: Download Results**

1. Find `scraped_news.zip` in Files (left sidebar)
2. Right-click → **Download**
3. Extract ZIP on your PC
4. Move JSONs to: `data/raw/news/`

### **Step 4: Process Locally**

On your PC, run:
```powershell
# Merge all JSONs
python src/scraping/2_merge_data.py --input data/raw/news

# Summarize articles
python src/processing/summarizer.py

# Prepare for FinBERT
python src/processing/prepare_finbert.py
```

---

## 🎯 Workflow Diagram

```
┌─────────────────────────────────────────────────┐
│         GOOGLE COLAB (Free Cloud)               │
│                                                 │
│  1. Run News_Scraper_Google_Colab.ipynb        │
│  2. Scrape 50+ articles (~30-60 mins)          │
│  3. Download scraped_news.zip                   │
└────────────────────┬────────────────────────────┘
                     │
                     ▼ Download
┌─────────────────────────────────────────────────┐
│         YOUR PC (Processing Only)               │
│                                                 │
│  4. Extract JSONs to data/raw/news/            │
│  5. Merge data                                  │
│  6. Summarize with Groq (free API)             │
│  7. Run FinBERT sentiment analysis             │
└─────────────────────────────────────────────────┘
```

**Total Cost:** $0.00 ✅

---

## 💡 Pro Tips

### **Tip 1: Run Weekly**
- Schedule Colab notebook to run every Sunday
- Keep getting fresh news data
- Always have latest market sentiment

### **Tip 2: Increase Articles**
In the notebook, change:
```python
articles = scraper.scrape_topic(topic, max_articles=10)  # Change to 20, 50, 100
```

### **Tip 3: Add More Topics**
```python
TOPICS = [
    "Nifty 50 stock market India",
    "BSE Sensex India stock market",
    "Indian stock market news",
    "NSE India trading",
    "Reliance Industries stock",      # Add custom topics!
    "Adani Group stocks",
    "TCS share price",
]
```

### **Tip 4: Monitor Progress**
The notebook shows progress bars:
```
Scraping Nifty 50: 100%|████████████| 10/10 [02:30<00:00, 15.0s/article]
```

---

## ⚠️ Troubleshooting

### **Problem:** Colab disconnects after 12 hours
**Solution:** Download ZIP every few hours as backup

### **Problem:** Rate limiting errors
**Solution:** Increase `time.sleep(3)` to `time.sleep(5)` in notebook

### **Problem:** Can't download ZIP
**Solution:** Click individual JSON files and download manually

---

## 🎉 Summary

**OLD WAY (Your PC):**
- Runs all night
- Costs electricity
- Can't use laptop
- Slows down your work

**NEW WAY (Colab):**
- ✅ Runs in cloud (free!)
- ✅ Close laptop anytime
- ✅ Download results when ready
- ✅ Process locally (fast!)

**Best of both worlds!** 🚀

---

**Next:** After downloading JSONs, continue with Day 3-4 summarization on your PC!
