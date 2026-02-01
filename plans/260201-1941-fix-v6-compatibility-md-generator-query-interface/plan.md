---
title: "Fix v6 KB Compatibility for Markdown Generator and Query Interface"
description: "Update markdown generator and query interface to use classes[].methods[] instead of deprecated standalone_methods[]"
status: completed
priority: P1
effort: 2h
branch: master
tags: [bugfix, compatibility, v6, markdown, query]
created: 2026-02-01
completed: 2026-02-01
---

# Fix v6 KB Compatibility: Markdown Generator and Query Interface

## Problem Summary

The v6 knowledge base architecture moved methods from `standalone_methods[]` (deprecated, 0 items) to `classes[].methods[]` (2,244 methods across 51 classes). Two critical consumers still use the deprecated structure:

| Component | Issue | Impact |
|-----------|-------|--------|
| `recurdyn-doc-parser.py` (lines 1247-1258) | Reads from `standalone_methods[]` | Markdown shows 0 methods |
| `processnet-query-interface.py` (4 locations) | Searches `standalone_methods[]` | Search returns 0 results |
| Test files (20+ locations) | Assert on `standalone_methods[]` | Tests fail |

## Data Structure (v6)

```
namespace.classes[] = [
  {
    name: "IApplication",
    methods: [
      { name: "NewModelDocumentWithUnitSystem", signature: "...", ... },
      ...
    ]
  },
  ...
]
namespace.standalone_methods[] = []  # Empty by design
```

## Fix Strategy

**Approach:** Aggregate methods from `classes[].methods[]` with class context preserved.

**Display Decision:** Class-grouped output (better UX, preserves context).

**Method Limit:** Show all classes, limit 10 methods per class in markdown.

---

## Phases (Parallel-Executable)

| Phase | File | Effort | Parallel |
|-------|------|--------|----------|
| 01 | recurdyn-doc-parser.py | 30m | Yes |
| 02 | processnet-query-interface.py | 30m | Yes |
| 03 | Test files | 30m | After 01+02 |
| 04 | Validation | 15m | After 03 |

### Dependency Graph

```
[Phase 01] ----+
               +---> [Phase 03] ---> [Phase 04]
[Phase 02] ----+
```

- Phase 01 and 02 can run in parallel
- Phase 03 depends on both 01 and 02
- Phase 04 validates all changes

---

## File Modifications

### Phase 01: Markdown Generator
- File: `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py`
- Lines: 1247-1270

### Phase 02: Query Interface
- File: `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/processnet-query-interface.py`
- Lines: 101, 235, 278, 320

### Phase 03: Test Files
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/test-integration-automation-scenarios.py`
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/test-integration-method-signatures.py`
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/test-integration-parameter-types.py`
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/test-extraction-validation-and-query-interface-verification.py`
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/helpers/validation-helpers.py`

---

## Success Criteria

1. Markdown output shows correct method count (2,244)
2. Markdown displays methods grouped by class
3. Query interface `find_method()` returns results
4. Query interface `search_method_fuzzy()` returns results
5. All tests pass with updated assertions
6. Backward compatibility preserved (no breaking changes)

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing consumers | Helper function abstracts data access |
| Performance with 2,244 methods | Lazy aggregation, limits in display |
| Test coverage gaps | Phase 03 updates all test files |

---

## Phase Files

- [Phase 01: Markdown Generator Fix](./phase-01-fix-markdown-generator.md)
- [Phase 02: Query Interface Fix](./phase-02-fix-query-interface.md)
- [Phase 03: Test File Updates](./phase-03-update-test-files.md)
- [Phase 04: Validation](./phase-04-validation.md)
