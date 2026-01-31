---
parent: ./plan.md
dependencies: [phase-04-parser-adjustment-regression-tests.md, phase-02-mcp-playwright-browser-verification.md]
---

# Phase 4: Spot-Check Validation and Metrics Tests

**Date:** 2026-01-31
**Status:** Pending
**Priority:** P1
**Implementation:** Not Started
**Review:** Not Started

## Context

Implement spot-check validation and metrics tests based on Workflow Phases 5-6. Validates full extraction results and use case coverage.

## Key Insights

From workflow doc:
- Random sampling: 10 files from extraction results
- Stratified sampling: one file per namespace
- Quick checks: title exists, method count ±20%, one signature matches
- Use case validation: DOE, Model introspection, Result processing
- Success metrics: 98% success rate, 90%+ accuracy

## Requirements

1. Random file sampling for spot-checks
2. Stratified namespace sampling
3. Use case method coverage tests
4. Success rate threshold validation
5. Accuracy metric assertions

## Architecture

```python
# test-spot-checks.py structure
class TestRandomSpotCheck:
    def test_random_sample_selection(self, knowledge_base)
    def test_title_exists_in_json(self, random_sample)
    def test_method_count_reasonable(self, random_sample)
    def test_signature_matches_source(self, random_sample)

class TestStratifiedSampling:
    def test_one_file_per_namespace(self, knowledge_base)
    def test_namespace_coverage(self, knowledge_base)

# test-use-case-coverage.py structure
class TestDOEUseCaseMethods:
    """UC-1: DOE Batch Execution"""
    def test_model_load_method_exists(self, kb)
    def test_model_clone_method_exists(self, kb)
    def test_set_parameter_method_exists(self, kb)
    def test_run_method_exists(self, kb)

class TestModelIntrospectionMethods:
    """UC-2: Model Introspection"""
    def test_get_all_bodies_method_exists(self, kb)
    def test_get_all_joints_method_exists(self, kb)
    def test_get_entity_by_id_method_exists(self, kb)

class TestResultProcessingMethods:
    """UC-3: Result Post-Processing"""
    def test_result_load_method_exists(self, kb)
    def test_get_time_array_method_exists(self, kb)
    def test_export_method_exists(self, kb)

class TestSuccessMetrics:
    def test_parsing_success_rate_above_threshold(self, extraction_stats)
    def test_method_extraction_accuracy(self, validation_results)
    def test_example_extraction_accuracy(self, validation_results)
```

## Related Code Files

- `src/processnet-query-interface.py:100-150` - `find_method()` implementation
- `src/processnet-query-interface.py:200-250` - `list_namespace_contents()`
- `ProcessNet_Hybrid_Verification_Workflow.md:490-590` - Spot-check validation
- `docs/project-overview-pdr.md:200-270` - Use case definitions

## Implementation Steps

1. Create `tests/test-spot-checks.py`
2. Implement random sampling logic
3. Add spot-check assertion tests
4. Create `tests/test-use-case-coverage.py`
5. Implement UC-1 (DOE) method tests
6. Implement UC-2 (Model) method tests
7. Implement UC-3 (Result) method tests
8. Add success metrics threshold tests

## Use Case Method Requirements

| Use Case | Required Methods | Source |
|----------|------------------|--------|
| UC-1: DOE | Load, Clone, SetParameter, Run, SaveAs | PDR:200-220 |
| UC-2: Model | GetAllBodies, GetAllJoints, GetEntityByID, GetID, GetType | PDR:230-245 |
| UC-3: Result | Result.Load, GetTimeArray, GetEntityData, Export | PDR:250-265 |

## Success Metrics (from workflow)

| Metric | Threshold | Test |
|--------|-----------|------|
| Parsing success rate | ≥98% | `test_parsing_success_rate_above_threshold` |
| Method extraction accuracy | ≥90% | `test_method_extraction_accuracy` |
| Example extraction accuracy | ≥85% | `test_example_extraction_accuracy` |
| Spot-check pass rate | ≥85% | `test_spot_check_pass_rate` |
| Use case coverage | 100% | `test_all_use_case_methods_found` |

## Todo

- [ ] Create test-spot-checks.py
- [ ] Implement random sampling fixture
- [ ] Add stratified sampling tests
- [ ] Create test-use-case-coverage.py
- [ ] Implement UC-1 method tests
- [ ] Implement UC-2 method tests
- [ ] Implement UC-3 method tests
- [ ] Add success metrics tests

## Success Criteria

- [ ] Random spot-check selects 10 diverse files
- [ ] Stratified sampling covers all namespaces
- [ ] All UC-1 required methods found
- [ ] All UC-2 required methods found
- [ ] All UC-3 required methods found
- [ ] Success rate ≥98%
- [ ] Accuracy ≥90%

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Methods renamed in docs | High | Use fuzzy matching fallback |
| Thresholds too strict | Medium | Make configurable |
| Missing namespaces | Medium | Log warnings, don't fail |

## Security Considerations

None - validation tests only

## Next Steps

→ Update main plan with test integration references
