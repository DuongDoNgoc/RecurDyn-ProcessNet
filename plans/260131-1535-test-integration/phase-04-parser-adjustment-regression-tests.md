---
parent: ./plan.md
dependencies: [phase-03-sample-extraction-validation-tests.md]
---

# Phase 3: Parser Adjustment Regression Tests

**Date:** 2026-01-31
**Status:** Pending
**Priority:** P1
**Implementation:** Not Started
**Review:** Not Started

## Context

Implement regression tests for parser adjustments based on Workflow Phase 3. Ensures parser fixes don't break existing functionality.

## Key Insights

From workflow doc section 3.1-3.2:
- Common patterns: count mismatches, signature format diffs, missing content
- Table-based method extraction needed
- Syntax-highlighted code extraction (`<div class="highlight">`)
- Methods in collapsed sections (`<details>`, `<summary>`)

## Requirements

1. Test table-based method extraction
2. Test syntax-highlighted code block extraction
3. Test collapsed section handling
4. Regression tests for each parser fix pattern

## Architecture

```python
# test-parser-adjustments.py structure
class TestTableExtraction:
    def test_table_method_extraction(self, parser)
    def test_table_with_header_skip(self, parser)
    def test_table_missing_columns(self, parser)

class TestHighlightedCodeExtraction:
    def test_div_highlight_extraction(self, parser)
    def test_pre_code_extraction(self, parser)
    def test_syntax_highlighted_spans(self, parser)

class TestCollapsedSections:
    def test_details_summary_extraction(self, parser)
    def test_expandable_method_lists(self, parser)

class TestRegressionPatterns:
    @pytest.mark.parametrize("pattern", KNOWN_PATTERNS)
    def test_pattern_regression(self, pattern, parser)
```

## Related Code Files

- `src/recurdyn-doc-parser.py:200-270` - Table parsing logic
- `src/recurdyn-doc-parser.py:280-350` - Code block extraction
- `ProcessNet_Hybrid_Verification_Workflow.md:325-430` - Parser adjustment patterns

## Implementation Steps

1. Create `tests/test-parser-adjustments.py`
2. Add table extraction test fixtures
3. Implement table-based method tests
4. Add highlight div test fixtures
5. Implement code block extraction tests
6. Add collapsed section test fixtures
7. Implement regression pattern tests

## Test Cases (from workflow)

| Pattern | Test Input | Expected Output |
|---------|------------|-----------------|
| Table methods | `<table class="methods"><tr><td>Method()</td>...` | Method object extracted |
| Highlight code | `<div class="highlight"><pre>code</pre></div>` | CodeExample extracted |
| Collapsed section | `<details><summary>Methods</summary>...` | Methods extracted |
| Missing params | `CreateArc(center, radius)` vs full signature | Partial extraction OK |

## Fixture HTML Patterns

```html
<!-- Table-based method doc -->
<table class="methods">
  <tr><th>Method</th><th>Description</th></tr>
  <tr><td>CreateArc()</td><td>Creates arc</td></tr>
</table>

<!-- Syntax-highlighted code -->
<div class="highlight-python">
  <pre><span class="n">app</span> = ProcessNet.Application()</pre>
</div>

<!-- Collapsed section -->
<details>
  <summary>Available Methods</summary>
  <dl><dt>Method()</dt><dd>Description</dd></dl>
</details>
```

## Todo

- [ ] Create test-parser-adjustments.py
- [ ] Add table extraction fixtures
- [ ] Implement table method tests
- [ ] Add highlight code fixtures
- [ ] Implement code block tests
- [ ] Add collapsed section fixtures
- [ ] Implement regression pattern tests

## Success Criteria

- [ ] Table-based methods extracted correctly
- [ ] `<div class="highlight">` code blocks captured
- [ ] Collapsed sections don't break parsing
- [ ] All regression patterns pass

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unknown HTML patterns | High | Add tests as patterns discovered |
| Parser changes break tests | Medium | Keep fixtures minimal |

## Security Considerations

None - test HTML fixtures only

## Next Steps

→ Phase 4: Validation metrics and spot-check tests
