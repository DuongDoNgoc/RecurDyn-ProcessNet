# Phase 06: Validation and Verification

## Context
- **Parent Plan:** [plan.md](plan.md)
- **Prerequisite:** Phase 05 complete (knowledge base generated)
- **Research:** [researcher-02-api-doc-structure.md](research/researcher-02-api-doc-structure.md) (Section: Validation Methods)

## Overview
**Date:** 2026-01-31
**Description:** Verify extracted content accuracy and validate query interface functionality
**Priority:** P1 (Quality assurance)
**Status:** pending
**Review Status:** Not started

## Key Insights
From research:
- Need count-based validation (±20% tolerance)
- Format validation (signature patterns)
- Content validation (namespaces, interfaces)
- Coverage metrics (minimum vs optimal targets)

## Requirements

### Functional
- Validate extraction accuracy against source HTML
- Test query interface with sample searches
- Verify parameter completeness
- Check return type accuracy
- Confirm namespace classification
- Test code example extraction

### Non-Functional
- Validation time <30 minutes
- Document all findings in report

## Architecture

```
Validation Tests:
  ├── Accuracy Tests
  │   ├── Parse success rate
  │   ├── Method detection rate
  │   ├── Parameter completeness
  │   └── Code example coverage
  ├── Format Tests
  │   ├── Signature contains parentheses
  │   ├── Parameter type format
  │   └── Return type format
  ├── Content Tests
  │   ├── Title extraction
  │   ├── Namespace detection
  │   └── Interface references
  └── Query Interface Tests
      ├── Exact method lookup
      ├── Fuzzy search
      ├── Description search
      └── Example finder
```

## Related Code Files

### Files to Use
- `src/recurdyn-doc-parser.py` - Parser being validated
- `src/processnet-query-interface.py` - Query interface
- `output/processnet-knowledge.json` - Knowledge base to validate
- `tests/fixtures/html-samples/*.html` - Source HTML for comparison

### Files to Create
- `tests/test_extraction_validation.py` - Validation test suite
- `reports/validation-report.md` - Validation findings

## Implementation Steps

1. **Parse success rate validation**
   ```python
   # tests/test_extraction_validation.py
   def test_parse_success_rate():
       """Verify >80% of files parsed successfully."""
       total_files = count_html_files('knowledge/extracted_chm')
       processed_files = get_processed_count('output/processnet-knowledge.json')
       success_rate = (processed_files / total_files) * 100
       assert success_rate >= 80, f"Success rate {success_rate}% < 80%"
   ```

2. **Method detection validation**
   ```python
   def test_method_detection_rate():
       """Verify methods extracted from sample files."""
       # For each test fixture HTML:
       # - Count expected methods (manual or heuristic)
       # - Count extracted methods
       # - Verify >90% detection rate
   ```

3. **Parameter completeness check**
   ```python
   def test_parameter_completeness():
       """Verify >60% of methods have parameter info."""
       methods = load_knowledge_base()['namespaces']['ProcessNet']['standalone_methods']
       methods_with_params = [m for m in methods if m.get('parameters')]
       completeness = (len(methods_with_params) / len(methods)) * 100
       assert completeness >= 60, f"Parameter completeness {completeness}% < 60%"
   ```

4. **Return type extraction check**
   ```python
   def test_return_type_extraction():
       """Verify return types captured for >50% methods."""
       methods = load_knowledge_base()['namespaces']['ProcessNet']['standalone_methods']
       methods_with_returns = [m for m in methods if m.get('returns')]
       rate = (len(methods_with_returns) / len(methods)) * 100
       assert rate >= 50, f"Return type rate {rate}% < 50%"
   ```

5. **Namespace classification validation**
   ```python
   def test_namespace_classification():
       """Verify ProcessNet namespace populated."""
       ns = load_knowledge_base()['namespaces'].get('ProcessNet', {})
       assert len(ns.get('standalone_methods', [])) > 0, "No methods in ProcessNet"
       assert len(ns.get('examples', [])) > 0, "No examples in ProcessNet"
   ```

6. **Code example coverage**
   ```python
   def test_code_example_coverage():
       """Verify >50% of expected examples extracted."""
       # Count code blocks in source HTML
       # Count extracted examples
       # Verify >50% coverage
   ```

7. **Query interface tests**
   ```python
   def test_exact_method_lookup():
       """Verify exact method lookup works."""
       kb = ProcessNetKnowledge('output/processnet-knowledge.json')
       result = kb.find_method('GetAllBodies')
       assert result is not None, "GetAllBodies not found"

   def test_fuzzy_search():
       """Verify fuzzy search returns relevant results."""
       kb = ProcessNetKnowledge('output/processnet-knowledge.json')
       results = kb.search_method_fuzzy('bodi', threshold=70)
       assert len(results) > 0, "Fuzzy search returned no results"

   def test_description_search():
       """Verify description search finds methods."""
       kb = ProcessNetKnowledge('output/processnet-knowledge.json')
       results = kb.search_by_description('geometry')
       assert len(results) > 0, "Description search returned no results"

   def test_example_finder():
       """Verify code example finder works."""
       kb = ProcessNetKnowledge('output/processnet-knowledge.json')
       examples = kb.find_examples('geometry')
       assert len(examples) > 0, "No geometry examples found"
   ```

8. **Manual spot checks**
   - Select 5-10 random methods from knowledge base
   - Compare against source HTML
   - Verify accuracy of:
     - Method name
     - Parameters (name, type)
     - Return type
     - Description

9. **Generate validation report**
   Create `reports/validation-report.md` with:
   - Parse success rate (target: >80%)
   - Method detection rate (target: >90%)
   - Parameter completeness (target: >60%)
   - Return type coverage (target: >50%)
   - Code example coverage (target: >50%)
   - Query interface test results
   - Spot check findings
   - Issues discovered
   - Recommendations for improvements

10. **Run complete test suite**
    ```bash
    cd /mnt/d/Vibecoding/RecurDyn-ProcessNet
    python -m pytest tests/test_extraction_validation.py -v
    python -m pytest tests/test_parser_enhancements.py -v
    python -m pytest tests/ -v  # All tests
    ```

## Todo List

- [ ] Create test_extraction_validation.py
- [ ] Implement parse success rate test
- [ ] Implement method detection test
- [ ] Implement parameter completeness test
- [ ] Implement return type extraction test
- [ ] Implement namespace classification test
- [ ] Implement code example coverage test
- [ ] Implement query interface tests
- [ ] Perform manual spot checks
- [ ] Run complete test suite
- [ ] Generate validation report

## Success Criteria

### Minimum Viable (Must Pass)
- Parse success rate >80%
- Method detection rate >90%
- Parameter completeness >60%
- Query interface returns results for basic searches
- No critical bugs (crashes, data loss)

### Optimal (Stretch Goals)
- Parse success rate >95%
- Method detection rate >98%
- Parameter completeness >90%
- Return type coverage >70%
- Code example coverage >80%
- All query interface tests pass
- Manual spot checks 100% accurate

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low extraction success rate | Medium | High | Fix parser bugs, re-run Phase 05 |
| Query interface returns wrong results | Medium | High | Debug index building, verify data |
| Missing expected methods | Medium | Medium | Check HTML patterns, enhance parser |
| Performance issues | Low | Low | Optimize if needed (not critical) |

## Security Considerations
- Read-only validation
- No external dependencies
- Test data is local documentation

## Next Steps
- If validation passes: Complete project, document final results
- If validation fails: Return to Phase 04 for additional parser enhancements

## Coverage Metrics Reference

From research report:

| Metric | Minimum | Optimal |
|--------|---------|---------|
| Parse success rate | 80% | 95% |
| Method detection | 90% | 98% |
| Parameter completeness | 60% | 90% |
| Return type coverage | 50% | 80% |
| Code example coverage | 50% | 80% |
| Namespace accuracy | N/A | 100% |

## Exit Criteria

Phase complete when:
1. All minimum viable metrics met OR
2. Issues documented with mitigation plan OR
3. Decision made to accept current state
