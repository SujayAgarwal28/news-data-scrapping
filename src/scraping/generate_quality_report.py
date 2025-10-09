"""
Data Quality Report Generator
==============================

Analyzes scraped news data and generates quality reports.

Features:
- Body length distribution
- Extraction method breakdown
- Publisher statistics
- Date coverage analysis
- Data quality metrics

Usage:
    python scripts/generate_quality_report.py
    python scripts/generate_quality_report.py --input data/raw/news/sample.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class QualityReporter:
    """Generate data quality reports"""
    
    def __init__(self, data_dir="data/raw/news"):
        self.data_dir = Path(data_dir)
        self.articles = []
        
    def load_data(self, file_pattern="*.json"):
        """Load all JSON files"""
        print(f"\n📂 Loading data from: {self.data_dir}")
        
        files = list(self.data_dir.glob(file_pattern))
        print(f"   Found {len(files)} JSON files")
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.articles.extend(data)
                    else:
                        self.articles.append(data)
                print(f"   ✅ Loaded: {file.name} ({len(data) if isinstance(data, list) else 1} articles)")
            except Exception as e:
                print(f"   ❌ Error loading {file.name}: {e}")
        
        print(f"\n📊 Total articles loaded: {len(self.articles)}\n")
        return len(self.articles)
    
    def analyze(self):
        """Generate comprehensive analysis"""
        if not self.articles:
            print("❌ No articles to analyze!")
            return {}
        
        report = {
            'total_articles': len(self.articles),
            'timestamp': datetime.now().isoformat(),
            'body_stats': self._analyze_body_length(),
            'extraction_methods': self._analyze_extraction_methods(),
            'publishers': self._analyze_publishers(),
            'dates': self._analyze_dates(),
            'topics': self._analyze_topics(),
            'metadata_quality': self._analyze_metadata_quality(),
        }
        
        return report
    
    def _analyze_body_length(self):
        """Analyze body text length distribution"""
        lengths = [a.get('body_length', 0) for a in self.articles]
        word_counts = [a.get('word_count', 0) for a in self.articles]
        
        return {
            'min_chars': min(lengths) if lengths else 0,
            'max_chars': max(lengths) if lengths else 0,
            'avg_chars': sum(lengths) / len(lengths) if lengths else 0,
            'median_chars': sorted(lengths)[len(lengths)//2] if lengths else 0,
            'min_words': min(word_counts) if word_counts else 0,
            'max_words': max(word_counts) if word_counts else 0,
            'avg_words': sum(word_counts) / len(word_counts) if word_counts else 0,
            'distribution': {
                'very_short_(<500)': sum(1 for l in lengths if l < 500),
                'short_(500-1500)': sum(1 for l in lengths if 500 <= l < 1500),
                'medium_(1500-3000)': sum(1 for l in lengths if 1500 <= l < 3000),
                'long_(3000-5000)': sum(1 for l in lengths if 3000 <= l < 5000),
                'very_long_(>5000)': sum(1 for l in lengths if l >= 5000),
            }
        }
    
    def _analyze_extraction_methods(self):
        """Analyze extraction methods used"""
        methods = [a.get('extraction_method', 'unknown') for a in self.articles]
        counter = Counter(methods)
        
        return {
            'breakdown': dict(counter),
            'newspaper3k_rate': counter.get('newspaper3k', 0) / len(methods) * 100 if methods else 0,
            'beautifulsoup_rate': counter.get('beautifulsoup', 0) / len(methods) * 100 if methods else 0,
        }
    
    def _analyze_publishers(self):
        """Analyze publisher distribution"""
        publishers = [a.get('publisher', 'Unknown') for a in self.articles]
        counter = Counter(publishers)
        
        return {
            'total_unique': len(counter),
            'top_10': dict(counter.most_common(10)),
        }
    
    def _analyze_dates(self):
        """Analyze date coverage"""
        scraped_dates = [a.get('scraped_date', '') for a in self.articles if a.get('scraped_date')]
        published_dates = [a.get('published_date', '') for a in self.articles if a.get('published_date')]
        
        return {
            'earliest_scraped': min(scraped_dates) if scraped_dates else 'N/A',
            'latest_scraped': max(scraped_dates) if scraped_dates else 'N/A',
            'total_scraped_dates': len(set(scraped_dates)),
            'articles_with_publish_date': len(published_dates),
            'publish_date_coverage': len(published_dates) / len(self.articles) * 100 if self.articles else 0,
        }
    
    def _analyze_topics(self):
        """Analyze topic distribution"""
        topics = [a.get('topic', 'Unknown') for a in self.articles]
        counter = Counter(topics)
        
        return {
            'total_unique': len(counter),
            'breakdown': dict(counter),
        }
    
    def _analyze_metadata_quality(self):
        """Analyze metadata completeness"""
        has_authors = sum(1 for a in self.articles if a.get('authors') and len(a.get('authors', [])) > 0)
        has_published_date = sum(1 for a in self.articles if a.get('published_date'))
        has_publisher = sum(1 for a in self.articles if a.get('publisher'))
        
        total = len(self.articles)
        
        return {
            'authors_coverage': has_authors / total * 100 if total else 0,
            'published_date_coverage': has_published_date / total * 100 if total else 0,
            'publisher_coverage': has_publisher / total * 100 if total else 0,
            'articles_with_authors': has_authors,
            'articles_with_published_date': has_published_date,
            'articles_with_publisher': has_publisher,
        }
    
    def print_report(self, report):
        """Print formatted report"""
        print("\n" + "="*70)
        print("📊 DATA QUALITY REPORT")
        print("="*70)
        print(f"\nGenerated: {report['timestamp']}")
        print(f"Total Articles: {report['total_articles']:,}")
        
        # Body Length Statistics
        print("\n" + "-"*70)
        print("📏 BODY LENGTH STATISTICS")
        print("-"*70)
        stats = report['body_stats']
        print(f"  Characters: {stats['min_chars']:,} (min) | {stats['avg_chars']:,.0f} (avg) | {stats['max_chars']:,} (max)")
        print(f"  Words: {stats['min_words']:,} (min) | {stats['avg_words']:,.0f} (avg) | {stats['max_words']:,} (max)")
        print(f"  Median: {stats['median_chars']:,} characters")
        
        print("\n  Length Distribution:")
        for category, count in stats['distribution'].items():
            percentage = count / report['total_articles'] * 100
            bar = "█" * int(percentage / 2)
            print(f"    {category:20s}: {count:4d} ({percentage:5.1f}%) {bar}")
        
        # Extraction Methods
        print("\n" + "-"*70)
        print("🔧 EXTRACTION METHODS")
        print("-"*70)
        methods = report['extraction_methods']
        print(f"  newspaper3k: {methods['newspaper3k_rate']:.1f}%")
        print(f"  beautifulsoup: {methods['beautifulsoup_rate']:.1f}%")
        print(f"\n  Breakdown:")
        for method, count in methods['breakdown'].items():
            print(f"    {method}: {count}")
        
        # Publishers
        print("\n" + "-"*70)
        print("📰 TOP PUBLISHERS")
        print("-"*70)
        publishers = report['publishers']
        print(f"  Total Unique Publishers: {publishers['total_unique']}")
        print(f"\n  Top 10:")
        for i, (pub, count) in enumerate(publishers['top_10'].items(), 1):
            print(f"    {i:2d}. {pub[:50]:50s}: {count:4d} articles")
        
        # Date Coverage
        print("\n" + "-"*70)
        print("📅 DATE COVERAGE")
        print("-"*70)
        dates = report['dates']
        print(f"  Scraped Date Range: {dates['earliest_scraped']} to {dates['latest_scraped']}")
        print(f"  Total Scraped Dates: {dates['total_scraped_dates']}")
        print(f"  Publish Date Coverage: {dates['publish_date_coverage']:.1f}%")
        
        # Topics
        print("\n" + "-"*70)
        print("🎯 TOPICS")
        print("-"*70)
        topics = report['topics']
        print(f"  Total Unique Topics: {topics['total_unique']}")
        print(f"\n  Breakdown:")
        for topic, count in topics['breakdown'].items():
            print(f"    {topic[:60]:60s}: {count:4d} articles")
        
        # Metadata Quality
        print("\n" + "-"*70)
        print("✅ METADATA QUALITY")
        print("-"*70)
        meta = report['metadata_quality']
        print(f"  Authors: {meta['authors_coverage']:.1f}% ({meta['articles_with_authors']}/{report['total_articles']})")
        print(f"  Published Date: {meta['published_date_coverage']:.1f}% ({meta['articles_with_published_date']}/{report['total_articles']})")
        print(f"  Publisher: {meta['publisher_coverage']:.1f}% ({meta['articles_with_publisher']}/{report['total_articles']})")
        
        # Quality Score
        quality_score = (
            meta['authors_coverage'] * 0.3 +
            meta['published_date_coverage'] * 0.3 +
            meta['publisher_coverage'] * 0.2 +
            methods['newspaper3k_rate'] * 0.2
        )
        
        print("\n" + "-"*70)
        print(f"🎯 OVERALL QUALITY SCORE: {quality_score:.1f}/100")
        print("-"*70)
        
        if quality_score >= 80:
            print("   ✅ EXCELLENT - Data quality is production-ready!")
        elif quality_score >= 60:
            print("   ✅ GOOD - Data quality is acceptable")
        elif quality_score >= 40:
            print("   ⚠️  FAIR - Some improvements needed")
        else:
            print("   ❌ POOR - Significant improvements required")
        
        print("\n" + "="*70 + "\n")
    
    def save_report(self, report, output_file="outputs/reports/data_quality_report.json"):
        """Save report to JSON"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate data quality report')
    parser.add_argument('--input', default='data/raw/news', help='Input directory or file')
    parser.add_argument('--output', default='outputs/reports/data_quality_report.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Generate report
    reporter = QualityReporter(data_dir=args.input)
    
    if reporter.load_data() > 0:
        report = reporter.analyze()
        reporter.print_report(report)
        reporter.save_report(report, args.output)
    else:
        print("\n❌ No data found to analyze!")
        print(f"   Check that {args.input} contains JSON files with scraped articles.\n")


if __name__ == "__main__":
    main()
