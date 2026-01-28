# ProcessNet Knowledge Base Extraction - Implementation Plan

**Date:** 2026-01-28
**Status:** In Progress

## Overview

Extract ProcessNet API documentation from RecurDyn installation files and build a structured knowledge base for automation workflows.

## Source Files

| Source | Path | Type | Size |
|--------|------|------|------|
| CHM File | `knowledge/ProcessNetHelp.chm` | MS HtmlHelp | 31MB |
| Sphinx HTML | `knowledge/RecurDynHelp/ProcessNet/` | 37 HTML files | ~2MB |
| Tutorials | `knowledge/Tutorial/ProcessNet/General/` | 3 HTML files | ~500KB |

## Target Outputs

1. `output/processnet_knowledge.json` - Complete API knowledge base
2. `output/markdown/` - One markdown file per namespace
3. `src/processnet_query.py` - Query interface module

---

## Implementation Phases

### Phase 1: Environment Setup
**Status:** Pending
**Files:** `requirements.txt`, `docs/tech-stack.md`

- [x] Install system dependencies (libchm-bin, p7zip-full)
- [x] Create requirements.txt with Python dependencies
- [x] Document tech stack decisions

### Phase 2: CHM Extraction
**Status:** Pending
**Files:** `output/extracted_chm/`

Tasks:
1. Extract CHM file using `extract_chmLib`
2. Detect and handle encoding (UTF-8/Windows-1252)
3. Validate extracted HTML files
4. Log extraction statistics

### Phase 3: HTML Parser Implementation
**Status:** Pending
**Files:** `src/recurdyn-doc-parser.py`

Tasks:
1. Implement recursive file discovery
2. Parse Sphinx HTML structure:
   - Definition lists (`<dl>`, `<dt>`, `<dd>`)
   - Field lists for parameters/returns
   - Code blocks for examples
3. Extract:
   - Page metadata (title, namespace)
   - Class definitions (name, inheritance, description)
   - Method signatures (params, return type)
   - Properties (name, type, read-only)
   - Code examples
4. Build JSON knowledge base structure
5. Generate search indices (exact match, fuzzy)

### Phase 4: Query Interface Implementation
**Status:** Pending
**Files:** `src/processnet-query.py`

Tasks:
1. Load and validate knowledge base
2. Implement search functions:
   - `find_method()` - Exact method lookup
   - `search_method_fuzzy()` - Fuzzy string matching
   - `search_by_description()` - Keyword search
   - `list_namespace_contents()` - Namespace exploration
   - `find_examples()` - Example finder
3. Output formatters (console, JSON, markdown)
4. Optional: Interactive CLI mode

### Phase 5: Markdown Export
**Status:** Pending
**Files:** `output/markdown/*.md`

Tasks:
1. Generate one markdown file per namespace
2. Include:
   - Namespace overview with statistics
   - Class documentation
   - Method signatures and descriptions
   - Parameter tables
   - Code examples
3. Generate cross-reference links

### Phase 6: Validation & Testing
**Status:** Pending
**Files:** `tests/test-processnet-extraction.py`

Tasks:
1. Validate parsing success rate (>80% target)
2. Test query interface accuracy
3. Verify use case coverage:
   - DOE batch execution methods
   - Model introspection methods
   - Result processing methods
4. Generate extraction statistics report

---

## File Structure

```
RecurDyn-ProcessNet/
├── docs/
│   └── tech-stack.md
├── knowledge/                   # Source data (read-only)
│   ├── ProcessNetHelp.chm
│   ├── RecurDynHelp/ProcessNet/
│   └── Tutorial/ProcessNet/
├── output/
│   ├── extracted_chm/           # Extracted CHM contents
│   ├── processnet_knowledge.json
│   └── markdown/
├── plans/
│   ├── 260128-processnet-extraction/
│   │   └── plan.md
│   └── reports/
├── src/
│   ├── recurdyn-doc-parser.py
│   └── processnet-query.py
├── tests/
│   └── test-processnet-extraction.py
├── requirements.txt
└── extraction-log.txt
```

---

## Success Criteria

- [ ] >80% HTML files successfully parsed
- [ ] All namespaces identified from documentation
- [ ] Method signatures extracted with >90% accuracy
- [ ] Query interface returns correct results
- [ ] Markdown output is readable and well-formatted

---

## Dependencies

**System:**
- libchm-bin (CHM extraction)
- p7zip-full (fallback extraction)

**Python:**
- beautifulsoup4 (HTML parsing)
- lxml (parser backend)
- rapidfuzz (fuzzy search)
- chardet (encoding detection)
