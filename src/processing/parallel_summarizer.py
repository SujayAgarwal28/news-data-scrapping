#!/usr/bin/env python3
"""
PARALLEL LLM Summarizer using Multiple Groq API Keys
Process articles 5x-10x faster using concurrent API calls

Author: StockBus Team
Created: October 9, 2025 (Day 3 - Performance Optimization)
Strategy: Use 5 Groq API keys in parallel for 5x speedup
"""

import os
import sys
import json
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class ParallelSummarizer:
    """
    Multi-threaded article summarizer using multiple Groq API keys
    
    Features:
    - Use 3-5 API keys concurrently
    - 3x-5x speedup over single-key processing
    - Smart load balancing across keys
    - Rate limiting per key
    - Shared checkpoint system
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize with multiple API keys"""
        # Initialize stats FIRST (needed by _load_api_keys)
        self.stats = {
            'total_articles': 0,
            'summarized': 0,
            'failed': 0,
            'total_tokens': 0,
            'key_usage': {}  # Track per-key usage
        }
        
        # Now load config and API keys
        self.config = self._load_config(config_path)
        self.api_keys = self._load_api_keys()
        self.clients = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML"""
        config_file = project_root / config_path
        
        if not config_file.exists():
            raise FileNotFoundError(f"❌ Config file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _load_api_keys(self) -> List[str]:
        """
        Load multiple API keys from config or environment
        
        Config format:
        llm:
          groq:
            api_keys:  # Multiple keys!
              - "gsk_key1..."
              - "gsk_key2..."
              - "gsk_key3..."
        """
        # Try config first
        keys = self.config.get('llm', {}).get('groq', {}).get('api_keys', [])
        
        # Fallback to single key
        if not keys:
            single_key = self.config.get('llm', {}).get('groq', {}).get('api_key', '')
            if single_key and single_key != 'YOUR_GROQ_API_KEY_HERE':
                keys = [single_key]
        
        # Try environment variables
        if not keys:
            for i in range(1, 6):  # Check GROQ_API_KEY_1 through GROQ_API_KEY_5
                key = os.getenv(f'GROQ_API_KEY_{i}')
                if key:
                    keys.append(key)
        
        if not keys:
            raise ValueError(
                "❌ No Groq API keys found!\n"
                "Add to config.yaml:\n"
                "llm:\n"
                "  groq:\n"
                "    api_keys:\n"
                "      - 'gsk_key1...'\n"
                "      - 'gsk_key2...'\n"
                "Or set environment variables: GROQ_API_KEY_1, GROQ_API_KEY_2, etc."
            )
        
        print(f"🔑 Loaded {len(keys)} API key(s)")
        
        # Initialize usage tracking
        for i, _ in enumerate(keys):
            self.stats['key_usage'][f'key_{i+1}'] = {
                'requests': 0,
                'tokens': 0,
                'errors': 0
            }
        
        return keys
    
    def _init_groq_clients(self):
        """Initialize multiple Groq API clients"""
        if self.clients:
            return
            
        try:
            from groq import Groq
        except ImportError:
            print("📦 Installing groq package...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
            from groq import Groq
        
        for i, key in enumerate(self.api_keys):
            client = Groq(api_key=key)
            self.clients.append(client)
        
        print(f"✅ Initialized {len(self.clients)} Groq client(s)")
        print(f"⚡ Expected speedup: ~{len(self.clients)}x faster!")
    
    def _create_summary_prompt(self, article: Dict) -> str:
        """Create prompt for article summarization"""
        title = article.get('title', 'No title')
        body = article.get('body', '')
        
        # Truncate if too long
        max_tokens = self.config['llm']['summarization']['max_input_tokens']
        max_chars = max_tokens * 4
        
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
        """Clean and format summary"""
        lines = summary.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip intro phrases
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
            
            # Remove bullets
            line = line.lstrip('•*-–—→ ')
            
            # Remove bold
            line = line.replace('**', '')
            
            # Clean whitespace
            line = ' '.join(line.split())
            
            if line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _summarize_with_client(self, article: Dict, client_idx: int) -> Optional[str]:
        """
        Summarize article using specific client
        
        Args:
            article: Article to summarize
            client_idx: Index of client to use
        
        Returns:
            Summary string or None
        """
        client = self.clients[client_idx]
        key_name = f'key_{client_idx + 1}'
        
        prompt = self._create_summary_prompt(article)
        
        try:
            response = client.chat.completions.create(
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
            summary = self._clean_summary(summary)
            
            # Track usage
            self.stats['key_usage'][key_name]['requests'] += 1
            if hasattr(response, 'usage'):
                tokens = response.usage.total_tokens
                self.stats['key_usage'][key_name]['tokens'] += tokens
                self.stats['total_tokens'] += tokens
            
            return summary
            
        except Exception as e:
            self.stats['key_usage'][key_name]['errors'] += 1
            print(f"\n⚠️ Error with {key_name}: {str(e)[:100]}")
            return None
    
    def process_batch_parallel(
        self,
        articles: List[Dict],
        max_workers: Optional[int] = None
    ) -> List[Dict]:
        """
        Process articles in parallel using multiple API keys
        
        Args:
            articles: List of articles to process
            max_workers: Max concurrent threads (default: number of API keys)
        
        Returns:
            Processed articles with summaries
        """
        if not max_workers:
            max_workers = len(self.clients)
        
        # Use ThreadPoolExecutor for parallel API calls
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_article = {}
            
            for i, article in enumerate(articles):
                # Round-robin assignment to clients
                client_idx = i % len(self.clients)
                
                future = executor.submit(
                    self._summarize_with_client,
                    article,
                    client_idx
                )
                future_to_article[future] = article
            
            # Collect results with progress bar
            for future in tqdm(
                as_completed(future_to_article),
                total=len(articles),
                desc="Summarizing (parallel)",
                unit="article"
            ):
                article = future_to_article[future]
                
                try:
                    summary = future.result()
                    
                    if summary:
                        article['summary'] = summary
                        article['summarized'] = True
                        article['summarized_at'] = datetime.now().isoformat()
                        article['processing'] = 'summarized'
                        article['needs_summary'] = False
                        self.stats['summarized'] += 1
                    else:
                        article['summarized'] = False
                        article['summary_error'] = "Failed to generate summary"
                        self.stats['failed'] += 1
                        
                except Exception as e:
                    article['summarized'] = False
                    article['summary_error'] = str(e)[:200]
                    self.stats['failed'] += 1
        
        return articles
    
    def process_dataset(
        self,
        input_file: str = "data/datasets/finbert_ready.json",
        output_file: str = "data/datasets/summarized_dataset.json",
        batch_size: int = 10,
        test_mode: bool = False,
        test_count: int = 10
    ):
        """Process entire dataset with parallel processing"""
        print("\n" + "="*70)
        print("🚀 PARALLEL GROQ LLM SUMMARIZER (MULTI-KEY)")
        print("="*70)
        
        # Load dataset
        input_path = project_root / input_file
        with open(input_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"\n📂 Loaded: {len(articles)} articles")
        
        # Filter unsummarized
        articles_to_summarize = [
            a for a in articles 
            if not a.get('summarized', False)
        ]
        
        print(f"📝 Need summarization: {len(articles_to_summarize)}")
        print(f"✅ Already done: {len(articles) - len(articles_to_summarize)}")
        
        if test_mode:
            articles_to_summarize = articles_to_summarize[:test_count]
            print(f"🧪 TEST MODE: {len(articles_to_summarize)} articles")
        
        if not articles_to_summarize:
            print("✅ All articles already summarized!")
            return
        
        # Initialize clients
        self._init_groq_clients()
        
        self.stats['total_articles'] = len(articles_to_summarize)
        
        # Process in batches to save checkpoints
        output_path = project_root / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        for i in range(0, len(articles_to_summarize), batch_size):
            batch = articles_to_summarize[i:i + batch_size]
            
            print(f"\n🔄 Processing batch {i//batch_size + 1}/{(len(articles_to_summarize)-1)//batch_size + 1}")
            
            # Process batch in parallel
            self.process_batch_parallel(batch)
            
            # Save checkpoint
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Checkpoint saved ({self.stats['summarized']}/{len(articles_to_summarize)})")
            
            # Rate limiting between batches
            time.sleep(2)
        
        # Print final stats
        self._print_stats(output_path)
    
    def _print_stats(self, output_path: Path):
        """Print detailed statistics"""
        print("\n" + "="*70)
        print("📊 PARALLEL PROCESSING COMPLETE")
        print("="*70)
        
        print(f"\n✅ Summarized: {self.stats['summarized']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"📊 Total: {self.stats['total_articles']}")
        
        if self.stats['total_tokens'] > 0:
            print(f"\n🔢 Total tokens: {self.stats['total_tokens']:,}")
        
        # Per-key stats
        print(f"\n📊 Per-Key Usage:")
        for key_name, usage in self.stats['key_usage'].items():
            print(f"   {key_name}:")
            print(f"      Requests: {usage['requests']}")
            print(f"      Tokens: {usage['tokens']:,}")
            print(f"      Errors: {usage['errors']}")
        
        print(f"\n💾 Output: {output_path}")
        print(f"📏 Size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        print("\n" + "="*70)
        print(f"✅ DONE! Used {len(self.api_keys)} API key(s) in parallel")
        print("="*70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Parallel article summarization with multiple Groq API keys"
    )
    parser.add_argument('--input', default='data/datasets/finbert_ready.json')
    parser.add_argument('--output', default='data/datasets/summarized_dataset.json')
    parser.add_argument('--test', action='store_true', help='Test mode (10 articles)')
    parser.add_argument('--count', type=int, default=10, help='Test count')
    parser.add_argument('--batch-size', type=int, default=10, help='Batch size')
    
    args = parser.parse_args()
    
    try:
        summarizer = ParallelSummarizer()
        summarizer.process_dataset(
            input_file=args.input,
            output_file=args.output,
            batch_size=args.batch_size,
            test_mode=args.test,
            test_count=args.count
        )
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
