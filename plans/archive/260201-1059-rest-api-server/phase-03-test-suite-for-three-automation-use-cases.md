---
title: "Phase 03 - Test Suite for 3 Automation Use Cases"
description: "Write comprehensive test suite covering DOE batch execution, model introspection, and result processing use cases"
status: pending
priority: P1
effort: 2h
tags: [testing, pytest, use-cases, coverage]
---

# Phase 03 - Test Suite for 3 Automation Use Cases

## Context Links

- [Plan Overview](./plan.md)
- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Phase 02: Endpoint Implementation](./phase-02-rest-api-endpoints-implementation.md)
- [Code Standards - Testing](../../../docs/code-standards.md#testing-standards)
- [Project Use Cases](../../../docs/project-overview-pdr.md#target-use-cases)

## Overview

**Priority:** P1 (High)
**Current Status:** Pending
**Estimated Effort:** 2 hours

Write comprehensive test suite for REST API server covering 3 target automation use cases: DOE batch execution, model introspection, and result processing. Use pytest with httpx for async testing.

## Key Insights

1. **Use Case Coverage:** Tests must validate all 3 use cases from project requirements
2. **API Testing:** Use httpx for async HTTP client testing
3. **Real KB Data:** Tests use actual knowledge base (not mocks)
4. **FastAPI TestClient:** Use FastAPI's TestClient for endpoint testing

## Requirements

### Functional Requirements

**FR-03-01: DOE Batch Execution Tests**
- Test parameter manipulation methods: SetParameter, GetParameter, Clone, SaveAs
- Verify exact method lookup returns correct signatures
- Validate search finds parameter-related methods
- Confirm method descriptions include parameter info

**FR-03-02: Model Introspection Tests**
- Test entity enumeration methods: GetAllBodies, GetAllJoints, GetAllForces
- Verify namespace browsing for ProcessNet.Model
- Validate method count matches expected
- Test fuzzy search for entity methods

**FR-03-03: Result Processing Tests**
- Test result loading methods: Load, GetTimeArray, GetEntityData
- Verify code examples for result processing
- Validate method signatures for result queries
- Test namespace filtering for result classes

**FR-03-04: Endpoint Coverage Tests**
- Test all 6 endpoints return valid responses
- Validate HTTP status codes (200, 404, 400, 500)
- Test error handling for invalid inputs
- Verify CORS headers present

### Non-Functional Requirements

**NFR-03-01: Code Coverage**
- Test coverage >80% for API routes
- All use cases have test coverage
- Error paths tested

**NFR-03-02: Test Execution Time**
- Full test suite completes in <2 minutes
- Individual tests run quickly

**NFR-03-03: Test Organization**
- Follow pytest conventions
- Use fixtures for common setup
- Markers for test categories

## Architecture

### Test Structure

```
tests/
├── conftest.py                                 # Shared fixtures
├── test-api-endpoints.py                       # Basic endpoint tests
├── test-use-case-api-coverage.py               # Use case validation tests
└── test-data/
    └── sample-knowledge-base.json              # Minimal KB for testing
```

### Test Categories

```
Test Suite
├── Basic Endpoint Tests
│   ├── Health check
│   ├── Root endpoint
│   └── Statistics
├── Search Endpoint Tests
│   ├── Fuzzy search
│   ├── Empty query validation
│   └── Threshold filtering
├── Method Lookup Tests
│   ├── Exact match
│   ├── Case insensitive
│   ├── Namespace filtering
│   └── Not found (404)
├── Use Case: DOE Batch Execution
│   ├── SetParameter lookup
│   ├── GetParameter lookup
│   ├── Clone method lookup
│   └── SaveAs method lookup
├── Use Case: Model Introspection
│   ├── GetAllBodies lookup
│   ├── GetAllJoints lookup
│   ├── GetAllForces lookup
│   └── Namespace browsing
└── Use Case: Result Processing
    ├── Load method lookup
    ├── GetTimeArray lookup
    ├── GetEntityData lookup
    └── Code examples
```

## Related Code Files

### Files to Create

**tests/conftest.py** (60 lines)
```python
"""Pytest configuration and fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from processnet_api_server import app


@pytest.fixture
def client():
    """
    FastAPI TestClient fixture.

    Provides HTTP client for testing endpoints without server.
    Uses actual ProcessNetKnowledge instance (not mocked).
    """
    return TestClient(app)


@pytest.fixture
def api_base_url():
    """Base URL for API endpoints."""
    return "/api/v1"


@pytest.fixture
def sample_kb_path():
    """Path to sample knowledge base for testing."""
    # Use actual KB if available, otherwise minimal test KB
    kb_path = Path(__file__).parent.parent / "output" / "processnet-knowledge.json"
    if not kb_path.exists():
        kb_path = Path(__file__).parent / "test-data" / "sample-knowledge-base.json"
    return kb_path
```

**tests/test-api-endpoints.py** (200 lines)
```python
"""Basic API endpoint tests."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.use_case("general")
def test_root_endpoint(client: TestClient):
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "endpoints" in data
    assert "docs" in data


@pytest.mark.use_case("general")
def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "kb_loaded" in data


@pytest.mark.use_case("general")
def test_statistics(client: TestClient):
    """Test statistics endpoint."""
    response = client.get("/api/v1/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "namespaces" in data
    assert "methods" in data
    assert "examples" in data
    assert data["namespaces"] > 0


@pytest.mark.use_case("search")
def test_search_with_query(client: TestClient):
    """Test search endpoint with valid query."""
    response = client.get("/api/v1/search?q=CreateArc")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "count" in data
    assert "results" in data
    assert "timing_ms" in data


@pytest.mark.use_case("search")
def test_search_empty_query(client: TestClient):
    """Test search endpoint rejects empty query."""
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 422  # Validation error


@pytest.mark.use_case("namespaces")
def test_list_namespaces(client: TestClient):
    """Test list namespaces endpoint."""
    response = client.get("/api/v1/namespaces")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "namespaces" in data
    assert len(data["namespaces"]) > 0
    # Verify sorted
    assert data["namespaces"] == sorted(data["namespaces"])


@pytest.mark.use_case("examples")
def test_examples_no_filter(client: TestClient):
    """Test examples endpoint without filter."""
    response = client.get("/api/v1/examples")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.use_case("examples")
def test_examples_with_keyword(client: TestClient):
    """Test examples endpoint with keyword filter."""
    response = client.get("/api/v1/examples?keyword=geometry")
    assert response.status_code == 200
    data = response.json()
    assert data["keyword"] == "geometry"
    assert "results" in data
```

**tests/test-use-case-api-coverage.py** (250 lines)
```python
"""Use case validation tests for 3 target automation scenarios."""

import pytest
from fastapi.testclient import TestClient


class TestDOEBatchExecution:
    """Tests for DOE Batch Execution use case."""

    @pytest.mark.use_case("doe")
    @pytest.mark.parametrize("method", ["SetParameter", "GetParameter", "Clone", "SaveAs"])
    def test_parameter_methods_exist(self, client: TestClient, method: str):
        """
        DOE Use Case: Verify parameter manipulation methods exist.

        Workflow: Load model → Clone → SetParameter → SaveAs → Run
        These methods are critical for batch parameter studies.
        """
        response = client.get(f"/api/v1/methods/{method}")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0
        # Verify method signature present
        assert any(r["signature"] for r in data["results"])

    @pytest.mark.use_case("doe")
    def test_search_parameter_methods(self, client: TestClient):
        """DOE Use Case: Search for parameter-related methods."""
        response = client.get("/api/v1/search?q=parameter")
        assert response.status_code == 200
        data = response.json()
        # Should find SetParameter, GetParameter
        result_names = [r["name"].lower() for r in data["results"]]
        assert "setparameter" in result_names or "getparameter" in result_names

    @pytest.mark.use_case("doe")
    def test_clone_method_signature(self, client: TestClient):
        """DOE Use Case: Verify Clone method has correct signature."""
        response = client.get("/api/v1/methods/Clone")
        assert response.status_code == 200
        data = response.json()
        clone_result = next((r for r in data["results"] if r["name"] == "Clone"), None)
        assert clone_result is not None
        assert "signature" in clone_result


class TestModelIntrospection:
    """Tests for Model Introspection use case."""

    @pytest.mark.use_case("model")
    @pytest.mark.parametrize("method", ["GetAllBodies", "GetAllJoints", "GetAllForces"])
    def test_entity_enumeration_methods(self, client: TestClient, method: str):
        """
        Model Introspection Use Case: Verify entity enumeration methods.

        Workflow: Load model → GetAllBodies → GetAllJoints → GetAllForces
        These methods map complete model structure.
        """
        response = client.get(f"/api/v1/methods/{method}")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0
        # Verify namespace is ProcessNet.Model
        assert any("Model" in r["namespace"] for r in data["results"])

    @pytest.mark.use_case("model")
    def test_model_namespace_contents(self, client: TestClient):
        """Model Introspection Use Case: Browse ProcessNet.Model namespace."""
        response = client.get("/api/v1/namespaces/ProcessNet.Model")
        assert response.status_code == 200
        data = response.json()
        assert "methods" in data
        assert len(data["methods"]) > 0
        # Should contain entity enumeration methods
        method_names = [m.lower() for m in data["methods"]]
        assert "getallbodies" in method_names

    @pytest.mark.use_case("model")
    def test_fuzzy_search_entity_methods(self, client: TestClient):
        """Model Introspection Use Case: Fuzzy search for entity methods."""
        # Test with typo
        response = client.get("/api/v1/search?q=GetAllBody")
        assert response.status_code == 200
        data = response.json()
        # Should find GetAllBodies despite typo
        result_names = [r["name"].lower() for r in data["results"]]
        assert "getallbodies" in result_names


class TestResultProcessing:
    """Tests for Result Processing use case."""

    @pytest.mark.use_case("result")
    @pytest.mark.parametrize("method", ["Load", "GetTimeArray", "GetEntityData"])
    def test_result_processing_methods(self, client: TestClient, method: str):
        """
        Result Processing Use Case: Verify result loading methods.

        Workflow: Load result file → GetTimeArray → GetEntityData → Export
        These methods enable offline result analysis.
        """
        response = client.get(f"/api/v1/methods/{method}")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0

    @pytest.mark.use_case("result")
    def test_result_examples(self, client: TestClient):
        """Result Processing Use Case: Find code examples for result processing."""
        response = client.get("/api/v1/examples?keyword=result")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        # At least one example should mention result
        if data["count"] > 0:
            has_result_example = any(
                "result" in r["code"].lower() or "result" in r["namespace"].lower()
                for r in data["results"]
            )
            assert has_result_example

    @pytest.mark.use_case("result")
    def test_load_method_description(self, client: TestClient):
        """Result Processing Use Case: Verify Load method has description."""
        response = client.get("/api/v1/methods/Load")
        assert response.status_code == 200
        data = response.json()
        load_result = next(
            (r for r in data["results"] if r["name"] == "Load"),
            None
        )
        assert load_result is not None
        # Should have description
        assert load_result.get("description") is not None


@pytest.mark.use_case("error-handling")
class test_error_handling:
    """Test error handling across all endpoints."""

    def test_method_not_found(self, client: TestClient):
        """Test 404 for non-existent method."""
        response = client.get("/api/v1/methods/NonExistentMethod12345")
        assert response.status_code == 404

    def test_namespace_not_found(self, client: TestClient):
        """Test 404 for non-existent namespace."""
        response = client.get("/api/v1/namespaces/NonExistent.Namespace")
        assert response.status_code == 404

    def test_invalid_threshold(self, client: TestClient):
        """Test 422 for invalid threshold parameter."""
        response = client.get("/api/v1/search?q=test&threshold=150")
        assert response.status_code == 422

    def test_invalid_limit(self, client: TestClient):
        """Test 422 for invalid limit parameter."""
        response = client.get("/api/v1/search?q=test&limit=0")
        assert response.status_code == 422
```

### Files to Modify

**pytest.ini** (Create in project root if not exists)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --cov=src/api --cov-report=term-missing
markers =
    use_case: Use case validation test (doe, model, result, general, search, namespaces, examples)
    unit: Unit tests
    integration: Integration tests
```

## Implementation Steps

### Step 1: Create Test Configuration

1. Create `tests/conftest.py` with fixtures
2. Create `pytest.ini` with test configuration
3. Verify pytest discovery finds tests

### Step 2: Write Basic Endpoint Tests

1. Create `tests/test-api-endpoints.py`
2. Test root, health, statistics endpoints
3. Test search endpoint
4. Test namespace and examples endpoints

### Step 3: Write Use Case Tests

1. Create `tests/test-use-case-api-coverage.py`
2. Implement DOE batch execution tests
3. Implement model introspection tests
4. Implement result processing tests

### Step 4: Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/api --cov-report=html

# Run specific use case tests
pytest -m use_case="doe"
pytest -m use_case="model"
pytest -m use_case="result"
```

### Step 5: Verify Coverage

1. Generate coverage report
2. Verify >80% code coverage
3. Identify uncovered code
4. Add tests for uncovered paths

## Todo List

- [ ] Create conftest.py with TestClient fixture
- [ ] Create pytest.ini with markers
- [ ] Write basic endpoint tests
- [ ] Write DOE batch execution tests
- [ ] Write model introspection tests
- [ ] Write result processing tests
- [ ] Write error handling tests
- [ ] Run full test suite
- [ ] Verify >80% coverage
- [ ] Fix any failing tests

## Success Criteria

**Functional:**
- [ ] All tests pass (pytest)
- [ ] All 3 use cases have test coverage
- [ ] All 6 endpoints have tests
- [ ] Error cases tested (404, 400)

**Coverage:**
- [ ] >80% code coverage achieved
- [ ] All API routes covered
- [ ] All use cases validated

**Performance:**
- [ ] Test suite completes in <2 minutes
- [ ] Individual tests run quickly

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| KB file missing | High | Use sample KB for tests, clear error |
| Slow tests | Low | Use TestClient (no network) |
| Flaky tests | Medium | Fixtures for consistent state |
| Coverage <80% | Low | Add tests for uncovered paths |

## Next Steps

After completing Phase 03:
1. **Phase 04:** Update documentation with usage examples
2. Run full test suite and verify all pass
3. Generate coverage report

## Related Files

- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Phase 02: Endpoint Implementation](./phase-02-rest-api-endpoints-implementation.md)
- [Phase 04: Documentation](./phase-04-documentation-updates.md)
- [Code Standards - Testing](../../../docs/code-standards.md#testing-standards)
