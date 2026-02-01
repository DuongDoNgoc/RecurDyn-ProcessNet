# Research: Root Cause Analysis of v3-v5 Extraction Failures

**Date:** 2026-02-01 17:42
**Sources:** 4 journals from today (17:00+)

## Executive Summary

The v3-v5 knowledge base extraction cycle reveals a **systemic validation failure**, not a parser bug. We tested the wrong things and celebrated the wrong metrics.

## The Pain Points (from Journals)

### 1. False Confidence from Metrics

**v3 Validation Results:**
- Method recall: 108% ✅
- Property recall: 99.78% ✅
- Test suite: 95%+ pass rate ✅

**Reality (Spot Check):**
- Failure rate: 40% ❌
- Methods as classes: 20%+ ❌
- Enum members: 0% captured ❌

**Why:** 108% recall means OVER-EXTRACTION. We extracted more than expected, which is a red flag, not success. We counted entities without validating relationships.

### 2. The Three Critical Bugs

| Bug | Description | Root Cause | Detection Method |
|-----|-------------|------------|------------------|
| Method/Class | Files in `/Methods/` create standalone classes | Parser treats method pages as class definitions | Spot check |
| Enum Members | Enum values not extracted | Parser doesn't recognize enum table pattern | Spot check |
| Inheritance | Base class info missing | Parser doesn't extract from `Bases:` text | Spot check |

All three bugs passed 86-sample validation because samples were biased toward "easy" class definition files.

### 3. Sample Selection Bias

**v3 Validation Samples:**
- Class definition files: 86 (100%)
- Method/Property files: 0 (0%)
- Enum files: 5 (6%)

**Spot Check Samples:**
- Class definition files: 2 (40%)
- Method files: 2 (40%) ← Found the bug
- Enum files: 1 (20%) ← Found the bug

**Lesson:** Stratified sampling must cover ALL file patterns, not just easy cases.

### 4. Architectural Decision: BeautifulSoup vs Browser

The journals considered switching to MCP browser extraction. Analysis:

| Aspect | BeautifulSoup | Browser |
|--------|---------------|---------|
| Speed | 4 min (40K files) | 6-10 hours |
| Will it fix bugs? | Depends on code | NO |
| Root cause | Pattern recognition | Pattern recognition |

**Conclusion:** Browser extraction won't fix our issues. The HTML structure is the same. We need better parsing logic, not different parsing tools.

## The Fix Strategy

### What Must Change

1. **Parser Logic:**
   - Detect `/Methods/` and `/Properties/` subdirs → don't create class entries
   - Parse enum member tables → extract as properties
   - Extract inheritance from `Bases:` pattern

2. **Validation Strategy:**
   - Test relationships, not just counts
   - Sample ALL file patterns (class, method, property, enum)
   - Automated spot check after every extraction

3. **Success Criteria:**
   - Spot check failure rate: <10% (was 40%)
   - Methods in parent class, not standalone
   - Enums have member properties

## Unresolved Questions

1. Why did 86 stratified samples all pass when 40% of random files fail?
   - **Answer:** Samples were biased toward class definition files

2. Is BeautifulSoup fundamentally incapable?
   - **Answer:** No, we just need better patterns

3. Should we switch architectures?
   - **Answer:** No, fix parser logic first

4. What's the theoretical maximum accuracy?
   - **Unknown:** Need more testing after fixes

## References

- `docs/journals/260201-knowledge-base-extraction-journey-v3-through-v5-iteration.md`
- `docs/journals/260201-architectural-decision-beautifulsoup-vs-mcp-browser-extraction-tradeoff-analysis.md`
- `docs/journals/260201-test-coverage-gap-why-validation-passed-when-production-failed.md`
- `docs/journals/260201-extraction-journey-summary-lessons-from-v3-through-v5-iterations.md`
