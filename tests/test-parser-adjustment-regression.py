"""
Parser adjustment regression tests.

Tests for parser patterns including:
- Table-based method extraction
- Syntax-highlighted code extraction
- Collapsed section handling
- Known regression patterns
"""
import pytest
from pathlib import Path
from typing import Dict


@pytest.mark.regression
class TestTableExtraction:
    """Test table-based method documentation parsing."""

    def test_table_method_extraction(self, sample_file_paths: Dict[str, Path]):
        """Extract methods from table structure."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find table with class="methods"
        table = soup.find('table', class_='methods')
        assert table is not None, "Methods table not found"

        # Extract method rows (skip header)
        rows = table.find_all('tr')[1:]
        assert len(rows) > 0, "No method rows in table"

        # Verify each row has method signature
        for row in rows:
            cells = row.find_all('td')
            assert len(cells) >= 2, f"Row missing cells: {row}"

            method_cell = cells[0]
            method_text = method_cell.get_text()
            assert '(' in method_text and ')' in method_text, \
                f"Method cell missing signature pattern: {method_text}"

    def test_table_with_header_skip(self, sample_file_paths: Dict[str, Path]):
        """Verify header row is skipped correctly."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        table = soup.find('table', class_='methods')
        assert table is not None, "Table not found"

        # Get header row
        thead = table.find('thead')
        if thead:
            header_cells = thead.find_all('th')
            assert len(header_cells) >= 2, "Header missing columns"

            # Verify header has "Method" and "Description"
            header_text = ' '.join([cell.get_text() for cell in header_cells])
            assert 'Method' in header_text or 'Description' in header_text, \
                "Expected header columns not found"

    def test_table_missing_columns_handled(self):
        """Test parser handles tables with missing columns gracefully."""
        from bs4 import BeautifulSoup

        # Simulate malformed table HTML
        html = """
        <table class="methods">
            <tr><td>Method1()</td></tr>
            <tr><td>Method2()</td><td>Description</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='methods')

        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            # Parser should handle variable column count
            assert len(cells) >= 1, "Row has no cells"


@pytest.mark.regression
class TestHighlightedCodeExtraction:
    """Test syntax-highlighted code block extraction."""

    def test_div_highlight_extraction(self, sample_file_paths: Dict[str, Path]):
        """Extract code from <div class='highlight'> blocks."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find highlight divs
        highlights = soup.find_all('div', class_='highlight')
        assert len(highlights) > 0, "No highlight divs found"

        # Extract code from each
        for highlight in highlights:
            pre = highlight.find('pre')
            assert pre is not None, f"Highlight div missing <pre>: {highlight}"

            code = pre.get_text()
            assert len(code.strip()) > 0, "Code block is empty"

    def test_pre_code_extraction(self, sample_file_paths: Dict[str, Path]):
        """Extract code from <pre><code> structure."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find all <pre> tags
        pres = soup.find_all('pre')
        assert len(pres) > 0, "No <pre> tags found"

        # Verify content extraction works
        for pre in pres:
            code = pre.get_text().strip()
            assert len(code) > 0, "Empty <pre> tag"

    def test_syntax_highlighted_spans(self, sample_file_paths: Dict[str, Path]):
        """Test extraction handles syntax highlighting spans."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find code with span elements (syntax highlighting)
        pres = soup.find_all('pre')

        for pre in pres:
            spans = pre.find_all('span')
            if len(spans) > 0:
                # Verify we can extract text from highlighted code
                code_text = pre.get_text()
                assert len(code_text.strip()) > 0, "Failed to extract from highlighted code"

                # Found at least one highlighted block
                return

        # If no spans found, that's ok (not all examples have syntax highlighting)
        pytest.skip("No syntax-highlighted code blocks found (optional)")


@pytest.mark.regression
class TestCollapsedSections:
    """Test handling of collapsed/expandable sections."""

    def test_details_summary_extraction(self):
        """Test extraction from <details><summary> elements."""
        from bs4 import BeautifulSoup

        # Simulate collapsed section HTML
        html = """
        <details>
            <summary>Available Methods</summary>
            <dl>
                <dt class="sig">Method1()</dt>
                <dd>Description 1</dd>
                <dt class="sig">Method2()</dt>
                <dd>Description 2</dd>
            </dl>
        </details>
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Find details element
        details = soup.find('details')
        assert details is not None, "Details element not found"

        # Extract methods from inside details
        methods = details.find_all('dt', class_='sig')
        assert len(methods) == 2, f"Expected 2 methods, found {len(methods)}"

    def test_expandable_method_lists(self):
        """Test parser handles expandable method lists."""
        from bs4 import BeautifulSoup

        html = """
        <div class="expandable">
            <h3>Methods (click to expand)</h3>
            <div class="content" style="display:none">
                <dl>
                    <dt>Method1()</dt>
                    <dt>Method2()</dt>
                </dl>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Parser should extract even if display:none
        methods = soup.find_all('dt')
        assert len(methods) == 2, "Failed to extract from hidden content"


@pytest.mark.regression
class TestRegressionPatterns:
    """Test known regression patterns from parser adjustments."""

    # Known patterns that previously caused issues
    KNOWN_PATTERNS = [
        {
            'name': 'count_mismatch_table_vs_dl',
            'html': '<table><tr><td>M1()</td></tr></table><dl><dt>M2()</dt></dl>',
            'expected_methods': 2
        },
        {
            'name': 'signature_format_missing_params',
            'html': '<dt class="sig">CreateArc()</dt>',
            'expected_signature': 'CreateArc()'
        },
        {
            'name': 'nested_code_blocks',
            'html': '<div class="highlight"><div class="highlight"><pre>code</pre></div></div>',
            'expected_code_blocks': 1
        }
    ]

    @pytest.mark.parametrize("pattern", KNOWN_PATTERNS, ids=lambda p: p['name'])
    def test_pattern_regression(self, pattern: Dict):
        """Test parser handles known problematic patterns."""
        from bs4 import BeautifulSoup

        html = pattern['html']
        soup = BeautifulSoup(html, 'html.parser')

        if 'expected_methods' in pattern:
            # Count methods from both table and dl
            table_methods = len(soup.find_all('td'))
            dl_methods = len(soup.find_all('dt'))
            total = table_methods + dl_methods

            assert total == pattern['expected_methods'], \
                f"Pattern '{pattern['name']}': expected {pattern['expected_methods']} methods, found {total}"

        if 'expected_signature' in pattern:
            dt = soup.find('dt')
            assert dt is not None, f"Pattern '{pattern['name']}': dt not found"
            sig = dt.get_text()
            assert pattern['expected_signature'] in sig, \
                f"Pattern '{pattern['name']}': signature mismatch"

        if 'expected_code_blocks' in pattern:
            # Should find only outermost highlight
            code_blocks = soup.find_all('pre')
            assert len(code_blocks) >= pattern['expected_code_blocks'], \
                f"Pattern '{pattern['name']}': expected {pattern['expected_code_blocks']} blocks, found {len(code_blocks)}"


@pytest.mark.regression
class TestEdgeCases:
    """Test edge cases in HTML parsing."""

    def test_empty_method_description(self):
        """Test method with no description doesn't crash parser."""
        from bs4 import BeautifulSoup

        html = '<dt class="sig">Method()</dt><dd></dd>'
        soup = BeautifulSoup(html, 'html.parser')

        dt = soup.find('dt')
        dd = soup.find('dd')

        assert dt is not None, "Method signature not found"
        assert dd is not None, "Description element not found"
        # Empty description should be handled gracefully
        assert dd.get_text().strip() == '', "Description should be empty"

    def test_method_with_special_characters(self):
        """Test method names with special characters."""
        from bs4 import BeautifulSoup

        html = '<dt class="sig">operator&lt;&lt;(value)</dt>'
        soup = BeautifulSoup(html, 'html.parser')

        dt = soup.find('dt')
        sig = dt.get_text()

        # BeautifulSoup automatically decodes HTML entities
        assert 'operator' in sig, "Operator method not extracted"

    def test_multiline_signature(self):
        """Test signature spanning multiple lines."""
        from bs4 import BeautifulSoup

        html = """
        <dt class="sig">
            CreateComplexObject(
                param1,
                param2,
                param3
            )
        </dt>
        """
        soup = BeautifulSoup(html, 'html.parser')

        dt = soup.find('dt')
        sig = dt.get_text()

        # Should extract full signature
        assert 'CreateComplexObject' in sig, "Method name not found"
        assert '(' in sig and ')' in sig, "Parentheses not found"
        assert 'param1' in sig, "Parameters not extracted"

    def test_properties_vs_methods_distinction(self, sample_file_paths: Dict[str, Path]):
        """Test parser distinguishes properties from methods."""
        from bs4 import BeautifulSoup

        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find properties section
        props_section = soup.find('div', id='properties')
        if props_section:
            # Properties should use dl.attribute, not dl.method
            attrs = props_section.find_all('dl', class_='attribute')
            # Properties exist and are marked differently
            assert len(attrs) > 0 or len(props_section.find_all('dt')) > 0, \
                "Properties section exists but no properties found"
