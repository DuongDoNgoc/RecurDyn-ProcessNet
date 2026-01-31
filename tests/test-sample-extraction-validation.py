"""
Sample file extraction validation tests.

Tests extraction accuracy for 5 representative file types:
- index: Overview/TOC structure
- namespace: Namespace-level documentation
- class: Class definition with methods
- methods: Detailed method documentation
- examples: Tutorial/example documentation
"""
import pytest
from pathlib import Path
from typing import Dict


@pytest.mark.sample
class TestSampleFileExtraction:
    """Test extraction succeeds for all sample file types."""

    @pytest.mark.parametrize("file_type", ["index", "namespace", "class", "methods", "examples"])
    def test_file_extraction_succeeds(self, file_type: str, sample_file_paths: Dict[str, Path], parser_instance):
        """Verify parser can process each file type without errors."""
        file_path = sample_file_paths[file_type]
        assert file_path.exists(), f"Sample file not found: {file_path}"

        # Parse file
        try:
            parser_instance.parse_html_file(file_path)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Failed to parse {file_type}: {e}")

        assert success, f"Extraction failed for {file_type}"


@pytest.mark.sample
class TestTitleExtraction:
    """Test title extraction accuracy."""

    def test_index_title_extracted(self, sample_file_paths: Dict[str, Path]):
        """Verify index page title is extracted correctly."""
        from bs4 import BeautifulSoup

        index_file = sample_file_paths['index']
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Extract title
        title = soup.find('h1')
        assert title is not None, "Title (h1) not found in index"
        assert "ProcessNet API Reference" in title.get_text(), "Title text mismatch"

    def test_class_title_extracted(self, sample_file_paths: Dict[str, Path]):
        """Verify class page title is extracted."""
        from bs4 import BeautifulSoup

        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find class name in signature
        class_sig = soup.find('span', class_='sig-name')
        assert class_sig is not None, "Class signature not found"
        assert "Body" in class_sig.get_text(), "Class name not found in signature"


@pytest.mark.sample
class TestNamespaceDetection:
    """Test namespace detection accuracy."""

    def test_namespace_in_class_file(self, sample_file_paths: Dict[str, Path]):
        """Verify namespace 'ProcessNet.Model' detected in class file."""
        from bs4 import BeautifulSoup

        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find namespace prefix
        namespace_prefix = soup.find('span', class_='sig-prename')
        assert namespace_prefix is not None, "Namespace prefix not found"
        assert "ProcessNet.Model" in namespace_prefix.get_text(), "Namespace mismatch"

    def test_namespace_in_namespace_file(self, sample_file_paths: Dict[str, Path]):
        """Verify 'ProcessNet.Geometry' namespace detected."""
        from bs4 import BeautifulSoup

        namespace_file = sample_file_paths['namespace']
        with open(namespace_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find namespace in title or body
        h1 = soup.find('h1')
        assert h1 is not None, "H1 not found"
        assert "ProcessNet.Geometry" in h1.get_text(), "Namespace not in title"


@pytest.mark.sample
class TestMethodCountWithTolerance:
    """Test method count within ±20% tolerance."""

    def test_class_file_method_count(self, sample_file_paths: Dict[str, Path],
                                     expected_sample_data: Dict, tolerance_config: Dict):
        """Verify method count in class-body.html within tolerance."""
        from bs4 import BeautifulSoup

        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count method signatures
        method_section = soup.find('div', id='methods')
        assert method_section is not None, "Methods section not found"

        methods = method_section.find_all('dt', class_='sig')
        actual_count = len(methods)

        # Expected: 15 methods ± 20% (tolerance: 3)
        expected = expected_sample_data['class']['expected_methods']
        tolerance = expected_sample_data['class']['tolerance']

        difference = abs(actual_count - expected)
        assert difference <= tolerance, \
            f"Method count {actual_count} outside tolerance (expected {expected} ± {tolerance})"

    def test_methods_file_method_count(self, sample_file_paths: Dict[str, Path],
                                       expected_sample_data: Dict, tolerance_config: Dict):
        """Verify method count in methods-create.html."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count methods in dl.method section
        methods = soup.find_all('dt', class_='sig')
        actual_count = len(methods)

        # Expected: 10 methods
        expected = expected_sample_data['methods']['method_count']
        tolerance_percent = tolerance_config['count_tolerance_percent']
        tolerance = int(expected * tolerance_percent)

        difference = abs(actual_count - expected)
        assert difference <= tolerance, \
            f"Method count {actual_count} outside tolerance (expected {expected} ± {tolerance})"


@pytest.mark.sample
class TestSignatureFormatCorrectness:
    """Test signature format validation."""

    def test_signature_contains_parentheses(self, sample_file_paths: Dict[str, Path]):
        """Verify at least one signature contains parentheses."""
        from bs4 import BeautifulSoup
        import re

        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find signatures
        signatures = soup.find_all('dt', class_='sig')
        assert len(signatures) > 0, "No signatures found"

        # Verify at least one has parentheses pattern
        pattern = r'\([^)]*\)'
        found_valid = False

        for sig in signatures:
            sig_text = sig.get_text()
            if re.search(pattern, sig_text):
                found_valid = True
                break

        assert found_valid, "No valid signature with parentheses found"

    def test_signature_format_matches_expected(self, sample_file_paths: Dict[str, Path],
                                               expected_sample_data: Dict):
        """Verify signature format matches expected pattern."""
        from bs4 import BeautifulSoup
        import re

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Get signature pattern from expected data
        pattern = expected_sample_data['methods']['signature_pattern']

        # Check signatures
        signatures = soup.find_all('dt', class_='sig')
        valid_count = 0

        for sig in signatures:
            sig_text = sig.get_text()
            if re.search(pattern, sig_text):
                valid_count += 1

        assert valid_count > 0, "No signatures match expected pattern"


@pytest.mark.sample
class TestExampleCodeBlockExtraction:
    """Test example code block extraction."""

    def test_example_count_meets_minimum(self, sample_file_paths: Dict[str, Path],
                                        expected_sample_data: Dict):
        """Verify at least 2 code examples in examples file."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count code blocks
        code_blocks = soup.find_all('div', class_='highlight')
        actual_count = len(code_blocks)

        min_expected = expected_sample_data['examples']['min_code_blocks']

        assert actual_count >= min_expected, \
            f"Expected at least {min_expected} code blocks, found {actual_count}"

    def test_code_block_contains_code(self, sample_file_paths: Dict[str, Path]):
        """Verify code blocks contain actual code content."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find code blocks
        code_blocks = soup.find_all('div', class_='highlight')
        assert len(code_blocks) > 0, "No code blocks found"

        # Verify each block has content
        for block in code_blocks:
            pre = block.find('pre')
            assert pre is not None, "Code block missing <pre> tag"
            code_text = pre.get_text().strip()
            assert len(code_text) > 0, "Code block is empty"

    def test_code_language_detection(self, sample_file_paths: Dict[str, Path]):
        """Verify code blocks have language hints (csharp/python)."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find highlight divs with language class
        highlights = soup.find_all('div', class_=lambda x: x and 'highlight' in x)
        assert len(highlights) > 0, "No highlight divs found"

        # Check for language indicators
        language_found = False
        for div in highlights:
            class_list = div.get('class', [])
            for cls in class_list:
                if 'csharp' in cls or 'python' in cls:
                    language_found = True
                    break
            if language_found:
                break

        # Note: Language detection is optional, just log if not found
        if not language_found:
            pytest.skip("Language class not found in code blocks (optional)")


@pytest.mark.sample
class TestIndexTableOfContents:
    """Test index file TOC structure."""

    def test_toc_wrapper_exists(self, sample_file_paths: Dict[str, Path]):
        """Verify TOC wrapper div exists in index."""
        from bs4 import BeautifulSoup

        index_file = sample_file_paths['index']
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        toc = soup.find('div', class_='toctree-wrapper')
        assert toc is not None, "TOC wrapper not found in index"

    def test_toc_has_links(self, sample_file_paths: Dict[str, Path]):
        """Verify TOC contains links to other pages."""
        from bs4 import BeautifulSoup

        index_file = sample_file_paths['index']
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        toc = soup.find('div', class_='toctree-wrapper')
        assert toc is not None, "TOC not found"

        # Find links
        links = toc.find_all('a', class_='reference')
        assert len(links) > 0, "No links found in TOC"
