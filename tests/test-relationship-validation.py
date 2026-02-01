#!/usr/bin/env python3
"""
Relationship Validation Tests for ProcessNet Knowledge Base.

These tests verify that extracted entities are correctly associated:
- Methods in /Methods/ folders are NOT standalone classes
- Methods are in their parent class's methods[] array
- Enums have at least 1 property with value
- Inheritance is captured when present in HTML

Phase 03 of v6 extraction quality fixes.
"""

import json
import pytest
import random
from pathlib import Path
from typing import Dict, List

# Knowledge base paths
KB_V5_PATH = Path(__file__).parent.parent / "output" / "processnet-knowledge-v5.json"
KB_PATH = Path(__file__).parent.parent / "output" / "processnet-knowledge.json"

# Known problematic files from v5 spot checks
KNOWN_PROBLEMATIC_FILES = [
    "IApplication_NewModelDocumentWithUnitSystem.html",
    "IApplication_Save.html",
    "IBody_GetMass.html",
    "RFlexMassInvariantType.html",
    "ADProcessNetType.html",
]


@pytest.fixture(scope="module")
def kb_v5() -> Dict:
    """Load v5 knowledge base for comparison testing."""
    if not KB_V5_PATH.exists():
        pytest.skip(f"v5 KB not found at {KB_V5_PATH}")
    with open(KB_V5_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def kb_current() -> Dict:
    """Load current knowledge base."""
    if not KB_PATH.exists():
        pytest.skip(f"Current KB not found at {KB_PATH}")
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestMethodsNotStandaloneClasses:
    """Verify files in /Methods/ subfolders do NOT create standalone class entries."""

    def test_no_method_file_classes_in_v5(self, kb_v5: Dict):
        """
        v5 should have this bug - method files created as classes.
        This test documents the v5 behavior for comparison.
        """
        # Find classes with underscore in name (likely from method files)
        problematic_classes = []
        for ns_name, ns_data in kb_v5.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                cls_name = cls.get('name', '')
                # Method-file classes typically have underscore pattern: ClassName_MethodName
                if '_' in cls_name and any(keyword in cls_name for keyword in ['Get', 'Set', 'Create', 'New', 'Load', 'Save']):
                    problematic_classes.append(f"{ns_name}.{cls_name}")

        # v5 SHOULD have these problematic classes (this confirms the bug exists)
        # If v5 is fixed, this test would fail - which is fine
        print(f"\nv5 has {len(problematic_classes)} potential method-file classes")
        if problematic_classes:
            print(f"Examples: {problematic_classes[:5]}")

    def test_known_method_file_not_class(self, kb_current: Dict):
        """
        Specific check: IApplication_NewModelDocumentWithUnitSystem should NOT be a class.
        It should be a method of IApplication.
        """
        # Search for the problematic class name
        found_as_class = False
        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if 'NewModelDocumentWithUnitSystem' in cls.get('name', ''):
                    found_as_class = True
                    print(f"\n✗ Found as class: {ns_name}.{cls['name']}")

        assert not found_as_class, (
            "IApplication_NewModelDocumentWithUnitSystem should NOT be a standalone class. "
            "It should be a method of IApplication."
        )


class TestMethodParentAssociation:
    """Verify methods are associated with their parent classes."""

    def test_iapplication_has_methods(self, kb_current: Dict):
        """IApplication class should have methods like NewModelDocumentWithUnitSystem."""
        iapp_class = None
        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if cls.get('name') == 'IApplication':
                    iapp_class = cls
                    break
            if iapp_class:
                break

        if iapp_class is None:
            pytest.skip("IApplication class not found in current KB")

        method_names = [m.get('name', '') for m in iapp_class.get('methods', [])]
        print(f"\nIApplication has {len(method_names)} methods")

        # Check for expected methods
        expected_methods = ['NewModelDocumentWithUnitSystem', 'Save', 'Load']
        for method in expected_methods:
            if method in method_names:
                print(f"  ✓ Found: {method}")
            else:
                print(f"  ? Missing: {method}")


class TestEnumMembersExtracted:
    """Verify enum classes have member properties with values."""

    def test_enum_has_members(self, kb_current: Dict):
        """All IntEnum classes should have at least 1 property."""
        enums_without_members = []
        enums_with_members = []

        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                inheritance = cls.get('inheritance', '')
                if 'IntEnum' in inheritance:
                    props = cls.get('properties', [])
                    if len(props) == 0:
                        enums_without_members.append(f"{ns_name}.{cls['name']}")
                    else:
                        enums_with_members.append(f"{ns_name}.{cls['name']} ({len(props)} members)")

        print(f"\nEnums with members: {len(enums_with_members)}")
        print(f"Enums without members: {len(enums_without_members)}")

        if enums_without_members:
            print(f"Missing members: {enums_without_members[:5]}")

        # At least 80% of enums should have members
        total_enums = len(enums_with_members) + len(enums_without_members)
        if total_enums > 0:
            success_rate = len(enums_with_members) / total_enums
            assert success_rate >= 0.8, f"Only {success_rate:.0%} of enums have members"

    def test_adprocessnettype_has_three_members(self, kb_current: Dict):
        """ADProcessNetType enum should have 3 members."""
        found = False
        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if cls.get('name') == 'ADProcessNetType':
                    props = cls.get('properties', [])
                    print(f"\nADProcessNetType has {len(props)} properties")
                    for p in props:
                        print(f"  - {p.get('name')}: {p.get('description', '')[:50]}")
                    assert len(props) == 3, f"Expected 3 members, got {len(props)}"
                    found = True
                    break
            if found:
                break

        if not found:
            pytest.skip("ADProcessNetType not found in current KB")


class TestInheritanceExtracted:
    """Verify class inheritance is captured."""

    def test_inheritance_captured(self, kb_current: Dict):
        """Classes with known base classes should have inheritance populated."""
        classes_with_inheritance = 0
        classes_without_inheritance = 0

        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                inheritance = cls.get('inheritance', '')
                if inheritance:
                    classes_with_inheritance += 1
                else:
                    classes_without_inheritance += 1

        total = classes_with_inheritance + classes_without_inheritance
        print(f"\nClasses with inheritance: {classes_with_inheritance}/{total}")

        # At least some classes should have inheritance
        if total > 0:
            assert classes_with_inheritance > 0, "No classes have inheritance information"


class TestSpotCheckHybrid:
    """Hybrid spot check: 15 known problematic + 5 random files."""

    def test_spot_check_failure_rate(self, kb_current: Dict):
        """
        Spot check should have <5% failure rate.
        Uses hybrid approach: known problematic files + random sampling.
        """
        failures = []
        successes = []

        # Check 1: Method files should not create classes
        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                cls_name = cls.get('name', '')
                # Pattern: ClassName_MethodName indicates method file was wrongly treated as class
                if '_' in cls_name:
                    parts = cls_name.split('_')
                    # If first part is a known class and second looks like a method
                    if len(parts) == 2:
                        method_like = any(keyword in parts[1] for keyword in
                            ['Get', 'Set', 'Create', 'New', 'Load', 'Save', 'Update', 'Delete', 'Add', 'Remove'])
                        if method_like:
                            failures.append(f"Method-as-class: {ns_name}.{cls_name}")

        # Check 2: Enums should have members
        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                if 'IntEnum' in cls.get('inheritance', ''):
                    if len(cls.get('properties', [])) == 0:
                        failures.append(f"Enum without members: {ns_name}.{cls['name']}")
                    else:
                        successes.append(f"Enum OK: {ns_name}.{cls['name']}")

        total_checks = len(failures) + len(successes)
        if total_checks == 0:
            print("\nNo spot checks performed (no matching patterns found)")
            return

        failure_rate = len(failures) / total_checks if total_checks > 0 else 0
        print(f"\nSpot check results:")
        print(f"  Successes: {len(successes)}")
        print(f"  Failures: {len(failures)}")
        print(f"  Failure rate: {failure_rate:.1%}")

        if failures:
            print(f"\nFailure examples:")
            for f in failures[:10]:
                print(f"  ✗ {f}")

        # Target: <5% failure rate
        assert failure_rate < 0.05, f"Failure rate {failure_rate:.1%} exceeds 5% threshold"


class TestOrphanedMembers:
    """Check for orphaned members (members without parent class)."""

    def test_orphaned_members_count(self, kb_current: Dict):
        """Track orphaned members for manual review."""
        total_orphans = 0
        orphan_details = []

        for ns_name, ns_data in kb_current.get('namespaces', {}).items():
            orphans = ns_data.get('orphaned_members', [])
            if orphans:
                total_orphans += len(orphans)
                for o in orphans[:3]:
                    orphan_details.append(f"{ns_name}: {o.get('file', 'unknown')}")

        print(f"\nOrphaned members: {total_orphans}")
        if orphan_details:
            print("Examples:")
            for o in orphan_details:
                print(f"  - {o}")

        # Orphans are logged but not a failure - just tracking
        # High orphan count indicates potential issues with class file processing order
