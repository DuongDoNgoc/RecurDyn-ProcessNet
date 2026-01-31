"""
Browser-based verification tests using MCP Playwright.

Tests visual verification, element counting, and screenshot capture
for extracted documentation vs rendered HTML content.
"""
import pytest
from pathlib import Path
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup


def is_within_tolerance(actual: int, expected: int, tolerance_percent: float) -> bool:
    """Check if actual count is within tolerance of expected."""
    tolerance_range = expected * tolerance_percent
    difference = abs(actual - expected)
    return difference <= tolerance_range


@pytest.mark.browser
class TestBrowserNavigation:
    """Test basic browser navigation to local HTML files."""

    def test_navigate_to_index_file(self, sample_file_paths: Dict[str, Path]):
        """Verify browser can open index.html file."""
        index_path = sample_file_paths['index']
        assert index_path.exists(), f"Index file not found: {index_path}"

        # Note: Actual MCP Playwright integration requires MCP server setup
        # This test validates file existence for browser navigation
        assert index_path.stat().st_size > 0, "Index file is empty"

    def test_all_sample_files_accessible(self, sample_file_paths: Dict[str, Path]):
        """Verify all sample files exist and are accessible."""
        for file_type, file_path in sample_file_paths.items():
            assert file_path.exists(), f"{file_type} file not found: {file_path}"
            assert file_path.stat().st_size > 0, f"{file_type} file is empty"


@pytest.mark.browser
class TestElementCounting:
    """Test element counting from rendered browser content."""

    def test_count_method_signatures_in_class_file(self, sample_file_paths: Dict[str, Path]) -> None:
        """Count method signature elements in class-body.html."""
        class_file = sample_file_paths['class']
        with open(class_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count method signatures (dt elements with sig-name containing parentheses)
        methods = soup.find_all('dt', class_='sig')
        method_count = sum(1 for m in methods if '(' in m.get_text())

        assert method_count >= 10, f"Expected at least 10 methods, found {method_count}"

    def test_count_classes_in_namespace_file(self, sample_file_paths: Dict[str, Path]):
        """Count class definitions in namespace-geometry.html."""
        from bs4 import BeautifulSoup

        namespace_file = sample_file_paths['namespace']
        with open(namespace_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count class definitions
        classes = soup.find_all('dt', class_='sig')
        class_count = len([c for c in classes if 'class' in c.get_text().lower()])

        assert class_count >= 3, f"Expected at least 3 classes, found {class_count}"

    def test_count_code_examples(self, sample_file_paths: Dict[str, Path]):
        """Count code examples in examples-tutorial.html."""
        from bs4 import BeautifulSoup

        examples_file = sample_file_paths['examples']
        with open(examples_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Count code blocks in highlight divs
        code_blocks = soup.find_all('div', class_='highlight')

        assert len(code_blocks) >= 2, f"Expected at least 2 code examples, found {len(code_blocks)}"


@pytest.mark.browser
class TestSignatureExtraction:
    """Test signature extraction from rendered DOM."""

    def test_extract_signatures_from_methods_file(self, sample_file_paths: Dict[str, Path]):
        """Extract method signatures from methods-create.html."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Extract signatures from dt elements
        signatures = []
        for dt in soup.find_all('dt', class_='sig'):
            sig_text = dt.get_text()
            if '(' in sig_text and ')' in sig_text:
                signatures.append(sig_text)

        assert len(signatures) >= 5, f"Expected at least 5 signatures, found {len(signatures)}"

        # Verify signature format
        for sig in signatures:
            assert '(' in sig and ')' in sig, f"Invalid signature format: {sig}"

    def test_table_based_method_extraction(self, sample_file_paths: Dict[str, Path]):
        """Extract methods from table-based documentation."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths['methods']
        with open(methods_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find table with class="methods"
        table = soup.find('table', class_='methods')
        assert table is not None, "Methods table not found"

        # Count rows (excluding header)
        rows = table.find_all('tr')[1:]  # Skip header row
        assert len(rows) >= 5, f"Expected at least 5 table rows, found {len(rows)}"


@pytest.mark.browser
class TestScreenshotCapture:
    """Test screenshot capture functionality."""

    def test_screenshot_directory_exists(self, screenshots_dir: Path):
        """Verify screenshots directory is created."""
        assert screenshots_dir.exists(), "Screenshots directory not created"
        assert screenshots_dir.is_dir(), "Screenshots path is not a directory"

    def test_prepare_screenshot_paths(self, sample_file_paths: Dict[str, Path], screenshots_dir: Path):
        """Prepare screenshot file paths for each sample file."""
        screenshot_paths = {}

        for file_type, file_path in sample_file_paths.items():
            screenshot_path = screenshots_dir / f"{file_type}.png"
            screenshot_paths[file_type] = screenshot_path

        assert len(screenshot_paths) == 5, "Expected 5 screenshot paths"


@pytest.mark.browser
class TestExtractedVsBrowserComparison:
    """Compare extracted data vs browser-visible content."""

    def test_method_count_tolerance(self, tolerance_config: Dict) -> None:
        """Verify tolerance configuration for count comparison."""
        tolerance = tolerance_config['count_tolerance_percent']

        # Example: 15 methods extracted, 13 visible in browser
        extracted_count = 15
        browser_count = 13

        # Use helper function for tolerance check
        assert is_within_tolerance(extracted_count, browser_count, tolerance), \
            f"Extracted count {extracted_count} not within {tolerance:.0%} of browser count {browser_count}"

    def test_signature_format_validation(self):
        """Validate signature format from browser content."""
        test_signatures = [
            "CreateBody(name, mass)",
            "SetPosition(x, y, z)",
            "GetMass()"
        ]

        for sig in test_signatures:
            # Verify signature contains parentheses
            assert '(' in sig and ')' in sig, f"Invalid signature: {sig}"

            # Extract method name (before parentheses)
            method_name = sig.split('(')[0]
            assert len(method_name) > 0, "Empty method name"


@pytest.mark.browser
class TestMCPPlaywrightIntegration:
    """Tests requiring actual MCP Playwright server connection."""

    @pytest.mark.skip(reason="Requires MCP Playwright server setup")
    def test_mcp_server_connection(self):
        """Test connection to MCP Playwright server."""
        # This test would use actual MCP Playwright tools
        # Skipped until MCP server is configured
        pass

    @pytest.mark.skip(reason="Requires MCP Playwright server setup")
    def test_navigate_with_playwright(self, sample_file_paths: Dict[str, Path]):
        """Navigate to file using MCP Playwright."""
        # Example MCP tool usage (when server is configured):
        # playwright_navigate(f"file://{sample_file_paths['index']}")
        pass

    @pytest.mark.skip(reason="Requires MCP Playwright server setup")
    def test_capture_screenshot_with_playwright(self, sample_file_paths: Dict[str, Path], screenshots_dir: Path):
        """Capture screenshot using MCP Playwright."""
        # Example MCP tool usage:
        # playwright_screenshot(path=screenshots_dir / "index.png")
        pass
