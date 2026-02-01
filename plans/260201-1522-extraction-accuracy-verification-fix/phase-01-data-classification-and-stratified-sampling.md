---
phase: 01
title: "Data Classification & Stratified Sampling"
status: complete
effort: 0.5h
completed: 2026-02-01
---

# Phase 01: Data Classification & Stratified Sampling

## Context

- **Plan**: [plan.md](./plan.md)
- **Research**: [reports/researcher-260201-1525-html-parsing-statistical-sampling-validation-framework.md](./reports/researcher-260201-1525-html-parsing-statistical-sampling-validation-framework.md)
- **Knowledge Base**: `output/processnet-knowledge.json`

## Overview

Classify extraction targets and select 100 stratified samples for verification with 85-90% statistical confidence.

## Requirements

1. Classify by namespace (23 namespaces)
2. Classify by data type (class/interface/enum/method/property)
3. Classify by complexity (simple/medium/complex HTML depth)
4. Classify by HTML pattern (dl.py.method, dl.py.property, dl.py.class)
5. Select 100 total samples with proportional allocation

## Implementation Steps

### Step 1: Generate Classification Report
```bash
# Query knowledge base for distribution stats
python -c "
import json
from pathlib import Path
kb = json.load(open('output/processnet-knowledge.json'))
for ns, data in kb['namespaces'].items():
    print(f'{ns}: {len(data.get(\"classes\", []))} classes, {len(data.get(\"standalone_methods\", []))} methods')
"
```

### Step 2: Stratified Sample Selection

| Category | Allocation | Selection Criteria |
|----------|------------|-------------------|
| By Namespace | 4-5 samples each from top 5 namespaces | Proportional to file count |
| By Type | 30 classes, 40 methods, 20 properties, 10 misc | Balanced representation |
| By Complexity | 30 simple, 50 medium, 20 complex | Based on HTML nesting depth |
| Edge Cases | 10 samples | Malformed, rare patterns |

### Step 3: Create Sample Manifest
Output file: `verification/sample-manifest.json`
```json
{
  "samples": [
    {
      "id": 1,
      "file": "RecurDynHelp/IApplication.html",
      "type": "class",
      "namespace": "ProcessNet",
      "complexity": "medium",
      "expected_methods": 15,
      "expected_properties": 8
    }
  ]
}
```

### Step 4: Document Selection Methodology
- Random selection within strata
- Seed for reproducibility: 42
- Exclusions: _static, _images, navigation pages

## Success Criteria

- [ ] 100 samples selected across all categories
- [ ] Sample manifest JSON created
- [ ] At least 4 samples per major namespace
- [ ] Balanced type distribution (class/method/property)
- [ ] Selection methodology documented

## Output Artifacts

- `verification/sample-manifest.json`
- `verification/classification-report.md`
- `verification/sample-selection-log.txt`

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Uneven namespace distribution | Low | Use proportional allocation |
| Missing edge cases | Medium | Reserve 10% for edge cases |
