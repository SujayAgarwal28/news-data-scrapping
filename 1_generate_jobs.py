"""
Script 1: Generate Parallel Scraping Jobs
==========================================
Split large date ranges into multiple jobs for parallel execution.

Usage:
    python 1_generate_jobs.py --start 2018-01-01 --end 2025-06-30 --splits 8
"""

import argparse
import json
from datetime import date, timedelta

def split_dates(start, end, splits):
    """Split date range into N parts"""
    total_days = (end - start).days
    days_per_split = total_days // splits
    
    jobs = []
    current = start
    
    for i in range(splits):
        if i == splits - 1:
            job_end = end
        else:
            job_end = current + timedelta(days=days_per_split)
        
        jobs.append({
            'job': i + 1,
            'start': current.isoformat(),
            'end': job_end.isoformat(),
            'command': f'python scraper.py --start {current} --end {job_end}'
        })
        
        current = job_end + timedelta(days=1)
    
    return jobs

def main():
    parser = argparse.ArgumentParser(description='Generate parallel scraping jobs')
    parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--splits', type=int, required=True, help='Number of jobs')
    parser.add_argument('--max-articles', type=int, help='Max articles per job')
    
    args = parser.parse_args()
    
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    
    jobs = split_dates(start, end, args.splits)
    
    # Add max-articles if specified
    if args.max_articles:
        for job in jobs:
            job['command'] += f' --max-articles {args.max_articles}'
    
    # Save to JSON
    with open('parallel_jobs.json', 'w') as f:
        json.dump(jobs, f, indent=2)
    
    # Print
    print(f"\n{'='*70}")
    print(f"PARALLEL JOBS GENERATED ({args.splits} jobs)")
    print(f"{'='*70}")
    print(f"Date range: {start} to {end}")
    print(f"Jobs saved to: parallel_jobs.json")
    print(f"{'='*70}\n")
    
    for job in jobs:
        print(f"Job {job['job']}: {job['start']} to {job['end']}")
        print(f"  {job['command']}\n")
    
    # Create batch file for Windows
    with open('run_all.bat', 'w') as f:
        f.write('@echo off\n')
        f.write('echo Starting all scraping jobs...\n\n')
        for job in jobs:
            f.write(f'echo Job {job["job"]}: {job["start"]} to {job["end"]}\n')
            f.write(f'start cmd /k "{job["command"]}"\n')
            f.write('timeout /t 2 /nobreak >nul\n\n')
        f.write('echo All jobs started!\n')
        f.write('pause\n')
    
    print("✅ Batch file created: run_all.bat")
    print("   Run this to start all jobs in separate windows\n")

if __name__ == "__main__":
    main()
