---
phase: 03
title: "Update Test Files to Use classes[].methods[] Instead of standalone_methods[]"
status: pending
effort: 30m
parallel: false
depends_on: [01, 02]
---

# Phase 03: Update Test Files

## Context

Multiple test files assert on deprecated `standalone_methods[]`. All tests will fail until updated.

## Files to Update

| File | Occurrences |
|------|-------------|
| `tests/test-integration-automation-scenarios.py` | 20+ |
| `tests/test-integration-method-signatures.py` | 8 |
| `tests/test-integration-parameter-types.py` | 3 |
| `tests/test-extraction-validation-and-query-interface-verification.py` | 4 |
| `tests/helpers/validation-helpers.py` | 3 |

## Helper Function Pattern

Add to `tests/helpers/validation-helpers.py`:

```python
def get_all_methods_from_namespace(ns_data: dict) -> list:
    """Aggregate methods from all classes in a namespace.

    Works with v6 KB structure where methods are in classes[].methods[].
    """
    all_methods = []
    for cls in ns_data.get('classes', []):
        cls_name = cls.get('name', '')
        for method in cls.get('methods', []):
            method_copy = dict(method)
            method_copy['parent_class'] = cls_name
            all_methods.append(method_copy)
    return all_methods
```

## Search/Replace Pattern

**Before:**
```python
for method in ns_data.get('standalone_methods', []):
```

**After:**
```python
for method in get_all_methods_from_namespace(ns_data):
```

## Test File: test-integration-automation-scenarios.py

### Changes Required

Lines 66, 82, 99, 115, 132, 155, 176, 192, 208, 220, 252, 267, 282, 297, 313, 347, 364, 384, 408:

Replace all occurrences of:
```python
for method in ns_data.get('standalone_methods', []):
```

With:
```python
from tests.helpers.validation_helpers import get_all_methods_from_namespace
# ...
for method in get_all_methods_from_namespace(ns_data):
```

And for count assertions:
```python
# Before
method_count = len(auto_ns.get('standalone_methods', []))

# After
method_count = len(get_all_methods_from_namespace(auto_ns))
```

## Test File: test-integration-method-signatures.py

Lines 113, 117, 171, 252, 264, 312, 326:

Same pattern as above.

## Test File: test-integration-parameter-types.py

Lines 207, 227, 253:

Same pattern as above.

## Test File: test-extraction-validation-and-query-interface-verification.py

Lines 56, 103, 111, 122:

Same pattern as above.

## Implementation Steps

1. [ ] Add helper function to `tests/helpers/validation-helpers.py`
2. [ ] Update `tests/test-integration-automation-scenarios.py`
3. [ ] Update `tests/test-integration-method-signatures.py`
4. [ ] Update `tests/test-integration-parameter-types.py`
5. [ ] Update `tests/test-extraction-validation-and-query-interface-verification.py`

## Validation

```bash
# Run all tests
cd /mnt/d/Vibecoding/RecurDyn-ProcessNet
pytest tests/ -v --tb=short

# Expected: All tests pass
```

## Files Modified

- `tests/helpers/validation-helpers.py`
- `tests/test-integration-automation-scenarios.py`
- `tests/test-integration-method-signatures.py`
- `tests/test-integration-parameter-types.py`
- `tests/test-extraction-validation-and-query-interface-verification.py`

## Rollback

```bash
git checkout tests/
```
