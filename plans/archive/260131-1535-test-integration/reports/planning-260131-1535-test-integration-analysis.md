# Planning Report: Hybrid Verification Test Integration

**Date:** 2026-01-31
**Agent:** planner
**Status:** Complete

## Summary

Analyzed `ProcessNet_Hybrid_Verification_Workflow.md` for test case extraction and integration into main plan.

## Findings

### Workflow Document Analysis

| Section | Test Potential | Automation Level |
|---------|---------------|------------------|
| Phase 1: Smart Sampling | High | Fully automatable |
| Phase 2: Browser Verification | Medium | File-based assertions only |
| Phase 3: Parser Adjustment | High | Regression tests |
| Phase 4: Full Extraction | High | Stats validation |
| Phase 5: Spot-Check | High | Random sampling |
| Phase 6: Sign-Off | High | Metrics assertions |

### Test Cases Extracted

1. **Sample File Tests** (5 types)
   - index.html - TOC structure
   - namespace-*.html - Namespace docs
   - class-*.html - Class definitions
   - methods-*.html - Method references
   - examples-*.html - Code examples

2. **Parser Adjustment Tests**
   - Table-based method extraction
   - `<div class="highlight">` code blocks
   - Collapsed `<details>` sections

3. **Validation Tests**
   - Random spot-check (10 files)
   - Stratified namespace sampling
   - Use case method coverage

4. **Success Metrics**
   - Parsing success: ≥98%
   - Method accuracy: ≥90%
   - Example accuracy: ≥85%
   - Use case coverage: 100%

## Integration Plan

### Main Plan Changes

1. **Add Phase 3.5** - Sample verification before full extraction
2. **Expand Phase 6** - Concrete test structure with pytest files
3. **Update Success Criteria** - Specific thresholds from workflow
4. **Add Test Dependencies** - pytest, pytest-cov

### New Test Files

```
tests/
├── conftest.py                    # + MCP Playwright fixtures
├── test-browser-verification.py   # NEW: Browser-based tests
├── test-sample-extraction.py
├── test-parser-adjustments.py
├── test-spot-checks.py            # + Browser spot-checks
├── test-use-case-coverage.py
├── fixtures/sample-html/
└── screenshots/                   # Browser verification captures
```

## Decisions Made

1. **MCP Playwright integrated** for true browser-based verification (user choice)
2. **Tolerance thresholds** made configurable via conftest.py
3. **Use case methods** aligned with PDR requirements (UC-1, UC-2, UC-3)
4. **Dual verification** - both file-based parsing AND browser rendering tests

## Unresolved Questions

1. Real HTML sample files needed - currently using mock fixtures
2. Exact method names may differ from PDR (fuzzy fallback added)
3. Threshold values may need adjustment after real data testing

## Effort Estimate

| Phase | Effort |
|-------|--------|
| Test Infrastructure | 30min |
| MCP Playwright Setup | 45min |
| Sample Extraction Tests | 45min |
| Parser Adjustment Tests | 45min |
| Spot-Check & Metrics | 1h |
| **Total** | ~4h |

## Recommendation

**Proceed with implementation.** The workflow document provides solid test case patterns.

**Key advantages of MCP Playwright:**
- True browser verification matches original workflow intent
- Screenshot capture aids debugging and documentation
- Detects JS-rendered content if present
- More reliable element counting than regex parsing

**Main risks:**
1. Mock fixtures not matching real RecurDyn doc structure → mitigate by inspecting actual docs
2. MCP connection issues → fallback to file-based tests available
3. Browser overhead → mark browser tests as slow, run separately
