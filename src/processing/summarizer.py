#!/usr/bin/env python3
"""
LLM-powered Article Summarizer using Groq API
Reduces long articles to 5-10 key points for FinBERT processing

Author: StockBus Team
Created: October 9, 2025 (Day 3)
Free API: Groq (14,400 requests/day)
"""

import os
import sys
import json
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class ArticleSummarizer:
    """
    Summarizes financial news articles using Groq LLM API
    
    Features:
    - Free Groq API (llama-3.1-8b-instant)
    - Batch processing with progress bars
    - Automatic retry logic
    - Rate limiting (25 req/min)
    - Saves intermediate results
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize summarizer with config"""
        self.config = self._load_config(config_path)
        self.client = None
        self.stats = {
            'total_articles': 0,
            'summarized': 0,
            'skipped': 0,
            'failed': 0,
            'total_tokens': 0
        }
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML"""
        config_file = project_root / config_path
        
        if not config_file.exists():
            raise FileNotFoundError(
                f"❌ Config file not found: {config_file}\n"
                f"Please create config/config.yaml with your Groq API key"
            )
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate API key
        api_key = config.get('llm', {}).get('groq', {}).get('api_key', '')
        if not api_key or api_key == 'YOUR_GROQ_API_KEY_HERE':
            raise ValueError(
                "❌ Groq API key not set!\n"
                "1. Get free API key: https://console.groq.com/keys\n"
                "2. Add to config/config.yaml under llm.groq.api_key"
            )
        
        return config
    
    def _init_groq_client(self):
        """Initialize Groq API client"""
        try:
            from groq import Groq
        except ImportError:
            print("📦 Installing groq package...")
            os.system(f"{sys.executable} -m pip install groq")
            from groq import Groq
        
        api_key = self.config['llm']['groq']['api_key']
        self.client = Groq(api_key=api_key)
        print(f"✅ Groq API initialized (Model: {self.config['llm']['groq']['model']})")
    
    def _create_summary_prompt(self, article: Dict) -> str:
        """Create prompt for article summarization"""
        title = article.get('title', 'No title')
        body = article.get('body', '')
        
        # Truncate if too long
        max_tokens = self.config['llm']['summarization']['max_input_tokens']
        max_chars = max_tokens * 4  # Rough estimate: 1 token ≈ 4 chars
        
        if len(body) > max_chars:
            body = body[:max_chars] + "..."
        
        prompt = f"""You are a financial news analyst. Extract 5-10 KEY FACTS from this Indian stock market news article.

CRITICAL REQUIREMENTS:
- Output ONLY the factual statements, one per line
- NO introductory text like "Here are the key points" or "Summary:"
- NO bullet symbols (•, *, -) - just plain text facts
- NO bold markdown (**text**)
- Focus on: market movements, company news, economic indicators, policy changes
- Keep each fact concise (1-2 sentences max)
- Preserve ALL numbers, percentages, and company names exactly
- Remove opinions and editorial commentary

TITLE: {title}

ARTICLE:
{body}

KEY FACTS (one per line, no bullets, no formatting):"""
        
        return prompt
    
    def _clean_summary(self, summary: str) -> str:
        """
        Clean and format summary for FinBERT processing
        
        Removes:
        - Introductory phrases ("Here are the key points...")
        - Bullet symbols (•, *, -)
        - Bold markdown (**text**)
        - Extra whitespace and empty lines
        """
        lines = summary.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip common intro phrases
            skip_phrases = [
                'here are the key',
                'summary:',
                'key points:',
                'key facts:',
                'main points:',
                'highlights:',
            ]
            
            if any(phrase in line.lower()[:30] for phrase in skip_phrases):
                continue
            
            # Remove bullet symbols at start
            line = line.lstrip('•*-–—→ ')
            
            # Remove bold markdown
            line = line.replace('**', '')
            
            # Remove extra spaces
            line = ' '.join(line.split())
            
            if line:  # Only add non-empty lines
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def summarize_article(self, article: Dict) -> Optional[str]:
        """
        Summarize a single article using Groq API
        
        Args:
            article: Article dictionary with 'title' and 'body'
        
        Returns:
            Summary string or None if failed
        """
        if not self.client:
            self._init_groq_client()
        
        prompt = self._create_summary_prompt(article)
        
        # Retry logic
        max_retries = self.config['llm']['rate_limit']['retry_attempts']
        retry_delay = self.config['llm']['rate_limit']['retry_delay']
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config['llm']['groq']['model'],
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a financial news analyst specializing in Indian stock markets."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.config['llm']['summarization']['temperature'],
                    max_tokens=self.config['llm']['summarization']['max_tokens'],
                )
                
                summary = response.choices[0].message.content.strip()
                
                # Clean up the summary
                summary = self._clean_summary(summary)
                
                # Track token usage
                if hasattr(response, 'usage'):
                    self.stats['total_tokens'] += response.usage.total_tokens
                
                return summary
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Attempt {attempt + 1} failed: {str(e)[:100]}. Retrying...")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ Failed after {max_retries} attempts: {str(e)[:100]}")
                    return None
        
        return None
    
    def process_dataset(
        self,
        input_file: str = "data/datasets/finbert_ready.json",
        output_file: str = "data/datasets/summarized_dataset.json",
        batch_size: int = 10,
        test_mode: bool = False,
        test_count: int = 5
    ):
        """
        Process entire dataset and summarize articles that need it
        
        Args:
            input_file: Path to finbert_ready.json
            output_file: Path to save summarized dataset
            batch_size: Save results every N articles
            test_mode: If True, only process first test_count articles
            test_count: Number of articles to process in test mode
        """
        print("\n" + "="*70)
        print("🤖 GROQ LLM ARTICLE SUMMARIZER")
        print("="*70)
        
        # Load dataset
        input_path = project_root / input_file
        if not input_path.exists():
            raise FileNotFoundError(f"❌ Input file not found: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"\n📂 Loaded: {len(articles)} articles from {input_file}")
        
        # Filter articles that need summarization
        # Check both 'processing' field and legacy 'needs_summary' field
        # ALSO summarize 'use_as_is' articles to remove noise and improve accuracy
        articles_to_summarize = [
            a for a in articles 
            if (a.get('processing') == 'needs_summary' or 
                a.get('processing') == 'use_as_is' or
                a.get('needs_summary', False) or
                not a.get('summarized', False))  # Skip already summarized
        ]
        
        print(f"📝 Articles to summarize: {len(articles_to_summarize)}")
        print(f"💡 Benefit: Removes ads, links, and noise for better sentiment accuracy")
        
        if test_mode:
            articles_to_summarize = articles_to_summarize[:test_count]
            print(f"🧪 TEST MODE: Processing only {len(articles_to_summarize)} articles")
        
        if not articles_to_summarize:
            print("✅ No articles need summarization!")
            return
        
        # Initialize client
        self._init_groq_client()
        
        # Process articles with progress bar
        print(f"\n🚀 Starting summarization...")
        print(f"⏱️ Estimated time: ~{len(articles_to_summarize) * 3 // 60} minutes\n")
        
        self.stats['total_articles'] = len(articles_to_summarize)
        
        # Rate limiting
        max_rpm = self.config['llm']['rate_limit']['max_requests_per_minute']
        delay_between_requests = 60 / max_rpm
        
        output_path = project_root / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        for idx, article in enumerate(tqdm(
            articles_to_summarize,
            desc="Summarizing",
            unit="article"
        ), 1):
            
            # Generate summary
            summary = self.summarize_article(article)
            
            if summary:
                article['summary'] = summary
                article['summarized'] = True
                article['summarized_at'] = datetime.now().isoformat()
                article['processing'] = 'summarized'  # Update processing status
                article['needs_summary'] = False  # Legacy field
                self.stats['summarized'] += 1
            else:
                article['summarized'] = False
                article['summary_error'] = "Failed to generate summary"
                self.stats['failed'] += 1
            
            # Rate limiting
            if idx < len(articles_to_summarize):
                time.sleep(delay_between_requests)
            
            # Save intermediate results every batch_size articles
            if idx % batch_size == 0:
                self._save_dataset(articles, output_path)
                print(f"\n💾 Saved checkpoint: {idx}/{len(articles_to_summarize)} articles")
        
        # Final save
        self._save_dataset(articles, output_path)
        
        # Print statistics
        self._print_stats(output_path)
    
    def _save_dataset(self, articles: List[Dict], output_path: Path):
        """Save dataset to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
    
    def _print_stats(self, output_path: Path):
        """Print summarization statistics"""
        print("\n" + "="*70)
        print("📊 SUMMARIZATION COMPLETE")
        print("="*70)
        print(f"\n✅ Summarized: {self.stats['summarized']}")
        print(f"⏭️ Skipped: {self.stats['skipped']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"📊 Total: {self.stats['total_articles']}")
        
        if self.stats['total_tokens'] > 0:
            print(f"\n🔢 Total tokens used: {self.stats['total_tokens']:,}")
            print(f"💰 Cost: $0.00 (Free tier)")
        
        print(f"\n💾 Output saved to: {output_path}")
        print(f"📏 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        print("\n" + "="*70)
        print("✅ ALL DONE!")
        print("="*70)
        print("\nNext steps:")
        print("1. Review sample summaries in the output file")
        print("2. If quality is good, process all articles")
        print("3. Move to Day 5: FinBERT sentiment analysis")
        print("="*70 + "\n")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Summarize financial news articles using Groq LLM"
    )
    parser.add_argument(
        '--input',
        default='data/datasets/finbert_ready.json',
        help='Input file path (default: data/datasets/finbert_ready.json)'
    )
    parser.add_argument(
        '--output',
        default='data/datasets/summarized_dataset.json',
        help='Output file path (default: data/datasets/summarized_dataset.json)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: only process 5 articles'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Number of articles to process in test mode (default: 5)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Save checkpoint every N articles (default: 10)'
    )
    
    args = parser.parse_args()
    
    try:
        summarizer = ArticleSummarizer()
        summarizer.process_dataset(
            input_file=args.input,
            output_file=args.output,
            batch_size=args.batch_size,
            test_mode=args.test,
            test_count=args.count
        )
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
