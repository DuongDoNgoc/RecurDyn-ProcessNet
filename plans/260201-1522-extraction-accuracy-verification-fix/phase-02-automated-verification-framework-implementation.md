---
phase: 02
title: "Automated Verification Framework Implementation"
status: pending
effort: 1h
depends_on: [phase-01]
---

# Phase 02: Automated Verification Framework Implementation

## Context

- **Plan**: [plan.md](./plan.md)
- **Sample Manifest**: `verification/sample-manifest.json`
- **Parser Source**: `src/recurdyn-doc-parser.py`

## Overview

Build automated validators using multi-parser consensus (BeautifulSoup + lxml) to compare extracted data against HTML ground truth.

## Requirements

1. Multi-parser consensus validation (2/3 parsers agree)
2. Comparison scripts: extracted JSON vs HTML source
3. Accuracy metrics: precision, recall, F1 score
4. Verification report template

## Implementation Steps

### Step 1: Create Verification Module

File: `tests/helpers/extraction-verification-validator.py`

```python
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json

@dataclass
class VerificationResult:
    sample_id: int
    file_path: str
    expected_methods: int
    extracted_methods: int
    expected_properties: int
    extracted_properties: int
    precision: float
    recall: float
    f1_score: float
    mismatches: List[str]

class ExtractionValidator:
    def __init__(self, knowledge_base_path: str):
        with open(knowledge_base_path) as f:
            self.kb = json.load(f)

    def validate_sample(self, html_path: str, sample_id: int) -> VerificationResult:
        """Compare extracted data against HTML source."""
        # Multi-parser extraction
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()

        parsers = {
            'html.parser': BeautifulSoup(html, 'html.parser'),
            'lxml': BeautifulSoup(html, 'lxml')
        }

        # Extract ground truth from HTML
        ground_truth = self._extract_ground_truth(parsers['lxml'])

        # Get extracted data from knowledge base
        extracted = self._get_extracted_data(html_path)

        # Calculate metrics
        return self._calculate_metrics(sample_id, html_path, ground_truth, extracted)

    def _extract_ground_truth(self, soup) -> Dict:
        """Extract expected elements from HTML."""
        methods = soup.find_all('dl', class_=lambda x: x and 'method' in str(x))
        properties = soup.find_all('dl', class_=lambda x: x and 'property' in str(x))
        classes = soup.find_all('dl', class_=lambda x: x and 'class' in str(x))
        return {
            'methods': len(methods),
            'properties': len(properties),
            'classes': len(classes),
            'method_names': [self._extract_name(m) for m in methods],
            'property_names': [self._extract_name(p) for p in properties]
        }

    def _calculate_metrics(self, sample_id, path, truth, extracted) -> VerificationResult:
        tp = len(set(truth['method_names']) & set(extracted.get('method_names', [])))
        fp = len(set(extracted.get('method_names', [])) - set(truth['method_names']))
        fn = len(set(truth['method_names']) - set(extracted.get('method_names', [])))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return VerificationResult(
            sample_id=sample_id,
            file_path=path,
            expected_methods=truth['methods'],
            extracted_methods=extracted.get('methods', 0),
            expected_properties=truth['properties'],
            extracted_properties=extracted.get('properties', 0),
            precision=precision,
            recall=recall,
            f1_score=f1,
            mismatches=[]
        )
```

### Step 2: Create Accuracy Metrics Calculator

File: `tests/helpers/accuracy-metrics-calculator.py`

```python
def calculate_aggregate_metrics(results: List[VerificationResult]) -> Dict:
    """Calculate aggregate metrics across all samples."""
    total_precision = sum(r.precision for r in results) / len(results)
    total_recall = sum(r.recall for r in results) / len(results)
    total_f1 = sum(r.f1_score for r in results) / len(results)

    return {
        'total_samples': len(results),
        'avg_precision': round(total_precision, 4),
        'avg_recall': round(total_recall, 4),
        'avg_f1': round(total_f1, 4),
        'samples_passing': sum(1 for r in results if r.f1_score >= 0.90),
        'pass_rate': sum(1 for r in results if r.f1_score >= 0.90) / len(results)
    }
```

### Step 3: Create Report Template

File: `verification/report-template.md`

```markdown
# Extraction Verification Report

**Date:** {{date}}
**Samples:** {{total_samples}}
**Pass Rate:** {{pass_rate}}%

## Aggregate Metrics
| Metric | Value | Target |
|--------|-------|--------|
| Precision | {{precision}} | 95%+ |
| Recall | {{recall}} | 95%+ |
| F1 Score | {{f1}} | 94%+ |

## Category Breakdown
{{category_table}}

## Failed Samples
{{failed_samples}}
```

## Success Criteria

- [ ] ExtractionValidator class implemented
- [ ] Multi-parser consensus working
- [ ] Metrics calculator tested
- [ ] Report template created
- [ ] pytest integration added

## Output Artifacts

- `tests/helpers/extraction-verification-validator.py`
- `tests/helpers/accuracy-metrics-calculator.py`
- `verification/report-template.md`
