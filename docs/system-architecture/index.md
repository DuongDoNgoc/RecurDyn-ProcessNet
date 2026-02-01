# RecurDyn ProcessNet - System Architecture

**Date:** 2026-02-01
**Version:** 2.0
**Status:** Active

## Overview

The RecurDyn ProcessNet Knowledge Base Extraction system uses a modular, pipeline-based architecture to transform static HTML documentation into a queryable knowledge base. The system is designed for reliability, maintainability, and performance.

## Contents

- [High-Level Architecture](#high-level-architecture) - System architecture diagram
- [Architecture Principles](#architecture-principles) - Design principles and goals
- [Component Details](#component-details) - Layer breakdown
- [Data Flow](#data-flow) - Extraction and query flows
- [Performance](#performance-architecture) - Performance characteristics
- [Security](#security-architecture) - Security considerations

## Architecture Principles

### Core Design Principles

1. **Separation of Concerns** - Distinct components for extraction, storage, and querying
2. **Fail-Safe Operation** - Errors in individual files don't stop processing
3. **Progressive Enhancement** - Multiple parsing strategies with fallbacks
4. **Index-Driven Query** - Pre-computed indices for fast lookups
5. **Encoding Resilience** - Automatic detection with fallback chain

### Architectural Goals

| Goal | Description | Priority |
|------|-------------|----------|
| Reliability | Handle malformed HTML and encoding issues | P0 |
| Performance | Fast extraction and query response | P0 |
| Maintainability | Easy to extend and modify | P1 |
| Usability | Simple CLI interface | P1 |
| Extensibility | Support new documentation formats | P2 |

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Input Layer                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  HTML Files    │  │  CHM Archives  │  │  Tutorial HTML │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
└───────────┼──────────────────┼──────────────────┼─────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Extraction Layer                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            ProcessNetDocParser                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ File         │  │ Encoding     │  │ HTML         │  │  │
│  │  │ Discovery    │  │ Detection    │  │ Parsing      │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Sphinx       │  │ Knowledge    │  │ Index        │  │  │
│  │  │ Parameter    │  │ Base Build   │  │ Building     │  │  │
│  │  │ Extraction   │  │              │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Knowledge Base (JSON)                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Metadata     │  │ Namespaces   │  │ Indices       │  │  │
│  │  │              │  │              │  │              │  │  │
│  │  │ • Source     │  │ • Classes    │  │ • Method     │  │  │
│  │  │ • Version    │  │ • Methods    │  │ • Class      │  │  │
│  │  │ • Date       │  │ • Examples   │  │ • Interface │  │  │
│  │  │ • Stats      │  │ • Files      │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Markdown Documentation                       │  │
│  │  • Namespace files (ProcessNet_Geometry.md)              │  │
│  │  • Cross-references                                      │  │
│  │  • Code examples                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Query Layer                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            ProcessNetKnowledge                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Exact        │  │ Fuzzy        │  │ Description  │  │  │
│  │  │ Lookup       │  │ Search       │  │ Search       │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Namespace    │  │ Example      │  │ Statistics   │  │  │
│  │  │ Browse       │  │ Finder       │  │ Reporting    │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Interactive CLI                             │  │
│  │  • Command parsing                                       │  │
│  │  • Result formatting                                     │  │
│  │  • JSON/Console output                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REST API Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Server                               │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Health       │  │ Statistics   │  │ Namespace    │  │  │
│  │  │ Check        │  │ Endpoint     │  │ Endpoints    │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Search       │  │ Exact        │  │ Code         │  │  │
│  │  │ Endpoints    │  │ Lookup       │  │ Examples     │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  • CORS support for browser access                             │
│  • OpenAPI documentation at /docs and /redoc                   │
│  • Async request handling with uvicorn                         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Layer Breakdown

| Layer | Component | Description | Details |
|-------|-----------|-------------|---------|
| **Input** | File Discovery | Recursive HTML file discovery | [→ Input Layer](./input-layer.md) |
| **Input** | Encoding Detection | Auto-detect file encoding | [→ Input Layer](./input-layer.md) |
| **Extraction** | HTML Parser | BeautifulSoup + lxml parsing | [→ Extraction Layer](./extraction-layer.md) |
| **Extraction** | Content Extractor | Methods, classes, properties | [→ Extraction Layer](./extraction-layer.md) |
| **Extraction** | Sphinx Parser | Parameter extraction v2 | [→ Extraction Layer](./extraction-layer.md) |
| **Storage** | JSON Knowledge Base | Structured data storage | [→ Storage Layer](./storage-layer.md) |
| **Storage** | Markdown Exporter | Human-readable docs | [→ Storage Layer](./storage-layer.md) |
| **Query** | ProcessNetKnowledge | Search and lookup engine | [→ Query Layer](./query-layer.md) |
| **Query** | Interactive CLI | Command-line interface | [→ Query Layer](./query-layer.md) |
| **REST API** | FastAPI Server | HTTP REST API | [→ REST API Layer](./rest-api-layer.md) |
| **Testing** | Integration Tests | 51 tests, 88% pass rate | [→ Testing Layer](./testing-layer.md) |

## Data Flow

### Extraction Flow

```
[HTML Files]
    ↓
[File Discovery] → List all .html files
    ↓
[Encoding Detection] → Detect UTF-8, Windows-1252, etc.
    ↓
[HTML Parsing] → BeautifulSoup with lxml
    ↓
[Content Extraction]
    ├─→ [Method Signatures] → Method objects
    ├─→ [Class Definitions] → ClassDef objects
    ├─→ [Properties] → Property objects
    └─→ [Code Examples] → CodeExample objects
    ↓
[Knowledge Base Build]
    ├─→ [Namespace Organization] → Group by namespace
    ├─→ [Index Building] → method_index, class_index, interface_index
    └─→ [Statistics] → File counts, extraction time
    ↓
[Export]
    ├─→ [JSON] → processnet_knowledge.json
    └─→ [Markdown] → ProcessNet_*.md files
```

### Query Flow

```
[User Query]
    ↓
[Command Parsing] → Parse command and arguments
    ↓
[Query Type Detection]
    ├─→ [Exact Lookup] → O(1) index lookup
    ├─→ [Fuzzy Search] → RapidFuzz matching
    ├─→ [Description Search] → Full-text scan
    ├─→ [Namespace Browse] → Direct namespace access
    └─→ [Example Finder] → Code search
    ↓
[Result Assembly]
    ├─→ [Retrieve from Knowledge Base]
    ├─→ [Create SearchResult Objects]
    └─→ [Score Results (for fuzzy)]
    ↓
[Output Formatting]
    ├─→ [Console Output] → Formatted text
    └─→ [JSON Output] → Machine-readable
    ↓
[Display Results]
```

## Performance Architecture

### Extraction Performance

**Target:** <5 minutes for 500 HTML files

**Optimizations:**
1. Streaming Processing - Process files sequentially
2. Lazy Parsing - Only parse what's needed
3. Efficient Data Structures - Use dataclasses
4. Progress Feedback - Show progress to user

### Query Performance

**Target:** <100ms for any lookup

**Query Complexities:**

| Query Type | Complexity | Typical Performance |
|------------|------------|---------------------|
| Exact Lookup | O(1) | <10ms |
| Fuzzy Search | O(n log n) | <100ms |
| Description Search | O(n) | <100ms |
| Namespace Browse | O(1) | <10ms |

## Security Architecture

### Input Validation

- File path validation (prevent directory traversal)
- File size limits (10MB max per file)
- Encoding detection with fallback chain

### Output Sanitization

- Filename sanitization (remove unsafe characters)
- Path traversal prevention
- Error message sanitization

## Related Documents

- [README.md](../README.md) - Project overview
- [docs/project-overview-pdr.md](project-overview-pdr.md) - Product requirements
- [docs/code-standards.md](code-standards.md) - Code conventions
- [docs/codebase-summary.md](codebase-summary.md) - Code structure
- [docs/tech-stack.md](tech-stack.md) - Technology stack
- [docs/project-roadmap.md](project-roadmap.md) - Development timeline

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-02-01 | Added REST API Layer, integration testing, restructured into modular documentation |
| 1.0 | 2026-01-28 | Initial architecture document |

---

**Status:** Active
**Last Updated:** 2026-02-01
**Maintainer:** Development Team
