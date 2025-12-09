#!/usr/bin/env python3
"""
Go Squad Knowledge Loader (Advanced)
Extends base loader with API integration capabilities for AI-powered analysis.

Features:
- API key management (environment variables + config file)
- AI-powered summarization (OpenAI, Anthropic, etc.)
- Semantic search across knowledge base
- Continuity checking and validation
- Character relationship graphs
- Timeline analysis

Usage:
    python3 gosquad_knowledge_loader_advanced.py --essential
    python3 gosquad_knowledge_loader_advanced.py --ai-summary characters
    python3 gosquad_knowledge_loader_advanced.py --semantic-search "time powers"
    python3 gosquad_knowledge_loader_advanced.py --validate-continuity
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

# Import base loader
from gosquad_knowledge_loader import KnowledgeBase, KnowledgeFile


class APIProvider(Enum):
    """Supported API providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    LOCAL = "local"  # For local LLM APIs (Ollama, etc.)


@dataclass
class APIConfig:
    """API configuration and credentials"""
    provider: APIProvider
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    enabled: bool = False

    @classmethod
    def from_env(cls, provider: APIProvider) -> 'APIConfig':
        """Load API config from environment variables"""
        env_prefix = provider.value.upper()

        api_key = os.getenv(f'{env_prefix}_API_KEY')
        api_base = os.getenv(f'{env_prefix}_API_BASE')
        model = os.getenv(f'{env_prefix}_MODEL')

        # Default models per provider
        default_models = {
            APIProvider.OPENAI: "gpt-4",
            APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
            APIProvider.COHERE: "command-r-plus",
            APIProvider.LOCAL: "llama2",
        }

        return cls(
            provider=provider,
            api_key=api_key,
            api_base=api_base,
            model=model or default_models.get(provider),
            enabled=api_key is not None
        )

    @classmethod
    def from_config_file(cls, config_path: Path) -> Dict[APIProvider, 'APIConfig']:
        """Load API configs from JSON config file"""
        if not config_path.exists():
            return {}

        with open(config_path, 'r') as f:
            data = json.load(f)

        configs = {}
        for provider_str, config_data in data.get('api_providers', {}).items():
            try:
                provider = APIProvider(provider_str)
                configs[provider] = cls(
                    provider=provider,
                    api_key=config_data.get('api_key'),
                    api_base=config_data.get('api_base'),
                    model=config_data.get('model'),
                    max_tokens=config_data.get('max_tokens', 4000),
                    temperature=config_data.get('temperature', 0.7),
                    enabled=config_data.get('enabled', False)
                )
            except ValueError:
                print(f"⚠ Unknown provider '{provider_str}' in config")

        return configs


class APIManager:
    """Manages API connections and requests"""

    def __init__(self, configs: Dict[APIProvider, APIConfig]):
        self.configs = configs
        self.active_provider = None
        self._select_active_provider()

    def _select_active_provider(self):
        """Select first enabled provider"""
        for provider, config in self.configs.items():
            if config.enabled and config.api_key:
                self.active_provider = provider
                print(f"✓ API enabled: {provider.value} ({config.model})")
                return
        print("ℹ No API providers enabled (API features disabled)")

    def is_available(self) -> bool:
        """Check if any API is available"""
        return self.active_provider is not None

    def make_request(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Make API request to active provider"""
        if not self.is_available():
            return None

        config = self.configs[self.active_provider]

        try:
            if self.active_provider == APIProvider.OPENAI:
                return self._openai_request(config, prompt, system_prompt)
            elif self.active_provider == APIProvider.ANTHROPIC:
                return self._anthropic_request(config, prompt, system_prompt)
            elif self.active_provider == APIProvider.LOCAL:
                return self._local_request(config, prompt, system_prompt)
            else:
                print(f"⚠ Provider {self.active_provider.value} not yet implemented")
                return None
        except Exception as e:
            print(f"⚠ API request failed: {e}")
            return None

    def _openai_request(self, config: APIConfig, prompt: str, system_prompt: Optional[str]) -> str:
        """Make OpenAI API request"""
        try:
            import openai
        except ImportError:
            print("⚠ openai package not installed. Run: pip install openai")
            return None

        client = openai.OpenAI(
            api_key=config.api_key,
            base_url=config.api_base
        )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )

        return response.choices[0].message.content

    def _anthropic_request(self, config: APIConfig, prompt: str, system_prompt: Optional[str]) -> str:
        """Make Anthropic API request"""
        try:
            import anthropic
        except ImportError:
            print("⚠ anthropic package not installed. Run: pip install anthropic")
            return None

        client = anthropic.Anthropic(
            api_key=config.api_key,
            base_url=config.api_base
        )

        response = client.messages.create(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            system=system_prompt or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    def _local_request(self, config: APIConfig, prompt: str, system_prompt: Optional[str]) -> str:
        """Make local LLM API request (Ollama, etc.)"""
        import requests

        api_base = config.api_base or "http://localhost:11434"

        payload = {
            "model": config.model,
            "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
            "stream": False,
            "options": {
                "temperature": config.temperature,
                "num_predict": config.max_tokens
            }
        }

        response = requests.post(f"{api_base}/api/generate", json=payload)
        response.raise_for_status()

        return response.json()['response']


class AdvancedKnowledgeBase(KnowledgeBase):
    """Extended knowledge base with API-powered features"""

    def __init__(self, root_path: Path, api_manager: Optional[APIManager] = None):
        super().__init__(root_path)
        self.api_manager = api_manager or APIManager({})

    def ai_summarize_category(self, category: str) -> Optional[str]:
        """Generate AI-powered summary of category"""
        if not self.api_manager.is_available():
            print("⚠ AI features require API configuration")
            return None

        if category not in self.files:
            print(f"⚠ Category '{category}' not found")
            return None

        print(f"\n🤖 Generating AI summary for '{category}'...")

        # Gather content from category
        content_parts = []
        for kf in self.files[category]:
            if not kf.content:
                kf.load()
            content_parts.append(f"=== {kf.name} ===\n{kf.content}\n")

        combined_content = "\n".join(content_parts)

        # Truncate if too large (rough token estimate: 4 chars = 1 token)
        max_chars = 12000  # ~3000 tokens
        if len(combined_content) > max_chars:
            combined_content = combined_content[:max_chars] + "\n\n[Content truncated...]"

        system_prompt = """You are analyzing knowledge base documentation for the Go Squad book series.
Provide a comprehensive yet concise summary highlighting:
- Key characters and their roles
- Important plot points
- Continuity elements
- Relationships and conflicts
- Any inconsistencies or gaps"""

        prompt = f"Summarize this {category} documentation:\n\n{combined_content}"

        response = self.api_manager.make_request(prompt, system_prompt)

        if response:
            print("✓ Summary generated\n")

        return response

    def semantic_search(self, query: str, top_k: int = 5) -> Optional[List[Tuple[KnowledgeFile, str, float]]]:
        """AI-powered semantic search (finds relevant content by meaning, not just keywords)"""
        if not self.api_manager.is_available():
            print("⚠ Semantic search requires API configuration")
            return None

        print(f"\n🔍 Semantic search for: '{query}'...")

        # Load all content
        for files in self.files.values():
            for kf in files:
                if not kf.content:
                    kf.load()

        # Create search prompt
        file_summaries = []
        for category, files in self.files.items():
            for kf in files:
                # Get excerpt
                excerpt = '\n'.join(kf.content.splitlines()[:50])
                file_summaries.append(f"File: {kf.name}\nCategory: {category}\nExcerpt: {excerpt}\n")

        combined = "\n---\n".join(file_summaries[:20])  # Limit to prevent token overflow

        system_prompt = """You are helping search Go Squad knowledge base documentation.
For the given query, identify which files are most relevant and explain why.
Return response as JSON array: [{"file": "filename", "relevance": "explanation", "score": 0.0-1.0}]"""

        prompt = f"Query: {query}\n\nFiles:\n{combined}\n\nReturn top {top_k} most relevant files as JSON."

        response = self.api_manager.make_request(prompt, system_prompt)

        if response:
            try:
                # Parse JSON response
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    results = json.loads(json_match.group())
                    print(f"✓ Found {len(results)} relevant files\n")
                    return results
            except Exception as e:
                print(f"⚠ Failed to parse semantic search results: {e}")

        return None

    def validate_continuity(self) -> Optional[str]:
        """Check for continuity issues across knowledge base"""
        if not self.api_manager.is_available():
            print("⚠ Continuity validation requires API configuration")
            return None

        print("\n🔍 Validating continuity across knowledge base...")

        # Gather key files for validation
        key_categories = ['characters', 'timeline', 'root']
        content_parts = []

        for category in key_categories:
            if category in self.files:
                for kf in self.files[category][:5]:  # Limit to prevent overflow
                    if not kf.content:
                        kf.load()
                    excerpt = '\n'.join(kf.content.splitlines()[:100])
                    content_parts.append(f"=== {kf.name} ===\n{excerpt}\n")

        combined_content = "\n".join(content_parts)

        system_prompt = """You are reviewing Go Squad series documentation for continuity issues.
Check for:
- Timeline inconsistencies
- Character contradictions
- Plot holes
- Power/ability conflicts
- Setting/location mismatches
- Relationship status conflicts

Report any issues found with specific file references."""

        prompt = f"Review this content for continuity issues:\n\n{combined_content}"

        response = self.api_manager.make_request(prompt, system_prompt)

        if response:
            print("✓ Continuity check complete\n")

        return response

    def analyze_character_relationships(self) -> Optional[str]:
        """Generate character relationship analysis"""
        if not self.api_manager.is_available():
            print("⚠ Relationship analysis requires API configuration")
            return None

        if 'characters' not in self.files:
            print("⚠ No character files found")
            return None

        print("\n🤖 Analyzing character relationships...")

        # Load character files
        char_content = []
        for kf in self.files['characters']:
            if not kf.content:
                kf.load()
            excerpt = '\n'.join(kf.content.splitlines()[:150])
            char_content.append(f"=== {kf.name} ===\n{excerpt}\n")

        combined = "\n".join(char_content[:10])  # Limit files

        system_prompt = """You are analyzing character relationships in the Go Squad series.
Generate a relationship map showing:
- Primary relationships (family, romantic, friends)
- Professional connections
- Conflicts and tensions
- Character dynamics
- Relationship evolution across books

Format as clear hierarchy or network."""

        prompt = f"Analyze relationships in this character data:\n\n{combined}"

        response = self.api_manager.make_request(prompt, system_prompt)

        if response:
            print("✓ Relationship analysis complete\n")

        return response


def load_api_config(config_path: Path) -> Dict[APIProvider, APIConfig]:
    """Load API configuration from environment and config file"""
    configs = {}

    # Load from environment variables
    for provider in APIProvider:
        config = APIConfig.from_env(provider)
        if config.enabled:
            configs[provider] = config

    # Load from config file (overrides env vars)
    file_configs = APIConfig.from_config_file(config_path)
    configs.update(file_configs)

    return configs


def create_example_config(config_path: Path):
    """Create example configuration file"""
    example_config = {
        "_comment": "Go Squad Knowledge Loader API Configuration",
        "_note": "API keys can be set here or via environment variables",
        "_security": "DO NOT commit this file with real API keys!",
        "api_providers": {
            "openai": {
                "enabled": False,
                "api_key": "sk-...",
                "api_base": None,
                "model": "gpt-4",
                "max_tokens": 4000,
                "temperature": 0.7
            },
            "anthropic": {
                "enabled": False,
                "api_key": "sk-ant-...",
                "api_base": None,
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 4000,
                "temperature": 0.7
            },
            "local": {
                "enabled": False,
                "api_key": None,
                "api_base": "http://localhost:11434",
                "model": "llama2",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        }
    }

    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=2)

    print(f"✓ Created example config at: {config_path}")
    print(f"  Edit this file to configure API providers")
    print(f"  Or set environment variables: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.")


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Go Squad knowledge loader with API integration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Base options
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    parser.add_argument('--essential', action='store_true', help='Essential context')
    parser.add_argument('--category', type=str, help='Load specific category')
    parser.add_argument('--search', type=str, help='Keyword search')
    parser.add_argument('--export', type=str, help='Export to JSON')

    # API-powered options
    parser.add_argument('--ai-summary', type=str, help='AI-powered category summary')
    parser.add_argument('--semantic-search', type=str, help='Semantic search query')
    parser.add_argument('--validate-continuity', action='store_true', help='Check continuity')
    parser.add_argument('--analyze-relationships', action='store_true', help='Analyze character relationships')

    # Configuration
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--create-config', action='store_true', help='Create example config')
    parser.add_argument('--api-provider', type=str, help='Preferred API provider')

    args = parser.parse_args()

    # Initialize paths - go up two levels from editor_suite/knowledge_system/ to workspace root
    root_path = Path(__file__).parent.parent.parent
    config_path = Path(args.config) if args.config else root_path / '.gosquad' / 'api_config.json'

    # Handle config creation
    if args.create_config:
        create_example_config(config_path)
        return

    # Load API configuration
    api_configs = load_api_config(config_path)
    api_manager = APIManager(api_configs)

    # Initialize knowledge base
    kb = AdvancedKnowledgeBase(root_path=root_path, api_manager=api_manager)
    kb.discover_files()

    # Handle API-powered features
    if args.ai_summary:
        kb.load_all(categories=[args.ai_summary])
        result = kb.ai_summarize_category(args.ai_summary)
        if result:
            print("=" * 80)
            print(f"AI SUMMARY: {args.ai_summary.upper()}")
            print("=" * 80)
            print(result)
        return

    if args.semantic_search:
        kb.load_all()
        results = kb.semantic_search(args.semantic_search)
        if results:
            print("=" * 80)
            print("SEMANTIC SEARCH RESULTS")
            print("=" * 80)
            for result in results:
                print(f"\n📄 {result['file']}")
                print(f"   Relevance: {result.get('score', 'N/A')}")
                print(f"   {result['relevance']}")
        return

    if args.validate_continuity:
        kb.load_all()
        result = kb.validate_continuity()
        if result:
            print("=" * 80)
            print("CONTINUITY VALIDATION")
            print("=" * 80)
            print(result)
        return

    if args.analyze_relationships:
        kb.load_all(categories=['characters'])
        result = kb.analyze_character_relationships()
        if result:
            print("=" * 80)
            print("CHARACTER RELATIONSHIP ANALYSIS")
            print("=" * 80)
            print(result)
        return

    # Fall back to base functionality
    print("ℹ For AI-powered features, use: --ai-summary, --semantic-search, etc.")
    print("ℹ To configure APIs, use: --create-config")
    print()

    # Basic mode
    categories = [args.category] if args.category else None
    kb.load_all(categories=categories)

    if args.summary:
        print(kb.generate_summary())
    elif args.essential:
        print(kb.get_essential_context())
    elif args.search:
        results = kb.search(args.search)
        if results:
            print(f"\n🔍 Found {len(results)} files with '{args.search}':\n")
            for kf, lines in results:
                print(f"📄 {kf.name} ({len(lines)} matches)")
                for line in lines[:3]:
                    print(f"   {line.strip()}")
                if len(lines) > 3:
                    print(f"   ... ({len(lines) - 3} more matches)")
                print()
    elif args.export:
        kb.export_json(Path(args.export))
    else:
        print(kb.get_essential_context())


if __name__ == '__main__':
    main()
