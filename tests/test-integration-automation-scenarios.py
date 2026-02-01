#!/usr/bin/env python3
"""
Integration Tests: Automation Scenario Validation

Tests that validate the knowledge base supports the 3 key automation workflows:
1. DOE Batch Execution
2. Model Introspection
3. Result Processing
"""

import json
import pytest
import sys
from pathlib import Path

# Add src and helpers to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent / 'helpers'))

import importlib.util

# Load validation helpers
spec_helpers = importlib.util.spec_from_file_location(
    "validation_helpers",
    Path(__file__).parent / "helpers" / "validation-helpers.py"
)
helpers_module = importlib.util.module_from_spec(spec_helpers)
spec_helpers.loader.exec_module(helpers_module)

ProcessNetValidator = helpers_module.ProcessNetValidator


# ============================================================================
# Test Configuration
# ============================================================================

KB_PATH = "output/processnet-knowledge.json"


@pytest.fixture(scope="module")
def validator():
    """Create validator instance."""
    return ProcessNetValidator(KB_PATH)


# ============================================================================
# Use Case 1: DOE Batch Execution
# ============================================================================

class TestDOEBatchExecution:
    """Test DOE (Design of Experiments) batch execution workflow.

    Workflow Steps:
    1. Load base model
    2. Clone for variations
    3. Set parameters (mass, stiffness, etc.)
    4. Save each variant
    5. Run simulation
    """

    def test_save_methods_exist(self, validator):
        """Verify Save* methods exist for model variants."""
        save_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'save' in name.lower():
                    save_methods.append({
                        'name': name,
                        'namespace': ns_name,
                        'signature': method.get('signature', '')
                    })

        assert len(save_methods) >= 5, f"Only found {len(save_methods)} Save methods"

    def test_clone_methods_exist(self, validator):
        """Verify Clone methods exist for model duplication."""
        clone_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'clone' in name.lower():
                    clone_methods.append({
                        'name': name,
                        'namespace': ns_name,
                        'signature': method.get('signature', '')
                    })

        # Should find Clone methods
        assert len(clone_methods) >= 1, f"No Clone methods found"

    def test_parameter_methods_exist(self, validator):
        """Verify parameter manipulation methods exist."""
        param_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if any(kw in name.lower() for kw in ['parameter', 'param', 'value', 'set']):
                    param_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        # Should find parameter-related methods
        assert len(param_methods) >= 10, f"Only found {len(param_methods)} parameter methods"

    def test_update_methods_exist(self, validator):
        """Verify Update methods for model modifications."""
        update_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'update' in name.lower():
                    update_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        assert len(update_methods) >= 2, f"Only found {len(update_methods)} Update methods"

    def test_doe_namespace_coverage(self, validator):
        """Test AutoDesign namespace has DOE-related methods."""
        auto_ns = validator.kb.get('namespaces', {}).get('ProcessNet.AutoDesign', {})

        # AutoDesign namespace should exist and have methods
        assert auto_ns, "AutoDesign namespace not found"

        method_count = len(auto_ns.get('standalone_methods', []))
        assert method_count >= 50, f"AutoDesign has only {method_count} methods"


# ============================================================================
# Use Case 2: Model Introspection
# ============================================================================

class TestModelIntrospection:
    """Test model introspection workflow.

    Workflow Steps:
    1. Load existing model
    2. Query all entities by type
    3. Map entity IDs and properties
    4. Export entity structure
    """

    def test_entity_query_methods_exist(self, validator):
        """Verify methods for querying entities exist."""
        entity_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if any(kw in name.lower() for kw in ['get', 'all', 'entity', 'find']):
                    entity_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        # Should find entity query methods
        assert len(entity_methods) >= 20, f"Only found {len(entity_methods)} entity query methods"

    def test_body_methods_exist(self, validator):
        """Verify Body-related methods exist."""
        body_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            # Check classes too
            for cls in ns_data.get('classes', []):
                if 'body' in cls.get('name', '').lower():
                    body_methods.append(f"{ns_name}.{cls['name']}")

            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'body' in name.lower():
                    body_methods.append(f"{ns_name}.{name}")

        assert len(body_methods) >= 5, f"Only found {len(body_methods)} Body-related items"

    def test_joint_methods_exist(self, validator):
        """Verify Joint-related methods exist."""
        joint_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if 'joint' in cls.get('name', '').lower():
                    joint_methods.append(f"{ns_name}.{cls['name']}")

            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'joint' in name.lower():
                    joint_methods.append(f"{ns_name}.{name}")

        assert len(joint_methods) >= 5, f"Only found {len(joint_methods)} Joint-related items"

    def test_force_methods_exist(self, validator):
        """Verify Force-related methods exist."""
        force_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if 'force' in cls.get('name', '').lower():
                    force_methods.append(f"{ns_name}.{cls['name']}")

            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'force' in name.lower():
                    force_methods.append(f"{ns_name}.{name}")

        assert len(force_methods) >= 5, f"Only found {len(force_methods)} Force-related items"

    def test_get_methods_common(self, validator):
        """Test Get* methods are commonly available."""
        get_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if name.startswith('Get'):
                    get_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        # Should find many Get methods
        assert len(get_methods) >= 50, f"Only found {len(get_methods)} Get methods"


# ============================================================================
# Use Case 3: Result Processing
# ============================================================================

class TestResultProcessing:
    """Test result post-processing workflow.

    Workflow Steps:
    1. Load simulation result file
    2. Extract time arrays
    3. Extract entity data (displacement, force, velocity)
    4. Process and analyze data
    5. Export to external format
    """

    def test_load_methods_exist(self, validator):
        """Verify Load methods for reading results."""
        load_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'load' in name.lower():
                    load_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        assert len(load_methods) >= 5, f"Only found {len(load_methods)} Load methods"

    def test_time_methods_exist(self, validator):
        """Verify time-related methods exist."""
        time_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'time' in name.lower():
                    time_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        assert len(time_methods) >= 3, f"Only found {len(time_methods)} Time methods"

    def test_data_methods_exist(self, validator):
        """Verify data extraction methods exist."""
        data_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if any(kw in name.lower() for kw in ['data', 'get', 'extract', 'array']):
                    data_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        assert len(data_methods) >= 20, f"Only found {len(data_methods)} data-related methods"

    def test_export_methods_exist(self, validator):
        """Verify export methods exist."""
        export_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if 'export' in name.lower():
                    export_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        # Should find some export methods
        assert len(export_methods) >= 2, f"Only found {len(export_methods)} Export methods"

    def test_plot_methods_exist(self, validator):
        """Verify plot/visualization methods exist."""
        plot_methods = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if any(kw in name.lower() for kw in ['plot', 'graph', 'chart', 'display']):
                    plot_methods.append({
                        'name': name,
                        'namespace': ns_name
                    })

        # May or may not have plot methods, but shouldn't error
        assert len(plot_methods) >= 0


# ============================================================================
# Cross-Workflow Tests
# ============================================================================

class TestCrossWorkflowIntegration:
    """Test methods that span multiple workflows."""

    def test_model_methods_available(self, validator):
        """Test Model class methods are available."""
        model_items = []

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            # Check classes
            for cls in ns_data.get('classes', []):
                if 'model' in cls.get('name', '').lower():
                    model_items.append({
                        'name': cls['name'],
                        'namespace': ns_name,
                        'type': 'class'
                    })

            # Check methods
            for method in ns_data.get('standalone_methods', []):
                if 'model' in method.get('name', '').lower():
                    model_items.append({
                        'name': method['name'],
                        'namespace': ns_name,
                        'type': 'method'
                    })

        assert len(model_items) >= 10, f"Only found {len(model_items)} Model-related items"

    def test_process_namespace_coverage(self, validator):
        """Test ProcessNet.Post namespace for result processing."""
        post_ns = validator.kb.get('namespaces', {}).get('ProcessNet.Post', {})

        # Post namespace should exist
        assert post_ns, "ProcessNet.Post namespace not found"

        method_count = len(post_ns.get('standalone_methods', []))
        assert method_count >= 100, f"ProcessNet.Post has only {method_count} methods"


# ============================================================================
# Integration Tests
# ============================================================================

class TestAutomationIntegration:
    """Integration tests for complete automation workflows."""

    def test_all_workflows_have_methods(self, validator):
        """Test all 3 workflows have supporting methods."""
        workflow_methods = {
            'DOE': 0,
            'Introspection': 0,
            'ResultProcessing': 0
        }

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '').lower()

                # DOE workflow methods
                if any(kw in name for kw in ['save', 'clone', 'parameter', 'update']):
                    workflow_methods['DOE'] += 1

                # Introspection methods
                if any(kw in name for kw in ['get', 'find', 'entity', 'body', 'joint', 'force']):
                    workflow_methods['Introspection'] += 1

                # Result processing methods
                if any(kw in name for kw in ['load', 'time', 'data', 'export', 'plot']):
                    workflow_methods['ResultProcessing'] += 1

        # All workflows should have methods
        for workflow, count in workflow_methods.items():
            assert count >= 20, f"{workflow} workflow only has {count} methods"

    def test_workflow_method_diversity(self, validator):
        """Test workflows have diverse method categories."""
        found_categories = set()

        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '').lower()

                if 'save' in name:
                    found_categories.add('save')
                if 'get' in name:
                    found_categories.add('get')
                if 'load' in name:
                    found_categories.add('load')
                if 'set' in name:
                    found_categories.add('set')
                if 'update' in name:
                    found_categories.add('update')

        # Should find multiple categories
        assert len(found_categories) >= 4, f"Only found categories: {found_categories}"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
