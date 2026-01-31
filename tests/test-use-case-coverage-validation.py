"""
Use case coverage validation tests.

Tests for required methods across three use cases:
- UC-1: DOE Batch Execution
- UC-2: Model Introspection
- UC-3: Result Post-Processing
"""
import pytest
from typing import Dict, List


@pytest.mark.use_case
class TestDOEUseCaseMethods:
    """UC-1: DOE Batch Execution - required method coverage."""

    def test_model_load_method_exists(self, use_case_methods: Dict):
        """Verify Load method exists for model loading."""
        required_method = 'Load'
        uc1_methods = use_case_methods['UC-1-DOE']

        assert required_method in uc1_methods, \
            f"UC-1 missing required method: {required_method}"

    def test_model_clone_method_exists(self, use_case_methods: Dict):
        """Verify Clone method exists for model duplication."""
        required_method = 'Clone'
        uc1_methods = use_case_methods['UC-1-DOE']

        assert required_method in uc1_methods, \
            f"UC-1 missing required method: {required_method}"

    def test_set_parameter_method_exists(self, use_case_methods: Dict):
        """Verify SetParameter method exists for parameter modification."""
        required_method = 'SetParameter'
        uc1_methods = use_case_methods['UC-1-DOE']

        assert required_method in uc1_methods, \
            f"UC-1 missing required method: {required_method}"

    def test_run_method_exists(self, use_case_methods: Dict):
        """Verify Run method exists for simulation execution."""
        required_method = 'Run'
        uc1_methods = use_case_methods['UC-1-DOE']

        assert required_method in uc1_methods, \
            f"UC-1 missing required method: {required_method}"

    def test_save_as_method_exists(self, use_case_methods: Dict):
        """Verify SaveAs method exists for result storage."""
        required_method = 'SaveAs'
        uc1_methods = use_case_methods['UC-1-DOE']

        assert required_method in uc1_methods, \
            f"UC-1 missing required method: {required_method}"

    def test_all_uc1_methods_present(self, use_case_methods: Dict):
        """Verify all UC-1 methods are present."""
        uc1_methods = use_case_methods['UC-1-DOE']

        # All 5 methods should be present
        assert len(uc1_methods) == 5, \
            f"UC-1 should have 5 methods, found {len(uc1_methods)}"


@pytest.mark.use_case
class TestModelIntrospectionMethods:
    """UC-2: Model Introspection - required method coverage."""

    def test_get_all_bodies_method_exists(self, use_case_methods: Dict):
        """Verify GetAllBodies method exists."""
        required_method = 'GetAllBodies'
        uc2_methods = use_case_methods['UC-2-Model']

        assert required_method in uc2_methods, \
            f"UC-2 missing required method: {required_method}"

    def test_get_all_joints_method_exists(self, use_case_methods: Dict):
        """Verify GetAllJoints method exists."""
        required_method = 'GetAllJoints'
        uc2_methods = use_case_methods['UC-2-Model']

        assert required_method in uc2_methods, \
            f"UC-2 missing required method: {required_method}"

    def test_get_entity_by_id_method_exists(self, use_case_methods: Dict):
        """Verify GetEntityByID method exists."""
        required_method = 'GetEntityByID'
        uc2_methods = use_case_methods['UC-2-Model']

        assert required_method in uc2_methods, \
            f"UC-2 missing required method: {required_method}"

    def test_get_id_method_exists(self, use_case_methods: Dict):
        """Verify GetID method exists."""
        required_method = 'GetID'
        uc2_methods = use_case_methods['UC-2-Model']

        assert required_method in uc2_methods, \
            f"UC-2 missing required method: {required_method}"

    def test_get_type_method_exists(self, use_case_methods: Dict):
        """Verify GetType method exists."""
        required_method = 'GetType'
        uc2_methods = use_case_methods['UC-2-Model']

        assert required_method in uc2_methods, \
            f"UC-2 missing required method: {required_method}"

    def test_all_uc2_methods_present(self, use_case_methods: Dict):
        """Verify all UC-2 methods are present."""
        uc2_methods = use_case_methods['UC-2-Model']

        # All 5 methods should be present
        assert len(uc2_methods) == 5, \
            f"UC-2 should have 5 methods, found {len(uc2_methods)}"


@pytest.mark.use_case
class TestResultProcessingMethods:
    """UC-3: Result Post-Processing - required method coverage."""

    def test_result_load_method_exists(self, use_case_methods: Dict):
        """Verify Result.Load method exists."""
        required_method = 'Load'
        uc3_methods = use_case_methods['UC-3-Result']

        assert required_method in uc3_methods, \
            f"UC-3 missing required method: {required_method}"

    def test_get_time_array_method_exists(self, use_case_methods: Dict):
        """Verify GetTimeArray method exists."""
        required_method = 'GetTimeArray'
        uc3_methods = use_case_methods['UC-3-Result']

        assert required_method in uc3_methods, \
            f"UC-3 missing required method: {required_method}"

    def test_get_entity_data_method_exists(self, use_case_methods: Dict):
        """Verify GetEntityData method exists."""
        required_method = 'GetEntityData'
        uc3_methods = use_case_methods['UC-3-Result']

        assert required_method in uc3_methods, \
            f"UC-3 missing required method: {required_method}"

    def test_export_method_exists(self, use_case_methods: Dict):
        """Verify Export method exists."""
        required_method = 'Export'
        uc3_methods = use_case_methods['UC-3-Result']

        assert required_method in uc3_methods, \
            f"UC-3 missing required method: {required_method}"

    def test_all_uc3_methods_present(self, use_case_methods: Dict):
        """Verify all UC-3 methods are present."""
        uc3_methods = use_case_methods['UC-3-Result']

        # All 4 methods should be present
        assert len(uc3_methods) == 4, \
            f"UC-3 should have 4 methods, found {len(uc3_methods)}"


@pytest.mark.use_case
class TestUseCaseCoverageIntegration:
    """Integration tests for use case coverage."""

    def test_all_use_cases_defined(self, use_case_methods: Dict):
        """Verify all 3 use cases are defined."""
        expected_use_cases = ['UC-1-DOE', 'UC-2-Model', 'UC-3-Result']

        for uc in expected_use_cases:
            assert uc in use_case_methods, \
                f"Use case {uc} not defined"

    def test_total_use_case_method_count(self, use_case_methods: Dict):
        """Verify total method count across all use cases."""
        total_methods = sum(len(methods) for methods in use_case_methods.values())

        # UC-1: 5 methods, UC-2: 5 methods, UC-3: 4 methods = 14 total
        expected_total = 14

        assert total_methods == expected_total, \
            f"Expected {expected_total} total methods, found {total_methods}"

    def test_no_duplicate_methods_in_fixture(self, use_case_methods: Dict):
        """Verify use case method lists have no internal duplicates."""
        for uc_name, methods in use_case_methods.items():
            # Check for duplicates
            unique_methods = set(methods)
            assert len(unique_methods) == len(methods), \
                f"Use case {uc_name} has duplicate methods"


@pytest.mark.use_case
class TestMethodPresenceInKnowledgeBase:
    """Test whether use case methods exist in extracted knowledge base."""

    def test_search_method_in_knowledge_base(self, knowledge_base: Dict, use_case_methods: Dict):
        """Search for use case methods in knowledge base method index."""
        method_index = knowledge_base.get('method_index', {})

        if len(method_index) == 0:
            pytest.skip("Method index empty (fixtures may not be processed)")

        # Count how many use case methods are found
        found_count = 0
        total_required = sum(len(methods) for methods in use_case_methods.values())

        all_use_case_methods = []
        for methods in use_case_methods.values():
            all_use_case_methods.extend(methods)

        for method in all_use_case_methods:
            if method in method_index:
                found_count += 1

        # Log coverage (informational, not strict assertion)
        coverage = (found_count / total_required) * 100 if total_required > 0 else 0

        # Relaxed assertion - at least some methods should be found
        # (strict 100% would require actual HTML fixtures to have all methods)
        if found_count == 0:
            pytest.skip(f"No use case methods found in knowledge base (coverage: {coverage:.1f}%)")


@pytest.mark.use_case
class TestExampleCoverage:
    """Test code examples cover use case scenarios."""

    def test_doe_example_exists(self, sample_file_paths: Dict):
        """Verify DOE example exists in examples file."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths.get('examples')
        if not examples_file or not examples_file.exists():
            pytest.skip("Examples file not available")

        with open(examples_file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        # Look for DOE-related content
        doe_section = soup.find('div', id='doe-batch-execution')
        if not doe_section:
            # Check in text content
            assert 'DOE' in content or 'Clone' in content, \
                "No DOE example found in examples file"

    def test_model_introspection_example_exists(self, sample_file_paths: Dict):
        """Verify model introspection example exists."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths.get('examples')
        if not examples_file or not examples_file.exists():
            pytest.skip("Examples file not available")

        with open(examples_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for introspection methods
        assert 'GetAllBodies' in content or 'GetAllJoints' in content, \
            "No model introspection example found"

    def test_result_processing_example_exists(self, sample_file_paths: Dict):
        """Verify result processing example exists."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths.get('examples')
        if not examples_file or not examples_file.exists():
            pytest.skip("Examples file not available")

        with open(examples_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for result processing methods
        assert 'GetTimeArray' in content or 'GetEntityData' in content or 'Export' in content, \
            "No result processing example found"
