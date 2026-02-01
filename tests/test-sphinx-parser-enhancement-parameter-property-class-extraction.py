#!/usr/bin/env python3
"""
Test Suite for Parser Enhancements (Phase 04)

Tests Sphinx-specific parsing capabilities:
- Parameter extraction with types
- Return type parsing
- Property extraction
- Class extraction with inheritance
- Enhanced namespace detection
"""

import pytest
from pathlib import Path
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from recurdyn_doc_parser import ProcessNetDocParser, Method, Property, ClassDef, Parameter


# Fixtures directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures' / 'html-samples'


class TestSphinxParameterExtraction:
    """Test parameter extraction from Sphinx-formatted methods."""

    def test_method_with_parameter_type(self):
        """Verify parameter name and type extracted correctly."""
        # Read IForceConnectorBushing_CopyActionToBase.html
        html_file = FIXTURES_DIR / 'IForceConnectorBushing_CopyActionToBase.html'

        parser = ProcessNetDocParser(Path('input'), Path('output'))
        soup = parser.read_html_file(html_file)

        methods = parser.extract_method_signatures(soup)

        assert len(methods) > 0, "Should extract at least one method"

        method = methods[0]
        assert method.name == 'CopyActionToBase', f"Method name should be 'CopyActionToBase', got '{method.name}'"
        assert len(method.parameters) > 0, "Should extract parameters"

        # Check parameter
        param = method.parameters[0]
        assert param['name'] == 'Type', f"Parameter name should be 'Type', got '{param['name']}'"
        assert 'CopyMarkerType' in param['type'], f"Parameter type should contain 'CopyMarkerType', got '{param['type']}'"

    def test_parameter_optional_detection(self):
        """Verify optional parameters detected by default value."""
        # Create test HTML with optional parameter
        html = """
        <dl class="py method">
            <dt class="sig sig-object py">
                <span class="sig-name descname"><span class="pre">TestMethod</span></span>
                <span class="sig-paren">(</span>
                <em class="sig-param">
                    <span class="n"><span class="pre">optParam</span></span>
                    <span class="o"><span class="pre">=</span></span>
                    <span class="default_value"><span class="pre">None</span></span>
                </em>
                <span class="sig-paren">)</span>
            </dt>
            <dd><p>Test method</p></dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        methods = parser.extract_method_signatures(soup)
        assert len(methods) > 0

        param = methods[0].parameters[0]
        assert param['is_optional'] == True, "Parameter with default value should be optional"
        assert param['default'] == 'None', f"Default value should be 'None', got '{param['default']}'"


class TestSphinxReturnTypeExtraction:
    """Test return type extraction from Sphinx field-list."""

    def test_return_type_from_field_list(self):
        """Verify return type parsed from Type field."""
        html = """
        <dl class="py method">
            <dt class="sig sig-object py">
                <span class="sig-name descname"><span class="pre">GetValue</span></span>
                <span class="sig-paren">()</span>
            </dt>
            <dd>
                <p>Returns a value</p>
                <dl class="field-list simple">
                    <dt class="field-odd">Return Type</dt>
                    <dd class="field-odd"><p>float</p></dd>
                </dl>
            </dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        methods = parser.extract_method_signatures(soup)
        assert len(methods) > 0

        method = methods[0]
        assert method.returns == 'float', f"Return type should be 'float', got '{method.returns}'"


class TestSphinxPropertyExtraction:
    """Test property extraction from Sphinx-formatted documentation."""

    def test_property_with_type(self):
        """Verify property name and type extracted."""
        # Read IForceConnectorBushing_Name.html
        html_file = FIXTURES_DIR / 'IForceConnectorBushing_Name.html'

        parser = ProcessNetDocParser(Path('input'), Path('output'))
        soup = parser.read_html_file(html_file)

        properties = parser.extract_sphinx_properties(soup)

        assert len(properties) > 0, "Should extract at least one property"

        prop = properties[0]
        assert prop.name == 'Name', f"Property name should be 'Name', got '{prop.name}'"
        assert prop.type == 'str', f"Property type should be 'str', got '{prop.type}'"

    def test_property_read_only_detection(self):
        """Verify property read-only status detected."""
        html = """
        <dl class="py property">
            <dt class="sig sig-object py">
                <em class="property"><span class="pre">property</span></em>
                <span class="sig-name descname"><span class="pre">ReadOnlyProp</span></span>
            </dt>
            <dd>
                <p>This property is read-only</p>
                <dl class="field-list simple">
                    <dt class="field-odd">Type</dt>
                    <dd class="field-odd"><p>int</p></dd>
                </dl>
            </dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        properties = parser.extract_sphinx_properties(soup)
        assert len(properties) > 0

        prop = properties[0]
        assert prop.read_only == True, "Property should be detected as read-only"


class TestSphinxClassExtraction:
    """Test class extraction with inheritance."""

    def test_class_with_inheritance(self):
        """Verify inheritance chain captured."""
        html = """
        <dl class="py class">
            <dt class="sig sig-object py">
                <em class="property"><span class="pre">class</span></em>
                <span class="sig-name descname"><span class="pre">TestClass</span></span>
            </dt>
            <dd>
                <p>Bases: <code class="xref py py-class">BaseClass</code></p>
                <p>Test class description</p>
            </dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        classes = parser.extract_sphinx_classes(soup)
        assert len(classes) > 0

        cls = classes[0]
        assert cls.name == 'TestClass', f"Class name should be 'TestClass', got '{cls.name}'"
        assert 'BaseClass' in cls.inheritance, f"Inheritance should contain 'BaseClass', got '{cls.inheritance}'"


class TestNamespaceDetection:
    """Test enhanced namespace detection."""

    def test_namespace_from_module_id(self):
        """Verify namespace extracted from module ID."""
        html = """
        <section id="module-recurdyn.ToolkitCommon">
            <h1>ToolkitCommon Module</h1>
        </section>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        namespace = parser.determine_namespace_from_content(soup, "ToolkitCommon")
        assert namespace == 'ProcessNet.ToolkitCommon', f"Namespace should be 'ProcessNet.ToolkitCommon', got '{namespace}'"

    def test_namespace_from_dt_id(self):
        """Verify namespace extracted from dt element ID."""
        html = """
        <dl class="py class">
            <dt class="sig sig-object py" id="recurdyn.Geometry.IGeometry">
                <span class="sig-name descname"><span class="pre">IGeometry</span></span>
            </dt>
            <dd><p>Geometry interface</p></dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        namespace = parser.determine_namespace_from_content(soup, "")
        assert namespace == 'ProcessNet.Geometry', f"Namespace should be 'ProcessNet.Geometry', got '{namespace}'"


class TestBackwardCompatibility:
    """Ensure backward compatibility with existing tests."""

    def test_legacy_method_extraction_still_works(self):
        """Verify legacy definition list extraction still functional."""
        html = """
        <dl>
            <dt>TestMethod(param1)</dt>
            <dd>Method description</dd>
        </dl>
        """

        soup = BeautifulSoup(html, 'lxml')
        parser = ProcessNetDocParser(Path('input'), Path('output'))

        methods = parser.extract_method_signatures(soup)
        assert len(methods) > 0, "Legacy extraction should still work"
        assert methods[0].name == 'TestMethod'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
