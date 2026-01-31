# CHM Extraction and API Documentation Processing - Implementation Plan

**Date:** 2026-01-31
**Plan ID:** 260131-2250-chm-extraction-and-api-documentation
**Status:** Ready for Implementation

---

## Executive Summary

Comprehensive implementation plan created for extracting ProcessNetHelp.chm and enhancing the parser to capture actual API documentation. Plan addresses critical gap: current parser extracted 0 methods from tutorial HTML - needs to process actual API documentation.

## Plan Structure

### Main Plan
**File:** `/mnt/d/Vibecoding/RecurDyn-ProcessNet/plans/260131-2250-chm-extraction-and-api-documentation/plan.md`

### Phase Files

| Phase | File | Description | Effort |
|-------|------|-------------|--------|
| 01 | [phase-01-chm-extraction-on-windows.md](phase-01-chm-extraction-on-windows.md) | Extract CHM using 7-Zip on Windows | 30m |
| 02 | [phase-02-file-transfer-to-wsl.md](phase-02-file-transfer-to-wsl.md) | Transfer HTML files via WSL mount | 15m |
| 03 | [phase-03-html-structure-analysis.md](phase-03-html-structure-analysis.md) | Analyze HTML patterns for parser | 45m |
| 04 | [phase-04-parser-enhancement-for-api-docs.md](phase-04-parser-enhancement-for-api-docs.md) | Add parameter/return type extraction | 3h |
| 05 | [phase-05-run-enhanced-parser-on-api-docs.md](phase-05-run-enhanced-parser-on-api-docs.md) | Execute extraction on API docs | 1h |
| 06 | [phase-06-validation-and-verification.md](phase-06-validation-and-verification.md) | Verify extraction quality | 1h |

**Total Estimated Effort:** ~8 hours

## Key Requirements by Phase

### Phase 01: CHM Extraction
- Locate ProcessNetHelp.chm on Windows
- Use 7-Zip: `7z x file.chm -ooutput_dir -y`
- Verify extraction completeness (>50 HTML files)

### Phase 02: File Transfer
- Copy via WSL mount: `/mnt/c/temp/extracted_chm/`
- Target: `knowledge/extracted_chm/`
- Verify file count matches source

### Phase 03: HTML Analysis
- Sample 5-10 representative files
- Document class/ID patterns
- Identify method signature format
- Create test fixtures

### Phase 04: Parser Enhancement
**Critical Updates to `src/recurdyn-doc-parser.py`:**

```python
# New dataclass fields
@dataclass
class Parameter:
    is_optional: bool = False
    is_out: bool = False

@dataclass
class Method:
    return_description: str = ""
    exceptions: list = field(default_factory=list)
    is_static: bool = False
    access_modifier: str = ""

# New methods to implement
def parse_parameters(sig_text: str) -> list
def parse_return_type(sig_text, dt_element) -> tuple
def extract_properties(soup) -> list
def extract_classes(soup) -> list
```

### Phase 05: Re-extraction
```bash
python src/recurdyn-doc-parser.py \
    --input knowledge/extracted_chm \
    --output output/processnet-knowledge.json \
    --markdown output/markdown \
    --verbose
```

### Phase 06: Validation
**Target Metrics:**

| Metric | Minimum | Optimal |
|--------|---------|---------|
| Parse success | 80% | 95% |
| Method detection | 90% | 98% |
| Parameter completeness | 60% | 90% |
| Return type coverage | 50% | 80% |
| Example coverage | 50% | 80% |

## Architecture Overview

```
Windows                     WSL
┌─────────────┐            ┌─────────────────────┐
│ProcessNet   │  7-Zip     │ extracted_chm/      │
│Help.chm     ├──────────► │ ├── *.html          │
└─────────────┘            │ └── ...             │
                           └─────────────────────┘
                                       │
                                       ▼
                           ┌─────────────────────┐
                           │ Enhanced Parser     │
                           │ - Parameters        │
                           │ - Return types      │
                           │ - Classes           │
                           └─────────────────────┘
                                       │
                                       ▼
                           ┌─────────────────────┐
                           │ Knowledge Base      │
                           │ - JSON              │
                           │ - Markdown          │
                           │ - Query Interface   │
                           └─────────────────────┘
```

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| CHM encoding issues | High | Medium | Use 7-Zip with encoding detection |
| HTML structure differs | High | Medium | Phase 03 analysis before enhancement |
| No API docs in CHM | Critical | Low | Verify CHM content before running |
| Parser crashes | Medium | Medium | Add try/except, continue on error |

## Dependencies

**Required Tools:**
- 7-Zip on Windows (https://www.7-zip.org/)
- WSL with filesystem access
- Python 3.10+ with BeautifulSoup4

**Input Files:**
- ProcessNetHelp.chm (location to be determined)

**Baseline Code:**
- `src/recurdyn-doc-parser.py` (475 lines, 0 methods extracted currently)

## Success Criteria

### Minimum Viable
- CHM successfully extracted to HTML
- Parser extracts >50 methods
- Parameters extracted for >60% of methods
- Query interface returns accurate results
- All tests pass

### Optimal
- Parser extracts >100 methods
- Parameters extracted for >90% of methods
- Return types captured for >70% of methods
- Complete class hierarchy preserved
- All code examples extracted

## Next Actions

1. **User:** Locate ProcessNetHelp.chm on Windows filesystem
2. **User:** Verify 7-Zip installed (or install)
3. **Agent:** Execute Phase 01 extraction
4. **Agent:** Continue through Phases 02-06

## References

**Research Reports Analyzed:**
- [researcher-01-chm-extraction-methods.md](research/researcher-01-chm-extraction-methods.md)
  - 7-Zip extraction procedure
  - WSL-Windows file sharing
  - CHM format overview

- [researcher-02-api-doc-structure.md](research/researcher-02-api-doc-structure.md)
  - Current parser limitations
  - Expected HTML patterns
  - Validation requirements
  - Coverage metrics

**Codebase Context:**
- [README.md](../../README.md) - Project overview
- [src/recurdyn-doc-parser.py](../../src/recurdyn-doc-parser.py) - Baseline parser
- [src/processnet-query-interface.py](../../src/processnet-query-interface.py) - Query interface

## Unresolved Questions

1. What is the exact location of ProcessNetHelp.chm?
2. Does RecurDyn use any proprietary CHM extensions?
3. What is the typical size of the CHM file?
4. Are there licensing restrictions on extracting the documentation?
5. Does the CHM contain embedded binaries (images, code samples)?

## Notes

- Plan follows KISS/YAGNI/DRY principles
- Each phase has clear exit criteria
- Validation before moving to next phase
- Defensive parsing for HTML structure variations
- Comprehensive test coverage for enhanced parser

---

**Plan Status:** Ready for implementation
**Estimated Completion:** 8 hours across 6 phases
**Next Step:** Execute Phase 01 (CHM Extraction on Windows)
