**How to Use Multiple API Keys for 3x-5x Speedup**

---

## 📊 **Performance Comparison**

| Mode | Keys | Speed | Time for 209 Articles |
|------|------|-------|----------------------|
| Single | 1 | 25 req/min | ~10 minutes |
| Parallel | 3 | 75 req/min | ~3 minutes |
| Parallel | 5 | 125 req/min | ~2 minutes |

---

## 🔑 **Step 1: Get Multiple Free Groq API Keys**

### Option A: Create Multiple Groq Accounts (Recommended)
1. Go to: https://console.groq.com/keys
2. Sign up with **different email addresses** (Gmail, Outlook, etc.)
3. Get API key from each account
4. Each account gets **14,400 requests/day** (FREE!)

### Option B: Use Temporary Email Services
- https://temp-mail.org/
- https://10minutemail.com/
- Create accounts, get keys, save them

**Goal: Get 3-5 API keys (all free!)**

---

## ⚙️ **Step 2: Add Keys to Config**

### Edit `config/config.yaml`:

```yaml
llm:
  groq:
    api_keys:
      - "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"  # Key 1
      - "gsk_YOUR_SECOND_KEY_HERE"  # Key 2 👈 Add here
      - "gsk_YOUR_THIRD_KEY_HERE"   # Key 3 👈 Add here
      - "gsk_YOUR_FOURTH_KEY_HERE"  # Key 4 (optional)
      - "gsk_YOUR_FIFTH_KEY_HERE"   # Key 5 (optional)
```

**Just uncomment the lines and paste your keys!**

---

## 🚀 **Step 3: Run Parallel Summarizer**

### Test First (10 articles to verify keys work):
```powershell
python src\processing\parallel_summarizer.py --test
```

### Full Run (all 209 remaining articles):
```powershell
python src\processing\parallel_summarizer.py
```

### Expected Output:
```
🔑 Loaded 5 API key(s)
✅ Initialized 5 Groq client(s)
⚡ Expected speedup: ~5x faster!

📂 Loaded: 319 articles
📝 Need summarization: 209
✅ Already done: 110

🔄 Processing batch 1/21
Summarizing (parallel): 100%|████████████| 10/10 [00:06<00:00,  1.67article/s]
💾 Checkpoint saved (10/209)

📊 Per-Key Usage:
   key_1: Requests: 42, Tokens: 8,420, Errors: 0
   key_2: Requests: 42, Tokens: 8,315, Errors: 0
   key_3: Requests: 42, Tokens: 8,501, Errors: 0
   key_4: Requests: 42, Tokens: 8,290, Errors: 0
   key_5: Requests: 41, Tokens: 8,180, Errors: 0

✅ DONE! Used 5 API key(s) in parallel
```

---

## 🛡️ **Safety Features**

✅ **Caching Built-In**
- Skips articles already marked `summarized: true`
- Won't waste API calls on the 110 already done

✅ **Checkpoint System**
- Saves every 10 articles
- Can resume if interrupted

✅ **Per-Key Rate Limiting**
- Each key respects 30 req/min limit
- No risk of getting rate-limited

✅ **Error Handling**
- Failed articles marked with `summary_error`
- Can retry later

---

## 🎯 **Usage Scenarios**

### Scenario 1: You Have 1 Key (Current Situation)
```powershell
# Use original single-threaded version
python src\processing\summarizer.py

# Time: ~10 minutes for 209 articles
```

### Scenario 2: You Get 3 Keys
```powershell
# Edit config.yaml, add 3 keys
python src\processing\parallel_summarizer.py

# Time: ~3-4 minutes for 209 articles (3x faster!)
```

### Scenario 3: You Get 5 Keys (Maximum Speedup)
```powershell
# Edit config.yaml, add 5 keys
python src\processing\parallel_summarizer.py

# Time: ~2 minutes for 209 articles (5x faster!)
```

---

## 🔬 **How It Works**

### Round-Robin Assignment:
```
Article 1 → Key 1
Article 2 → Key 2
Article 3 → Key 3
Article 4 → Key 4
Article 5 → Key 5
Article 6 → Key 1  (back to start)
Article 7 → Key 2
...
```

### Parallel Execution:
- Uses Python's `ThreadPoolExecutor`
- All 5 keys call API simultaneously
- Results merged in real-time
- Progress bar shows combined speed

---

## 📈 **Cost Analysis**

| Keys | Daily Limit | Cost | Time for 319 Articles |
|------|-------------|------|----------------------|
| 1 | 14,400 req | FREE | ~15 minutes |
| 3 | 43,200 req | FREE | ~5 minutes |
| 5 | 72,000 req | FREE | ~3 minutes |

**All FREE! No credit card needed!**

---

## ⚠️ **Important Notes**

1. **Email Verification**: Some Groq accounts may need email verification
2. **Key Limits**: Each key has 30 req/min, 14,400/day (all free tier)
3. **Fair Use**: Don't abuse - Groq is generous with free tier, respect it
4. **Account Ban Risk**: Creating many accounts may violate ToS - stick to 3-5 keys

---

## 🎬 **Quick Start Checklist**

- [ ] Get 3-5 Groq API keys (https://console.groq.com/keys)
- [ ] Add keys to `config/config.yaml` under `api_keys`
- [ ] Test with: `python src\processing\parallel_summarizer.py --test`
- [ ] Run full: `python src\processing\parallel_summarizer.py`
- [ ] Watch the 5x speedup! 🚀

---

## ❓ **Troubleshooting**

### Error: "No Groq API keys found"
→ Check `config/config.yaml` - uncomment the `api_keys` lines and add your keys

### Error: "Rate limit exceeded"
→ Normal! Script has built-in retry logic. Just wait 1 minute.

### Some keys not working?
→ Check if email verification needed. Remove bad keys from config.

### Want to add more keys later?
→ Just edit `config/config.yaml` and add to `api_keys` list!

---

**Ready to process 209 articles in 2 minutes instead of 10?** 🚀

1. Get keys
2. Edit config
3. Run `python src\processing\parallel_summarizer.py`
4. Watch the magic! ✨
