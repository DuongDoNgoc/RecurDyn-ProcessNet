---
title: "v7 KB: C#/VB API + User Guide Extraction"
description: "Extend knowledge base with C#/VB API from CHM and User Guide tutorials"
status: completed
priority: P1
effort: 8h
branch: master
tags: [kb, extraction, csharp, vb, userguide, v7]
created: 2026-02-01
---

# v7 Knowledge Base: C#/VB API + User Guide Extraction

## Overview

Extend the ProcessNet knowledge base to v7 by adding:
1. **C#/VB API extraction** from 21,274 CHM HTML files
2. **User Guide tutorials** from Word-exported HTML and Sphinx HTML files

## Current State (v6)

| Metric | Value |
|--------|-------|
| Python API Files | 40,625 |
| Classes | 1,830 |
| Methods | 6,773 |
| KB Size | 21 MB |
| Parser | `src/recurdyn-doc-parser.py` (1344 lines) |

## New Content Sources

### Source 1: C#/VB API (CHM HTML)
- **Location:** `output/extracted_chm/html/` - 21,274 HTM files (184 MB)
- **Format:** XHTML with collapsible syntax tabs
- **Languages:** C# (`*_code_Div1`) and VB (`*_code_Div2`)
- **Namespaces:** `FunctionBay.Post.ProcessNet`, `FunctionBay.RecurDyn.ProcessNet`

### Source 2: User Guide (Word HTML)
- **Location:** `output/extracted_chm/Content/UserGuideFiles/` - 7 HTM files (3.2 MB)
- **Format:** Microsoft Word 15 HTML export
- **Content:** Tutorials, workflows, UI guidance

### Source 3: User Guide (Sphinx)
- **Location:** `knowledge/RecurDynHelp/ProcessNet/` - 27 HTML files
- **Format:** Sphinx ReadTheDocs with toctree navigation
- **Content:** Hierarchical chapters (43 > 43.1 > 43.1.1)

## Architecture

```
src/
├── recurdyn-doc-parser.py          # Existing Python API parser
├── chm-api-extractor.py            # NEW: C#/VB from html/
├── userguide-word-extractor.py     # NEW: Word HTML guides
├── userguide-sphinx-extractor.py   # NEW: Sphinx guides
└── kb-consolidator.py              # NEW: Merge all into v7

output/
├── processnet-knowledge-v6.json    # Current Python-only KB
├── processnet-csharp-vb-api.json   # Intermediate: C#/VB API
├── processnet-userguide.json       # Intermediate: User Guides
└── processnet-knowledge-v7.json    # Final: Unified KB
```

## Phases

| Phase | Description | Effort | Dependencies | Parallel |
|-------|-------------|--------|--------------|----------|
| [Phase 1](phase-01-chm-html-csharp-vb-api-extractor.md) | C#/VB API from CHM HTML | 3h | None | ✓ |
| [Phase 2](phase-02-userguide-word-html-extractor.md) | Word HTML user guide | 1.5h | None | ✓ |
| [Phase 3](phase-03-userguide-sphinx-html-extractor.md) | Sphinx user guide | 1h | None | ✓ |
| [Phase 4](phase-04-knowledge-base-consolidation-v7-merger.md) | Merge into v7 unified KB | 1.5h | P1, P2, P3 | - |
| [Phase 5](phase-05-validation-testing-v7-quality-assurance.md) | Validation and testing | 1h | P4 | - |

**Execution:** Phases 1-3 run in parallel, Phase 4 waits for all, Phase 5 follows.

## Success Criteria

1. **C#/VB API extraction:** >20,000 API members with both language variants
2. **User Guide extraction:** All 34 guide files (7 Word + 27 Sphinx) parsed
3. **Unified KB:** Single JSON output compatible with existing query interface
4. **No regressions:** Python API quality maintained (6,773 methods)
5. **Performance:** Full extraction <10 minutes

## Key Decisions

1. **Modular extractors:** Separate scripts for each source type (KISS, DRY)
2. **Reuse infrastructure:** BeautifulSoup, encoding detection, logging patterns
3. **Unified output:** Single v7 JSON (not separate files for API vs guides)
4. **Backward compatibility:** Query interface works without modification

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CHM HTML parsing complexity | Medium | High | Test on 100 files first |
| Word HTML MSO artifacts | Medium | Low | Strip namespaces early |
| Memory usage (184 MB input) | Low | Medium | Stream processing |
| Query interface breaking | Low | High | Integration tests |

## Related Files

- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py` - Current parser
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/processnet-query-interface.py` - Query interface
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v6.json` - Current KB
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/docs/code-standards.md` - Coding standards

## Validation Summary

**Validated:** 2026-02-01
**Questions asked:** 7

### Confirmed Decisions

| Decision | User Choice |
|----------|-------------|
| Enum storage | Nested in parent entity (members array) |
| Duplicate APIs | Keep separate in python_api and csharp_vb_api sections |
| Query interface | v6 compatible (unchanged, use python_api by default) |
| CHM metadata | Full metadata (assembly, version, F1 key, help ID) |
| Script architecture | Standalone scripts (4 separate files in src/) |
| Word Guide extraction | Full content (include image references) |
| Execution order | Parallel (P1, P2, P3 independent, merge in P4) |

### Action Items

- [x] Enum members → nested in parent (already in Phase 1 schema)
- [x] Update Phase 1 to preserve full metadata (assembly, version, help ID, F1)
- [x] Update Phase 2 to include image references from .files/ directories
- [x] Confirm Phase 1-3 can run in parallel in plan.md dependencies
- [x] Complete Phase 1: C#/VB API extraction (21,274 files, 21,723 members)
- [x] Complete Phase 4: Merge all sources into v7 unified KB
- [x] Generate v7 output at output/processnet-knowledge-v7.json (47.45 MB)

### Resolved Questions

1. ~~Should enum members be stored as properties or separate entity type?~~ → Nested in parent
2. ~~How to handle duplicate API members across C#/VB and Python?~~ → Keep separate, link via unified_index
3. ~~What metadata to preserve for assembly/version info?~~ → Full metadata (assembly, version, F1, help ID)
