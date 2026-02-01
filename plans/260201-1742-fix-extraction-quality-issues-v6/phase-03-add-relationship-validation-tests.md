# Phase 03: Add Relationship Validation Tests

## Context Links
- Parent: [plan.md](./plan.md)
- Depends on: [Phase 01](./phase-01-fix-method-property-subfolder-detection.md), [Phase 02](./phase-02-add-enum-member-table-extraction.md)
- Test suite: `tests/`

## Overview
- **Priority:** P1 (High)
- **Status:** completed
- **Description:** Add tests that validate relationships, not just entity counts

## Key Insights

From journal analysis:
- Current tests: "Did we extract N methods?" ✅ PASS
- Missing tests: "Are methods in correct parent class?" ❌ NOT TESTED
- 108% recall = over-extraction (red flag, not success)
- 86 samples all from class definition files (biased sample)

## Requirements

### Functional
1. Test: Methods in `/Methods/` files are NOT standalone classes
2. Test: Methods are in their parent class's `methods[]` array
3. Test: Enums have at least 1 property with value
4. Test: Inheritance captured when present in HTML
5. Automated spot check: 20 random files after extraction

### Non-Functional
- Tests runnable via `pytest`
- Clear pass/fail with specific failure messages
- Fast execution (<30 seconds for relationship tests)

## Architecture

```
Relationship Validation Tests
├── test_methods_not_standalone_classes.py
│   └── Verify /Methods/ files don't create class entries
├── test_method_parent_association.py
│   └── Verify methods in parent class.methods[]
├── test_enum_members_extracted.py
│   └── Verify enums have properties with values
├── test_inheritance_captured.py
│   └── Verify base class extracted when present
└── test_spot_check_random_files.py
    └── Random 20-file verification
```

## Related Code Files

### Create
- `tests/test_relationship_validation.py` - main relationship tests

### Modify
- `tests/conftest.py` - add fixtures for loaded knowledge base

## Implementation Steps

1. Create test fixture to load knowledge base JSON
2. Add `test_methods_subfolder_not_classes()`:
   - Scan knowledge base for class names containing `_`
   - Verify they're not from `/Methods/` or `/Properties/` paths
3. Add `test_method_in_parent_class()`:
   - For known method files, verify method in parent class
   - Use `IApplication.NewModelDocumentWithUnitSystem` as test case
4. Add `test_enum_has_members()`:
   - Find all classes with `IntEnum` inheritance
   - Verify each has at least 1 property
5. Add `test_inheritance_extracted()`:
   - Sample classes with known base classes
   - Verify inheritance field populated
6. Add `test_random_spot_check()`:
   - Select 20 random HTML files
   - Verify extraction matches HTML content

## Todo List

- [ ] Create `tests/test_relationship_validation.py`
- [ ] Add fixture for loading knowledge base
- [ ] Implement method/class association test
- [ ] Implement enum member test
- [ ] Implement inheritance test
- [ ] Implement random spot check test
- [ ] Run tests, ensure all pass after Phase 01+02 fixes

## Success Criteria

- [ ] All relationship tests pass
- [ ] Spot check: <10% failure rate (was 40%)
- [ ] No false positives (tests don't pass when they should fail)
- [ ] Tests catch the v5 issues when run against v5 KB

## Risk Assessment

- **Risk:** Tests may be flaky with random spot checks
- **Mitigation:** Use fixed seed for reproducibility, or test specific known files

## Next Steps
- After this phase: Phase 04 (re-extraction and verification)
