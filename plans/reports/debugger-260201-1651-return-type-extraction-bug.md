# Return Type Extraction Bug Report

**Date:** 2026-02-01
**Agent:** debugger
**Issue:** Return type extraction truncates generic type annotations (e.g., `list[float]` → `list`)

## Executive Summary

**Root Cause:** Regex pattern in `parse_sphinx_return_type()` only matches alphanumeric characters, causing it to truncate generic type annotations at the first `[` bracket.

**Impact:** Medium - Affects all methods with generic return types (lists, dicts, tuples, optional types).

**Status:** Root cause identified, fix proposed.

## Evidence

### HTML Source Analysis

**File:** `output/extracted_chm/Python/Post/IDataFileDatabase/Methods/IDataFileDatabase_GetValues.html`

```html
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>list[float]</p></dd>
```

**Actual return type in HTML:** `list[float]`

### Knowledge Base Analysis

**File:** `output/processnet-knowledge-v4.json`
**Line:** 325444

```json
"returns": "list",
"return_description": "list[float]",
```

**Extracted return type:** `list`
**Expected:** `list[float]`

### Problematic Code

**File:** `src/recurdyn-doc-parser.py`
**Lines:** 436-439

```python
# Extract first word/type as return type
type_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_<>,\s]*)', full_text)
if type_match:
    return_type = return_type or type_match.group(1).strip()
```

**Issue:** The pattern `[a-zA-Z0-9_<>,\s]` includes underscore, angle brackets, commas, and whitespace, but **missing square brackets `[` and `]`** and **period `.`**.

### Test Results

```python
# Current behavior:
'list[float]'     -> 'list'      # WRONG
'dict[str, int]'  -> 'dict'      # WRONG
'tuple[str, ...]' -> 'tuple'     # WRONG
'list[str]'       -> 'list'      # WRONG
'optional[str]'   -> 'optional'  # WRONG
'str'             -> 'str'       # OK
'int'             -> 'int'       # OK
```

## Affected Methods (Sample)

| Method | Expected Return Type | Extracted Return Type |
|--------|---------------------|----------------------|
| `GetValues` | `list[float]` | `list` |
| `GetUnit` | `str` | `str` ✓ |
| `GetDatabaseItem` | `recurdyn.Post.IDatabaseItem` | `recurdyn` |
| `GetPlottableNameList` | (unknown) | Not found |

**Note:** Methods with qualified type names like `recurdyn.Post.IDatabaseItem` also truncated to just `recurdyn`.

## Root Cause Analysis

1. **Missing characters in regex:**
   - `[` and `]` for generic types
   - `.` for qualified type names (e.g., `module.Class`)

2. **Pattern location:**
   - Line 436 in `src/recurdyn-doc-parser.py`
   - Inside `parse_sphinx_return_type()` method

3. **Code path:**
   - When field label contains "Return" keyword
   - Extracts first "word" as return type
   - Regex stops at first unsupported character

## Recommended Fix

**Option 1: Comprehensive regex (RECOMMENDED)**

```python
# Support Python type annotations including generics and qualified names
type_match = re.match(r'^[a-zA-Z_][a-zA-Z0-9_\[\]<>,\s\.\[\]\(\)\.\.\-]*', full_text)
```

**Option 2: Capture entire return type text**

```python
# Remove word boundary, capture until whitespace or end
return_type = full_text.split()[0]  # Get first token
```

**Option 3: Match balanced brackets (most robust)**

```python
def extract_type_with_generics(text):
    """Extract type including generic parameters like list[str], dict[str, int]."""
    # Match type name with optional generic parameters
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(?:\[[^\]]*\](?:\.\.\.)?)?(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*'
    match = re.match(pattern, text)
    return match.group(0) if match else ''
```

## Validation Strategy

1. **Unit test cases:**
   - Simple types: `str`, `int`, `bool`
   - Generic types: `list[str]`, `dict[str, int]`, `tuple[str, ...]`
   - Qualified names: `recurdyn.Post.IDatabaseItem`
   - Complex types: `list[tuple[str, int]]`

2. **Integration test:**
   - Re-parse HTML files
   - Verify GetValues has `returns: list[float]`

3. **Regression test:**
   - Ensure simple types still work
   - Check no truncation of qualified names

## Implementation Plan

1. Update regex pattern in line 436
2. Add unit tests for type extraction
3. Re-run parser to regenerate v5 knowledge base
4. Validate sample methods

## Next Steps

1. Review proposed fix options
2. Implement chosen solution
3. Run test suite
4. Regenerate knowledge base

## Unresolved Questions

- None
