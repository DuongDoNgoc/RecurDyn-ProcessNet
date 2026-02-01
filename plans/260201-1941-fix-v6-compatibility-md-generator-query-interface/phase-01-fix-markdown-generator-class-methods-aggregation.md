---
phase: 01
title: "Fix Markdown Generator to Aggregate Methods from Classes"
status: completed
effort: 30m
parallel: true
---

# Phase 01: Fix Markdown Generator

## Context

- **File:** `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py`
- **Function:** `generate_markdown()` (lines 1233-1273)
- **Problem:** Uses deprecated `standalone_methods[]` (0 items) instead of `classes[].methods[]` (2,244 items)

## Current Code (Lines 1247-1258)

```python
# Line 1247: Shows 0 because standalone_methods is empty
f.write(f"**Methods:** {len(ns_data.get('standalone_methods', []))}\n\n")
f.write(f"**Examples:** {len(ns_data.get('examples', []))}\n\n")

# Lines 1251-1258: Never renders because standalone_methods is empty
if ns_data.get('standalone_methods'):
    f.write("## Methods\n\n")
    for method in ns_data['standalone_methods'][:50]:  # Limit for readability
        f.write(f"### {method['name']}\n\n")
        if method.get('signature'):
            f.write(f"```\n{method['signature']}\n```\n\n")
        if method.get('description'):
            f.write(f"{method['description']}\n\n")
```

## Fixed Code

Replace lines 1244-1270 with:

```python
# Overview
f.write("## Overview\n\n")
f.write(f"**Full Name:** {ns_data.get('full_name', ns_name)}\n\n")

# Count methods from all classes
classes = ns_data.get('classes', [])
total_methods = sum(len(cls.get('methods', [])) for cls in classes)

f.write(f"**Classes:** {len(classes)}\n\n")
f.write(f"**Methods:** {total_methods}\n\n")
f.write(f"**Examples:** {len(ns_data.get('examples', []))}\n\n")

# Classes section with methods grouped by class
if classes:
    f.write("## Classes\n\n")
    for cls in classes:
        cls_name = cls.get('name', 'Unknown')
        f.write(f"### {cls_name}\n\n")

        if cls.get('description'):
            f.write(f"{cls['description']}\n\n")

        # Show methods for this class
        methods = cls.get('methods', [])
        if methods:
            f.write(f"**Methods ({len(methods)}):**\n\n")
            for method in methods[:10]:  # Limit 10 methods per class
                method_name = method.get('name', 'Unknown')
                f.write(f"#### {method_name}\n\n")
                if method.get('signature'):
                    f.write(f"```\n{method['signature']}\n```\n\n")
                if method.get('description'):
                    f.write(f"{method['description'][:300]}\n\n")

            if len(methods) > 10:
                f.write(f"*... and {len(methods) - 10} more methods*\n\n")
```

## Implementation Steps

1. [x] Open `src/recurdyn-doc-parser.py`
2. [x] Locate `generate_markdown()` function (line 1233)
3. [x] Replace lines 1244-1270 with fixed code above
4. [x] Preserve examples section (lines 1261-1271)
5. [x] Test with: `python3 src/recurdyn-doc-parser.py -i knowledge -o output/test.json -m output/test-md`

## Validation

```bash
# Check markdown output
cat output/test-md/ProcessNet.md | head -30

# Expected output should show:
# **Classes:** 51
# **Methods:** 2244
# **Examples:** 887
```

## Files Modified

- `src/recurdyn-doc-parser.py` (lines 1244-1270)

## Rollback

If issues occur, revert to original code using git:
```bash
git checkout src/recurdyn-doc-parser.py
```
