# Phase 5: Validation and Testing - v7 Quality Assurance

## Context

- **Plan:** [v7 KB: C#/VB API + User Guide Extraction](plan.md)
- **Date:** 2026-02-01
- **Status:** Pending
- **Effort:** 1h
- **Dependencies:** Phase 4

## Overview

Validate v7 knowledge base extraction quality and ensure backward compatibility with existing query interface. Run integration tests, spot-checks, and performance benchmarks.

## Key Insights

### Validation Layers

1. **Structural validation:** JSON schema, required keys, data types
2. **Content validation:** Expected counts, no empty values
3. **Query validation:** Existing search patterns still work
4. **Cross-reference validation:** Indices match actual content
5. **Performance validation:** Query response times acceptable

### Expected Statistics (v7)

| Metric | Expected Value | Source |
|--------|----------------|--------|
| Python classes | ~1,830 | v6 baseline |
| Python methods | ~6,773 | v6 baseline |
| C#/VB members | ~21,274 | CHM file count |
| C#/VB namespaces | ~10 | FunctionBay.* |
| User guide sections | ~50 | 7 Word + 27 Sphinx |
| Total searchable | ~28,000 | All combined |

## Requirements

1. Validate v7 JSON structure and schema
2. Verify content counts match expectations
3. Test query interface with v7 KB
4. Spot-check C#/VB extraction accuracy
5. Spot-check user guide content
6. Benchmark query performance
7. Generate validation report

## Architecture

### Test Script Structure

```python
# tests/test-v7-knowledge-base-validation.py

class TestV7KnowledgeBase:
    """Validation tests for v7 KB."""

    @pytest.fixture
    def v7_kb(self):
        """Load v7 KB for testing."""
        with open('output/processnet-knowledge-v7.json') as f:
            return json.load(f)

    # Structural tests
    def test_required_keys_present(self, v7_kb): ...
    def test_metadata_complete(self, v7_kb): ...
    def test_python_api_structure(self, v7_kb): ...
    def test_csharp_vb_api_structure(self, v7_kb): ...
    def test_user_guides_structure(self, v7_kb): ...
    def test_unified_index_structure(self, v7_kb): ...

    # Content tests
    def test_python_class_count(self, v7_kb): ...
    def test_python_method_count(self, v7_kb): ...
    def test_csharp_vb_member_count(self, v7_kb): ...
    def test_user_guide_section_count(self, v7_kb): ...
    def test_no_empty_descriptions(self, v7_kb): ...

    # Query tests
    def test_find_method_exact(self, v7_kb): ...
    def test_search_fuzzy(self, v7_kb): ...
    def test_search_csharp_vb(self, v7_kb): ...
    def test_search_guide(self, v7_kb): ...

    # Spot-check tests
    def test_csharp_syntax_present(self, v7_kb): ...
    def test_vb_syntax_present(self, v7_kb): ...
    def test_enum_members_extracted(self, v7_kb): ...
    def test_guide_content_not_empty(self, v7_kb): ...
```

## Implementation Steps

### Step 1: Create validation test file (15 min)

```python
# tests/test-v7-knowledge-base-validation.py
#!/usr/bin/env python3
"""
v7 Knowledge Base Validation Tests

Validates structure, content, and query compatibility.
"""

import json
import pytest
from pathlib import Path

V7_KB_PATH = Path('output/processnet-knowledge-v7.json')


@pytest.fixture(scope="module")
def v7_kb():
    """Load v7 KB once for all tests."""
    if not V7_KB_PATH.exists():
        pytest.skip(f"v7 KB not found: {V7_KB_PATH}")
    with open(V7_KB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Step 2: Implement structural tests (15 min)

```python
class TestStructure:
    """Structural validation tests."""

    def test_required_top_level_keys(self, v7_kb):
        """Verify all required top-level keys present."""
        required = ['metadata', 'python_api', 'csharp_vb_api', 'user_guides', 'unified_index']
        for key in required:
            assert key in v7_kb, f"Missing required key: {key}"

    def test_metadata_has_version(self, v7_kb):
        """Verify metadata contains version."""
        assert v7_kb['metadata']['version'] == 'v7'

    def test_metadata_has_statistics(self, v7_kb):
        """Verify metadata contains statistics."""
        stats = v7_kb['metadata']['statistics']
        assert 'python_classes' in stats
        assert 'python_methods' in stats
        assert 'csharp_vb_members' in stats

    def test_python_api_has_namespaces(self, v7_kb):
        """Verify Python API has namespaces."""
        assert 'namespaces' in v7_kb['python_api']
        assert len(v7_kb['python_api']['namespaces']) > 0

    def test_csharp_vb_api_has_namespaces(self, v7_kb):
        """Verify C#/VB API has namespaces."""
        assert 'namespaces' in v7_kb['csharp_vb_api']
        assert len(v7_kb['csharp_vb_api']['namespaces']) > 0

    def test_user_guides_has_content(self, v7_kb):
        """Verify user guides section has content."""
        guides = v7_kb['user_guides']
        has_word = len(guides.get('word_guides', [])) > 0
        has_sphinx = len(guides.get('sphinx_guides', {}).get('sections', {})) > 0
        assert has_word or has_sphinx, "No user guide content found"
```

### Step 3: Implement content count tests (10 min)

```python
class TestContentCounts:
    """Content count validation tests."""

    def test_python_class_count_reasonable(self, v7_kb):
        """Verify Python class count is reasonable (v6 baseline: ~1830)."""
        count = len(v7_kb['python_api'].get('class_index', {}))
        assert count >= 1500, f"Python class count too low: {count}"
        assert count <= 3000, f"Python class count too high: {count}"

    def test_python_method_count_reasonable(self, v7_kb):
        """Verify Python method count is reasonable (v6 baseline: ~6773)."""
        count = len(v7_kb['python_api'].get('method_index', {}))
        assert count >= 5000, f"Python method count too low: {count}"
        assert count <= 10000, f"Python method count too high: {count}"

    def test_csharp_vb_member_count_reasonable(self, v7_kb):
        """Verify C#/VB member count is reasonable (~21K files)."""
        total = 0
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            total += len(ns_data.get('members', []))
        assert total >= 15000, f"C#/VB member count too low: {total}"
        assert total <= 30000, f"C#/VB member count too high: {total}"

    def test_user_guide_section_count(self, v7_kb):
        """Verify user guide section count (7 Word + 27 Sphinx)."""
        word_count = sum(
            len(g.get('sections', []))
            for g in v7_kb['user_guides'].get('word_guides', [])
        )
        sphinx_count = len(
            v7_kb['user_guides'].get('sphinx_guides', {}).get('sections', {})
        )
        total = word_count + sphinx_count
        assert total >= 20, f"User guide section count too low: {total}"
```

### Step 4: Implement spot-check tests (10 min)

```python
class TestSpotChecks:
    """Spot-check validation for specific content."""

    def test_csharp_syntax_extracted(self, v7_kb):
        """Verify C# syntax is present in at least one member."""
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('syntax_csharp'):
                    assert 'public' in member['syntax_csharp'].lower() or \
                           'private' in member['syntax_csharp'].lower() or \
                           'class' in member['syntax_csharp'].lower() or \
                           'enum' in member['syntax_csharp'].lower()
                    return
        pytest.fail("No C# syntax found in any member")

    def test_vb_syntax_extracted(self, v7_kb):
        """Verify VB syntax is present in at least one member."""
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('syntax_vb'):
                    assert 'Public' in member['syntax_vb'] or \
                           'Private' in member['syntax_vb'] or \
                           'Class' in member['syntax_vb'] or \
                           'Enumeration' in member['syntax_vb']
                    return
        pytest.fail("No VB syntax found in any member")

    def test_enum_has_members(self, v7_kb):
        """Verify at least one enum has member values."""
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('entity_type') == 'enum':
                    if member.get('members'):
                        assert len(member['members']) > 0
                        return
        pytest.fail("No enum with members found")

    def test_guide_has_prose_content(self, v7_kb):
        """Verify guides have actual prose content."""
        for guide in v7_kb['user_guides'].get('word_guides', []):
            for section in guide.get('sections', []):
                if len(section.get('content', '')) > 100:
                    return
        for section in v7_kb['user_guides'].get('sphinx_guides', {}).get('sections', {}).values():
            if len(section.get('content', '')) > 100:
                return
        pytest.fail("No substantial guide content found")
```

### Step 5: Implement query compatibility tests (10 min)

```python
class TestQueryCompatibility:
    """Query interface compatibility tests."""

    def test_unified_method_index_searchable(self, v7_kb):
        """Verify unified method index has searchable entries."""
        methods = v7_kb['unified_index'].get('methods', {})
        assert len(methods) > 100, f"Method index too small: {len(methods)}"

        # Check at least one method has both Python and C#/VB entries
        for name, sources in methods.items():
            if sources.get('python') and sources.get('csharp_vb'):
                return
        # It's OK if no overlap exists, just log warning
        print("Warning: No methods found in both Python and C#/VB APIs")

    def test_class_index_searchable(self, v7_kb):
        """Verify class index has searchable entries."""
        classes = v7_kb['unified_index'].get('classes', {})
        assert len(classes) > 100, f"Class index too small: {len(classes)}"

    def test_backward_compatible_python_structure(self, v7_kb):
        """Verify Python API structure matches v6 for backward compatibility."""
        python_api = v7_kb['python_api']
        # These keys must exist for query interface
        assert 'namespaces' in python_api
        assert 'method_index' in python_api
        assert 'class_index' in python_api

        # Check namespace structure
        for ns_name, ns_data in python_api['namespaces'].items():
            assert 'classes' in ns_data or 'methods' in ns_data or 'files' in ns_data
```

## Validation Report Template

```markdown
# v7 Knowledge Base Validation Report

**Date:** {date}
**KB Path:** output/processnet-knowledge-v7.json
**KB Size:** {size_mb} MB

## Statistics

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Python classes | ~1,830 | {actual} | {pass/fail} |
| Python methods | ~6,773 | {actual} | {pass/fail} |
| C#/VB members | ~21,274 | {actual} | {pass/fail} |
| User guide sections | ~50 | {actual} | {pass/fail} |

## Test Results

- Structural tests: {passed}/{total}
- Content tests: {passed}/{total}
- Spot-check tests: {passed}/{total}
- Query tests: {passed}/{total}

## Issues Found

{list of issues or "None"}

## Recommendations

{recommendations for improvement}
```

## Todo List

- [ ] Create `tests/test-v7-knowledge-base-validation.py`
- [ ] Implement structural validation tests
- [ ] Implement content count tests
- [ ] Implement spot-check tests
- [ ] Implement query compatibility tests
- [ ] Create validation report generator
- [ ] Run full test suite
- [ ] Generate validation report
- [ ] Fix any issues found
- [ ] Re-run validation

## Success Criteria

1. All structural tests pass
2. Content counts within expected ranges
3. C# and VB syntax both present
4. Enum members extracted
5. User guide prose content present
6. Query interface backward compatible
7. Validation report generated

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Missing content | Medium | Medium | Detailed spot-checks |
| Query breaks | Low | High | Backward compat tests |
| Performance regression | Low | Medium | Benchmark queries |

## Related Code

- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v7.json` - Target
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/processnet-query-interface.py` - Query interface
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/tests/` - Test directory
