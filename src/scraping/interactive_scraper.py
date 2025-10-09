"""
🚀 INTERACTIVE NEWS SCRAPER - MENU DRIVEN
==========================================
Unified menu-driven interface for scraping, merging, and managing news data.

Features:
- Simple menu navigation (no complex command-line arguments)
- Scrape news from 2018 onwards for maximum accuracy
- Split large date ranges for parallel processing
- Merge all scraped data automatically
- Quality reports and validation

Author: StockBus Team
Created: October 9, 2025
"""

import json
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def check_dependencies():
    """Check and install required dependencies"""
    required = {
        'gnews': 'gnews',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
        'newspaper': 'newspaper3k',
        'nltk': 'nltk',
        'tqdm': 'tqdm',
        'beautifulsoup4': 'beautifulsoup4'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("="*70)
        print("📦 INSTALLING MISSING DEPENDENCIES")
        print("="*70)
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\n⏳ Installing... (this may take 1-2 minutes)\n")
        
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install"
        ] + missing)
        
        print("\n✅ All dependencies installed!")
        print("="*70)
        time.sleep(2)


class InteractiveScraper:
    """Menu-driven scraper interface"""
    
    def __init__(self):
        self.project_root = project_root
        self.scraper_dir = Path(__file__).parent
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print header"""
        self.clear_screen()
        print("="*70)
        print("🚀 INTERACTIVE NEWS SCRAPER - STOCKBUS TRADE PULSE")
        print("="*70)
        print("Scrape Indian stock market news for sentiment analysis")
        print("="*70)
        print()
    
    def main_menu(self):
        """Show main menu"""
        while True:
            self.print_header()
            print("MAIN MENU:")
            print()
            print("1. 📰 Scrape News (New Scraping Session)")
            print("2. 🔄 Merge All Scraped Data")
            print("3. 📊 Generate Quality Report")
            print("4. 📂 View Scraping Status")
            print("5. ⚙️  Advanced Options")
            print("6. ❌ Exit")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.scrape_menu()
            elif choice == '2':
                self.merge_data()
            elif choice == '3':
                self.quality_report()
            elif choice == '4':
                self.view_status()
            elif choice == '5':
                self.advanced_menu()
            elif choice == '6':
                print("\n👋 Goodbye! Happy trading!\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Press Enter to continue...")
                input()
    
    def scrape_menu(self):
        """Scraping options menu"""
        self.print_header()
        print("📰 NEWS SCRAPING OPTIONS:")
        print()
        print("1. 🚀 Quick Scrape (Last 30 days)")
        print("2. 📅 Custom Date Range")
        print("3. 🎯 Recommended: Full Dataset (2018 to Today)")
        print("4. 🔙 Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            self.quick_scrape()
        elif choice == '2':
            self.custom_scrape()
        elif choice == '3':
            self.full_scrape()
        elif choice == '4':
            return
        else:
            print("\n❌ Invalid choice!")
            time.sleep(2)
    
    def quick_scrape(self):
        """Quick 30-day scrape"""
        self.print_header()
        print("🚀 QUICK SCRAPE (Last 30 Days)")
        print("="*70)
        
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        print(f"\nDate Range: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")
        print(f"Duration: 30 days")
        
        confirm = input("\nStart scraping? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self._run_scraper(start_date, end_date, splits=1)
    
    def custom_scrape(self):
        """Custom date range scrape"""
        self.print_header()
        print("📅 CUSTOM DATE RANGE SCRAPE")
        print("="*70)
        print()
        print("Enter dates in format: DD/MM/YYYY")
        print("Example: 01/01/2024 or 15/06/2025")
        print()
        
        # Get start date
        while True:
            start_str = input("Start Date (DD/MM/YYYY): ").strip()
            try:
                start_date = datetime.strptime(start_str, '%d/%m/%Y').date()
                break
            except:
                print("❌ Invalid format! Use DD/MM/YYYY (e.g., 01/01/2024)")
        
        # Get end date
        while True:
            end_str = input("End Date (DD/MM/YYYY): ").strip()
            try:
                end_date = datetime.strptime(end_str, '%d/%m/%Y').date()
                if end_date < start_date:
                    print("❌ End date must be after start date!")
                    continue
                break
            except:
                print("❌ Invalid format! Use DD/MM/YYYY (e.g., 31/12/2024)")
        
        # Calculate duration
        days = (end_date - start_date).days
        
        print(f"\n📊 Summary:")
        print(f"   Start: {start_date.strftime('%d/%m/%Y')}")
        print(f"   End: {end_date.strftime('%d/%m/%Y')}")
        print(f"   Duration: {days} days")
        
        # Ask about parallel processing
        splits = 1
        if days > 90:
            print(f"\n⚡ This is a large date range ({days} days)!")
            print("   Recommendation: Split into parallel jobs for faster scraping")
            print()
            print("How many parallel jobs? (1-10)")
            print("  1 = Single job (slower, but simpler)")
            print("  4 = 4 parallel jobs (recommended)")
            print("  8 = 8 parallel jobs (fastest)")
            
            while True:
                try:
                    splits = int(input("\nNumber of parallel jobs (1-10): ").strip())
                    if 1 <= splits <= 10:
                        break
                    print("❌ Please enter a number between 1 and 10")
                except:
                    print("❌ Please enter a valid number")
        
        print(f"\n🚀 Will scrape in {splits} parallel job(s)")
        confirm = input("\nStart scraping? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self._run_scraper(start_date, end_date, splits)
    
    def full_scrape(self):
        """Full historical scrape (2018 to today)"""
        self.print_header()
        print("🎯 RECOMMENDED: FULL DATASET SCRAPE")
        print("="*70)
        print()
        print("📈 Why scrape from 2018?")
        print("   ✅ More training data = Better accuracy")
        print("   ✅ Captures market cycles (bull/bear markets)")
        print("   ✅ Better sentiment pattern recognition")
        print("   ✅ Recommended for production trading systems")
        print()
        
        start_date = date(2018, 1, 1)
        end_date = date.today()
        days = (end_date - start_date).days
        
        print(f"📊 Dataset Size:")
        print(f"   Start: {start_date.strftime('%d/%m/%Y')}")
        print(f"   End: {end_date.strftime('%d/%m/%Y')}")
        print(f"   Duration: {days} days (~{days//365} years)")
        print(f"   Expected articles: ~15,000-25,000")
        print()
        
        print("⚡ PARALLEL PROCESSING OPTIONS:")
        print("   1. Conservative (4 parallel jobs) - ~3-4 hours")
        print("   2. Balanced (8 parallel jobs) - ~2 hours")
        print("   3. Fast (12 parallel jobs) - ~1.5 hours")
        print("   4. Maximum (16 parallel jobs) - ~1 hour")
        print()
        
        while True:
            mode = input("Select mode (1-4): ").strip()
            if mode == '1':
                splits = 4
                break
            elif mode == '2':
                splits = 8
                break
            elif mode == '3':
                splits = 12
                break
            elif mode == '4':
                splits = 16
                break
            else:
                print("❌ Please enter 1, 2, 3, or 4")
        
        print(f"\n🚀 Will scrape {days} days in {splits} parallel jobs")
        print(f"⏱️  Estimated time: {self._estimate_time(days, splits)}")
        
        confirm = input("\nStart scraping? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self._run_scraper(start_date, end_date, splits)
    
    def _estimate_time(self, days, splits):
        """Estimate scraping time"""
        # Rough estimate: ~1 article per 2 seconds
        # ~10 articles per day on average
        total_seconds = (days * 10 * 2) / splits
        hours = total_seconds / 3600
        
        if hours < 1:
            return f"{int(hours * 60)} minutes"
        else:
            return f"{hours:.1f} hours"
    
    def _run_scraper(self, start_date, end_date, splits=1):
        """Run the actual scraper"""
        print("\n" + "="*70)
        print("🚀 STARTING SCRAPER")
        print("="*70)
        
        # Convert dates to YYYY-MM-DD format for the scraper
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        if splits == 1:
            # Single job
            print(f"\n📰 Scraping: {start_str} to {end_str}")
            print("⏳ Please wait...\n")
            
            cmd = f'python "{self.scraper_dir}/news_scraper.py" --start {start_str} --end {end_str}'
            os.system(cmd)
            
        else:
            # Generate parallel jobs
            print(f"\n⚡ Generating {splits} parallel jobs...")
            
            cmd = f'python "{self.scraper_dir}/1_generate_jobs.py" --start {start_str} --end {end_str} --splits {splits}'
            os.system(cmd)
            
            print(f"\n✅ Jobs generated!")
            print(f"📂 Jobs saved to: {self.scraper_dir}/parallel_jobs.json")
            print(f"🚀 Batch file created: {self.scraper_dir}/run_all.bat")
            print()
            print("OPTIONS:")
            print("  1. Run all jobs now (in separate windows)")
            print("  2. View job details and run manually")
            print("  3. Return to main menu")
            
            choice = input("\nYour choice (1-3): ").strip()
            
            if choice == '1':
                batch_file = self.scraper_dir / "run_all.bat"
                print(f"\n🚀 Starting all {splits} jobs...")
                print("⚠️  Each job will open in a separate window")
                print("⏳ This may take 1-4 hours depending on date range")
                print()
                input("Press Enter to start...")
                os.system(f'"{batch_file}"')
                
            elif choice == '2':
                self._show_jobs()
        
        print("\n✅ Scraping initiated!")
        print("\n💡 TIP: After scraping completes, use option 2 to merge all data")
        input("\nPress Enter to continue...")
    
    def _show_jobs(self):
        """Show parallel jobs"""
        jobs_file = self.scraper_dir / "parallel_jobs.json"
        
        if not jobs_file.exists():
            print("❌ No jobs file found!")
            return
        
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
        
        print("\n" + "="*70)
        print(f"PARALLEL JOBS ({len(jobs)} jobs)")
        print("="*70)
        
        for job in jobs:
            print(f"\nJob {job['job']}: {job['start']} to {job['end']}")
            print(f"  Command: {job['command']}")
        
        print("\n" + "="*70)
        print("To run all jobs, execute: run_all.bat")
        print("To run individual jobs, copy-paste commands above")
        print("="*70)
        
        input("\nPress Enter to continue...")
    
    def merge_data(self):
        """Merge all scraped data"""
        self.print_header()
        print("🔄 MERGE ALL SCRAPED DATA")
        print("="*70)
        print()
        print("This will:")
        print("  ✅ Combine all JSON files from data/raw/news/")
        print("  ✅ Remove duplicate articles")
        print("  ✅ Create unified dataset")
        print("  ✅ Save to data/datasets/complete_dataset.json")
        print()
        
        confirm = input("Start merging? (y/n): ").strip().lower()
        
        if confirm == 'y':
            print("\n⏳ Merging data...\n")
            cmd = f'python "{self.scraper_dir}/2_merge_data.py"'
            os.system(cmd)
            
            print("\n✅ Data merged!")
            input("\nPress Enter to continue...")
    
    def quality_report(self):
        """Generate quality report"""
        self.print_header()
        print("📊 GENERATE QUALITY REPORT")
        print("="*70)
        print()
        print("Analyzing dataset quality...")
        print()
        
        cmd = f'python "{self.scraper_dir}/generate_quality_report.py"'
        os.system(cmd)
        
        input("\nPress Enter to continue...")
    
    def view_status(self):
        """View scraping status"""
        self.print_header()
        print("📂 SCRAPING STATUS")
        print("="*70)
        print()
        
        # Check data directory
        data_dir = self.project_root / "data" / "raw" / "news"
        
        if not data_dir.exists():
            print("❌ No scraped data found!")
            print("   Start scraping from the main menu")
        else:
            json_files = list(data_dir.glob("*.json"))
            print(f"📂 Data Directory: {data_dir}")
            print(f"📰 JSON Files: {len(json_files)}")
            print()
            
            if json_files:
                total_articles = 0
                print("Files:")
                for f in sorted(json_files)[:20]:  # Show first 20
                    try:
                        with open(f, 'r') as file:
                            articles = json.load(file)
                            total_articles += len(articles)
                            print(f"  ✅ {f.name}: {len(articles)} articles")
                    except:
                        print(f"  ❌ {f.name}: Error reading")
                
                if len(json_files) > 20:
                    print(f"  ... and {len(json_files) - 20} more files")
                
                print()
                print(f"📊 Total Articles: {total_articles:,}")
        
        # Check merged dataset
        merged_file = self.project_root / "data" / "datasets" / "complete_dataset.json"
        if merged_file.exists():
            try:
                with open(merged_file, 'r') as f:
                    merged = json.load(f)
                print(f"\n✅ Merged Dataset: {len(merged):,} articles")
                print(f"   Location: {merged_file}")
            except:
                pass
        
        print()
        input("Press Enter to continue...")
    
    def advanced_menu(self):
        """Advanced options"""
        self.print_header()
        print("⚙️  ADVANCED OPTIONS")
        print("="*70)
        print()
        print("1. 🔧 Configure Search Topics")
        print("2. 📊 View Cache Status")
        print("3. 🗑️  Clear Cache")
        print("4. 📝 View Logs")
        print("5. 🔙 Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            self.configure_topics()
        elif choice == '2':
            self.view_cache()
        elif choice == '3':
            self.clear_cache()
        elif choice == '4':
            self.view_logs()
        elif choice == '5':
            return
        else:
            print("\n❌ Invalid choice!")
            time.sleep(2)
    
    def configure_topics(self):
        """Configure search topics"""
        print("\n⚠️  This feature requires editing news_scraper.py")
        print("Current topics:")
        print("  - Nifty 50 stock market India")
        print("  - BSE Sensex India stock market")
        print("  - Indian stock market news")
        print("  - NSE India trading")
        input("\nPress Enter to continue...")
    
    def view_cache(self):
        """View cache status"""
        self.print_header()
        print("📊 CACHE STATUS")
        print("="*70)
        
        cache_dir = self.scraper_dir / "cache"
        
        if cache_dir.exists():
            scraped_file = cache_dir / "scraped.json"
            failed_file = cache_dir / "failed.json"
            
            if scraped_file.exists():
                with open(scraped_file, 'r') as f:
                    scraped = json.load(f)
                print(f"\n✅ Scraped URLs: {len(scraped):,}")
            
            if failed_file.exists():
                with open(failed_file, 'r') as f:
                    failed = json.load(f)
                print(f"❌ Failed URLs: {len(failed):,}")
        else:
            print("\n📂 No cache found")
        
        input("\nPress Enter to continue...")
    
    def clear_cache(self):
        """Clear cache"""
        print("\n⚠️  This will delete all cached URLs")
        print("You may re-scrape duplicate articles!")
        
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            cache_dir = self.scraper_dir / "cache"
            if cache_dir.exists():
                for file in cache_dir.glob("*.json"):
                    file.unlink()
                print("✅ Cache cleared!")
            else:
                print("📂 No cache to clear")
        
        input("\nPress Enter to continue...")
    
    def view_logs(self):
        """View recent logs"""
        self.print_header()
        print("📝 RECENT LOGS")
        print("="*70)
        
        log_dir = self.scraper_dir / "logs"
        
        if log_dir.exists():
            logs = sorted(log_dir.glob("*.log"), reverse=True)[:10]
            
            if logs:
                print("\nRecent log files:")
                for i, log in enumerate(logs, 1):
                    size = log.stat().st_size / 1024
                    print(f"{i}. {log.name} ({size:.1f} KB)")
                
                print(f"\n📂 Log directory: {log_dir}")
            else:
                print("\n📂 No logs found")
        else:
            print("\n📂 No logs directory")
        
        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    try:
        # Check dependencies first
        check_dependencies()
        
        # Start scraper
        scraper = InteractiveScraper()
        scraper.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
