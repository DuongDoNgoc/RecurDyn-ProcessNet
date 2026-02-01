#!/usr/bin/env python3
"""
Test Suite for ProcessNet API Automation Use Cases

Tests the REST API server against 3 key automation workflows:
1. DOE Batch Execution - Parameter manipulation methods
2. Model Introspection - Entity enumeration methods
3. Result Processing - Result loading and data extraction methods
"""

"""
Test Suite for ProcessNet API Automation Use Cases

Tests the REST API server against 3 key automation workflows:
1. DOE Batch Execution - Parameter manipulation methods
2. Model Introspection - Entity enumeration methods
3. Result Processing - Result loading and data extraction methods
"""

import json
import pytest
import sys
from pathlib import Path
import importlib.util

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Load API server module using importlib (handles kebab-case filenames)
spec_api = importlib.util.spec_from_file_location(
    "processnet_api_server",
    Path(__file__).parent.parent / "src" / "processnet-api-server.py"
)
api_module = importlib.util.module_from_spec(spec_api)
spec_api.loader.exec_module(api_module)

create_app = api_module.create_app
APIConfig = api_module.APIConfig


# ============================================================================
# Test Configuration
# ============================================================================

API_BASE_URL = "http://testserver/api"
KB_PATH = "output/processnet-knowledge-v5.json"


@pytest.fixture(scope="module")
def kb_exists():
    """Check if knowledge base file exists."""
    kb_file = Path(KB_PATH)
    if not kb_file.exists():
        pytest.skip(f"Knowledge base not found: {KB_PATH}")
    return True


@pytest.fixture
def app(kb_exists):
    """Create FastAPI test application."""
    return create_app(KB_PATH)


@pytest.fixture
def client(app):
    """Create HTTP test client (synchronous)."""
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client


# ============================================================================
# Use Case 1: DOE Batch Execution
# ============================================================================

class TestDOEBatchExecution:
    """Test DOE (Design of Experiments) batch execution workflow.

    Workflow:
    1. Load base model
    2. Clone model for each variation
    3. Set parameters (mass, stiffness, etc.)
    4. Save each variant
    5. Run simulation

    Note: Actual method names in ProcessNet may differ from these generic names.
    Tests verify API functionality and availability of related methods.
    """

    def test_search_save_methods(self, client):
        """Test finding Save-related methods for DOE workflow."""
        response = client.get("/api/search?q=save&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Save methods not found"
        # Verify we have save-related methods
        assert any("save" in r["name"].lower() for r in data["results"])

    def test_search_model_methods(self, client):
        """Test finding Model-related methods."""
        response = client.get("/api/search?q=model&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Model methods not found"

    def test_search_parameter_methods(self, client):
        """Test finding parameter-related methods."""
        response = client.get("/api/search?q=parameter&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Parameter methods not found"

    def test_doe_workflow_methods_exist(self, client):
        """Test that DOE-related methods can be found via search."""
        required_searches = ["save", "model", "parameter"]
        found_count = 0

        for search_term in required_searches:
            response = client.get(f"/api/search?q={search_term}&limit=10")
            assert response.status_code == 200
            data = response.json()
            if data["count"] > 0:
                found_count += 1

        # At least 2 of 3 search categories should find results
        assert found_count >= 2, f"Too few DOE-related methods found: {found_count}/3"


# ============================================================================
# Use Case 2: Model Introspection
# ============================================================================

class TestModelIntrospection:
    """Test model introspection workflow.

    Workflow:
    1. Load existing model
    2. Query all entities by type
    3. Map entity IDs and properties
    4. Export entity structure

    Note: Tests verify API can find entity-related methods.
    """

    def test_search_body_methods(self, client):
        """Test finding Body-related methods."""
        response = client.get("/api/search?q=body&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Body methods not found"

    def test_search_joint_methods(self, client):
        """Test finding Joint-related methods."""
        response = client.get("/api/search?q=joint&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Joint methods not found"

    def test_search_force_methods(self, client):
        """Test finding Force-related methods."""
        response = client.get("/api/search?q=force&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Force methods not found"

    def test_search_getall_methods(self, client):
        """Test finding GetAll* style methods."""
        response = client.get("/api/search?q=getall&limit=30")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "GetAll methods not found"

    def test_introspection_methods_exist(self, client):
        """Test that introspection-related methods can be found."""
        required_searches = ["body", "joint", "force", "entity"]
        found_count = 0

        for search_term in required_searches:
            response = client.get(f"/api/search?q={search_term}&limit=10")
            assert response.status_code == 200
            data = response.json()
            if data["count"] > 0:
                found_count += 1

        # At least 3 of 4 entity types should be found
        assert found_count >= 3, f"Too few entity types found: {found_count}/4"


# ============================================================================
# Use Case 3: Result Processing
# ============================================================================

class TestResultProcessing:
    """Test result post-processing workflow.

    Workflow:
    1. Load simulation result file
    2. Extract time arrays
    3. Extract entity data (displacement, force, velocity)
    4. Process and analyze data
    5. Export to external format

    Note: Tests verify API can find result processing methods.
    """

    def test_search_time_methods(self, client):
        """Test finding time-related methods."""
        response = client.get("/api/search?q=time&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Time methods not found"

    def test_search_data_methods(self, client):
        """Test finding data extraction methods."""
        response = client.get("/api/search?q=data&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Data methods not found"

    def test_search_export_methods(self, client):
        """Test finding export methods."""
        response = client.get("/api/search?q=export&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Export methods not found"

    def test_search_result_methods(self, client):
        """Test finding result-related methods."""
        response = client.get("/api/search?q=result&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0, "Result methods not found"

    def test_result_processing_methods_exist(self, client):
        """Test that result processing methods can be found."""
        required_searches = ["time", "data", "export", "plot"]
        found_count = 0

        for search_term in required_searches:
            response = client.get(f"/api/search?q={search_term}&limit=10")
            assert response.status_code == 200
            data = response.json()
            if data["count"] > 0:
                found_count += 1

        # At least 3 of 4 result processing categories should be found
        assert found_count >= 3, f"Too few result processing methods found: {found_count}/4"


# ============================================================================
# API Health and Statistics Tests
# ============================================================================

class TestAPIHealth:
    """Test API health endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "kb_loaded" in data

    def test_statistics(self, client):
        """Test statistics endpoint."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "namespaces" in data
        assert "methods" in data
        assert data["namespaces"] > 0

    def test_namespaces_list(self, client):
        """Test namespaces list endpoint."""
        response = client.get("/api/namespaces")
        assert response.status_code == 200
        data = response.json()
        assert "namespaces" in data
        assert data["count"] > 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegrationWorkflows:
    """Integration tests for complete workflows."""

    def test_full_doe_workflow_simulation(self, client):
        """Simulate complete DOE workflow using API."""
        # Search for model-related methods
        model_resp = client.get("/api/search?q=model&limit=20")
        assert model_resp.status_code == 200
        assert model_resp.json()["count"] > 0

        # Search for save methods
        save_resp = client.get("/api/search?q=save&limit=10")
        assert save_resp.status_code == 200

        # Search for parameter methods
        param_resp = client.get("/api/search?q=parameter&limit=10")
        assert param_resp.status_code == 200

    def test_full_introspection_workflow_simulation(self, client):
        """Simulate complete introspection workflow."""
        # Find body methods
        body_resp = client.get("/api/search?q=body&limit=20")
        assert body_resp.status_code == 200
        assert body_resp.json()["count"] > 0

        # Find joint methods
        joint_resp = client.get("/api/search?q=joint&limit=20")
        assert joint_resp.status_code == 200

    def test_full_result_workflow_simulation(self, client):
        """Simulate complete result processing workflow."""
        # Find time methods
        time_resp = client.get("/api/search?q=time&limit=20")
        assert time_resp.status_code == 200
        assert time_resp.json()["count"] > 0

        # Find data methods
        data_resp = client.get("/api/search?q=data&limit=20")
        assert data_resp.status_code == 200
        assert data_resp.json()["count"] > 0


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test API error handling."""

    def test_search_with_no_results(self, client):
        """Test search for non-existent term returns empty or minimal results."""
        response = client.get("/api/search?q=NonExistentMethodXYZ123&limit=10")
        assert response.status_code == 200
        data = response.json()
        # Fuzzy search may find some matches, so we just verify the response structure
        assert "count" in data
        assert "results" in data
        # Count should be reasonable (< 20 since we're searching for something obscure)
        assert data["count"] < 20

    def test_not_found_namespace(self, client):
        """Test response for non-existent namespace."""
        response = client.get("/api/namespaces/NonExistentNamespaceXYZ")
        # API returns 200 with empty namespace data
        assert response.status_code == 200
        data = response.json()
        # Non-existent namespace should have empty classes and methods
        assert data.get("classes") == []
        assert data.get("methods") == []
        assert data.get("examples_count") == 0

    def test_invalid_threshold(self, client):
        """Test search with invalid threshold (FastAPI validation)."""
        response = client.get("/api/search?q=test&threshold=150")
        # FastAPI validates ge=0 le=100, so should get 422
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
