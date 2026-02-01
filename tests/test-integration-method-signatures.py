#!/usr/bin/env python3
"""
Integration Tests: Method Signature Validation

Validates that extracted method signatures match expected patterns
and cross-references with source documentation where available.
"""

import json
import pytest
import re
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
MethodSignature = helpers_module.MethodSignature
create_validation_targets = helpers_module.create_validation_targets


# ============================================================================
# Test Configuration
# ============================================================================

KB_PATH = "output/processnet-knowledge.json"
TARGETS_PATH = "tests/fixtures/validation-targets.json"


@pytest.fixture(scope="module")
def validator():
    """Create validator instance."""
    return ProcessNetValidator(KB_PATH)


@pytest.fixture(scope="module")
def validation_targets():
    """Load validation targets."""
    targets_path = Path(TARGETS_PATH)
    if not targets_path.exists():
        targets = create_validation_targets(KB_PATH)
    else:
        with open(targets_path) as f:
            data = json.load(f)
            # Reconstruct MethodSignature objects
            targets = {
                'namespaces': data['namespaces'],
                'expected_methods': {
                    k: MethodSignature(**v)
                    for k, v in data['expected_methods'].items()
                },
                'sample_methods': data.get('sample_methods', []),
                'validation_config': data.get('validation_config', {})
            }
    return targets


# ============================================================================
# Method Name Validation Tests
# ============================================================================

class TestMethodNames:
    """Test that method names are correctly extracted."""

    def test_all_methods_have_names(self, validator):
        """Verify all extracted methods have non-empty names."""
        report = validator.validate_namespace_methods('ProcessNet', limit=100)

        # Should have checked methods
        assert report.total_methods_checked > 0

        # All should have names (passed = checked - missing name failures)
        missing_names = sum(
            1 for d in report.discrepancies
            if d.category == 'missing' and 'method name' in d.expected
        )

        assert missing_names == 0, f"{missing_names} methods missing names"

    def test_method_names_are_valid_identifiers(self, validator):
        """Verify method names are valid programming identifiers."""
        samples = validator.get_sample_methods_for_validation(30)

        invalid_names = []
        for method in samples:
            name = method.get('name', '')
            if not name:
                continue
            # Check if name is valid (alphanumeric, underscores, no spaces)
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                invalid_names.append(name)

        # Allow some invalid names (could be properties with special chars)
        assert len(invalid_names) <= len(samples) * 0.1, \
            f"Too many invalid method names: {invalid_names[:5]}"

    def test_no_duplicate_method_names_in_namespace(self, validator):
        """Check for duplicate method names within same namespace."""
        ns_data = validator.kb.get('namespaces', {}).get('ProcessNet', {})
        methods = ns_data.get('standalone_methods', [])

        name_counts = {}
        for method in methods:
            name = method.get('name', '').lower()
            if name:
                name_counts[name] = name_counts.get(name, 0) + 1

        # Find duplicates
        duplicates = {k: v for k, v in name_counts.items() if v > 1}

        # Duplicates may be valid (overloads), but flag if excessive
        assert len(duplicates) <= 10, f"Too many duplicates: {list(duplicates.keys())[:5]}"


# ============================================================================
# Parameter Count Validation Tests
# ============================================================================

class TestParameterCounts:
    """Test parameter count extraction accuracy."""

    def test_extract_parameter_count_from_signature(self, validator):
        """Test parameter count extraction logic."""
        test_cases = [
            ("Method()", 0),
            ("Method(int x)", 1),
            ("Method(int x, string y)", 2),
            ("Method(int x, string y, double z)", 3),
            ("Method(List<int> values)", 1),
            ("Method(Dictionary<string, int> map)", 1),
        ]

        for signature, expected_count in test_cases:
            actual_count = validator.extract_parameter_count(signature)
            assert actual_count == expected_count, \
                f"Failed for '{signature}': expected {expected_count}, got {actual_count}"

    def test_key_methods_have_parameters(self, validator):
        """Verify key workflow methods have expected parameters."""
        # Test AutoDesign save methods
        save_method = validator.get_method_by_name('SaveNewModel', 'ProcessNet.AutoDesign')
        assert save_method is not None, "SaveNewModel not found"

        param_count = validator.extract_parameter_count(save_method.get('signature', ''))
        assert param_count >= 2, f"SaveNewModel should have 2-3 params, got {param_count}"

    def test_parameter_extraction_consistency(self, validator):
        """Test parameter extraction is consistent across similar methods."""
        # Get multiple Save* methods
        save_methods = []
        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                if 'save' in method.get('name', '').lower():
                    save_methods.append(method)

        # At least some Save methods should be found
        assert len(save_methods) > 0, "No Save methods found"

        # Most Save methods should have reasonable parameter counts (0-5)
        reasonable_count = 0
        for method in save_methods[:20]:
            count = validator.extract_parameter_count(method.get('signature', ''))
            if 0 <= count <= 5:
                reasonable_count += 1

        assert reasonable_count >= len(save_methods[:20]) * 0.8, \
            "Too many Save methods have unusual parameter counts"


# ============================================================================
# Signature Format Validation Tests
# ============================================================================

class TestSignatureFormats:
    """Test signature format and structure."""

    def test_signatures_contain_parentheses(self, validator):
        """Verify method signatures contain parentheses."""
        samples = validator.get_sample_methods_for_validation(30)

        missing_parens = []
        for method in samples:
            sig = method.get('signature', '')
            if sig and ('(' not in sig or ')' not in sig):
                missing_parens.append(method.get('name', '<unknown>'))

        # Most signatures should have parentheses
        assert len(missing_parens) <= len(samples) * 0.2, \
            f"Too many signatures missing parentheses: {missing_parens}"

    def test_signatures_have_method_name(self, validator):
        """Verify signature contains the method name."""
        samples = validator.get_sample_methods_for_validation(30)

        missing_name = []
        for method in samples:
            name = method.get('name', '')
            sig = method.get('signature', '')
            if name and sig and name not in sig:
                # Allow some flexibility (might be formatted differently)
                missing_name.append(name)

        # At least 80% should have name in signature
        assert len(missing_name) <= len(samples) * 0.2, \
            f"Too many signatures don't contain method name: {missing_name[:5]}"


# ============================================================================
# Expected Method Validation Tests
# ============================================================================

class TestExpectedMethods:
    """Test validation of expected key workflow methods."""

    def test_expected_autodesign_methods_exist(self, validator, validation_targets):
        """Verify expected AutoDesign workflow methods exist."""
        expected = validation_targets['expected_methods']

        found_methods = []
        for method_name, expected_sig in expected.items():
            if 'AutoDesign' in expected_sig.namespace:
                method = validator.get_method_by_name(method_name, expected_sig.namespace)
                if method:
                    found_methods.append(method_name)

        # At least 2 AutoDesign methods should be found
        assert len(found_methods) >= 2, f"Only found AutoDesign methods: {found_methods}"

    def test_save_model_methods_present(self, validator):
        """Test Save* model methods are present."""
        save_methods = []
        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if name.startswith('Save') and 'model' in name.lower():
                    save_methods.append(f"{ns_name}.{name}")

        # Should find several Save*Model methods
        assert len(save_methods) >= 3, f"Only found Save*Model methods: {save_methods}"

    def test_update_methods_present(self, validator):
        """Test Update* methods are present."""
        update_methods = []
        for ns_name, ns_data in validator.kb.get('namespaces', {}).items():
            for method in ns_data.get('standalone_methods', []):
                name = method.get('name', '')
                if name.startswith('Update'):
                    update_methods.append(f"{ns_name}.{name}")

        # Should find Update methods
        assert len(update_methods) >= 2, f"Only found Update methods: {update_methods}"


# ============================================================================
# Cross-Reference Validation Tests
# ============================================================================

class TestCrossReference:
    """Test cross-referencing with source documentation."""

    def test_cross_reference_structure(self, validator):
        """Test cross-reference method returns expected structure."""
        result = validator.cross_reference_with_source('SaveNewModel')

        assert isinstance(result, dict)
        assert 'method_name' in result
        assert 'kb_data' in result
        assert 'source_available' in result

    def test_cross_reference_finds_method(self, validator):
        """Test cross-reference can find existing methods."""
        result = validator.cross_reference_with_source('SaveNewModel')

        # Should find the method in KB
        assert result['kb_data'] is not None or result['kb_data'] is False
        assert result['method_name'] == 'SaveNewModel'


# ============================================================================
# Namespace Coverage Tests
# ============================================================================

class TestNamespaceCoverage:
    """Test validation coverage across namespaces."""

    def test_all_namespaces_have_methods(self, validator, validation_targets):
        """Verify all namespaces contain extracted methods."""
        namespaces = validation_targets['namespaces']

        empty_namespaces = []
        for ns in namespaces:
            ns_data = validator.kb.get('namespaces', {}).get(ns, {})
            method_count = len(ns_data.get('standalone_methods', []))
            if method_count == 0:
                empty_namespaces.append(ns)

        # Most namespaces should have methods
        assert len(empty_namespaces) <= len(namespaces) * 0.1, \
            f"Too many empty namespaces: {empty_namespaces}"

    def test_top_namespaces_well_populated(self, validator):
        """Test top namespaces have good method coverage."""
        top_ns = ['ProcessNet', 'ProcessNet.ProcessNet', 'ProcessNet.Post']

        for ns in top_ns:
            ns_data = validator.kb.get('namespaces', {}).get(ns, {})
            method_count = len(ns_data.get('standalone_methods', []))

            assert method_count > 100, f"Namespace {ns} has only {method_count} methods"


# ============================================================================
# Integration Tests
# ============================================================================

class TestSignatureIntegration:
    """Integration tests for signature validation."""

    def test_full_signature_validation_workflow(self, validator, validation_targets):
        """Test complete signature validation workflow."""
        expected = validation_targets['expected_methods']

        total_checked = 0
        total_passed = 0

        for method_name, expected_sig in expected.items():
            actual_method = validator.get_method_by_name(
                method_name,
                expected_sig.namespace
            )

            if actual_method:
                total_checked += 1
                is_valid, discrepancies = validator.validate_method_signature(
                    expected_sig,
                    actual_method
                )

                if is_valid:
                    total_passed += 1

        # At least some methods should be validated
        assert total_checked > 0, "No expected methods found for validation"

        # Report pass rate
        pass_rate = (total_passed / total_checked * 100) if total_checked > 0 else 0
        assert pass_rate >= 50, f"Pass rate too low: {pass_rate:.1f}%"


if __name__ == '__main__':
    # Add regex import for tests
    import re
    pytest.main([__file__, '-v', '--tb=short'])
