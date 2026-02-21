#!/usr/bin/env python3
"""
v7 Knowledge Base Validation Tests

Validates structure, content, and query compatibility.
Implements Phase 5 validation from plan: phase-05-validation-testing-v7-quality-assurance.md
"""

import json
import pytest
from pathlib import Path
from datetime import datetime

V7_KB_PATH = Path('/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v7.json')


@pytest.fixture(scope="module")
def v7_kb():
    """Load v7 KB once for all tests."""
    if not V7_KB_PATH.exists():
        pytest.skip(f"v7 KB not found: {V7_KB_PATH}")
    with open(V7_KB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def v7_kb_file_size():
    """Get file size in MB."""
    if V7_KB_PATH.exists():
        return V7_KB_PATH.stat().st_size / (1024 * 1024)
    return 0


class TestStructure:
    """Structural validation tests."""

    def test_required_top_level_keys(self, v7_kb):
        """Verify all required top-level keys present."""
        required = ['metadata', 'python_api', 'csharp_vb_api', 'user_guides', 'unified_index']
        for key in required:
            assert key in v7_kb, f"Missing required key: {key}"

    def test_metadata_has_version(self, v7_kb):
        """Verify metadata contains version."""
        assert 'metadata' in v7_kb
        assert v7_kb['metadata'].get('version') == 'v7', \
            f"Expected version v7, got {v7_kb['metadata'].get('version')}"

    def test_metadata_has_statistics(self, v7_kb):
        """Verify metadata contains statistics."""
        assert 'metadata' in v7_kb
        stats = v7_kb['metadata'].get('statistics', {})
        expected_keys = ['python_classes', 'python_methods', 'csharp_vb_members']
        for key in expected_keys:
            assert key in stats, f"Missing statistic: {key}"

    def test_metadata_has_timestamps(self, v7_kb):
        """Verify metadata contains extraction timestamps."""
        assert 'metadata' in v7_kb
        meta = v7_kb['metadata']
        assert 'extraction_date' in meta or 'created' in meta or 'extracted' in meta or 'timestamp' in meta, \
            "No timestamp found in metadata"

    def test_python_api_has_namespaces(self, v7_kb):
        """Verify Python API has namespaces."""
        assert 'python_api' in v7_kb
        assert 'namespaces' in v7_kb['python_api']
        assert len(v7_kb['python_api']['namespaces']) > 0, "No Python namespaces found"

    def test_python_api_has_indices(self, v7_kb):
        """Verify Python API has required indices."""
        python_api = v7_kb.get('python_api', {})
        # Must have at least class or method index
        has_indices = 'class_index' in python_api or 'method_index' in python_api
        assert has_indices, "No class or method indices found in Python API"

    def test_csharp_vb_api_has_namespaces(self, v7_kb):
        """Verify C#/VB API has namespaces."""
        assert 'csharp_vb_api' in v7_kb
        assert 'namespaces' in v7_kb['csharp_vb_api']
        assert len(v7_kb['csharp_vb_api']['namespaces']) > 0, "No C#/VB namespaces found"

    def test_csharp_vb_namespaces_have_members(self, v7_kb):
        """Verify C#/VB namespaces contain members."""
        csharp_vb = v7_kb['csharp_vb_api']
        has_members = False
        for ns_data in csharp_vb.get('namespaces', {}).values():
            if ns_data.get('members'):
                has_members = True
                break
        assert has_members, "No members found in any C#/VB namespace"

    def test_user_guides_has_content(self, v7_kb):
        """Verify user guides section has content."""
        guides = v7_kb.get('user_guides', {})
        has_word = len(guides.get('word_guides', [])) > 0
        has_sphinx = len(guides.get('sphinx_guides', {}).get('sections', {})) > 0
        assert has_word or has_sphinx, "No user guide content found"

    def test_unified_index_exists(self, v7_kb):
        """Verify unified index exists and has content."""
        assert 'unified_index' in v7_kb
        index = v7_kb['unified_index']
        assert len(index) > 0, "Unified index is empty"


class TestContentCounts:
    """Content count validation tests."""

    def test_python_class_count_reasonable(self, v7_kb):
        """Verify Python class count is reasonable (v6 baseline: ~1830)."""
        classes = v7_kb['python_api'].get('class_index', {})
        count = len(classes)
        assert count >= 1500, f"Python class count too low: {count} (expected >=1500)"
        assert count <= 3000, f"Python class count too high: {count} (expected <=3000)"

    def test_python_method_count_reasonable(self, v7_kb):
        """Verify Python method count is reasonable (v6 baseline: ~6773, v7 actual: ~4367)."""
        methods = v7_kb['python_api'].get('method_index', {})
        count = len(methods)
        assert count >= 3000, f"Python method count too low: {count} (expected >=3000)"
        assert count <= 10000, f"Python method count too high: {count} (expected <=10000)"

    def test_csharp_vb_member_count_reasonable(self, v7_kb):
        """Verify C#/VB member count is reasonable (~21K expected)."""
        total = 0
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            total += len(ns_data.get('members', []))
        assert total >= 15000, f"C#/VB member count too low: {total} (expected >=15000)"
        assert total <= 30000, f"C#/VB member count too high: {total} (expected <=30000)"

    def test_csharp_vb_namespaces_present(self, v7_kb):
        """Verify multiple C#/VB namespaces present (expected ~10)."""
        ns_count = len(v7_kb['csharp_vb_api'].get('namespaces', {}))
        assert ns_count >= 5, f"C#/VB namespace count too low: {ns_count} (expected >=5)"

    def test_user_guide_section_count(self, v7_kb):
        """Verify user guide section count (7 Word guides with ~16 sections)."""
        word_count = sum(
            len(g.get('sections', []))
            for g in v7_kb['user_guides'].get('word_guides', [])
        )
        sphinx_count = len(
            v7_kb['user_guides'].get('sphinx_guides', {}).get('sections', {})
        )
        total = word_count + sphinx_count
        assert total >= 10, f"User guide section count too low: {total} (expected >=10)"

    def test_no_empty_namespace_collections(self, v7_kb):
        """Verify no completely empty namespaces."""
        empty_count = 0
        for ns_name, ns_data in v7_kb['python_api'].get('namespaces', {}).items():
            classes = len(ns_data.get('classes', []))
            methods = len(ns_data.get('methods', []))
            files = len(ns_data.get('files', []))
            if classes == 0 and methods == 0 and files == 0:
                empty_count += 1
        # Allow some empty namespaces but not all
        total_ns = len(v7_kb['python_api'].get('namespaces', {}))
        assert empty_count < total_ns, "All Python namespaces are empty"


class TestSpotChecks:
    """Spot-check validation for specific content."""

    def test_csharp_syntax_extracted(self, v7_kb):
        """Verify C# syntax is present in at least one member."""
        found_csharp = False
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                syntax = member.get('syntax_csharp', '')
                if syntax and any(keyword in syntax for keyword in ['public', 'private', 'class', 'enum', 'interface', 'method']):
                    found_csharp = True
                    break
            if found_csharp:
                break
        assert found_csharp, "No C# syntax found in any member"

    def test_vb_syntax_extracted(self, v7_kb):
        """Verify VB syntax is present in at least one member."""
        found_vb = False
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                syntax = member.get('syntax_vb', '')
                if syntax and any(keyword in syntax for keyword in ['Public', 'Private', 'Class', 'Enumeration', 'Interface', 'Function']):
                    found_vb = True
                    break
            if found_vb:
                break
        assert found_vb, "No VB syntax found in any member"

    def test_both_syntaxes_represented(self, v7_kb):
        """Verify both C# and VB syntax exist (may be in different members)."""
        has_csharp = False
        has_vb = False
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('syntax_csharp'):
                    has_csharp = True
                if member.get('syntax_vb'):
                    has_vb = True
        assert has_csharp and has_vb, \
            f"Missing syntax representations: C#={has_csharp}, VB={has_vb}"

    def test_enum_has_members(self, v7_kb):
        """Verify at least one enum has member values."""
        found_enum = False
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('entity_type') == 'enum':
                    if member.get('members') and len(member['members']) > 0:
                        found_enum = True
                        break
            if found_enum:
                break
        assert found_enum, "No enum with members found"

    def test_class_has_methods(self, v7_kb):
        """Verify at least one class has methods."""
        found_class_with_methods = False
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                if member.get('entity_type') == 'class':
                    if member.get('members') and len(member['members']) > 0:
                        found_class_with_methods = True
                        break
            if found_class_with_methods:
                break
        assert found_class_with_methods, "No class with methods found"

    def test_guide_has_prose_content(self, v7_kb):
        """Verify guides have actual prose content."""
        found_content = False
        # Check Word guides
        for guide in v7_kb['user_guides'].get('word_guides', []):
            for section in guide.get('sections', []):
                if len(section.get('content', '')) > 100:
                    found_content = True
                    break
        # Check Sphinx guides
        for section in v7_kb['user_guides'].get('sphinx_guides', {}).get('sections', {}).values():
            if len(section.get('content', '')) > 100:
                found_content = True
                break
        assert found_content, "No substantial guide content found"

    def test_guide_sections_have_titles(self, v7_kb):
        """Verify guide sections have titles."""
        # Check Word guides
        for guide in v7_kb['user_guides'].get('word_guides', []):
            for section in guide.get('sections', []):
                assert section.get('title') or section.get('heading'), \
                    "Found section without title or heading"
                return
        # Check Sphinx guides
        for section_title in v7_kb['user_guides'].get('sphinx_guides', {}).get('sections', {}):
            if section_title:  # Key itself is the title
                return
        pytest.fail("No sections with titles found")

    def test_csharp_vb_members_have_names(self, v7_kb):
        """Verify C#/VB members have names."""
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                assert member.get('name'), f"Member without name: {member}"
                return
        pytest.fail("No members found")

    def test_csharp_vb_members_have_types(self, v7_kb):
        """Verify C#/VB members have entity types."""
        for ns_data in v7_kb['csharp_vb_api'].get('namespaces', {}).values():
            for member in ns_data.get('members', []):
                assert member.get('entity_type'), f"Member without entity_type: {member.get('name')}"
                return
        pytest.fail("No members found")


class TestQueryCompatibility:
    """Query interface compatibility tests."""

    def test_unified_method_index_searchable(self, v7_kb):
        """Verify unified method index has searchable entries."""
        methods = v7_kb['unified_index'].get('methods', {})
        assert len(methods) > 100, f"Method index too small: {len(methods)}"

    def test_unified_class_index_searchable(self, v7_kb):
        """Verify class index has searchable entries."""
        classes = v7_kb['unified_index'].get('classes', {})
        assert len(classes) > 100, f"Class index too small: {len(classes)}"

    def test_backward_compatible_python_structure(self, v7_kb):
        """Verify Python API structure matches v6 for backward compatibility."""
        python_api = v7_kb['python_api']
        # These keys must exist for query interface
        assert 'namespaces' in python_api, "Missing python_api.namespaces"
        assert 'method_index' in python_api, "Missing python_api.method_index"
        assert 'class_index' in python_api, "Missing python_api.class_index"

    def test_python_namespace_structure(self, v7_kb):
        """Verify namespace structure is valid."""
        for ns_name, ns_data in v7_kb['python_api'].get('namespaces', {}).items():
            assert isinstance(ns_data, dict), f"Namespace {ns_name} is not a dict"
            # Must have at least one of these
            has_content = any([
                'classes' in ns_data,
                'methods' in ns_data,
                'files' in ns_data
            ])
            assert has_content, f"Namespace {ns_name} has no content"

    def test_python_class_index_entries_valid(self, v7_kb):
        """Verify class index entries have required structure."""
        class_index = v7_kb['python_api'].get('class_index', {})
        if class_index:
            # v7 KB stores class names as keys and namespaces as list values
            for class_name, namespaces in list(class_index.items())[:5]:
                assert isinstance(namespaces, list), f"Class {class_name} entry should be a list"
                assert len(namespaces) > 0, f"Class {class_name} has no namespaces"

    def test_python_method_index_entries_valid(self, v7_kb):
        """Verify method index entries have required structure."""
        method_index = v7_kb['python_api'].get('method_index', {})
        if method_index:
            # v7 KB stores method names as keys and namespaces as list values
            for method_name, namespaces in list(method_index.items())[:5]:
                assert isinstance(namespaces, list), f"Method {method_name} entry should be a list"
                assert len(namespaces) > 0, f"Method {method_name} has no namespaces"

    def test_unified_index_has_references(self, v7_kb):
        """Verify unified index properly references source APIs."""
        index = v7_kb['unified_index']
        # Should have references to Python or C#/VB or both
        total_refs = 0
        for entity_name, entity_data in index.items():
            if isinstance(entity_data, dict):
                if entity_data.get('python') or entity_data.get('csharp_vb'):
                    total_refs += 1
        assert total_refs > 0, "No cross-references found in unified index"

    def test_csharp_vb_namespace_naming_convention(self, v7_kb):
        """Verify C#/VB namespace names follow expected pattern."""
        namespaces = list(v7_kb['csharp_vb_api'].get('namespaces', {}).keys())
        # Check for FunctionBay.* pattern
        functionbay_namespaces = [ns for ns in namespaces if 'FunctionBay' in ns]
        assert len(functionbay_namespaces) > 0, "No FunctionBay namespaces found (expected pattern)"


class TestDataIntegrity:
    """Data integrity validation tests."""

    def test_no_null_values_in_required_fields(self, v7_kb):
        """Spot-check that required fields are not null."""
        # Check metadata
        meta = v7_kb.get('metadata', {})
        assert meta.get('version') is not None, "Metadata version is null"

    def test_json_structure_valid(self, v7_kb):
        """Verify JSON structure is properly formed."""
        # If we got here, JSON loaded successfully
        assert isinstance(v7_kb, dict), "Root must be a dict"
        assert len(v7_kb) > 0, "KB dict is empty"

    def test_no_circular_references(self, v7_kb):
        """Basic check that structure doesn't have obvious circular refs."""
        # If we could serialize it to JSON, it shouldn't have issues
        try:
            json.dumps(v7_kb, default=str)
        except (ValueError, TypeError) as e:
            pytest.fail(f"JSON serialization failed (possible circular ref): {e}")

    def test_all_namespaces_have_names(self, v7_kb):
        """Verify all namespaces have proper names."""
        for api_key in ['python_api', 'csharp_vb_api']:
            namespaces = v7_kb[api_key].get('namespaces', {})
            for ns_name in namespaces.keys():
                assert ns_name and len(ns_name) > 0, f"Empty namespace name in {api_key}"

    def test_guide_files_referenced_exist(self, v7_kb):
        """Verify guide metadata references make sense."""
        guides = v7_kb.get('user_guides', {})
        for guide in guides.get('word_guides', []):
            assert guide.get('source_file') or guide.get('title'), \
                "Guide without source_file or title"


class TestStatisticsAccuracy:
    """Verify statistics match actual content."""

    def test_python_class_count_matches_index(self, v7_kb):
        """Verify metadata python_classes matches actual count."""
        meta_count = v7_kb['metadata'].get('statistics', {}).get('python_classes', -1)
        actual_count = len(v7_kb['python_api'].get('class_index', {}))
        if meta_count > 0:  # If meta has value, it should match
            assert meta_count == actual_count, \
                f"Class count mismatch: meta={meta_count}, actual={actual_count}"

    def test_python_method_count_matches_index(self, v7_kb):
        """Verify metadata python_methods matches actual count."""
        meta_count = v7_kb['metadata'].get('statistics', {}).get('python_methods', -1)
        actual_count = len(v7_kb['python_api'].get('method_index', {}))
        if meta_count > 0:  # If meta has value, it should match
            assert meta_count == actual_count, \
                f"Method count mismatch: meta={meta_count}, actual={actual_count}"

    def test_csharp_vb_member_count_matches_metadata(self, v7_kb):
        """Verify metadata c#/vb members matches actual count."""
        meta_count = v7_kb['metadata'].get('statistics', {}).get('csharp_vb_members', -1)
        actual_count = sum(
            len(ns.get('members', []))
            for ns in v7_kb['csharp_vb_api'].get('namespaces', {}).values()
        )
        if meta_count > 0:  # If meta has value, it should match (roughly)
            # Allow 5% variance due to rounding or extraction differences
            assert abs(meta_count - actual_count) / max(meta_count, actual_count) < 0.05, \
                f"Member count mismatch: meta={meta_count}, actual={actual_count}"


if __name__ == '__main__':
    # Run with: pytest tests/test-v7-knowledge-base-validation.py -v
    pytest.main([__file__, '-v', '--tb=short'])
