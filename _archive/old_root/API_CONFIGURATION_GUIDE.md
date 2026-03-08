# Go Squad Knowledge Loader - API Configuration Guide

## Overview

The advanced knowledge loader supports AI-powered features through multiple API providers:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude 3.5 Sonnet, Opus, Haiku)
- **Local LLMs** (Ollama, LM Studio, etc.)
- **Cohere** (Command R+)

These APIs enable powerful features:
- AI-powered category summaries
- Semantic search (find by meaning, not just keywords)
- Continuity validation across knowledge base
- Character relationship analysis
- Plot consistency checking

## Security First

**⚠️ CRITICAL: Never commit API keys to git!**

The `.gitignore` is configured to exclude:
- `.gosquad/api_config.json`
- `.env` files
- Any file matching `*api_config.json`

## Configuration Methods

### Method 1: Environment Variables (Recommended)

Set environment variables for your preferred provider:

**For OpenAI:**
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4"  # Optional, defaults to gpt-4
```

**For Anthropic:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"  # Optional
```

**For Local LLMs (Ollama):**
```bash
export LOCAL_API_BASE="http://localhost:11434"
export LOCAL_MODEL="llama2"
```

Then run:
```bash
python3 gosquad_knowledge_loader_advanced.py --ai-summary characters
```

The script automatically detects environment variables and enables features.

### Method 2: Configuration File

Create a config file (excluded from git):

```bash
python3 gosquad_knowledge_loader_advanced.py --create-config
```

This creates `.gosquad/api_config.json` with template:

```json
{
  "_comment": "Go Squad Knowledge Loader API Configuration",
  "_note": "API keys can be set here or via environment variables",
  "_security": "DO NOT commit this file with real API keys!",
  "api_providers": {
    "openai": {
      "enabled": true,
      "api_key": "sk-...",
      "api_base": null,
      "model": "gpt-4",
      "max_tokens": 4000,
      "temperature": 0.7
    },
    "anthropic": {
      "enabled": false,
      "api_key": "sk-ant-...",
      "api_base": null,
      "model": "claude-3-5-sonnet-20241022",
      "max_tokens": 4000,
      "temperature": 0.7
    },
    "local": {
      "enabled": false,
      "api_key": null,
      "api_base": "http://localhost:11434",
      "model": "llama2",
      "max_tokens": 4000,
      "temperature": 0.7
    }
  }
}
```

**Edit with your API keys:**
1. Set `"enabled": true` for your provider
2. Add your `"api_key"`
3. Adjust `"model"` if desired
4. Save the file

**The file is automatically ignored by git.**

### Method 3: Custom Config Path

Store config elsewhere:

```bash
python3 gosquad_knowledge_loader_advanced.py \
  --config ~/secure/gosquad_api.json \
  --ai-summary characters
```

## API-Powered Features

### 1. AI Category Summaries

Generate comprehensive AI-powered summaries of any category:

```bash
# Summarize all character profiles
python3 gosquad_knowledge_loader_advanced.py --ai-summary characters

# Summarize timeline events
python3 gosquad_knowledge_loader_advanced.py --ai-summary timeline

# Summarize themes
python3 gosquad_knowledge_loader_advanced.py --ai-summary themes
```

**What it does:**
- Loads all files in category
- Sends to AI with specialized prompt
- Generates summary highlighting:
  - Key characters/concepts
  - Important relationships
  - Continuity elements
  - Potential inconsistencies

**Use cases:**
- Quick refresh on character details
- Understanding theme evolution
- Catching up on timeline events

### 2. Semantic Search

Find content by meaning, not just keywords:

```bash
# Find content about time manipulation powers
python3 gosquad_knowledge_loader_advanced.py --semantic-search "time powers"

# Find relationship conflicts
python3 gosquad_knowledge_loader_advanced.py --semantic-search "character conflicts"

# Find plot holes
python3 gosquad_knowledge_loader_advanced.py --semantic-search "inconsistencies"
```

**How it's different from keyword search:**
- Keyword: Finds exact word matches ("temporal" finds "temporal" only)
- Semantic: Finds related concepts ("time powers" finds "temporal manipulation", "chronokinesis", "reality warping", etc.)

**Returns:**
- Relevant files ranked by relevance
- Explanation of why each file matches
- Relevance scores

**Use cases:**
- Finding related content across categories
- Research for writing scenes
- Verifying how concepts are described

### 3. Continuity Validation

Check for timeline issues, contradictions, and plot holes:

```bash
python3 gosquad_knowledge_loader_advanced.py --validate-continuity
```

**What it checks:**
- Timeline inconsistencies (events out of order)
- Character contradictions (personality, abilities, status)
- Plot holes (missing connections, unexplained events)
- Power/ability conflicts (rules violated)
- Setting/location mismatches
- Relationship status conflicts

**Returns:**
- List of potential issues
- File references where conflicts occur
- Severity assessment

**Use cases:**
- Pre-publication continuity review
- Planning new books (avoid conflicts)
- Fixing reported inconsistencies

### 4. Character Relationship Analysis

Generate relationship maps and dynamics:

```bash
python3 gosquad_knowledge_loader_advanced.py --analyze-relationships
```

**What it generates:**
- Relationship network (who's connected to whom)
- Relationship types (family, romantic, professional, conflict)
- Relationship evolution across books
- Key dynamics and tensions
- Missing relationship development

**Use cases:**
- Planning character arcs
- Ensuring consistent relationship progression
- Finding underutilized relationships
- Tracking character dynamics

## Cost Management

### Token Usage Estimates

**AI Summary (per category):**
- Characters (20 files): ~3,000 input tokens + 1,000 output = $0.04 (GPT-4)
- Timeline (2 files): ~1,000 input tokens + 500 output = $0.015 (GPT-4)

**Semantic Search:**
- Per query: ~2,000 input tokens + 200 output = $0.025 (GPT-4)

**Continuity Validation:**
- Full knowledge base: ~5,000 input tokens + 1,500 output = $0.065 (GPT-4)

**Cost per API provider (approximate):**
- **OpenAI GPT-4**: $0.03/1K input tokens, $0.06/1K output tokens
- **Anthropic Claude 3.5 Sonnet**: $0.003/1K input tokens, $0.015/1K output tokens
- **Local LLMs**: Free (but requires local compute)

**Recommendation:** Use Claude 3.5 Sonnet for cost-effective analysis, or local LLMs for zero cost.

### Token Limits

The script automatically truncates content to prevent token overflow:
- Category summaries: Max 12,000 chars (~3,000 tokens)
- Semantic search: Max 20 files analyzed
- Continuity checks: Max 5 files per category

For larger analysis, the script processes in batches.

## Provider-Specific Setup

### OpenAI Setup

1. Get API key: https://platform.openai.com/api-keys
2. Set environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
3. Verify:
   ```bash
   python3 gosquad_knowledge_loader_advanced.py --ai-summary characters
   ```

**Pricing:** https://openai.com/pricing

### Anthropic Setup

1. Get API key: https://console.anthropic.com/
2. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```
3. Verify:
   ```bash
   python3 gosquad_knowledge_loader_advanced.py --ai-summary characters
   ```

**Pricing:** https://www.anthropic.com/pricing

### Local LLM Setup (Ollama)

**Free and private - no API keys needed!**

1. Install Ollama: https://ollama.ai/
2. Pull model:
   ```bash
   ollama pull llama2
   # or for better quality:
   ollama pull llama2:70b
   ```
3. Verify server running:
   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama2",
     "prompt": "test"
   }'
   ```
4. Configure:
   ```bash
   export LOCAL_API_BASE="http://localhost:11434"
   export LOCAL_MODEL="llama2"
   ```
5. Use:
   ```bash
   python3 gosquad_knowledge_loader_advanced.py --ai-summary characters
   ```

**Advantages:**
- Free (no API costs)
- Private (data never leaves your machine)
- Fast (no network latency)
- No rate limits

**Disadvantages:**
- Requires local GPU/CPU compute
- Quality varies by model size
- Setup complexity higher

## Requirements

Install required packages:

```bash
# For OpenAI
pip install openai

# For Anthropic
pip install anthropic

# For local APIs (if using requests)
pip install requests

# All at once
pip install openai anthropic requests
```

Or create `requirements-api.txt`:
```
openai>=1.0.0
anthropic>=0.18.0
requests>=2.31.0
```

Then:
```bash
pip install -r requirements-api.txt
```

## Graceful Degradation

**If no API is configured:**
- Script runs normally in basic mode
- AI features show warning: "⚠ AI features require API configuration"
- All base functionality still works (summary, search, export, etc.)

**If API request fails:**
- Error message displayed
- Script continues (doesn't crash)
- Returns None for AI features

**If package missing:**
- Helpful message: "⚠ openai package not installed. Run: pip install openai"
- Other providers still work if available

## Privacy & Security

### API Key Storage Best Practices

**DO:**
- ✅ Store in environment variables
- ✅ Use config file excluded from git
- ✅ Use cloud secret managers (AWS Secrets, etc.)
- ✅ Rotate keys periodically
- ✅ Use separate keys for dev/prod

**DON'T:**
- ❌ Commit API keys to git
- ❌ Share keys in chat/email
- ❌ Use production keys for testing
- ❌ Hard-code keys in scripts

### Data Privacy

**What gets sent to APIs:**
- File content excerpts (truncated)
- Prompts with context
- Your queries

**What doesn't get sent:**
- Full files (only excerpts)
- File paths (only names)
- Personal information (unless in content)

**For maximum privacy:** Use local LLMs (Ollama). Data never leaves your machine.

## Troubleshooting

### "No API providers enabled"

**Cause:** No API keys configured

**Fix:**
```bash
# Option 1: Environment variable
export OPENAI_API_KEY="sk-..."

# Option 2: Create config
python3 gosquad_knowledge_loader_advanced.py --create-config
# Then edit .gosquad/api_config.json
```

### "API request failed: 401 Unauthorized"

**Cause:** Invalid API key

**Fix:**
- Verify key is correct
- Check key hasn't expired
- Ensure key has proper permissions
- For OpenAI: Check billing is active

### "openai package not installed"

**Cause:** Missing Python package

**Fix:**
```bash
pip install openai anthropic requests
```

### "Content too large for API"

**Cause:** Category has too many/large files

**Fix:**
- Script automatically truncates (should be rare)
- If still fails, contact the developer (script needs adjustment)

### Local LLM not responding

**Cause:** Ollama not running or wrong port

**Fix:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve

# If using different port:
export LOCAL_API_BASE="http://localhost:PORT"
```

## Examples

### Example 1: Quick Character Refresh
```bash
# Using OpenAI
export OPENAI_API_KEY="sk-..."
python3 gosquad_knowledge_loader_advanced.py --ai-summary characters

# Output: Comprehensive character summary with relationships, arcs, conflicts
```

### Example 2: Find Continuity Issues
```bash
# Using Anthropic (more cost-effective)
export ANTHROPIC_API_KEY="sk-ant-..."
python3 gosquad_knowledge_loader_advanced.py --validate-continuity

# Output: List of potential timeline conflicts, character contradictions, etc.
```

### Example 3: Research for Writing
```bash
# Find all content related to temporal powers
python3 gosquad_knowledge_loader_advanced.py --semantic-search "time manipulation mechanics"

# Output: Ranked list of relevant files with explanations
```

### Example 4: Private Local Analysis
```bash
# Using free local LLM
ollama pull llama2
export LOCAL_API_BASE="http://localhost:11434"
python3 gosquad_knowledge_loader_advanced.py --analyze-relationships

# Output: Character relationship map, all processed locally
```

## Future Enhancements

Planned API-powered features:
- **Scene suggestions:** AI generates scene ideas based on plot gaps
- **Dialogue consistency:** Check character voice across books
- **Pacing analysis:** Identify slow sections needing action
- **Theme tracking:** Ensure themes are developed consistently
- **Foreshadowing checker:** Verify setups have payoffs
- **World-building validator:** Check setting details match
- **Character arc analyzer:** Track character development curves
- **Beta reader simulation:** AI reads as target audience, provides feedback

## Support

**Issues?**
- Check this guide first
- Verify API keys are valid
- Test with simple example
- Check provider status pages

**Feature requests?**
- Document your use case
- Suggest which APIs would help
- Estimate value to workflow

## Quick Reference

```bash
# Create config template
python3 gosquad_knowledge_loader_advanced.py --create-config

# AI-powered summary
python3 gosquad_knowledge_loader_advanced.py --ai-summary CATEGORY

# Semantic search
python3 gosquad_knowledge_loader_advanced.py --semantic-search "QUERY"

# Continuity check
python3 gosquad_knowledge_loader_advanced.py --validate-continuity

# Relationship analysis
python3 gosquad_knowledge_loader_advanced.py --analyze-relationships

# Use custom config
python3 gosquad_knowledge_loader_advanced.py --config PATH --ai-summary CATEGORY

# Environment variables
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export LOCAL_API_BASE="http://localhost:11434"
```
