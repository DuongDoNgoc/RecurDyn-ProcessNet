---
title: "Extraction Accuracy Verification & Parser Bug Fixes"
description: "Fix build_knowledge_base() bug causing 0% class method/property extraction, implement verification framework"
status: pending
priority: P1
effort: 5h
branch: master
tags: [parser, bug-fix, verification, extraction]
created: 2026-02-01
---

# Extraction Accuracy Verification & Parser Bug Fixes

## Context

- **Plan Dir**: `plans/260201-1522-extraction-accuracy-verification-fix/`
- **Research**: `reports/researcher-260201-1525-html-parsing-statistical-sampling-validation-framework.md`
- **Source**: `src/recurdyn-doc-parser.py`

## Problem Statement

Spot check revealed **0% extraction accuracy** for class methods/properties:
- Parser extracts 1,803 classes correctly
- Parser extracts 5,606 methods correctly
- **BUG**: `build_knowledge_base()` stores methods as `standalone_methods` at namespace level
- **Result**: All classes have empty `methods[]` and `properties[]` arrays

## Root Cause Analysis

In `build_knowledge_base()` lines 855-866:
```python
# Methods added to namespace, NOT to classes
ns_data['standalone_methods'].append(method_dict)
```

Missing: Association of methods/properties with their parent classes.

## Phase Overview

| Phase | Description | Effort | Status |
|-------|-------------|--------|--------|
| 01 | Data Classification & Sampling | 0.5h | pending |
| 02 | Verification Framework | 1h | pending |
| 03 | Spot Check Execution | 0.5h | pending |
| 04 | Parser Bug Fixes | 2h | pending |
| 05 | Re-extraction & Validation | 0.5h | pending |
| 06 | Documentation Update | 0.5h | pending |

## Success Criteria

- [ ] 100 stratified samples verified
- [ ] Precision/Recall F1 > 0.90 for all categories
- [ ] Class.methods populated correctly
- [ ] Class.properties populated correctly
- [ ] Re-extraction shows >80% method-to-class association

## Dependencies

- BeautifulSoup4, lxml (installed)
- pytest (installed)
- Existing test infrastructure

## Risks

| Risk | Mitigation |
|------|------------|
| Method-class association ambiguous | Use file naming convention: `ClassName_MethodName.html` |
| HTML structure variance | Multi-parser consensus validation |
| Regression in existing extraction | Run existing test suite before/after |

## Phase Files

- [Phase 01: Data Classification](./phase-01-data-classification-and-stratified-sampling.md)
- [Phase 02: Verification Framework](./phase-02-automated-verification-framework-implementation.md)
- [Phase 03: Spot Check Execution](./phase-03-spot-check-execution-and-findings.md)
- [Phase 04: Parser Bug Fixes](./phase-04-parser-bug-fixes-method-class-association.md)
- [Phase 05: Re-extraction & Validation](./phase-05-reextraction-and-validation-comparison.md)
- [Phase 06: Documentation Update](./phase-06-documentation-and-completion-report-update.md)
