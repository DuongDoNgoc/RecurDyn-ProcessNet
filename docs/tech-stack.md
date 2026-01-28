# ProcessNet Extraction - Tech Stack

**Date:** 2026-01-28

## Overview

This document defines the technology stack for the ProcessNet API documentation extraction project.

## Core Dependencies

### Python Runtime
- **Python 3.10+** - Target runtime for all scripts

### CHM Extraction
| Tool | Purpose | Install |
|------|---------|---------|
| `libchm-bin` | Primary CHM extraction | `apt install libchm-bin` |
| `p7zip-full` | Fallback extraction | `apt install p7zip-full` |

### HTML Parsing
| Library | Purpose | Install |
|---------|---------|---------|
| `beautifulsoup4` | HTML parsing | `pip install beautifulsoup4` |
| `lxml` | Fast parser backend | `pip install lxml` |

### Search & Indexing
| Library | Purpose | Install |
|---------|---------|---------|
| `rapidfuzz` | Fuzzy string matching | `pip install rapidfuzz` |

### Utilities
| Library | Purpose | Install |
|---------|---------|---------|
| `chardet` | Encoding detection | `pip install chardet` |

## System Requirements

```bash
# System packages (Ubuntu/Debian/WSL)
apt update && apt install -y libchm-bin p7zip-full

# Python packages
pip install beautifulsoup4 lxml rapidfuzz chardet
```

## Project Structure

```
RecurDyn-ProcessNet/
├── docs/                    # Project documentation
│   └── tech-stack.md        # This file
├── knowledge/               # Source data (CHM + HTML files)
│   ├── ProcessNetHelp.chm   # CHM file to extract
│   ├── RecurDynHelp/        # Sphinx HTML documentation
│   └── Tutorial/            # Tutorial HTML files
├── output/                  # Generated outputs
│   ├── extracted_chm/       # Extracted CHM contents
│   ├── processnet_knowledge.json  # Main knowledge base
│   └── markdown/            # Generated markdown docs
├── src/                     # Source code
│   ├── recurdyn_doc_parser.py     # HTML/CHM parser
│   └── processnet_query.py        # Query interface
├── plans/                   # Implementation plans
│   └── reports/             # Research reports
└── requirements.txt         # Python dependencies
```

## Key Design Decisions

### 1. CHM Extraction Strategy
- **Primary:** `extract_chmLib` - Simple, reliable, preserves structure
- **Fallback:** `7zip` - Universal archive handler
- **Encoding:** Auto-detect with chardet, fallback chain: UTF-8 → Windows-1252 → Latin-1

### 2. HTML Parsing Strategy
- Use semantic selectors (`dl`, `dt`, `dd`) over CSS classes
- Target Sphinx/ReadTheDocs structure patterns
- Extract definition lists for API signatures and metadata

### 3. JSON Knowledge Base Design
- **Hierarchical:** Namespaces → Classes → Methods → Parameters
- **Indexed:** Exact match + fuzzy search indices
- **Schema:** JSON Schema Draft 2020-12 for parameter definitions

### 4. Query Interface
- Exact match: O(1) dict lookup
- Fuzzy search: rapidfuzz with configurable threshold
- Full-text: Simple inverted index (no external DB needed)

## File Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `processnet_knowledge.json` | JSON | Complete API knowledge base |
| `output/markdown/*.md` | Markdown | One file per namespace |
| Search indices | Embedded in JSON | Pre-computed for fast queries |
