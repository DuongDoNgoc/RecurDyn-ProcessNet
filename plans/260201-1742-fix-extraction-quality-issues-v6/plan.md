---
title: "Fix Knowledge Base Extraction Quality Issues - v6"
description: "Fix method/class association, enum extraction, and validation gaps"
status: pending
priority: P0
effort: 4h
branch: master
tags: [parser, extraction, validation, critical]
created: 2026-02-01
---

# Fix Knowledge Base Extraction Quality Issues - v6

## Problem Statement

After v3-v5 iterations, spot checks revealed **40% failure rate** despite 108% method recall. The core issues:

1. **Methods in `/Methods/` subfolders extracted as separate classes** (20%+ failure)
2. **Enum members not extracted from tables** (100% failure for enums)
3. **Validation tested counts, not relationships** (false confidence)

## Root Cause Analysis

### Issue 1: Method File Parsing Bug
**Location:** `_associate_members_with_classes()` line 872-923

The parser correctly extracts class name from filename (e.g., `IApplication` from `IApplication_NewModelDocumentWithUnitSystem.html`), BUT the method still gets added to the `standalone_methods` list AND a new class is created if the parent class doesn't exist yet.

**The actual bug:** When parsing `/Methods/` files, the parser:
1. Creates a new class with name from filename split (e.g., `IApplication`)
2. Associates method with that class
3. But also adds to `standalone_methods`
4. Result: Methods appear in wrong namespaces, multiple times

### Issue 2: Enum Member Table Pattern Not Recognized
**Location:** `extract_autosummary_members()` line 490-546

The parser only looks for `<p class="rubric">` + `<table class="autosummary">` pattern.
Enum members are in a different pattern: `<table class="docutils">` with name/value rows.

### Issue 3: Validation Blind Spots
- Sampled only class definition files (easy cases)
- Tested "did we extract N items" not "are they correctly organized"
- 108% recall = extracting TOO MUCH, not success

## Solution Architecture

### Fix 1: Detect Method/Property Subfolders
- If path contains `/Methods/` or `/Properties/` → parse as member file, not class file
- Don't create new class entries for method/property pages
- Associate extracted members with existing parent class only

### Fix 2: Add Enum Member Table Extraction
- Look for `<table class="docutils">` tables in enum pages
- Extract member name from first column, value from second column
- Add as properties with `default` field set to value

### Fix 3: Add Relationship Validation
- Test: Is method in parent class? (not standalone)
- Test: Does enum have members?
- Test: Is inheritance captured when present in HTML?
- Automated spot check: 20 random files after each extraction

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 01 | Fix method/property subfolder detection | completed |
| 02 | Add enum member table extraction | completed |
| 03 | Add relationship validation tests | pending |
| 04 | Re-extract and spot check verification | pending |

## Success Criteria

- Spot check failure rate: <10% (was 40%)
- Methods in `/Methods/` folders NOT creating standalone classes
- Enums have at least 1 property with value
- 20+ random file spot check passes

## Research

- [Root Cause Analysis](./research/root-cause-analysis-v3-v5-extraction-failures.md)

## Phase Details

- [Phase 01: Fix Method/Property Subfolder Detection](./phase-01-fix-method-property-subfolder-detection.md)
- [Phase 02: Add Enum Member Table Extraction](./phase-02-add-enum-member-table-extraction.md)
- [Phase 03: Add Relationship Validation Tests](./phase-03-add-relationship-validation-tests.md)
- [Phase 04: Re-Extract and Spot Check Verification](./phase-04-reextract-and-spot-check-verification.md)

## Related Files

- Parser: `src/recurdyn-doc-parser.py`
- Tests: `tests/`
- Journals: `docs/journals/260201-*.md`
- Spot check report: `plans/reports/debugger-260201-1705-*.md`

## Key Lessons from v3-v5

1. **108% recall = red flag, not success** - Over-extraction means wrong things extracted
2. **Count-based validation is dangerous** - Must test relationships, not just counts
3. **Sample diversity critical** - 86 samples from "easy" files missed all bugs
4. **Manual spot checks essential** - 30 min of checking found what automation missed
5. **Don't celebrate prematurely** - v3 marked "100% complete" with 40% failure rate

## Validation Summary

**Validated:** 2026-02-01
**Questions asked:** 6

### Confirmed Decisions

| Decision | User Choice |
|----------|-------------|
| Orphan method handling | Collect in special 'orphans' section for manual review |
| Spot check threshold | <5% failure rate (stricter than plan's <10%) |
| Standalone methods array | Remove (don't keep for backward compat) |
| Enum table detection | IntEnum inheritance only (precise) |
| Spot check reproducibility | Hybrid: 15 known problematic + 5 random files |
| File processing order | Sort by path depth (shallow class files first) |

### Action Items (Plan Updates Needed)

- [ ] Phase 01: Add orphan collection logic instead of skip/warn
- [ ] Phase 01: Remove standalone_methods[] population entirely
- [ ] Phase 01: Implement path-depth sorting for file processing
- [ ] Phase 02: Only extract enum members from IntEnum classes
- [ ] Phase 03: Update spot check to hybrid (15 known + 5 random)
- [ ] Phase 04: Update success threshold from <10% to <5%
