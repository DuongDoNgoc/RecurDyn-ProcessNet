---
parent: ./plan.md
dependencies: [phase-01-test-infrastructure-setup.md, phase-02-mcp-playwright-browser-verification.md]
---

# Phase 2: Sample Extraction Validation Tests

**Date:** 2026-01-31
**Status:** Pending
**Priority:** P0
**Implementation:** Not Started
**Review:** Not Started

## Context

Implement tests for sample file extraction based on Workflow Phase 1-2. Validates extraction accuracy before full processing.

## Key Insights

From workflow doc:
- 5 file types: index, namespace, class, methods, examples
- Verification checks: title, namespace, method count, signature format
- Tolerance: ±20% for count validation
- Must verify at least one signature exactly matches

## Requirements

1. Test title extraction accuracy
2. Test namespace detection
3. Test method count within tolerance
4. Test signature format correctness
5. Test example code block extraction

## Architecture

```python
# test-sample-extraction.py structure
class TestSampleExtraction:
    @pytest.mark.sample
    @pytest.mark.parametrize("file_type", ["index", "namespace", "class", "methods", "examples"])
    def test_file_extraction_succeeds(self, file_type, parser)

    def test_title_extraction_accuracy(self, sample_results)
    def test_namespace_detection(self, sample_results)
    def test_method_count_within_tolerance(self, sample_results)
    def test_signature_format_correct(self, sample_results)
    def test_example_extraction(self, sample_results)
```

## Related Code Files

- `src/recurdyn-doc-parser.py:60-100` - `parse_html_file()` method
- `src/recurdyn-doc-parser.py:150-200` - Method extraction logic
- `ProcessNet_Hybrid_Verification_Workflow.md:60-120` - Sample extraction test script

## Implementation Steps

1. Create `tests/test-sample-extraction.py`
2. Implement parametrized file type tests
3. Add title/namespace extraction assertions
4. Add method count tolerance validation (±20%)
5. Add signature format verification
6. Add example block count verification

## Test Cases (from workflow)

| Test | Input | Expected | Tolerance |
|------|-------|----------|-----------|
| Title extraction | index.html | "ProcessNet API Reference" | Exact |
| Namespace detection | class_Body.html | "ProcessNet.Model" | Exact |
| Method count | class_Body.html | 15 methods | ±3 (20%) |
| Signature format | any | Contains `()` | Exact pattern |
| Example count | examples.html | ≥2 code blocks | Minimum |

## Todo

- [ ] Create test-sample-extraction.py
- [ ] Implement 5 file type parametrized tests
- [ ] Add title extraction test
- [ ] Add namespace detection test
- [ ] Add method count tolerance test
- [ ] Add signature format test
- [ ] Add example extraction test

## Success Criteria

- [ ] All 5 file types parse successfully
- [ ] Title extraction matches expected
- [ ] Method counts within ±20% tolerance
- [ ] At least one signature exactly matches
- [ ] Example count ≥ expected minimum

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mock data unrealistic | High | Base on actual doc structure |
| Tolerance too strict | Medium | Make configurable via conftest |

## Security Considerations

None - test files only

## Next Steps

→ Phase 3: Parser adjustment regression tests
