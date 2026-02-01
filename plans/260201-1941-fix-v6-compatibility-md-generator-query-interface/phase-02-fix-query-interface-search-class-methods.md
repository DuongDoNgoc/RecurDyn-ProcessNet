---
phase: 02
title: "Fix Query Interface to Search Methods in Classes"
status: completed
effort: 30m
parallel: true
completed_at: 2026-02-01T19:44:00
---

# Phase 02: Fix Query Interface

## Context

- **File:** `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/processnet-query-interface.py`
- **Problem:** 4 locations use deprecated `standalone_methods[]`
- **Impact:** Search returns 0 results despite 2,244 methods in KB

## Affected Locations

| Line | Function | Issue |
|------|----------|-------|
| 101 | `find_method()` | Searches `standalone_methods[]` |
| 235 | `search_by_description()` | Searches `standalone_methods[]` |
| 278 | `list_namespace_contents()` | Returns `standalone_methods[]` |
| 320 | `get_statistics()` | Counts `standalone_methods[]` |

## Fix 1: Add Helper Method (Insert after line 76)

```python
def _get_all_methods_from_classes(self, ns_data: dict) -> list:
    """Aggregate methods from all classes in a namespace."""
    all_methods = []
    for cls in ns_data.get('classes', []):
        cls_name = cls.get('name', '')
        for method in cls.get('methods', []):
            # Add class context to method
            method_with_class = dict(method)
            method_with_class['parent_class'] = cls_name
            all_methods.append(method_with_class)
    return all_methods
```

## Fix 2: Update `find_method()` (Lines 99-110)

**Before:**
```python
ns_data = self.kb['namespaces'].get(ns, {})
for method in ns_data.get('standalone_methods', []):
    if method['name'].lower() == method_lower:
```

**After:**
```python
ns_data = self.kb['namespaces'].get(ns, {})
all_methods = self._get_all_methods_from_classes(ns_data)
for method in all_methods:
    if method['name'].lower() == method_lower:
```

## Fix 3: Update `search_by_description()` (Lines 233-245)

**Before:**
```python
for method in ns_data.get('standalone_methods', []):
    desc = method.get('description', '').lower()
```

**After:**
```python
all_methods = self._get_all_methods_from_classes(ns_data)
for method in all_methods:
    desc = method.get('description', '').lower()
```

## Fix 4: Update `list_namespace_contents()` (Line 278)

**Before:**
```python
'methods': [m['name'] for m in ns_data.get('standalone_methods', [])],
```

**After:**
```python
'methods': [m['name'] for m in self._get_all_methods_from_classes(ns_data)],
```

## Fix 5: Update `get_statistics()` (Lines 319-322)

**Before:**
```python
total_methods = sum(
    len(ns.get('standalone_methods', []))
    for ns in self.kb.get('namespaces', {}).values()
)
```

**After:**
```python
total_methods = sum(
    len(self._get_all_methods_from_classes(ns))
    for ns in self.kb.get('namespaces', {}).values()
)
```

## Fix 6: Update `_build_indices()` (Lines 62-66)

**Before:**
```python
self._method_names = list(self.kb.get('method_index', {}).keys())
```

**After:**
```python
# Build method names from classes if method_index is empty
self._method_names = list(self.kb.get('method_index', {}).keys())
if not self._method_names:
    for ns_data in self.kb.get('namespaces', {}).values():
        for cls in ns_data.get('classes', []):
            for method in cls.get('methods', []):
                name = method.get('name', '').lower()
                if name and name not in self._method_names:
                    self._method_names.append(name)
```

## Implementation Steps

1. [x] Open `src/processnet-query-interface.py`
2. [x] Add helper method `_get_all_methods_from_classes()` after line 76
3. [x] Update `find_method()` (lines 99-110)
4. [x] Update `search_by_description()` (lines 233-245)
5. [x] Update `list_namespace_contents()` (line 278)
6. [x] Update `get_statistics()` (lines 319-322)
7. [x] Update `_build_indices()` (lines 62-66)

## Validation

```bash
# Test search
python3 src/processnet-query-interface.py --search "CreateBody" --kb output/processnet-knowledge-v6.json

# Expected: Results for CreateBody method

# Test stats
python3 src/processnet-query-interface.py --kb output/processnet-knowledge-v6.json
# In interactive mode, type: stats
# Expected: Methods: 2244
```

## Files Modified

- `src/processnet-query-interface.py` (6 locations)

## Rollback

```bash
git checkout src/processnet-query-interface.py
```
