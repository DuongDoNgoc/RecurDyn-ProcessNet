# ProcessNet Extraction - Tech Stack

**Date:** 2026-02-01
**Version:** 2.0

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

### REST API Server
| Library | Purpose | Install |
|---------|---------|---------|
| `fastapi` | REST API framework | `pip install fastapi` |
| `uvicorn[standard]` | ASGI server | `pip install uvicorn[standard]` |
| `pydantic` | Data validation | `pip install pydantic` |
| `httpx` | Async HTTP client (testing) | `pip install httpx` |
| `pytest-asyncio` | Async test support | `pip install pytest-asyncio` |

## System Requirements

```bash
# System packages (Ubuntu/Debian/WSL)
apt update && apt install -y libchm-bin p7zip-full

# Python packages (core)
pip install beautifulsoup4 lxml rapidfuzz chardet

# Python packages (REST API server)
pip install fastapi uvicorn[standard] pydantic

# Python packages (testing)
pip install httpx pytest-asyncio
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
│   ├── recurdyn-doc-parser.py      # HTML/CHM parser (851 lines)
│   ├── processnet-query-interface.py # Query CLI (581 lines)
│   └── processnet-api-server.py     # REST API server (410 lines)
├── tests/                   # Test suite (200+ tests)
│   ├── helpers/             # Test helpers
│   │   └── validation-helpers.py    # Validation utilities
│   └── ... (various test files)
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
- **Enhanced (v2):** Sphinx parameter extraction from field-lists

### 3. JSON Knowledge Base Design
- **Hierarchical:** Namespaces → Classes → Methods → Parameters
- **Indexed:** Exact match + fuzzy search indices
- **Schema:** JSON Schema Draft 2020-12 for parameter definitions
- **Enhanced (v2):** 6,035 parameters extracted (+42% from v1.5)

### 4. Query Interface
- Exact match: O(1) dict lookup
- Fuzzy search: rapidfuzz with configurable threshold
- Full-text: Simple inverted index (no external DB needed)

### 5. REST API Server
- **Framework:** FastAPI with async/await support
- **Documentation:** Automatic OpenAPI (Swagger UI, ReDoc)
- **Validation:** Pydantic models for request/response
- **CORS:** Enabled for browser access
- **Deployment:** uvicorn ASGI server

## File Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `processnet_knowledge.json` | JSON | Complete API knowledge base |
| `output/markdown/*.md` | Markdown | One file per namespace |
| Search indices | Embedded in JSON | Pre-computed for fast queries |
| REST API | HTTP endpoints | `/api/health`, `/api/stats`, `/api/search`, etc. |

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Knowledge base statistics |
| GET | `/api/namespaces` | List all namespaces |
| GET | `/api/namespaces/{name}` | Get namespace details |
| GET | `/api/search?q={query}` | Fuzzy search for methods |
| GET | `/api/find/{name}` | Exact method lookup |
| GET | `/api/examples?keyword={kw}` | Find code examples |

## Extraction Statistics (v2)

- **Methods extracted:** 5,606
- **Classes extracted:** 1,803
- **Properties extracted:** 13,377
- **Namespaces:** 23
- **Methods with parameters:** 3,807 (+89% from v1.5)
- **Total parameters extracted:** 6,035 (+42% from v1.5)
- **Integration tests:** 51 tests, 88% pass rate

## Performance Characteristics

| Component | Metric | Target | Actual |
|-----------|--------|--------|--------|
| Extraction Speed | Files/second | ~1-2 files/s | Achieved |
| Query Response | Exact lookup | <10ms | <10ms |
| Query Response | Fuzzy search | <100ms | <100ms |
| API Response | Any endpoint | <200ms | <100ms |
| Test Execution | Full suite | <2 minutes | ~1 second |
