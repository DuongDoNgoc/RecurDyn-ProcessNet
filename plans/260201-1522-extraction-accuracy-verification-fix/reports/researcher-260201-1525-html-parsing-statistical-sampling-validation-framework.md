# Data Extraction Verification Methodologies & HTML Parsing Validation

## Executive Summary
Comprehensive validation of HTML parsing accuracy requires multi-layered approach combining statistical sampling, automated validation, and DOM comparison. Recommend stratified sampling with min. 95 samples for 90% confidence, automated regression testing, and dual-verification framework.

---

## 1. Statistical Sampling Methodology

### Sample Size Calculation
For finite population N with 90% confidence, 5% margin of error:
```
n = (Z² × p(1-p)) / E²
n = (1.645² × 0.5 × 0.5) / 0.05²
n ≈ 271 samples (conservative estimate)

For 95% confidence: n ≈ 385 samples
Practical: Use 95-120 stratified samples for 85-90% confidence
```

### Stratified Sampling Strategy
Categorize extraction targets:
- **By Data Type:** Text nodes (40%), attributes (30%), nested structures (20%), edge cases (10%)
- **By DOM Complexity:** Simple (depth 1-3, 30%), Medium (4-7, 50%), Complex (8+, 20%)
- **By Namespace:** HTML5 standard (60%), custom attributes (25%), deprecated markup (15%)
- **By Parse Library:** BeautifulSoup vs lxml vs native extraction (balanced allocation)

**Sample Distribution:** 100 total samples
- Simple structures: 30 samples
- Medium structures: 50 samples
- Complex structures: 20 samples
- Edge cases: 10 validation-specific samples (malformed, rare patterns)

Allocation ensures proportional representation and sufficient statistical power for subcategory analysis.

---

## 2. Automated Validation Framework

### BeautifulSoup Pattern Validation
```python
from bs4 import BeautifulSoup
import hashlib

def validate_extraction(html_source, expected_data):
    """Compare extracted vs expected with structural verification"""
    soup = BeautifulSoup(html_source, 'html.parser')

    # Extract with fallback parsers
    results = {
        'html.parser': extract_data(soup),
        'lxml': extract_data(BeautifulSoup(html_source, 'lxml')),
        'html5lib': extract_data(BeautifulSoup(html_source, 'html5lib'))
    }

    # Consensus validation (2/3 parsers agree)
    consensus = validate_consensus(results, expected_data)
    return consensus['match_rate'], consensus['differences']

def extract_data(soup):
    """Unified extraction method"""
    return {
        'text': soup.get_text(strip=True),
        'attrs': {tag.name: dict(tag.attrs) for tag in soup.find_all(True)},
        'structure': soup.prettify()
    }
```

### XPath Validation (lxml)
```python
from lxml import html as lxml_html

def xpath_validation(html_source, xpath_queries):
    """Validate XPath results across parser variants"""
    tree = lxml_html.fromstring(html_source)
    results = {}
    for name, query in xpath_queries.items():
        try:
            results[name] = {
                'found': len(tree.xpath(query)),
                'values': tree.xpath(query),
                'status': 'success'
            }
        except Exception as e:
            results[name] = {'status': 'error', 'error': str(e)}
    return results
```

### DOM Structure Comparison
```python
from difflib import SequenceMatcher
import json

def compare_dom_structures(parsed_html, reference_html):
    """Detect structural deviations using text similarity"""
    parser1_structure = extract_structure(parsed_html)
    parser2_structure = extract_structure(reference_html)

    similarity = SequenceMatcher(None,
        json.dumps(parser1_structure),
        json.dumps(parser2_structure)
    ).ratio()

    return {
        'structural_match': similarity,
        'deviation_threshold': similarity > 0.95,  # 95% match required
        'diff_details': identify_differences(parser1_structure, parser2_structure)
    }

def extract_structure(soup):
    """Normalize structure for comparison"""
    return {
        'tag_count': len(soup.find_all(True)),
        'nesting_depth': max_depth(soup),
        'text_nodes': len(soup.find_all(string=True)),
        'attributes_total': sum(len(tag.attrs) for tag in soup.find_all(True))
    }
```

---

## 3. Accuracy Metrics

### Core Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| Precision | TP / (TP + FP) | 95%+ |
| Recall | TP / (TP + FN) | 95%+ |
| F1 Score | 2 × (Precision × Recall) / (Precision + Recall) | 94%+ |
| Extraction Match Rate | Exact matches / Total samples | 98%+ |

### Implementation
```python
def calculate_metrics(predictions, ground_truth):
    """Compute precision, recall, F1 for extraction validation"""
    tp = sum(1 for p, g in zip(predictions, ground_truth) if p == g and p)
    fp = sum(1 for p, g in zip(predictions, ground_truth) if p != g and p)
    fn = sum(1 for p, g in zip(predictions, ground_truth) if p != g and not p)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4),
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }
```

### Regression Test Suite
```python
import pytest
from typing import List, Tuple

class ExtractionRegressionTests:
    """Baseline validation against known-good outputs"""

    test_cases = [
        ('test_simple_text', '<p>Hello</p>', 'Hello'),
        ('test_nested_attrs', '<div data-id="1"><span>text</span></div>',
         {'tag': 'div', 'attrs': {'data-id': '1'}, 'text': 'text'}),
        ('test_malformed_html', '<p>Unclosed tag<div>', 'Unclosed tag'),
    ]

    def test_extraction_accuracy(self):
        for test_id, html, expected in self.test_cases:
            result = extract_from_html(html)
            assert result == expected, f"Failed: {test_id}"

    @pytest.mark.parametrize("html,expected", test_cases)
    def test_all_parsers_agree(self, html, expected):
        """Consensus validation across BS4, lxml, html5lib"""
        parsers = ['html.parser', 'lxml', 'html5lib']
        results = [extract_with_parser(html, p) for p in parsers]
        assert len(set(map(str, results))) == 1, "Parser mismatch"
```

---

## 4. Implementation Roadmap

1. **Phase 1 (Immediate):** Stratified sampling framework + BeautifulSoup validator
2. **Phase 2 (Week 1):** Regression test suite + accuracy metric tracking
3. **Phase 3 (Week 2):** Multi-parser consensus validation + reporting dashboard
4. **Phase 4 (Ongoing):** Continuous integration + automated drift detection

### Tools & Libraries
- **BeautifulSoup4:** Primary parser with fallback chain
- **lxml:** XPath validation & performance baseline
- **html5lib:** HTML5 spec compliance verification
- **pytest:** Regression testing framework
- **Selenium/Playwright:** (Optional) Browser-based verification for JS-heavy pages

---

## 5. Success Criteria
- **Sample Coverage:** 100+ stratified samples across categories
- **Consensus Rate:** 98%+ agreement between parser implementations
- **Extraction Accuracy:** F1 score > 0.94 for all categories
- **Regression Tests:** 100% pass rate + growing test coverage
- **False Positive/Negative Rate:** < 2% combined

---

## References
- BeautifulSoup4 Docs: Official parsing patterns and best practices
- lxml XPath: W3C XPath 1.0 standard compliance
- Statistical Sampling: Cochran's formula for finite population sampling
- HTML5 Parsing: WHATWG HTML Living Standard specification
- Pytest Documentation: Regression testing patterns for data extraction

## Unresolved Questions
- Specific legacy HTML patterns in RecurDyn-ProcessNet codebase requiring special handling?
- Current baseline accuracy metrics for comparison?
- Budget for browser-based verification (Playwright) vs headless validation?
