# 🚀 QUICK START - GET YOUR GROQ API KEY

## Step-by-Step (2 minutes)

### 1️⃣ Open Groq Console
Click here: **https://console.groq.com/keys**

### 2️⃣ Sign Up / Login
- Click "Sign Up" if new user
- Or "Login" if you have account
- Use email/Google/GitHub
- **NO CREDIT CARD NEEDED** ✅

### 3️⃣ Create API Key
1. Click "Create API Key" button
2. Name: `StockBus-Summarizer`
3. Click "Create"
4. **COPY THE KEY** (starts with `gsk_`)
   - ⚠️ You can only see it once!
   - Save it somewhere safe

### 4️⃣ Add to Config
1. Open: `config/config.yaml`
2. Line 14: Replace `YOUR_GROQ_API_KEY_HERE` with your key
3. Save file

Example:
```yaml
# Before
api_key: "YOUR_GROQ_API_KEY_HERE"

# After
api_key: "gsk_abc123xyz789..."
```

### 5️⃣ Test It!
Run:
```powershell
python src/processing/summarizer.py --test
```

---

**That's it!** If you see "✅ Groq API initialized", you're ready! 🎉

**Next:** Process all 152 articles with `python src/processing/summarizer.py`
