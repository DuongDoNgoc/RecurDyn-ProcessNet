# Phase 04: Re-Extract and Spot Check Verification

## Context Links
- Parent: [plan.md](./plan.md)
- Depends on: [Phase 01](./phase-01-fix-method-property-subfolder-detection.md), [Phase 02](./phase-02-add-enum-member-table-extraction.md), [Phase 03](./phase-03-add-relationship-validation-tests.md)
- Parser: `src/recurdyn-doc-parser.py`

## Overview
- **Priority:** P0 (Critical - Final Validation)
- **Status:** completed
- **Description:** Run full extraction with fixes and verify quality

## Key Insights

This is the validation gate. Must pass before any production use.

Previous versions:
- v3: 108% recall, 99.78% precision → 40% spot check failure
- v4: Fixed return types → no re-validation
- v5: Fixed generic types → 40% spot check failure

v6 must:
- Run comprehensive spot checks BEFORE declaring success
- Test relationships, not just counts
- Achieve <10% failure rate

## Requirements

### Functional
1. Run full extraction on 40,625 HTML files
2. Generate `processnet-knowledge-v6.json`
3. Run relationship validation tests (Phase 03)
4. Run 20+ random spot checks
5. Document all issues found

### Non-Functional
- Extraction time: <5 minutes
- Spot check automation: <2 minutes
- Clear pass/fail reporting

## Architecture

```
Extraction Pipeline
    ↓
Run python src/recurdyn-doc-parser.py --output output/processnet-knowledge-v6.json
    ↓
Run pytest tests/test_relationship_validation.py
    ↓
Run spot check script (20 random files)
    ↓
Generate validation report
    ↓
Pass/Fail decision
```

## Implementation Steps

1. Run fixed parser on full HTML corpus
2. Verify extraction completes without errors
3. Run relationship validation tests:
   ```bash
   pytest tests/test_relationship_validation.py -v
   ```
4. Run spot check on specific files from v5 failures:
   - `IApplication_NewModelDocumentWithUnitSystem.html` → method not class
   - `RFlexMassInvariantType.html` → has enum members
   - `IGManagerRFlexGenerator.html` → has inheritance
5. Run automated 20-file random spot check
6. Calculate failure rate
7. If <10%: PASS, deploy v6
8. If ≥10%: Document issues, iterate

## Todo List

- [ ] Run full extraction with fixes
- [ ] Verify extraction stats (files, classes, methods, properties)
- [ ] Run relationship validation tests
- [ ] Spot check: IApplication method file
- [ ] Spot check: RFlexMassInvariantType enum
- [ ] Spot check: IGManagerRFlexGenerator inheritance
- [ ] Run 20-file random spot check
- [ ] Calculate and document failure rate
- [ ] Generate validation report

## Success Criteria

- [ ] Extraction completes without errors
- [ ] All relationship tests pass
- [ ] Specific spot checks pass:
  - [ ] `NewModelDocumentWithUnitSystem` is method of `IApplication`, not standalone class
  - [ ] `RFlexMassInvariantType` has 2 properties with values
  - [ ] `IGManagerRFlexGenerator` has `DispatchBaseClass` inheritance
- [ ] Random spot check: <10% failure rate

## Risk Assessment

- **Risk:** Unknown edge cases not covered by tests
- **Mitigation:** Run 50+ spot checks if initial 20 passes

## Verification Checklist

Before marking v6 as production-ready:

1. [ ] Extraction completed successfully
2. [ ] Relationship tests: ALL PASS
3. [ ] Manual spot check (5 files): ALL PASS
4. [ ] Automated spot check (20 files): <10% failure
5. [ ] No regressions from v5 (return types, generic types still work)
6. [ ] Documentation updated

## Next Steps

If v6 passes:
- Deploy to production
- Update API to use v6 KB path
- Archive v3-v5 knowledge bases
- Document lessons learned

If v6 fails:
- Identify new issues
- Create v7 plan
- Iterate until <10% failure
