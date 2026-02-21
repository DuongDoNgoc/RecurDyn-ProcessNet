---
title: "Fix Parameter and Return Type Extraction Bugs"
description: "Fix parser bugs in parameter type (HTML <strong> tags) and return type (case-insensitive matching) extraction"
status: pending
priority: P1
effort: 2h
branch: master
tags: [bugfix, parser, extraction, types]
created: 2026-02-01
---

# Fix Parameter and Return Type Extraction Bugs

## Overview
Fix two critical parser bugs preventing accurate type extraction from ProcessNet documentation HTML.

**Bug 1: Parameter Type Extraction (lines 349-356)**
- Parser checks for markdown `**param**` but HTML uses `<strong>param</strong>` tags
- Missing HTML regex fallback for parameter types

**Bug 2: Return Type Extraction (line 422)**
- Parser looks for 'Return Type' (capital T) but HTML has 'Return type' (lowercase)
- Missing case-insensitive matching for return type keywords

## Priority
**P1** - Critical bug fix. Type information accuracy directly impacts knowledge base quality for code generation.

## Current Status
Pending implementation. Debugger report identifies exact locations and fixes needed.

## Key Insights
From debugger analysis:
- Parameter extraction: Only checks markdown format (`**param**`), missing HTML `<strong>` tags
- Return type extraction: Case-sensitive keyword matching fails on 'Return type' vs 'Return Type'
- Both fixes are simple regex/condition additions
- Re-running extraction required after fixes to regenerate v3 knowledge base

## Requirements

### Functional Requirements
1. Fix parameter type extraction to handle HTML `<strong>` tags
2. Fix return type extraction to use case-insensitive matching
3. Re-run extraction to regenerate v3 knowledge base with fixed types
4. Run integration tests to verify fixes

### Non-Functional Requirements
- Maintain backward compatibility with existing knowledge base format
- No performance regression in extraction speed
- Preserve existing test pass rate (88%+)

## Architecture

### Bug 1: Parameter Type Extraction Fix
**Location:** `src/recurdyn-doc-parser.py:349-356`

**Current Code:**
```python
# Try markdown format first
param_match = re.search(
    rf'\*\*{re.escape(param.name)}\*\*\s*[:\-]\s*([^\-\n*]+?)(?:\n|\*|$)',
    str(dd)
)
if param_match:
    extracted_type = param_match.group(1).strip()
    if not param.type and extracted_type:
        param.type = extracted_type
```

**Fix Required:**
Add HTML `<strong>` tag regex fallback after markdown check:
```python
# Try HTML <strong> format if markdown didn't match
if not param.type:
    html_match = re.search(
        rf'<strong>{re.escape(param.name)}</strong>\s*[:\-]\s*([^\-\n<]+?)(?:\n|<|$)',
        str(dd),
        re.IGNORECASE
    )
    if html_match:
        extracted_type = html_match.group(1).strip()
        if extracted_type:
            param.type = extracted_type
```

### Bug 2: Return Type Extraction Fix
**Location:** `src/recurdyn-doc-parser.py:422`

**Current Code:**
```python
if any(keyword in dt_text for keyword in ['Return Type', 'Type', 'Returns', 'rtype']):
```

**Fix Required:**
Use case-insensitive matching:
```python
if any(keyword.lower() in dt_text.lower() for keyword in ['Return Type', 'Type', 'Returns', 'rtype']):
```

## Related Code Files

### Files to Modify
- `src/recurdyn-doc-parser.py` - Apply both regex fixes

### Files to Run
- `src/recurdyn-doc-parser.py` - Re-run extraction after fixes
- `tests/test_integration.py` - Run integration tests for verification

### Files to Update (if verification passes)
- `README.md` - Update extraction statistics if improved

## Implementation Steps

### Phase 1: Apply Fixes (30 min)
1. Open `src/recurdyn-doc-parser.py`
2. Navigate to line 349 (parameter type extraction)
3. Add HTML `<strong>` tag regex fallback after markdown check
4. Navigate to line 422 (return type extraction)
5. Replace case-sensitive `any()` with case-insensitive version using `.lower()`
6. Save file

### Phase 2: Regenerate Knowledge Base (45 min)
1. Run extraction script:
   ```bash
   python src/recurdyn-doc-parser.py \
       --input knowledge/RecurDynHelp \
       --output output/processnet-knowledge.json \
       --markdown output/markdown \
       --verbose
   ```
2. Monitor extraction logs for errors
3. Verify output JSON generation completes
4. Check extraction summary statistics

### Phase 3: Verify Fixes (30 min)
1. Run integration tests:
   ```bash
   pytest tests/test_integration.py -v
   ```
2. Check test results for improvements
3. Spot-check extracted methods for parameter types
4. Spot-check extracted methods for return types
5. Verify no regression in test pass rate

### Phase 4: Document Results (15 min)
1. Compare before/after extraction statistics
2. Document improvement in type accuracy
3. Update README.md if extraction stats improved
4. Create commit with conventional commit format

## Success Criteria

### Definition of Done
- [ ] Both regex fixes applied to parser
- [ ] Knowledge base regenerated without errors
- [ ] Integration tests pass (>=88% pass rate maintained)
- [ ] Parameter types now extract from HTML `<strong>` tags
- [ ] Return types now extract with case-insensitive matching
- [ ] No performance regression in extraction time
- [ ] Commit message follows conventional commit format

### Validation Methods
1. **Code Review:** Verify regex patterns match HTML structure
2. **Extraction Logs:** Check for successful extraction without errors
3. **Integration Tests:** Run full test suite for regression check
4. **Spot Checks:** Manually verify 5-10 methods have correct types
5. **Performance:** Extraction time <5 minutes (baseline: ~2-3 min)

## Risk Assessment

### Potential Issues
1. **Regex Complexity:** New HTML regex may have edge cases
   - Mitigation: Use non-greedy match `.*?` and test on sample HTML
2. **Performance:** Additional regex may slow extraction
   - Mitigation: Only run HTML regex if markdown fails (short-circuit)
3. **False Positives:** Case-insensitive matching may match wrong text
   - Mitigation: Context preserved by checking full field name, not just keyword

### Rollback Plan
If tests fail or performance degrades:
1. Revert parser changes via `git checkout -- src/recurdyn-doc-parser.py`
2. Restore previous knowledge base from git
3. Report issue for alternative approach

## Security Considerations
- No new security risks (HTML parsing already handled by BeautifulSoup)
- Regex uses `re.escape()` to prevent ReDoS on parameter names
- Input validation already in place via `MAX_PARAM_TEXT_LENGTH`

## Next Steps

### Immediate (After Approval)
1. Apply Bug 1 fix (parameter type HTML regex)
2. Apply Bug 2 fix (return type case-insensitive)
3. Re-run extraction
4. Run integration tests

### Follow-up Tasks
1. If tests pass: Commit changes with conventional commit format
2. If tests fail: Debug and adjust regex patterns
3. Update documentation if extraction statistics improve
4. Consider adding unit tests for these specific parsing scenarios

## Dependencies
- Requires access to RecurDyn HTML documentation (`knowledge/RecurDynHelp`)
- Requires Python environment with `beautifulsoup4` and `lxml`
- Requires `pytest` for integration tests
- No external dependencies or blocking tasks

## Time Estimate
- **Phase 1 (Apply Fixes):** 30 min
- **Phase 2 (Regenerate KB):** 45 min
- **Phase 3 (Verify):** 30 min
- **Phase 4 (Document):** 15 min
- **Total:** 2 hours

## Related Issues
- Debugger report: `plans/reports/debugger-260201-XXXX-extraction-accuracy-bug.md` (hypothetical)
- Previous fix: Commit `5199b3d` - "fix(parser): remediate extraction accuracy bug and generate v3 knowledge base"

## Notes
- Fixes are targeted and low-risk (small code changes)
- Both fixes address pattern matching issues identified by debugger
- Re-running extraction required to propagate fixes to knowledge base
- Integration tests will validate no regression in existing functionality
- If successful, this will improve type information accuracy for code generation use cases
