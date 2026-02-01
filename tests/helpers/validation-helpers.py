#!/usr/bin/env python3
"""
Validation Helpers for ProcessNet API Integration Testing

Utilities for validating extracted API data against expected patterns
and cross-referencing with source documentation.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class MethodSignature:
    """Expected method signature for validation."""
    name: str
    namespace: str
    parameter_count: int
    parameter_types: List[str] = field(default_factory=list)
    return_type: str = ""
    is_static: bool = False


@dataclass
class ValidationDiscrepancy:
    """Recorded discrepancy between expected and actual data."""
    severity: str  # critical, major, minor
    category: str  # signature, parameter_type, return_type, missing
    method_name: str
    namespace: str
    expected: str
    actual: str
    recommendation: str = ""


@dataclass
class ValidationReport:
    """Summary of validation results."""
    total_methods_checked: int = 0
    methods_passed: int = 0
    methods_failed: int = 0
    discrepancies: List[ValidationDiscrepancy] = field(default_factory=list)
    timestamp: str = ""

    def add_discrepancy(self, discrepancy: ValidationDiscrepancy):
        """Add a discrepancy to the report."""
        self.discrepancies.append(discrepancy)
        if discrepancy.severity in ('critical', 'major'):
            self.methods_failed += 1

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate percentage."""
        if self.total_methods_checked == 0:
            return 0.0
        return (self.methods_passed / self.total_methods_checked) * 100


# ============================================================================
# Validation Utilities
# ============================================================================

class ProcessNetValidator:
    """Validator for ProcessNet API extraction accuracy."""

    # Expected type patterns
    TYPE_PATTERNS = {
        'string': r'str|string|String',
        'integer': r'int|integer|Int32|Int64',
        'double': r'double|float|Double|decimal|number',
        'boolean': r'bool|boolean|Bool',
        'void': r'void|None|null',
    }

    # Known method signatures for key workflows
    EXPECTED_METHODS = {
        # DOE Batch Execution
        'SaveNewModel': MethodSignature('SaveNewModel', 'ProcessNet.AutoDesign', 3),
        'SaveCurrentModel': MethodSignature('SaveCurrentModel', 'ProcessNet.AutoDesign', 0),
        'UpdateCurrentModel': MethodSignature('UpdateCurrentModel', 'ProcessNet.AutoDesign', 1),
        'UpdateNewModel': MethodSignature('UpdateNewModel', 'ProcessNet.AutoDesign', 3),

        # Model Introspection (examples - actual names may vary)
        'GetAllBodies': MethodSignature('GetAllBodies', 'ProcessNet', 0),
        'GetAllJoints': MethodSignature('GetAllJoints', 'ProcessNet', 0),
        'GetAllForces': MethodSignature('GetAllForces', 'ProcessNet', 0),

        # Result Processing (examples)
        'GetTimeArray': MethodSignature('GetTimeArray', 'ProcessNet', 0),
    }

    def __init__(self, kb_path: str = "output/processnet-knowledge.json"):
        """Initialize validator with knowledge base path."""
        self.kb_path = Path(kb_path)
        self.kb: Dict = {}
        self._load_kb()

    def _load_kb(self):
        """Load knowledge base from JSON file."""
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base not found: {self.kb_path}")
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)

    def get_method_by_name(self, name: str, namespace: Optional[str] = None) -> Optional[Dict]:
        """Find method by exact name in knowledge base."""
        method_lower = name.lower()

        # Check method index first
        if method_lower in self.kb.get('method_index', {}):
            for ns in self.kb['method_index'][method_lower]:
                if namespace is None or ns.lower() == namespace.lower():
                    ns_data = self.kb['namespaces'].get(ns, {})
                    for method in ns_data.get('standalone_methods', []):
                        if method['name'].lower() == method_lower:
                            return method

        return None

    def extract_parameter_count(self, signature: str) -> int:
        """Extract parameter count from method signature."""
        # Find parameters between parentheses
        match = re.search(r'\(([^)]*)\)', signature)
        if not match:
            return 0

        params = match.group(1).strip()
        if not params or params == 'void':
            return 0

        # Count parameters by comma (handling generic types)
        param_count = 0
        depth = 0
        for char in params:
            if char in '<>[':
                depth += 1
            elif char in '>]':
                depth -= 1
            elif char == ',' and depth == 0:
                param_count += 1
        return param_count + 1  # Add 1 for the last parameter

    def normalize_type(self, type_str: str) -> str:
        """Normalize type string to common category."""
        type_str = type_str.strip().lower()

        for category, pattern in self.TYPE_PATTERNS.items():
            if re.search(pattern, type_str, re.IGNORECASE):
                return category

        return 'unknown'

    def validate_method_signature(
        self,
        expected: MethodSignature,
        actual: Dict
    ) -> Tuple[bool, List[ValidationDiscrepancy]]:
        """Validate a method signature against expected."""
        discrepancies = []
        is_valid = True

        # Check name
        if actual['name'] != expected.name:
            discrepancies.append(ValidationDiscrepancy(
                severity='critical',
                category='signature',
                method_name=expected.name,
                namespace=expected.namespace,
                expected=expected.name,
                actual=actual['name'],
                recommendation='Method name mismatch'
            ))
            is_valid = False

        # Check parameter count
        actual_param_count = self.extract_parameter_count(actual.get('signature', ''))
        if actual_param_count != expected.parameter_count:
            discrepancies.append(ValidationDiscrepancy(
                severity='major' if abs(actual_param_count - expected.parameter_count) == 1 else 'critical',
                category='signature',
                method_name=expected.name,
                namespace=expected.namespace,
                expected=f'{expected.parameter_count} parameters',
                actual=f'{actual_param_count} parameters',
                recommendation=f'Check signature: {actual.get("signature", "")}'
            ))
            is_valid = False

        return is_valid, discrepancies

    def validate_namespace_methods(
        self,
        namespace: str,
        limit: int = 50
    ) -> ValidationReport:
        """Validate methods in a namespace."""
        report = ValidationReport()

        ns_data = self.kb.get('namespaces', {}).get(namespace, {})
        methods = ns_data.get('standalone_methods', [])

        for method in methods[:limit]:
            report.total_methods_checked += 1

            # Basic validation: method should have name and signature
            if not method.get('name'):
                report.add_discrepancy(ValidationDiscrepancy(
                    severity='critical',
                    category='missing',
                    method_name='<unknown>',
                    namespace=namespace,
                    expected='method name',
                    actual='<missing>',
                    recommendation='Parser failed to extract method name'
                ))
                continue

            if not method.get('signature'):
                report.add_discrepancy(ValidationDiscrepancy(
                    severity='major',
                    category='signature',
                    method_name=method['name'],
                    namespace=namespace,
                    expected='method signature',
                    actual='<missing>',
                    recommendation='Check HTML structure for this method'
                ))
                continue

            # If we have both name and signature, count as passed
            report.methods_passed += 1

        return report

    def get_sample_methods_for_validation(self, count: int = 50) -> List[Dict]:
        """Get sample methods across all namespaces for validation."""
        samples = []

        for ns_name, ns_data in self.kb.get('namespaces', {}).items():
            methods = ns_data.get('standalone_methods', [])
            for method in methods[:5]:  # Take 5 from each namespace
                method['namespace'] = ns_name
                samples.append(method)
                if len(samples) >= count:
                    return samples

        return samples

    def cross_reference_with_source(
        self,
        method_name: str,
        source_html_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Cross-reference method with source HTML if available."""
        result = {
            'method_name': method_name,
            'kb_data': self.get_method_by_name(method_name),
            'source_available': source_html_path is not None and source_html_path.exists(),
            'source_path': str(source_html_path) if source_html_path else None
        }

        return result


# ============================================================================
# Test Fixtures
# ============================================================================

def create_validation_targets(kb_path: str = "output/processnet-knowledge.json") -> Dict:
    """Create validation target definitions for testing."""
    validator = ProcessNetValidator(kb_path)

    targets = {
        'namespaces': list(validator.kb.get('namespaces', {}).keys()),
        'expected_methods': validator.EXPECTED_METHODS,
        'sample_methods': validator.get_sample_methods_for_validation(50),
        'validation_config': {
            'min_parameter_accuracy': 0.95,
            'min_type_accuracy': 0.90,
            'min_signature_accuracy': 1.00,
        }
    }

    return targets


def save_validation_targets(
    targets: Dict,
    output_path: str = "tests/fixtures/validation-targets.json"
):
    """Save validation targets to JSON file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Convert dataclasses to dict for JSON serialization
    serializable_targets = {
        'namespaces': targets['namespaces'],
        'expected_methods': {
            k: {
                'name': v.name,
                'namespace': v.namespace,
                'parameter_count': v.parameter_count,
                'parameter_types': v.parameter_types,
                'return_type': v.return_type,
                'is_static': v.is_static
            }
            for k, v in targets['expected_methods'].items()
        },
        'sample_methods': targets['sample_methods'][:20],  # Limit for file size
        'validation_config': targets['validation_config']
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(serializable_targets, f, indent=2)


if __name__ == '__main__':
    # Generate validation targets when run directly
    print("Generating validation targets...")
    targets = create_validation_targets()
    save_validation_targets(targets)
    print(f"Generated {len(targets['sample_methods'])} validation targets")
    print(f"Covering {len(targets['namespaces'])} namespaces")
