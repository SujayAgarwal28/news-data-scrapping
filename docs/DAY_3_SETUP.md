# 🚀 Day 3: LLM Summarization Setup Guide

**Created:** October 9, 2025  
**Goal:** Summarize 152 long articles using FREE Groq API

---

## ✅ What We Just Built

1. **`config/config.yaml`** - Configuration file (API keys, settings)
2. **`src/processing/summarizer.py`** - Groq-powered summarizer (371 lines)
3. **Installed packages:** `groq`, `pyyaml`

---

## 📝 STEP 1: Get Your FREE Groq API Key

### 1. Go to Groq Console
👉 **https://console.groq.com**

### 2. Create Account
- Click "Sign Up" (top right)
- Use your email/Google/GitHub
- **NO CREDIT CARD REQUIRED** ✅

### 3. Create API Key
- After login, click "API Keys" (left sidebar)
- Click "Create API Key"
- Give it a name: `StockBus-Summarizer`
- Click "Create"
- **COPY THE KEY** (looks like: `gsk_...`)

### 4. Add Key to Config
- Open `config/config.yaml`
- Find line 14: `api_key: "YOUR_GROQ_API_KEY_HERE"`
- Replace with your actual key: `api_key: "gsk_your_actual_key_here"`
- **Save the file**

---

## 🧪 STEP 2: Test Summarizer (5 Articles)

Run this command to test on 5 articles:

```powershell
python src/processing/summarizer.py --test
```

**Expected output:**
```
======================================================================
🤖 GROQ LLM ARTICLE SUMMARIZER
======================================================================

📂 Loaded: 319 articles from data/datasets/finbert_ready.json
📝 Articles needing summarization: 152
🧪 TEST MODE: Processing only 5 articles
✅ Groq API initialized (Model: llama-3.1-8b-instant)

🚀 Starting summarization...
⏱️ Estimated time: ~0 minutes

Summarizing: 100%|████████████████| 5/5 [00:15<00:00, 3.2s/article]

======================================================================
📊 SUMMARIZATION COMPLETE
======================================================================

✅ Summarized: 5
⏭️ Skipped: 0
❌ Failed: 0
📊 Total: 5

🔢 Total tokens used: 3,847
💰 Cost: $0.00 (Free tier)

💾 Output saved to: data/datasets/summarized_dataset.json
📏 File size: 1.62 MB
```

---

## 🚀 STEP 3: Process All 152 Articles

If test looks good, process all articles:

```powershell
python src/processing/summarizer.py
```

**Time:** ~7-10 minutes  
**Free requests remaining:** 14,395/14,400

---

## 📊 What It Does

### Input (Long Article - 1,247 words):
```
The BSE Sensex and NSE Nifty 50 benchmarks continued their winning 
streak for the fourth consecutive session on Thursday, with the Sensex 
climbing 234.12 points to settle at 81,741.34 and the Nifty rising 
91.85 points to close at 25,041.10...
[1,200+ more words]
```

### Output (Concise Summary - 5-10 points):
```
• Sensex up 234 points to 81,741; Nifty gains 92 points to 25,041
• Banking stocks lead rally: HDFC Bank +2.1%, ICICI Bank +1.8%
• FII inflows of ₹2,341 crore boost market sentiment
• IT sector underperforms: TCS -0.8%, Infosys -0.5%
• Crude oil down 1.2% to $86.34/barrel supports market
• Analysts expect consolidation near 25,000 levels
```

✅ **Perfect for FinBERT!** (Under 512 tokens)

---

## 🔧 Features

- ✅ **Free:** 14,400 requests/day (way more than needed)
- ✅ **Fast:** ~3 seconds per article
- ✅ **Smart:** Preserves numbers, companies, key facts
- ✅ **Safe:** Auto-retry on failures, rate limiting
- ✅ **Trackable:** Progress bar, checkpoints every 10 articles
- ✅ **Resume:** If interrupted, just run again (skips done articles)

---

## ⚠️ Troubleshooting

### Error: "Groq API key not set"
→ Make sure you added your key to `config/config.yaml` line 14

### Error: "Rate limit exceeded"
→ Wait 1 minute, then run again (auto-retry built-in)

### Want different summary style?
→ Edit prompt in `summarizer.py` line 93-110

---

## 📈 Next Steps (After Summarization)

1. **Day 4:** Quality check summaries
2. **Day 5:** FinBERT sentiment analysis
3. **Day 6-7:** Market data integration

---

## 💡 Tips

- **Test first** (`--test` flag) before processing all 152
- **Review samples** in `summarized_dataset.json`
- **Adjust temperature** in config (lower = more factual)
- **Change model** to `mixtral-8x7b-32768` for better quality

---

**Ready?** Get your API key and run the test! 🚀
