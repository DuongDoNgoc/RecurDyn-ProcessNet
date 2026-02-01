#!/usr/bin/env python3
"""
Integration Tests: Parameter Type Validation

Validates that parameter types and return types are correctly extracted
from the ProcessNet API documentation.
"""

import json
import pytest
import sys
from pathlib import Path
from typing import Dict, List

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
# Type Normalization Tests
# ============================================================================

class TestTypeNormalization:
    """Test type string normalization and categorization."""

    def test_normalize_string_types(self, validator):
        """Test various string type formats normalize correctly."""
        test_cases = [
            ('string', 'string'),
            ('str', 'string'),
            ('String', 'string'),
            ('System.String', 'string'),
        ]

        for input_type, expected in test_cases:
            result = validator.normalize_type(input_type)
            assert result == expected, f"Failed for '{input_type}': expected {expected}, got {result}"

    def test_normalize_integer_types(self, validator):
        """Test various integer type formats normalize correctly."""
        test_cases = [
            ('int', 'integer'),
            ('integer', 'integer'),
            ('Int32', 'integer'),
            ('Int64', 'integer'),
            ('System.Int32', 'integer'),
        ]

        for input_type, expected in test_cases:
            result = validator.normalize_type(input_type)
            assert result == expected, f"Failed for '{input_type}': expected {expected}, got {result}"

    def test_normalize_double_types(self, validator):
        """Test various double/float type formats normalize correctly."""
        test_cases = [
            ('double', 'double'),
            ('float', 'double'),
            ('Double', 'double'),
            ('decimal', 'double'),
            ('System.Double', 'double'),
        ]

        for input_type, expected in test_cases:
            result = validator.normalize_type(input_type)
            assert result == expected, f"Failed for '{input_type}': expected {expected}, got {result}"

    def test_normalize_boolean_types(self, validator):
        """Test various boolean type formats normalize correctly."""
        test_cases = [
            ('bool', 'boolean'),
            ('boolean', 'boolean'),
            ('Bool', 'boolean'),
            ('System.Boolean', 'boolean'),
        ]

        for input_type, expected in test_cases:
            result = validator.normalize_type(input_type)
            assert result == expected, f"Failed for '{input_type}': expected {expected}, got {result}"

    def test_normalize_void_types(self, validator):
        """Test various void type formats normalize correctly."""
        test_cases = [
            ('void', 'void'),
            ('None', 'void'),
            ('null', 'void'),
        ]

        for input_type, expected in test_cases:
            result = validator.normalize_type(input_type)
            assert result == expected, f"Failed for '{input_type}': expected {expected}, got {result}"

    def test_unknown_types_remain_unknown(self, validator):
        """Test unknown types are categorized as unknown."""
        unknown_cases = [
            'CustomType',
            'IEnumerable<T>',
            'MyClass',
            'object',
        ]

        for input_type in unknown_cases:
            result = validator.normalize_type(input_type)
            assert result == 'unknown', f"Unknown type '{input_type}' should remain unknown, got {result}"


# ============================================================================
# Parameter Extraction Tests
# ============================================================================

class TestParameterExtraction:
    """Test parameter data extraction from methods."""

    def test_methods_have_parameter_data(self, validator):
        """Verify methods contain parameter information."""
        samples = validator.get_sample_methods_for_validation(30)

        methods_with_params = 0
        for method in samples:
            params = method.get('parameters', [])
            if params:
                methods_with_params += 1

        # At least some methods should have parameter data
        assert methods_with_params > 0, "No methods with parameter data found"

    def test_parameter_names_extracted(self, validator):
        """Test parameter names are extracted when present."""
        # Find methods with parameters
        samples = validator.get_sample_methods_for_validation(50)

        params_with_names = 0
        for method in samples:
            params = method.get('parameters', [])
            for param in params:
                if param.get('name'):
                    params_with_names += 1
                    break

        assert params_with_names > 0, "No parameter names found"

    def test_parameter_types_extracted(self, validator):
        """Test parameter types are extracted when present."""
        samples = validator.get_sample_methods_for_validation(50)

        params_with_types = 0
        for method in samples:
            params = method.get('parameters', [])
            for param in params:
                if param.get('type'):
                    params_with_types += 1
                    break

        assert params_with_types > 0, "No parameter types found"


# ============================================================================
# Return Type Tests
# ============================================================================

class TestReturnTypes:
    """Test return type extraction and validation."""

    def test_methods_have_return_type_field(self, validator):
        """Verify methods have return type information."""
        samples = validator.get_sample_methods_for_validation(30)

        methods_with_returns = 0
        for method in samples:
            if method.get('returns') or method.get('return_type'):
                methods_with_returns += 1

        # At least some methods should have return type data
        assert methods_with_returns > 0, "No methods with return type data found"

    def test_common_return_types_present(self, validator):
        """Test common return types appear in extracted data."""
        samples = validator.get_sample_methods_for_validation(50)

        return_types_found = set()
        for method in samples:
            returns = method.get('returns', '') or method.get('return_type', '')
            if returns:
                normalized = validator.normalize_type(returns)
                if normalized != 'unknown':
                    return_types_found.add(normalized)

        # Should find at least some standard types
        assert len(return_types_found) >= 2, f"Only found return types: {return_types_found}"

    def test_void_return_methods_exist(self, validator):
        """Test that void return methods are identified."""
        samples = validator.get_sample_methods_for_validation(50)

        void_methods = 0
        for method in samples:
            returns = method.get('returns', '') or method.get('return_type', '')
            if returns and validator.normalize_type(returns) == 'void':
                void_methods += 1

        # Should find some void methods
        assert void_methods > 0, "No void return methods found"


# ============================================================================
# Type Accuracy Tests
# ============================================================================

class TestTypeAccuracy:
    """Test accuracy of extracted type information."""

    def test_type_consistency_in_namespace(self, validator):
        """Test types are used consistently within namespace."""
        ns_data = validator.kb.get('namespaces', {}).get('ProcessNet', {})
        methods = ns_data.get('standalone_methods', [])

        # Collect parameter types
        param_types = {}
        for method in methods[:100]:
            for param in method.get('parameters', []):
                ptype = param.get('type', '')
                if ptype:
                    ptype_normalized = validator.normalize_type(ptype)
                    param_types[ptype_normalized] = param_types.get(ptype_normalized, 0) + 1

        # Should find standard types
        standard_types = {'string', 'integer', 'double', 'boolean'}
        found_standard = standard_types & param_types.keys()

        assert len(found_standard) >= 2, f"Only found standard types: {found_standard}"

    def test_no_invalid_type_characters(self, validator):
        """Test type strings don't contain invalid characters."""
        samples = validator.get_sample_methods_for_validation(30)

        invalid_types = []
        for method in samples:
            for param in method.get('parameters', []):
                ptype = param.get('type', '')
                if ptype:
                    # Check for obviously invalid characters
                    if any(char in ptype for char in ['<>', '\n', '\r', '\t']):
                        invalid_types.append(f"{method.get('name')}: {ptype}")

        # Should not have types with invalid characters
        assert len(invalid_types) == 0, f"Found types with invalid characters: {invalid_types[:5]}"


# ============================================================================
# Signature Type Tests
# ============================================================================

class TestSignatureTypes:
    """Test type information in method signatures."""

    def test_signatures_contain_type_information(self, validator):
        """Test signatures contain type hints."""
        samples = validator.get_sample_methods_for_validation(30)

        signatures_with_types = 0
        for method in samples:
            sig = method.get('signature', '')
            # Look for type indicators in signature
            if any(keyword in sig for keyword in ['int', 'string', 'double', 'bool', 'void', 'str']):
                signatures_with_types += 1

        # Most signatures should have some type information
        assert signatures_with_types >= len(samples) * 0.5, \
            "Too few signatures contain type information"


# ============================================================================
# Integration Tests
# ============================================================================

class TestTypeIntegration:
    """Integration tests for type validation."""

    def test_full_type_validation_workflow(self, validator):
        """Test complete type validation workflow."""
        samples = validator.get_sample_methods_for_validation(20)

        total_checks = 0
        passed_checks = 0

        for method in samples:
            # Check has name
            if not method.get('name'):
                continue

            total_checks += 1
            passed_checks += 1  # Having name is baseline pass

            # Check if signature exists
            if method.get('signature'):
                passed_checks += 1

            # Check parameters are list
            params = method.get('parameters', [])
            if isinstance(params, list):
                passed_checks += 1

        # Report pass rate
        pass_rate = (passed_checks / (total_checks * 3)) * 100 if total_checks > 0 else 0

        assert pass_rate >= 70, f"Type validation pass rate too low: {pass_rate:.1f}%"

    def test_workflow_methods_have_complete_type_info(self, validator):
        """Test key workflow methods have complete type information."""
        # Check SaveNewModel method
        method = validator.get_method_by_name('SaveNewModel', 'ProcessNet.AutoDesign')

        if method:
            # Should have signature
            assert method.get('signature'), "SaveNewModel missing signature"

            # Signature should contain type information
            sig = method.get('signature', '')
            assert any(kw in sig.lower() for kw in ['string', 'void', 'int', 'bool', 'str']), \
                "SaveNewModel signature lacks type information"


# ============================================================================
# Statistics Tests
# ============================================================================

class TestTypeStatistics:
    """Test type extraction statistics."""

    def test_type_distribution_report(self, validator):
        """Generate and validate type distribution report."""
        samples = validator.get_sample_methods_for_validation(100)

        type_counts = {'string': 0, 'integer': 0, 'double': 0, 'boolean': 0, 'void': 0, 'unknown': 0}

        for method in samples:
            # Check parameter types
            for param in method.get('parameters', []):
                ptype = param.get('type', '')
                if ptype:
                    normalized = validator.normalize_type(ptype)
                    type_counts[normalized] = type_counts.get(normalized, 0) + 1

            # Check return types
            returns = method.get('returns', '') or method.get('return_type', '')
            if returns:
                normalized = validator.normalize_type(returns)
                type_counts[normalized] = type_counts.get(normalized, 0) + 1

        # Should have found some types
        total_found = sum(type_counts.values())
        assert total_found > 0, "No types found in sample"

        # At least 2 categories should have entries
        non_zero = sum(1 for count in type_counts.values() if count > 0)
        assert non_zero >= 2, f"Only found {non_zero} type categories"

        # Report statistics
        print(f"\nType Distribution:")
        for type_name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"  {type_name:10s}: {count:4d}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
