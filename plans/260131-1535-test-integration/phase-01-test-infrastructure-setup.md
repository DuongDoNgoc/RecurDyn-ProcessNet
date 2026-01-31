---
parent: ./plan.md
dependencies: []
---

# Phase 1: Test Infrastructure Setup

**Date:** 2026-01-31
**Status:** Pending
**Priority:** P0
**Implementation:** Not Started
**Review:** Not Started

## Context

Setup pytest infrastructure to support hybrid verification test suite. Creates fixtures, markers, and test data structure.

## Key Insights

- Workflow doc uses 5 representative file types (index, namespace, class, methods, examples)
- Tests need parametrization for tolerance thresholds (±20% count validation)
- Markers needed: `@pytest.mark.sample`, `@pytest.mark.spot_check`, `@pytest.mark.use_case`

## Requirements

1. Create `tests/conftest.py` with shared fixtures
2. Create `tests/fixtures/sample-html/` directory with mock files
3. Configure pytest.ini with custom markers
4. Setup test data loader utilities

## Architecture

```
tests/
├── conftest.py              # Shared fixtures
│   ├── sample_files         # 5 representative file paths
│   ├── parser_instance      # ProcessNetDocParser fixture
│   ├── knowledge_base       # Loaded knowledge base fixture
│   └── extraction_results   # Cached extraction results
├── fixtures/
│   └── sample-html/
│       ├── index.html       # Overview/TOC structure
│       ├── namespace-geometry.html
│       ├── class-body.html
│       ├── methods-create.html
│       └── examples-tutorial.html
└── pytest.ini               # Markers configuration
```

## Related Code Files

- `src/recurdyn-doc-parser.py:1-50` - Parser class imports
- `src/processnet-query-interface.py:1-50` - Query class imports

## Implementation Steps

1. Create `tests/` directory structure
2. Create `conftest.py` with fixtures:
   - `@pytest.fixture` for sample file paths
   - `@pytest.fixture` for parser instance
   - `@pytest.fixture(scope="session")` for knowledge base
3. Create mock HTML files in `fixtures/sample-html/`
4. Add `pytest.ini` with marker definitions
5. Verify fixtures load correctly

## Todo

- [ ] Create tests directory structure
- [ ] Implement conftest.py fixtures
- [ ] Create 5 mock HTML sample files
- [ ] Configure pytest.ini markers
- [ ] Verify fixture loading

## Success Criteria

- [ ] `pytest --collect-only` shows all fixtures
- [ ] Sample files loadable by parser
- [ ] Markers properly registered (no warnings)

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mock HTML differs from real | Medium | Base on actual RecurDyn doc patterns |
| Fixture scope issues | Low | Use session scope for heavy fixtures |

## Security Considerations

- No external network access in fixtures
- Test files contain no sensitive data

## Next Steps

→ Phase 2: Implement sample extraction tests
