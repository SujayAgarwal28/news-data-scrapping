# 🎯 Quick Navigation Guide

> **Last Updated:** October 8, 2025, 11:20 PM IST

---

## 📚 WHICH FILE TO READ?

### For Daily Work:
1. **MASTER_TRACKER.md** → What to do today + track progress
2. **30_DAY_SPRINT_PLAN.md** → How to do it (code examples)
3. **docs/DASHBOARD_SPECIFICATION.md** → UI/UX design reference

### For Understanding the Project:
1. **README.md** → Project overview and quick start
2. **DAY_0_COMPLETE.md** → Initial setup summary
3. **REORGANIZATION.md** → What changed and why

### For Getting Started:
1. **START_DAY_1.md** → BEGIN HERE for Day 1 tasks
2. **config.yaml.template** → Configuration template
3. **requirements.txt** → Dependencies to install

---

## 🗂️ FILE PURPOSES

| File | Purpose | When to Use |
|------|---------|-------------|
| **MASTER_TRACKER.md** | Daily task tracking & progress | Every morning & evening |
| **30_DAY_SPRINT_PLAN.md** | Technical implementation guide | When coding |
| **README.md** | Project overview | For others/stakeholders |
| **START_DAY_1.md** | Day 1 kickoff guide | Starting development |
| **DAY_0_COMPLETE.md** | Setup summary | Understanding what was done |
| **REORGANIZATION.md** | File movement log | Finding where files went |
| **docs/DASHBOARD_SPECIFICATION.md** | UI design specs | Building dashboard |

---

## 🚀 QUICK START (Day 1)

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\activate

# 3. Install essentials
pip install newspaper3k trafilatura beautifulsoup4 selenium

# 4. Test existing scraper
python src/scraping/news_scraper.py --help

# 5. Open your guide
code MASTER_TRACKER.md
```

---

## 📁 WHERE IS EVERYTHING?

```
Root Files (9):
├── MASTER_TRACKER.md         ← Your command center
├── 30_DAY_SPRINT_PLAN.md     ← Technical guide
├── README.md                  ← Project overview
├── START_DAY_1.md             ← Day 1 starting point
├── DAY_0_COMPLETE.md          ← Setup summary
├── REORGANIZATION.md          ← File reorganization log
├── config.yaml.template       ← Config template
├── requirements.txt           ← Dependencies
└── .gitignore                 ← Git protection

Code:
└── src/scraping/news_scraper.py  ← Main scraper (was scraper.py)

Scripts:
├── scripts/1_generate_jobs.py
├── scripts/2_merge_data.py
└── scripts/3_test.py

Data:
├── data/datasets/complete_dataset.json
├── data/datasets/finbert_ready.json
└── data/raw/news_archive/...

Docs:
├── docs/DASHBOARD_SPECIFICATION.md
└── docs/archive/... (old docs)
```

---

## 🎯 DAILY WORKFLOW

### Every Morning:
1. Open **MASTER_TRACKER.md**
2. Find today's section (e.g., "Day 3-4")
3. Read task list
4. Reference **30_DAY_SPRINT_PLAN.md** for details

### During Work:
1. Write code in **src/** folders
2. Save data in **data/** folders
3. Use **scripts/** for utilities
4. Check **docs/** for references

### Every Evening:
1. Open **MASTER_TRACKER.md**
2. Check off completed tasks: ⬜ → ✅
3. Add **Remarks**: what worked, issues, learnings
4. Update **Actual Completion** date
5. Commit to git

---

## 💡 TIPS

- **Lost?** → Check **NAVIGATION.md** (this file)
- **Need code help?** → Check **30_DAY_SPRINT_PLAN.md**
- **Forgot what you did?** → Check **MASTER_TRACKER.md** remarks
- **Need old info?** → Check **docs/archive/**
- **Building dashboard?** → Check **docs/DASHBOARD_SPECIFICATION.md**

---

## 🔍 FINDING FILES

**Looking for old scraper.py?**
→ Now at `src/scraping/news_scraper.py`

**Looking for utility scripts?**
→ Now in `scripts/` folder

**Looking for data files?**
→ Now in `data/datasets/` and `data/raw/news_archive/`

**Looking for old README?**
→ Now at `docs/archive/README_OLD.md`

**Looking for old roadmap?**
→ Now at `docs/archive/PROJECT_ROADMAP.md`

---

## 📞 QUICK REFERENCE

### Installation:
```powershell
pip install -r requirements.txt
```

### Run Scraper:
```powershell
python src/scraping/news_scraper.py --start 2024-10-01 --end 2024-10-08
```

### Run Utilities:
```powershell
python scripts/3_test.py
python scripts/2_merge_data.py
```

### Open Dashboard (future):
```powershell
streamlit run src/dashboard/app.py
```

---

## 🎯 YOUR 30-DAY JOURNEY

```
Week 1 (Days 1-7): Data Pipeline
├─ Day 1-2: Enhanced news scraper → START HERE!
├─ Day 3-4: LLM summarization
├─ Day 5: Nifty 50 data
└─ Day 6-7: Feature engineering

Week 2 (Days 8-14): Sentiment Analysis
├─ Day 8-9: FinBERT setup
├─ Day 10-11: Sentiment scoring
├─ Day 12-13: Historical processing
└─ Day 14: Validation

Week 3 (Days 15-21): Prediction & Backtesting
├─ Day 15-16: Baseline models
├─ Day 17-18: LSTM training
├─ Day 19: Model evaluation
└─ Day 20-21: Backtesting

Week 4 (Days 22-30): Integration & Dashboard
├─ Day 22-23: Trading integration
├─ Day 24-25: Report generation
├─ Day 26-27: Automation
├─ Day 28: Dashboard
├─ Day 29: Testing
└─ Day 30: Live testing & celebration!
```

**Current Status:** Ready to begin Day 1!

---

## ✅ CHECKLIST

Before starting Day 1:
- [x] Project reorganized
- [x] Files in correct locations
- [x] Documentation complete
- [x] Structure understood
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Ready to code!

---

**🚀 START HERE:** Open **START_DAY_1.md**  
**📋 TRACK HERE:** Open **MASTER_TRACKER.md**  
**📖 LEARN HERE:** Open **30_DAY_SPRINT_PLAN.md**

**LET'S BUILD STOCKBUS - TRADE PULSE! 💪**
