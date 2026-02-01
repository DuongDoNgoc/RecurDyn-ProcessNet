---
phase: 05
title: "Re-extraction & Validation Comparison"
status: pending
effort: 0.5h
depends_on: [phase-04]
---

# Phase 05: Re-extraction & Validation Comparison

## Context

- **Plan**: [plan.md](./plan.md)
- **Fixed Parser**: `src/recurdyn-doc-parser.py`
- **Input**: `output/extracted_chm/` (19,344 HTML files)

## Overview

Run fixed parser on all HTML files, re-run spot check, and compare old vs new extraction statistics.

## Requirements

1. Backup existing knowledge base
2. Run fixed parser on all 19,344 HTML files
3. Re-run spot check verification on 100 samples
4. Compare before/after statistics
5. Generate accuracy improvement report

## Implementation Steps

### Step 1: Backup Existing Data

```bash
# Backup current knowledge base
cp output/processnet-knowledge.json output/processnet-knowledge-backup-pre-fix.json
cp output/processnet-knowledge.json verification/baseline-knowledge.json
```

### Step 2: Run Fixed Parser

```bash
python src/recurdyn-doc-parser.py \
  --input output/extracted_chm \
  --output output/processnet-knowledge.json \
  --markdown output/markdown \
  --verbose 2>&1 | tee verification/reextraction-log.txt
```

Expected output:
```
Files processed: 19,344
Classes extracted: ~1,803 (same)
Methods extracted: ~5,606 (same)
Methods in classes: ~4,500+ (NEW)
Properties in classes: ~10,000+ (NEW)
```

### Step 3: Re-run Spot Check

```bash
python tests/run-spot-check-verification.py \
  --manifest verification/sample-manifest.json \
  --output verification/spot-check-results-post-fix.json
```

### Step 4: Generate Comparison Report

File: `verification/before-after-comparison.md`

```markdown
# Before/After Extraction Comparison

## Statistics Comparison

| Metric | Before Fix | After Fix | Change |
|--------|-----------|-----------|--------|
| Classes extracted | 1,803 | 1,803 | 0% |
| Methods extracted | 5,606 | 5,606 | 0% |
| Properties extracted | 13,377 | 13,377 | 0% |
| **Methods in classes** | **0** | **TBD** | **+N%** |
| **Properties in classes** | **0** | **TBD** | **+N%** |

## Accuracy Comparison

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Class extraction | 100% | 100% | 98%+ |
| Method extraction | 100% | 100% | 95%+ |
| Method-class assoc. | 0% | TBD | 80%+ |
| Property-class assoc. | 0% | TBD | 80%+ |

## Sample Verification

| Sample | Before F1 | After F1 | Status |
|--------|----------|----------|--------|
| IApplication.html | 0.00 | TBD | - |
| IModelDocument.html | 0.00 | TBD | - |
...
```

### Step 5: Validate No Regressions

```bash
# Run existing test suite
pytest tests/ -v --tb=short 2>&1 | tee verification/test-suite-post-fix.txt

# Verify key metrics didn't decrease
python -c "
import json
old = json.load(open('verification/baseline-knowledge.json'))
new = json.load(open('output/processnet-knowledge.json'))

old_methods = old['metadata'].get('methods_extracted', 0)
new_methods = new['metadata'].get('methods_extracted', 0)

assert new_methods >= old_methods, f'Method count decreased: {old_methods} -> {new_methods}'
print(f'Methods: {old_methods} -> {new_methods} (OK)')
"
```

## Success Criteria

- [ ] All 19,344 files re-processed
- [ ] No decrease in class/method/property counts
- [ ] Method-class association rate > 80%
- [ ] Property-class association rate > 80%
- [ ] Existing test suite passes (200+ tests)
- [ ] Before/after comparison documented

## Output Artifacts

- `output/processnet-knowledge.json` (updated)
- `verification/baseline-knowledge.json` (backup)
- `verification/reextraction-log.txt`
- `verification/spot-check-results-post-fix.json`
- `verification/before-after-comparison.md`
- `verification/test-suite-post-fix.txt`

## Expected Improvements

| Metric | Expected Improvement |
|--------|---------------------|
| Methods in ClassDef | 0 → 4,500+ (80%+) |
| Properties in ClassDef | 0 → 10,000+ (75%+) |
| F1 Score (avg) | 0.0 → 0.85+ |
